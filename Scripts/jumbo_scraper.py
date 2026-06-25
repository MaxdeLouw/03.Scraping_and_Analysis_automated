from pathlib import Path
from urllib.parse import urljoin
from collections import Counter

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


# Save one rendered web page as an HTML file
def save_page_as_html(url, destination_folder):
    output_folder = Path(destination_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    filename = url.rstrip("/").split("/")[-1] + ".html"
    output_path = output_folder / filename

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        try:
            page = browser.new_page(locale="nl-NL")
            page.goto(url, wait_until="domcontentloaded", timeout=60_000)

            html = page.content()
            output_path.write_text(html, encoding="utf-8")

            print(f"Page title: {page.title()}")
            print(f"Saved to: {output_path.resolve()}")

        finally:
            browser.close()

    return output_path


# Save Jumbo category overview pages with offset pagination
def save_overviews_as_html(category_url, destination, page_size, max_pages):
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

                output_path = destination / f"jumbo_yoghurt_offset_{offset}.html"

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


# Extract product links from saved Jumbo overview HTML files
def find_product_links(folder_link):
    folder_link = Path(folder_link)
    product_links = []

    for file_path in folder_link.glob("*.html"):
        html = file_path.read_text(encoding="utf-8")
        soup = BeautifulSoup(html, "lxml")

        for link in soup.find_all("a"):
            href = link.get("href")

            if href is None:
                continue

            if href.startswith("/producten/"):
                full_url = urljoin("https://www.jumbo.com", href)
                product_links.append(full_url)

        print(f"Found {len(product_links)} links so far")

    link_counts = Counter(product_links)

    print(f"Total links found: {len(product_links)}")
    print(f"Unique links found: {len(link_counts)}")
    print(f"Duplicate links: {len(product_links) - len(link_counts)}")

    unique_links = sorted(set(product_links))

    return unique_links


# Save every Jumbo product page from a list of product URLs
def save_product_pages(links, destination_folder):
    output_folder = Path(destination_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    faulty_links = []

    for index, link in enumerate(links, start=1):
        filename = link.rstrip("/").split("/")[-1] + ".html"
        output_path = output_folder / filename

        if output_path.exists():
            print(f"[{index}/{len(links)}] Already processed: {output_path.name}")
            continue

        try:
            print(f"[{index}/{len(links)}] Saving: {link}")
            save_page_as_html(url=link, destination_folder=destination_folder)

        except Exception as error:
            print(f"[{index}/{len(links)}] Failed: {link}")
            print(f"Reason: {error}")
            faulty_links.append(link)
            continue

    print(f"Faulty links: {len(faulty_links)}")
    print(faulty_links)


# Run Jumbo scraper
def main():
    project_root = Path(__file__).resolve().parents[1]

    source_folder = project_root / "Data" / "Raw" / "Jumbo" / "Yoghurt_Jumbo"
    destination_folder = project_root / "Data" / "Raw" / "Jumbo" / "Individual_products"

    category_url = "https://www.jumbo.com/producten/zuivel,-boter-en-eieren/yoghurt-en-kwark/yoghurt-en-skyr/"

    save_overviews_as_html(
        category_url=category_url,
        destination=source_folder,
        page_size=24,
        max_pages=9,
    )

    links = find_product_links(folder_link=source_folder)

    save_product_pages(links, destination_folder)


if __name__ == "__main__":
    main()