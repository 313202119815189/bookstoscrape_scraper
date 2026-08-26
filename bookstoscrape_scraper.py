import csv
import json
import random
import time
from urllib.parse import urljoin

import httpx
from lxml import html

START_URL = 'https://books.toscrape.com'

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0'
]


def get_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9'
    }


def scrape_all(start_url):
    results = []
    url = start_url

    with httpx.Client(headers=get_headers(), follow_redirects=True) as client:
        while True:
            print(f'Scraping: {url}')
            try:
                resp = client.get(url, timeout=15)
                resp.raise_for_status()
            except httpx.HTTPStatusError as exc:
                if exc.response is not None and exc.response.status_code in (404, 429, 500):
                    print(f'HTTP {exc.response.status_code} for {url}; stopping.')
                    break
                raise
            except httpx.RequestError as exc:
                print(f'Request failed for {url}: {exc}')
                break

            tree = html.fromstring(resp.text)
            books = tree.xpath("//article[contains(@class, 'product_pod')]")

            for book in books:
                cover_rel = book.xpath("./div/a/img/@src")
                cover = urljoin(url, cover_rel[0]) if cover_rel else ''

                title_attr = book.xpath(".//h3/a/@title")
                if title_attr:
                    title = title_attr[0]
                else:
                    title_text = book.xpath(".//h3/a/text()")
                    title = ' '.join(part.strip() for part in title_text if part.strip())

                price_text = book.xpath(".//p[contains(@class, 'price_color')]/text()")
                price = price_text[0].strip() if price_text else ''

                availability_text = book.xpath(".//p[contains(@class, 'instock')]/text()")
                availability = ' '.join(part.strip() for part in availability_text if part.strip())

                rating_classes = book.xpath(".//p[contains(@class, 'star-rating')]/@class")
                rating = None
                if rating_classes:
                    classes = rating_classes[0].split()
                    for c in classes:
                        if c != 'star-rating':
                            rating = c
                            break

                results.append({
                    'title': title,
                    'cover': cover,
                    'price': price,
                    'availability': availability,
                    'rating': rating
                })

            next_link = tree.xpath("//li[contains(@class, 'next')]/a/@href")
            if next_link:
                url = urljoin(url, next_link[0])
                time.sleep(0.5)
                continue
            else:
                break

    return results


if __name__ == '__main__':
    books = scrape_all(START_URL)
    print(f'Found {len(books)} books')

    with open('books.json', 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

    with open('books.csv', 'w', newline='', encoding='utf-8-sig') as csv_file:
        headers = books[0].keys() if books else ['title', 'cover', 'price', 'availability', 'rating']
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(books)

    print('Saved to books.json and books.csv')
