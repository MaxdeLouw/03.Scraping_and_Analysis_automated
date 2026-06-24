from pathlib import Path
import json

from playwright.sync_api import sync_playwright


# Save Python data as a JSON file
def save_json(data, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


# Save one PLUS listing page JSON response
def save_plus_listing_page(page, category_url, page_number, output_folder):
    page_url = f"{category_url}?pagina={page_number}"
    output_path = output_folder / f"plus_listing_page_{page_number}.json"

    with page.expect_response(
        lambda response: "DataActionGetProductListAndCategoryInfo" in response.url,
        timeout=60_000
    ) as response_info:
        page.goto(
            page_url,
            wait_until="networkidle",
            timeout=60_000,
        )

    response = response_info.value
    data = response.json()

    save_json(data, output_path)

    print(f"Saved listing page: {output_path.name}")


# Collect all PLUS listing JSON pages
def collect_all_listing_json(category_url, output_folder):
    total_pages = 15

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        try:
            page = browser.new_page(locale="nl-NL")

            for page_number in range(1, total_pages + 1):
                save_plus_listing_page(
                    page=page,
                    category_url=category_url,
                    page_number=page_number,
                    output_folder=output_folder,
                )

        finally:
            browser.close()


# Load one saved JSON file
def load_json(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return json.loads(text)


# Extract product URLs from saved PLUS listing JSON files
def extract_url_from_listing_json(input_folder):
    input_folder = Path(input_folder)

    json_paths = sorted(input_folder.glob("*.json"))
    records = []

    for json_path in json_paths:
        data = load_json(json_path)

        product_items = (
            data
            .get("data", {})
            .get("ProductList", {})
            .get("List", [])
        )

        for item in product_items:
            product = item.get("PLP_Str", {})

            sku = product.get("SKU")
            slug = product.get("Slug")

            if not sku or not slug:
                continue

            product_url = "https://www.plus.nl/product/" + slug

            record = {
                "SKU": sku,
                "Source_File": json_path.name,
                "Product_Name": product.get("Name"),
                "Product_URL": product_url,
            }

            records.append(record)

    return records


# Remove duplicate products before visiting detail pages
def dedupe_records_by_sku(records):
    unique_records = {}

    for record in records:
        sku = record.get("SKU")

        if not sku:
            continue

        unique_records[sku] = record

    return list(unique_records.values())


# Visit one product page and save its product detail JSON response
def extract_product_json(page, record, output_folder):
    page_url = record.get("Product_URL")
    sku = record.get("SKU")

    output_path = output_folder / f"{sku}.json"

    if output_path.exists():
        print(f"Already processed: {output_path.name}")
        return

    with page.expect_response(
        lambda response: "DataActionGetProductDetailsAndAgeInfo" in response.url,
        timeout=60_000
    ) as response_info:
        page.goto(
            page_url,
            wait_until="networkidle",
            timeout=60_000,
        )

    response = response_info.value
    data = response.json()

    save_json(data, output_path)

    print(f"Saved product JSON: {output_path.name}")


# Visit all PLUS product URLs and save detail JSON files
def collect_all_product_json(records, output_folder):
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        try:
            page = browser.new_page(locale="nl-NL")

            for index, record in enumerate(records, start=1):
                try:
                    print(f"[{index}/{len(records)}] {record.get('Product_Name')}")
                    extract_product_json(
                        page=page,
                        record=record,
                        output_folder=output_folder,
                    )

                except Exception as error:
                    print(f"Error scraping product {record.get('SKU')}: {error}")

        finally:
            browser.close()


# Run PLUS scraper
def main():
    project_root = Path(__file__).resolve().parents[1]

    category_url = "https://www.plus.nl/producten/zuivel-eieren-boter/verse-zuivel/yoghurt"

    listing_json_folder = project_root / "Data" / "Raw" / "PLUS" / "Listing_JSON"
    product_json_folder = project_root / "Data" / "Raw" / "PLUS" / "Product_JSON"

    listing_json_folder.mkdir(parents=True, exist_ok=True)
    product_json_folder.mkdir(parents=True, exist_ok=True)

    collect_all_listing_json(category_url, listing_json_folder)

    records = extract_url_from_listing_json(listing_json_folder)
    records = dedupe_records_by_sku(records)

    print(f"Unique product URLs: {len(records)}")

    collect_all_product_json(records, product_json_folder)


if __name__ == "__main__":
    main()