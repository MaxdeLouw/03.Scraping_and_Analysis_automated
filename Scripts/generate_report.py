from pathlib import Path
import sqlite3

import pandas as pd


def main():
    project_root = Path(__file__).resolve().parents[1]
    sql_path = project_root/'SQL'/'Data_Exploration.sql'
    db_path = project_root/ 'Data'/'Processed'/'supermarket_products.db'
    output_path = project_root/ 'Report'/'Report.txt'

    output_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)

    sql_file = sql_path.read_text(encoding="utf-8")
    sql_blocks = sql_file.split(";")

    report = ""
    report += "PLUS + JUMBO YOGHURT REPORT\n"
    report += "==========================\n\n"

    
    for sql_block in sql_blocks:
        sql_block = sql_block.strip()

        lines = sql_block.split("\n")

        sql_title = lines[0].replace("--", "").strip()
        sql_query = "\n".join(lines[1:]).strip()

        if not sql_query:
                continue

        df = pd.read_sql_query(sql_query, conn)

        report += f"{sql_title}\n"
        report += "-" * len(sql_title)
        report += "\n\n"

        report += f"This query returned {len(df)} rows.\n\n"

        report += df.to_string(index=False)
        report += "\n\n"

    output_path.write_text(report, encoding="utf-8")


    conn.close()

    print("Report saved")


if __name__ == "__main__":
    main()