import requests
from datetime import datetime, timezone
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
import lxml
from collections import Counter

def save_page_as_html(url, destination):
    output_path = Path(destination)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page(locale="nl-NL")
            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60_000,
            )
            html = page.content()
            output_path.write_text(
                html,
                encoding="utf-8",
            )
            print(f"Page title: {page.title()}")
            print(f"Saved to: {output_path.resolve()}")
        finally:
            browser.close()

    return output_path

def save_overviews_as_html(category_url, destination, page_size, max_pages,):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)

    saved_paths = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        try:
            page = browser.new_page(locale="nl-NL")

            for page_number in range(max_pages):
                offset = page_number * page_size

                page_url = f"{category_url}?offSet={offset}"

                output_path = (destination/ f"jumbo_yoghurt_offset_{offset}.html")
                page.goto(
                    page_url,
                    wait_until="domcontentloaded",
                    timeout=60_000,
                )

                html = page.content()

                output_path.write_text(html, encoding="utf-8")

                saved_paths.append(output_path)

                print(f"Offset: {offset}")
                print(f"Page title: {page.title()}")
                print(f"Saved to: {output_path.resolve()}")
                print()
        finally:
            browser.close()
    return saved_paths

def find_product_links(folder_link):
    product_links = []
    folder_link = Path(folder_link)
    for file in folder_link.glob("*.html"):
        html = Path(file).read_text(encoding="utf-8")
        soup = BeautifulSoup(html,'lxml')

        for link in soup.find_all("a"):
            href = link.get("href")
            if href is None:
                continue

            if href.startswith("/producten/"):
                full_url = urljoin("https://www.jumbo.com", href)
                product_links.append(full_url)

        print(f"Found {len(product_links)} links")
    
    #Remove the duplicate links

    link_counts = Counter(product_links)
    print(f"Total links found: {len(product_links)}")
    print(f"Unique links found: {len(link_counts)}")
    print(f"Duplicate links: {len(product_links) - len(link_counts)}")
    
    unique_links = set(product_links)
    return unique_links

def main():

    # file_name = "jumbo_magere_yoghurt.html"    
    # save_as_html(url = "https://www.jumbo.com/producten/campina-magere-yoghurt-1-l-527014PAK",
    #             destination = Path.cwd()/"Data"/"Raw"/file_name
    # )
    
    # folder_name = "Yoghurt_Jumbo"
    # save_overviews_as_html(category_url = "https://www.jumbo.com/producten/zuivel,-boter-en-eieren/yoghurt-en-kwark/yoghurt-en-skyr/"
    #                       ,destination = Path.cwd()/"Data"/"Raw"/folder_name, page_size = 24, max_pages = 9)

    folder_name = "Yoghurt_Jumbo"
    links = find_product_links(folder_link = Path.cwd()/"Data"/"Raw"/folder_name)


main()