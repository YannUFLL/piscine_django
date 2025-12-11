import requests
import sys
import json
from bs4 import BeautifulSoup, Tag
from html.parser import HTMLParser



def get_relative_url(url):
    
    headers = {
        "User-Agent": "request_wikipedia.py/1.0 (https://github.com/yannUFLL)"
    }
    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    page_title = soup.find(id="firstHeading").text
    content = soup.find(id="mw-content-text")
    content_direct_child = content.find(class_="mw-parser-output")

    redir = content_direct_child.find(class_="redirectText", recursive=True)
    if redir: 
        return (redir.find('a', recursive=True).get("href"))

    child = next(content_direct_child.children)
    while child:
        if getattr(child, "name", None) in ("link", "img"):
            try:
                child = next(child.children)
                continue
            except StopIteration:
                child = child.next_element
                continue
        if getattr(child, "name", None) == 'p':
            all_a = child.find_all('a')
            for a in all_a:
                href = a["href"] 
                if not href.startswith("/wiki/"):
                    continue
                if ":" in href :
                    continue 
                return (href, page_title)
        elif getattr(child, "name", None) == "h2":
            return (None)
        child = child.next_sibling
    return (None)

def execute():

    if len(sys.argv) != 2:
        print("Error: you must provide the title of the page")
        sys.exit(1)
    
    first_article = sys.argv[1].replace(' ', '_')

    base_url =  "https://en.wikipedia.org"
    full_url = f'{base_url}/wiki/{first_article}?redirect=no'
    saved_url = []
    number = 0

    
    while (1):
        r_url, page_title = get_relative_url(full_url)
        if r_url == None:
            print("It leads to a dead end !")
            sys.exit(0)
        number += 1
        full_url = base_url + r_url + "?redirect=no"
        if (page_title == "Philosophy"):
            print(f"{number} roads from {first_article} to philosophy !")
            sys.exit(0)
        else:
            print(f"{page_title}")
        if full_url in saved_url: 
            print("It lead to an infinite loop !")
            sys.exit(0)
        saved_url.append(full_url)

    sys.exit(1)

    

if __name__ == "__main__":
    execute()
