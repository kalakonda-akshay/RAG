"""
Web Page and Documentation Archiver & Crawler for offline RAG indexing.
"""
import os
import re
import requests
from bs4 import BeautifulSoup


def crawl_and_save_webpage(url: str, output_dir: str) -> str:
    """
    Fetches a web page URL, strips HTML tags/scripts, extracts main text,
    and saves it as a clean text file in output_dir for RAG indexing.
    Returns path to saved text file.
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch webpage '{url}': {str(e)}") from e

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove script, style, header, footer, and nav tags
    for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
        element.extract()

    # Get page title
    title = soup.title.string.strip() if soup.title and soup.title.string else "Webpage"
    sanitized_title = re.sub(r"[^\w\-_]", "_", title)[:40]

    # Extract text content
    lines = [line.strip() for line in soup.get_text(separator="\n").splitlines() if line.strip()]
    full_text = f"Title: {title}\nURL: {url}\n\n" + "\n".join(lines)

    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"web_{sanitized_title}.txt")

    with open(file_path, "w", encoding="utf-8", errors="replace") as f:
        f.write(full_text)

    return file_path
