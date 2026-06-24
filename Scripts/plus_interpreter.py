from pathlib import Path
import json
from datetime import datetime

import pandas as pd


# Load one saved PLUS product JSON file
def load_json(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return json.loads(text)


# Parse one saved PLUS product JSON file
def parse_plus_product(json_path):
    scraped_at = datetime.today()
    product_id = json_path.stem

    data = load_json(json_path)

    product_out = data.get("data", {}).get("ProductOut", {})
    overview = product_out.get("Overview", {})

    product_name = overview.get("Name")
    product_price = overview.get("Price")
    price_per_unit = overview.get("BaseUnitPrice")

    nutrient_tables = (
        product_out
        .get("Nutrient", {})
        .get("Nutrients", {})
        .get("List", [])
    )

    nutrients = {}

    for nutrient in nutrient_tables:
        name = nutrient.get("Description", "").lower()
        quantity = nutrient.get("QuantityContained", {}).get("Value")

        if name:
            nutrients[name] = quantity

    energy_kj = nutrients.get("energie kj")
    fats = nutrients.get("vet")
    carbs = nutrients.get("koolhydraten")
    sugars = nutrients.get("waarvan suikers")
    protein = nutrients.get("eiwitten")
    salt = nutrients.get("zout")

    record = {
        "Source_File": json_path.name,
        "Date_Added": scraped_at,
        "Supermarket": "Plus",
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


# Parse all saved PLUS product JSON files into one dataframe
def parse_plus_folder(input_folder):
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

    for json_path in input_folder.glob("*.json"):
        try:
            record = parse_plus_product(json_path)
            records.append(record)
        except Exception as error:
            print(f"Error parsing {json_path}: {error}")

    df = pd.DataFrame(records, columns=columns)

    return df


# Run parser and save raw PLUS product CSV
def main():
    project_root = Path(__file__).resolve().parents[1]

    input_folder = project_root / "Data" / "Raw" / "PLUS" / "Product_JSON"
    output_path = project_root / "Data" / "Raw" / "plus_product_data.csv"

    product_df = parse_plus_folder(input_folder)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    product_df.to_csv(output_path, index=False)

    print(f"Parsed products: {len(product_df)}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()