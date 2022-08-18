# how-to-make-web-scraping-faster
How to Make Web Scraping Faster - Python Tutorial


```python
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
```

```bash
pip install requests
```

```python
import csv
import re
import time
import requests

def get_links():

    links = []

    with open("links.csv", "r") as f:

        reader = csv.reader(f)

        for i, row in enumerate(reader):

            links.append(row[0])

    return links

def get_response(session, url):

    with session.get(url) as resp:

        print('.', end='', flush=True)

        text = resp.text

        exp = r'(<title>).*(<\/title>)'

        return re.search(exp, text,flags=re.DOTALL).group(0)

def main():
    start_time = time.time()

    with requests.Session() as session:
        results = []
        for url in get_links():
            result = get_response(session, url)
            print(result)

    print(f"{(time.time() - start_time):.2f} seconds")

   

    

main()


```

```python
from multiprocessing import Pool
```

```python
def get_response(url):
    resp = requests.get(url)
    print('.', end='', flush=True)
    text = resp.text
    
    exp = r'(<title>).*(<\/title>)'
    return re.search(exp, text, flags=re.DOTALL).group(0)

def main():
    start_time = time.time()
    links = get_links()

    with Pool(100) as p:
        results = p.map(get_response, links)
        
        for result in results:
            print(result)

    print(f"{(time.time() - start_time):.2f} seconds")
```

```python
from concurrent.futures import ThreadPoolExecutor
```

```python
with ThreadPoolExecutor(max_workers=100) as p:
    results = p.map(get_response, links)
```

```python
python3 -m pip install aiohttp
```

```python
import aiohttp 
import asyncio
```

```python
async def get_response(session, url):
    async with session.get(url) as resp:
        text = await resp.text()
        
        exp = r'(<title>).*(<\/title>)'
        return re.search(exp, text,flags=re.DOTALL).group(0)
```

```python
async def main():
    start_time = time.time()
    async with aiohttp.ClientSession() as session:

        tasks = []
        for url in get_links():
            tasks.append(asyncio.create_task(get_response(session, url)))

        results = await asyncio.gather(*tasks)
        for result in results:
            print(result)

    print(f"{(time.time() - start_time):.2f} seconds")
```
