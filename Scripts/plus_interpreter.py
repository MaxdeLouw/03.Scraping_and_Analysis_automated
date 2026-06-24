from pathlib import Path
import json
from datetime import datetime
import pandas as pd

def load_json(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return json.loads(text)


def parse_plus_product(json_path):

    scraped_at = datetime.today()
    ID = json_path.stem.split(".")[0]
    data = load_json(json_path)

    product_name = data.get("data", {}).get("ProductOut", {}).get('Overview', {}).get("Name")
    product_price = data.get("data", {}).get("ProductOut", {}).get('Overview', {}).get("Price")
    price_per_unit = data.get("data", {}).get("ProductOut", {}).get('Overview', {}).get("BaseUnitPrice")

    nutrient_tables = (
        data
        .get("data", {})
        .get("ProductOut", {})
        .get("Nutrient")
        .get("Nutrients")
        .get("List", [])
    )

    nutrients = {}

    for nutrient in nutrient_tables:
        name = nutrient.get("Description").lower()
        quantity = nutrient.get("QuantityContained").get("Value")
        nutrients.update({name:quantity})

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
    "Product_ID": ID,
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
        except:
            print(f"Error parsing {json_path}")

    df = pd.DataFrame(records, columns=columns)
    return df

def main():
    input_folder = Path(r"C:\Users\maxde\03.Scraping_and_Analysis_automated\Data\Raw\PLUS\Product_JSON")
    output_path = Path(r"C:\Users\maxde\03.Scraping_and_Analysis_automated\Data\Raw\plus_product_data.csv")


    product_DF = parse_plus_folder(input_folder)
    product_DF.to_csv(output_path, index=False)

main()