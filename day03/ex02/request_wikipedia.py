import requests
import sys
import json
import dewiki

def execute():

    if len(sys.argv) != 2:
        print("Error: you must provide the title of the page")
        sys.exit(1)
    
    title = sys.argv[1]
    

    url = 'https://fr.wikipedia.org/w/api.php'
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "main",
        "redirects": 1
    }

    file_name = title.replace(" ", "_") + ".wiki"

    headers = {
        "User-Agent": "request_wikipedia.py/1.0 (https://github.com/yannUFLL)"
    }
    try:
        response = requests.get(url, params=params, headers=headers)
    except requests.RequestException:
        print("Error: request failed")
        sys.exit(1)
    
    if response.status_code != 200:
        print(f"Error: server returned status {response.status_code}")
        sys.exit(1)

    data = response.json()
    pages = data.get("query", {}).get("pages", {})

    page_id = next(iter(pages))
    page = pages[page_id]

    if page_id == "-1" or "missing" in page:
        print("Error: article not found")
        sys.exit(1)

    try:
        wikitext = page.get("revisions")[0].get("slots").get("main").get("*")
    except (KeyError, IndexError, TypeError):
        print("Error: could not find the text content")
        sys.exit(1)
    
    clean = dewiki.from_string(wikitext)
    real_title = page.get("title", title)
    file_name = title.replace(" ", "_") + ".wiki"

    try:
        with open(file_name, "w", encoding='utf-8') as file:
            file.write(clean.strip())
        print(f"Article saved to {file_name}")
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    execute()
