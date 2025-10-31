import requests
import sys
import json
import dewiki

def execute():
    url = 'https://fr.wikipedia.org/w/api.php'
    params =  {
        "action": "query",
        "prop": "extracts",
        "format": "json",
        "titles": "bonjour",
        "explaintext": 1,
        "redirects": 1
    }

    headers = {
        "User-Agent": "request_wikipedia.py/1.0 (https://github.com/yannUFLL)"
    }
    response = requests.get(url, params=params, headers=headers)
    print(response)
    if response.status_code != 200:
        print("Error: request failed")
        sys.exit(1)
    data = response.json()
    pages = data.get("query", {}).get("pages", {})

    if not pages: 
        print("Error: no result found")
        sys.exit(1)
    
    page = next(iter(pages.values()))
    text = page.get("extract")

    if not text:
        print("Error: artcile has no content")
        sys.exit(1)

    clean = dewiki.from_string(text)
    print(clean)

    filename = "bonjour"
    with open(filename, "w") as file:
        file.write(clean)

    print(f"Article saved to {filename}")

    

if __name__ == "__main__":
    execute()
