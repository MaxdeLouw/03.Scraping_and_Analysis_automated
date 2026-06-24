from pathlib import Path
import json
from playwright.sync_api import sync_playwright


def save_json(data, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(json.dumps(data), encoding="utf-8")


def save_plus_listing_page(page, category_url, page_number, output_folder):

    page_url = f"{category_url}?pagina={page_number}"
    output_path = output_folder / f"plus_listing_page_{page_number}.json"

    with page.expect_response(lambda response: "DataActionGetProductListAndCategoryInfo" in response.url, timeout=60_000) as response_info:
        page.goto(
            page_url,
            wait_until="networkidle",
            timeout=60_000,
        )

    response = response_info.value
    data = response.json()

    save_json(data, output_path)

    print(f"Saved: {output_path.name}")

def collect_all_json(category_url, output_folder):
    total_pages = 15

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page(locale="nl-NL")
            for page_number in range(1, total_pages + 1):
                save_plus_listing_page(page=page, category_url=category_url, page_number=page_number, output_folder=output_folder)

        finally:
            browser.close()

def load_json(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return json.loads(text)

def extract_url_from_listing_json(input_folder):

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
                "SKU" : sku,
                "Source_File": json_path.name,
                "Product_Name": product.get("Name"),
                "Product_URL": product_url
            }

            records.append(record)
    return records

def extract_product_json(record, output_folder):
    page_url = record.get('Product_URL')

    sku = record.get("SKU")
    output_path = output_folder/ f"{sku}.json"


    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page(locale="nl-NL")

            with page.expect_response(lambda response: "DataActionGetProductDetailsAndAgeInfo" in response.url, timeout=60_000) as response_info:
                page.goto(
                    page_url,
                    wait_until="networkidle",
                    timeout=60_000,
                )

            response = response_info.value
            data = response.json()

            save_json(data, output_path)

            print(f"Saved: {output_path.name}")
        
        finally:
            browser.close()



def main():
    category_url = "https://www.plus.nl/producten/zuivel-eieren-boter/verse-zuivel/yoghurt"

    output_json_folder = Path(r"Data\Raw\PLUS\Listing_JSON")
    output_json_folder.mkdir(parents=True, exist_ok=True)

    collect_all_json(category_url, output_json_folder)

    records = extract_url_from_listing_json(output_json_folder)

    output_json_product_folder = Path(r"Data\Raw\PLUS\Product_JSON")
    output_json_product_folder.mkdir(parents=True, exist_ok=True)


    for record in records:
        extract_product_json(record, output_json_product_folder)

main()