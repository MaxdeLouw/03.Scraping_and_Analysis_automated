from datetime import datetime
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup


# Parse one saved Jumbo product HTML page
def parse_jumbo_product(html_path):
    html = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "lxml")

    scraped_at = datetime.today()
    product_id = html_path.stem.split("-")[-1]

    title_element = soup.select_one(".current-item")
    product_name = title_element.get_text(" ", strip=True)

    price_element = soup.select_one("div.current-price")
    product_price = price_element.get_text(" ", strip=True)

    price_quantity_element = soup.select_one("div.price-per-unit")
    price_per_unit = price_quantity_element.get_text(" ", strip=True)

    nutrition = {}

    tables = soup.find_all("table")

    for table in tables:
        table_text = table.get_text(" ", strip=True).lower()

        if "voedingswaarden" not in table_text:
            continue

        rows = table.find_all("tr")

        for row in rows:
            cells = row.find_all("td")

            cell_texts = [
                cell.get_text(" ", strip=True)
                for cell in cells
            ]

            if len(cell_texts) < 2:
                continue

            nutrient = cell_texts[0].lower()

            if cell_texts[1]:
                per_100 = cell_texts[1]
            else:
                per_100 = cell_texts[2]

            nutrition[nutrient] = per_100

    energy_kj = nutrition.get("energie")
    fats = nutrition.get("vetten")
    carbs = nutrition.get("koolhydraten")
    sugars = nutrition.get("waarvan suikers")
    protein = nutrition.get("eiwitten")
    salt = nutrition.get("zout")

    record = {
        "Source_File": html_path.name,
        "Date_Added": scraped_at,
        "Supermarket": "Jumbo",
        "Product_Category": "Yoghurt",
        "Product_ID": product_id,
        "Product_Name": product_name,
        "Product_Price": product_price,
        "Price_Per_Unit": price_per_unit,
        "Energy_kj_100_g": energy_kj,
        "Fats_100_g": fats,
        "Carbs_100_g": carbs,
        "Sugars_100_g": sugars,
        "Protein_100_g": protein,
        "Salt_100_g": salt,
    }

    return record


# Parse all saved Jumbo product pages into one dataframe
def parse_jumbo_folder(input_folder):
    input_folder = Path(input_folder)

    columns = [
        "Source_File",
        "Date_Added",
        "Supermarket",
        "Product_Category",
        "Product_ID",
        "Product_Name",
        "Product_Price",
        "Price_Per_Unit",
        "Energy_kj_100_g",
        "Fats_100_g",
        "Carbs_100_g",
        "Sugars_100_g",
        "Protein_100_g",
        "Salt_100_g",
    ]

    records = []

    for html_path in input_folder.glob("*.html"):
        try:
            record = parse_jumbo_product(html_path)
            records.append(record)
        except Exception as error:
            print(f"Error parsing {html_path}: {error}")

    df = pd.DataFrame(records, columns=columns)

    return df


# Run parser and save raw Jumbo product CSV
def main():
    project_root = Path(__file__).resolve().parents[1]

    product_folder = project_root / "Data" / "Raw" / "Jumbo" / "Individual_products"
    output_path = project_root / "Data" / "Raw" / "jumbo_product_data.csv"

    product_df = parse_jumbo_folder(product_folder)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    product_df.to_csv(output_path, index=False)

    print(f"Parsed products: {len(product_df)}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()