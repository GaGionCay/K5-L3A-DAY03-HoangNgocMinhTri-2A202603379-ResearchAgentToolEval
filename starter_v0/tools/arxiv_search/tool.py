import requests
import xml.etree.ElementTree as ET

def run(query: str, max_results: int = 3):
    if not query:
        return {"error": "Query cannot be empty"}
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
    try:
        resp = requests.get(url, timeout=10)
        root = ET.fromstring(resp.content)
        entries = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            entries.append({
                "title": entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
                "link": entry.find('{http://www.w3.org/2005/Atom}id').text.strip(),
                "summary": entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
            })
        return {"results": entries}
    except Exception as e:
        return {"error": str(e)}