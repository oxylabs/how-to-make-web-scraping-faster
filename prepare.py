import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def fetch_links(url="https://books.toscrape.com/", links=[]):
    r = requests.get(url)
    print(r.url, flush=True)
    soup = BeautifulSoup(r.text, "html.parser")
    for link in soup.select("h3 a"):
        links.append(urljoin(url, link.get("href")))
    next_page = soup.select_one("li.next a")
    if next_page:
        return fetch_links(urljoin(url, next_page.get("href"), links))
    else:
        return links


def refresh_links():
    links = fetch_links()
    with open('links.csv', 'w') as f:
        for link in links:
            f.write(link + '\n')

refresh_links()