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
    params =  {
        "action": "query",
        "prop": "extracts",
        "format": "json",
        "titles": title,
        "explaintext": 1,
        "redirects": 1
    }

    file_name = title.replace(" ", "_") + ".wiki"

    headers = {
        "User-Agent": "request_wikipedia.py/1.0 (https://github.com/yannUFLL)"
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        print(f"Error: request failed code {response}")
        sys.exit(1)
    data = response.json()
    pages = data.get("query", {}).get("pages", {})

    if not pages: 
        print("Error: no result found")
        sys.exit(1)
    
    page = next(iter(pages.values()))
    text = page.get("extract")

    if not text:
        print("Error: artile has no content")
        sys.exit(1)

    clean = dewiki.from_string(text)

    with open(file_name, "w") as file:
        file.write(clean)

    print(f"Article saved to {file_name}")

    

if __name__ == "__main__":
    execute()
