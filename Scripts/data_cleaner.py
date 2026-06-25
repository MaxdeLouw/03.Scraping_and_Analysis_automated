from pathlib import Path
import pandas as pd


# Shared cleaning helpers
def clean_float(value):
    if pd.isna(value):
        return None

    try:
        return float(value)
    except Exception:
        pass

    try:
        return float(str(value).split(" ")[0].replace(",", "."))
    except Exception:
        return None


def clean_price(price_text):
    if pd.isna(price_text):
        return None

    try:
        return float(price_text)
    except Exception:
        pass

    try:
        return float(
            str(price_text)
            .split(" ")[1]
            .split("\xa0")[1]
            .replace(",", ".")
        )
    except Exception:
        return None


def clean_unit_price(price_unit_text):
    if pd.isna(price_unit_text):
        return None

    try:
        return float(price_unit_text)
    except Exception:
        pass

    try:
        return float(
            str(price_unit_text)
            .split(" ")[3]
            .replace(",", ".")
        )
    except Exception:
        return None


def clean_energy_kj(energy_text):
    return clean_float(energy_text)


def clean_nutrient(nutrient_text):
    return clean_float(nutrient_text)


# Build one standardized dataframe for both supermarkets
def make_clean_dataframe(raw_df, supermarket_name):
    clean_df = pd.DataFrame()

    clean_df["Source_File"] = raw_df["Source_File"]
    clean_df["Date_Added"] = pd.to_datetime(
        raw_df["Date_Added"]
    ).dt.date

    clean_df["Supermarket"] = supermarket_name
    clean_df["Product_Category"] = raw_df["Product_Category"]
    clean_df["Product_ID"] = raw_df["Product_ID"]

    clean_df["Product_Name"] = raw_df["Product_Name"].str.replace(" ", "_")
    clean_df["Brand"] = raw_df["Product_Name"].str.split(" ").str[0]

    product_price = raw_df["Product_Price"].apply(clean_price)
    price_per_unit = raw_df["Price_Per_Unit"].apply(clean_unit_price)

    clean_df["Product_Price"] = product_price.round(1)
    clean_df["Price_Per_Unit"] = price_per_unit.round(1)

    # Weight is estimated from product price and unit price.
    weight_g = product_price / price_per_unit * 1000

    if supermarket_name == "PLUS":
        weight_g = weight_g.where(weight_g <= 2500, weight_g / 10)
        weight_g = weight_g.where(weight_g >= 100, weight_g * 10)

    clean_df["Weight_g"] = weight_g.round(1)
    clean_df["Price_Per_kg"] = (clean_df["Product_Price"] * 1000 / clean_df['Weight_g']).round(1)

    energy_kj_100_g = raw_df["Energy_kj_100_g"].apply(clean_energy_kj)
    clean_df["Energy_kcal_100_g"] = (energy_kj_100_g / 4.184).round(1)

    fats_100_g = raw_df["Fats_100_g"].apply(clean_nutrient)
    carbs_100_g = raw_df["Carbs_100_g"].apply(clean_nutrient)
    sugars_100_g = raw_df["Sugars_100_g"].apply(clean_nutrient)
    protein_100_g = raw_df["Protein_100_g"].apply(clean_nutrient)
    salt_100_g = raw_df["Salt_100_g"].apply(clean_nutrient)

    clean_df["Fats_In_Product_g"] = (fats_100_g * clean_df["Weight_g"] / 100).round(1)
    clean_df["Carbs_In_Product_g"] = (carbs_100_g * clean_df["Weight_g"] / 100).round(1)
    clean_df["Sugars_In_Product_g"] = (sugars_100_g * clean_df["Weight_g"] / 100).round(1)
    clean_df["Protein_In_Product_g"] = (protein_100_g * clean_df["Weight_g"] / 100).round(1)
    clean_df["Salt_In_Product_g"] = (salt_100_g * clean_df["Weight_g"] / 100).round(1)

    clean_df = clean_df.dropna(subset=["Energy_kcal_100_g"]).reset_index(drop=True)

    return clean_df

# Save helper
def save_dataframe(df, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")
    print(df.shape)


# Individual supermarket cleaners
def clean_jumbo_data(input_path, output_path):
    jumbo_raw = pd.read_csv(input_path)
    jumbo_clean = make_clean_dataframe(jumbo_raw, "Jumbo")

    save_dataframe(jumbo_clean, output_path)

    return jumbo_clean


def clean_plus_data(input_path, output_path):
    plus_raw = pd.read_csv(input_path)
    plus_clean = make_clean_dataframe(plus_raw, "PLUS")

    save_dataframe(plus_clean, output_path)

    return plus_clean


# Combine both cleaned supermarket datasets
def combine_dataframes(jumbo_clean, plus_clean, output_path):
    combined_df = pd.concat(
        [jumbo_clean, plus_clean],
        ignore_index=True
    )

    save_dataframe(combined_df, output_path)

    return combined_df


def main():
    project_root = Path(__file__).resolve().parents[1]

    jumbo_input_path = project_root / "Data" / "Raw" / "jumbo_product_data.csv"
    plus_input_path = project_root / "Data" / "Raw" / "plus_product_data.csv"

    jumbo_output_path = project_root / "Data" / "Processed" / "jumbo_product_data_clean.csv"
    plus_output_path = project_root / "Data" / "Processed" / "plus_product_data_clean.csv"
    combined_output_path = project_root / "Data" / "Processed" / "supermarket_product_data_clean.csv"

    jumbo_clean = clean_jumbo_data(jumbo_input_path, jumbo_output_path)
    plus_clean = clean_plus_data(plus_input_path, plus_output_path)

    combine_dataframes(
        jumbo_clean,
        plus_clean,
        combined_output_path
    )


main()