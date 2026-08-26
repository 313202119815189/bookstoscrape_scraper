# Books to Scrape - Multi-Page Python Scraper

A robust, multi-page web scraper built with Python using `httpx` and `lxml`. It recursively crawls all catalog pages on `books.toscrape.com`, extracts detailed product metadata, and exports the dataset to both `JSON` and `CSV`.

## Features
- **Session Pooling:** Efficient connection reuse using `httpx.Client`.
- **XPath Parsing:** Precise data extraction using `lxml.html` for titles, prices, availability, and star ratings.
- **Robust Navigation:** Relative URL resolution via `urllib.parse.urljoin` for seamless pagination across all 50 pages.
- **Error Handling & Politeness:** Includes request timeouts, HTTP error handling, random User-Agent rotation, and rate-limiting delays.
- **Dual Export:** Outputs structured data to UTF-8 formatted `JSON` and UTF-8-BOM `CSV` (Excel-compatible).

## Tech Stack
- **HTTP Client:** `httpx`
- **HTML Parser:** `lxml`
- **Data Export:** `csv`, `json`

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/books-toscrape-scraper.git](https://github.com/your-username/books-toscrape-scraper.git)
   cd books-toscrape-scraper
