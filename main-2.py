import requests
from bs4 import BeautifulSoup
import json
import os

os.makedirs("output", exist_ok=True)


base_url = "http://quotes.toscrape.com"
quotes = []
authors_data = {}
visited_authors = set()

page = 1
while True:
    res = requests.get(f"{base_url}/page/{page}/")
    if res.status_code != 200:
        break

    soup = BeautifulSoup(res.text, "html.parser")
    quote_blocks = soup.select(".quote")

    if not quote_blocks:
        break

    for block in quote_blocks:
        text = block.find("span", class_="text").get_text(strip=True)
        author_name = block.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in block.select(".tags .tag")]

        quotes.append({
            "tags": tags,
            "author": author_name,
            "quote": text
        })

        if author_name not in visited_authors:
            author_link = block.find("a")["href"]
            author_res = requests.get(base_url + author_link)
            author_soup = BeautifulSoup(author_res.text, "html.parser")

            born_date = author_soup.find(class_="author-born-date").get_text(strip=True)
            born_location = author_soup.find(class_="author-born-location").get_text(strip=True)
            description = author_soup.find(class_="author-description").get_text(strip=True)

            authors_data[author_name] = {
                "fullname": author_name,
                "born_date": born_date,
                "born_location": born_location,
                "description": description
            }

            visited_authors.add(author_name)

    page += 1



with open("quotes.json", "w", encoding="utf-8") as f:
    json.dump(quotes, f, ensure_ascii=False, indent=2)

with open("authors.json", "w", encoding="utf-8") as f:
    json.dump(list(authors_data.values()), f, ensure_ascii=False, indent=2)

