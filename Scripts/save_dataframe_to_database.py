import pandas as pd
import sqlite3 as sqlite
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
df_path = project_root / 'Data' / 'Processed' / 'supermarket_product_data_clean.csv'
df_path = Path(df_path)

db_path = project_root / "Data" / "Processed" / "supermarket_products.db"


supermarket_DF = pd.read_csv(df_path)
conn = sqlite.connect(db_path)

supermarket_DF.to_sql(
    name="supermarket_products",
    con=conn,
    if_exists="replace",
    index=False,
)

conn.close()

print("Database succesfully created")