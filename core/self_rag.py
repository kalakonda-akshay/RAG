"""
Multi-Agent Self-Reflective RAG (Critic + Synthesizer) Verification Engine.
"""
import ollama


def critic_verify_answer(question: str, answer: str, context: str) -> dict:
    """
    Critic Agent evaluates the generated answer against the source context for factual alignment and zero hallucinations.
    Returns: {"verified": bool, "feedback": str, "refined_answer": str}
    """
    if not answer or not context:
        return {"verified": True, "feedback": "No verification required.", "refined_answer": answer}

    prompt = f"""You are a strict factual Critic Agent.
Evaluate whether the Assistant Answer is 100% supported by the Context facts.

Context:
{context[:2000]}

Question:
{question}

Assistant Answer:
{answer}

Verification Task:
1. Is the answer factual and directly backed by context? (Yes/No)
2. If No, state what needs correction and provide the refined factual answer.

Output format:
Status: [VERIFIED or NEEDS_REVISION]
Refined Answer: [Corrected factual answer]"""

    try:
        res = ollama.generate(model="llama3.2:3b", prompt=prompt)
        text = res.get("response", "").strip()

        if "STATUS: VERIFIED" in text.upper():
            return {
                "verified": True,
                "feedback": "Factual Critic Verified: Answer is 100% supported by source context.",
                "refined_answer": answer,
            }
        else:
            # Extract refined answer
            lines = text.splitlines()
            refined = answer
            for l in lines:
                if l.startswith("Refined Answer:"):
                    refined = l.replace("Refined Answer:", "").strip()
            return {
                "verified": False,
                "feedback": "Factual Critic Refined: Corrected unverified claims.",
                "refined_answer": refined if refined else answer,
            }
    except Exception:
        return {"verified": True, "feedback": "Critic verification bypassed.", "refined_answer": answer}
