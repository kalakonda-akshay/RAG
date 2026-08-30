"""
Natural Language SQL Translator and SQLite Query Execution Engine.
"""
import os
import sqlite3
import pandas as pd
import ollama


def query_sqlite_database(db_path: str, user_question: str) -> dict:
    """
    Inspects SQLite schema, generates SQL via local LLM, executes query safely, and formats results.
    Returns: {"sql": "<generated sql>", "dataframe": <DataFrame or None>, "summary": "<AI summary>", "error": "<error or None>"}
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")

    filename = os.path.basename(db_path)

    # 1. Connect and extract table schemas
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]

        schema_info = []
        for tbl in tables[:10]:  # Limit to top 10 tables
            cursor.execute(f"PRAGMA table_info('{tbl}');")
            cols = [f"{c[1]} ({c[2]})" for c in cursor.fetchall()]
            schema_info.append(f"Table '{tbl}': {', '.join(cols)}")

        schema_str = "\n".join(schema_info)
    except Exception as e:
        return {"sql": "", "dataframe": None, "summary": f"Failed to inspect SQLite schema: {str(e)}", "error": str(e)}

    # 2. Ask local LLM to translate question to SQL
    prompt = f"""You are an expert SQLite SQL developer.
Translate the user question into a single valid SQLite SQL SELECT query using the schema below.
Output ONLY the executable SQL query enclosed in ```sql ... ``` code block. Do not add any text before or after.

Schema:
{schema_str}

User Question: {user_question}

SQL Query:"""

    try:
        res = ollama.generate(model="llama3.2:3b", prompt=prompt)
        raw_sql = res.get("response", "").strip()

        # Extract SQL query
        if "```sql" in raw_sql:
            sql_clean = raw_sql.split("```sql")[1].split("```")[0].strip()
        elif "```" in raw_sql:
            sql_clean = raw_sql.split("```")[1].split("```")[0].strip()
        else:
            sql_clean = raw_sql.strip()

        # Execute query into pandas DataFrame
        df = pd.read_sql_query(sql_clean, conn)
        conn.close()

        # Generate summary of results
        summary_prompt = f"Summarize the following SQL query results in 2 concise sentences:\n\nQuery: {sql_clean}\nResults ({len(df)} rows):\n{df.head(10).to_string()}\n\nSummary:"
        summary_res = ollama.generate(model="llama3.2:3b", prompt=summary_prompt)
        summary_text = summary_res.get("response", "").strip()

        return {
            "sql": sql_clean,
            "dataframe": df,
            "summary": summary_text,
            "error": None,
        }
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        return {
            "sql": sql_clean if 'sql_clean' in locals() else "",
            "dataframe": None,
            "summary": f"SQL execution error: {str(e)}",
            "error": str(e),
        }
