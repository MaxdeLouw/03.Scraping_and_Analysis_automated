# 03.Scraping_and_Analysis_automated# Supermarket Yoghurt Price & Nutrition Analysis

## Project Overview

This project is an automated data collection and analysis pipeline for yoghurt products from two Dutch supermarkets: **Jumbo** and **PLUS**.

The goal of the project is to compare supermarket yoghurt products on assortment, price, product size, nutrition, and value-for-money. The project collects product data from supermarket websites, parses the raw HTML/JSON data, cleans and standardizes the data, stores it in a SQLite database, runs SQL-based analysis, and generates a readable report.

This project covers:

* Web scraping with Playwright
* HTML parsing with BeautifulSoup
* JSON parsing
* Data cleaning with pandas
* Data validation and correction rules
* SQLite database creation
* SQL-based data exploration
* Automated report generation
* Pipeline automation through `main.py`

## Goal

The main question behind this project is:

> How do yoghurt products at Jumbo and PLUS compare in terms of price, assortment, nutrition, and value?

More specifically, the analysis looks at:

* Number of yoghurt products per supermarket
* Biggest brands per supermarket
* Missing values and data completeness
* Most expensive and cheapest products per kilogram
* House-brand products compared to other brands
* Price comparison for brands sold at both supermarkets
* Best protein value per euro
* Cheapest calories per euro
* Products with the highest and lowest sugar percentage
* High-protein and lower-sugar product options

## Data Sources

The data was collected from the public product pages of:

* [Jumbo](https://www.jumbo.com/)
* [PLUS](https://www.plus.nl/)

The collected data represents a snapshot of yoghurt products at the time of scraping. The values might obviously change over time. These sources were chosen because they required different scraping methods (JSON & HTML), and because other supermarket do not allow automated scraping.

## Pipeline Summary

The project follows this pipeline:

1. Scrape Jumbo overview and product pages
2. Parse Jumbo product HTML into structured data
3. Scrape PLUS listing JSON and product detail JSON
4. Parse PLUS product JSON into structured data
5. Clean and standardize both supermarket datasets
6. Combine both datasets into one cleaned CSV
7. Save cleaned data to a SQLite database
8. Run SQL analysis queries
9. Generate a text report

The entire pipeline can be run through `main.py`.

## Workflow Explanation

### 1. Jumbo scraping

The Jumbo scraper first collects category overview html pages. These pages contain links to individual yoghurt product pages. The scraper then extracts product URLs from the saved overview HTML files and visits each product page. The rendered HTML of each individual product page is saved locally.

This creates a raw HTML archive of Jumbo product pages.

### 2. Jumbo parsing

The Jumbo parser reads each saved product HTML file and extracts relevant product information, including:

* Product name
* Product ID
* Product price
* Price per unit
* Nutrition values
* Source file
* Scrape date
* Supermarket name
* Product category

The parsed output is saved.

### 3. PLUS scraping

PLUS was handled differently from Jumbo because the useful product data was available through JSON responses.

The PLUS scraper collects listing JSON files from the yoghurt category pages. These listing JSON files contain product metadata such as SKU, name, slug, and product URL information.

The scraper then uses the product slugs to visit individual product pages and captures the product-detail JSON response.

This creates two raw PLUS data folders.

### 4. PLUS parsing

The PLUS parser reads the saved product-detail JSON files and extracts structured product data, including (same format as Jumbo dataframe):

* Product name
* Product ID / SKU
* Product price
* Base unit price
* Nutrition values
* Source file
* Scrape date
* Supermarket name
* Product category

The parsed output is saved.

### 5. Data cleaning

The cleaning script standardizes the Jumbo and PLUS datasets into a shared structure.

Important cleaning steps include:

* Converting prices from text to numeric values
* Converting energy from kilojoules to kilocalories
* Estimating product weight by combining unit price and actual price
* Calculating total nutrients per product
* Standardizing supermarket names
* Extracting brand names
* Combining Jumbo and PLUS data into one dataset
* Dropping products where key nutrition values are missing

The final combined cleaned dataset is saved.

### 6. SQLite database creation

The cleaned dataset is saved to a SQLite database table called:

```text
supermarket_products
```

The database is saved as:

```text
Data/Processed/supermarket_products.db
```

This allows the cleaned product data to be queried with SQL.

### 7. SQL analysis

The SQL file contains several analysis queries, including:

* Product count per supermarket
* Largest brands per supermarket
* Missing value checks
* Most expensive products
* Cheapest products
* Most expensive brands
* House-brand comparison
* Same-brand price comparison
* Protein per euro
* Calories per euro
* Highest sugar percentage
* Lowest sugar percentage
* High-protein and lower-sugar products

The SQL file is located at:

```text
SQL/Data_Exploration.sql
```

### 8. Report generation

The report script reads the SQL file, executes the queries against the SQLite database, and writes the results into a text report. This text report takes the output of the queries and is meant for an analist to review what they want to focus on in further analysis.

The generated report is saved as:

```text
Reports/basic_supermarket_report.txt
```

## Key Findings

Paste the generated report output below this section.

```text
PLUS + JUMBO YOGHURT REPORT
==========================

01. Slice head
--------------

This query returned 5 rows.

                                     Source_File Date_Added Supermarket Product_Category Product_ID                      Product_Name   Brand  Product_Price  Price_Per_Unit  Weight_g  Price_Per_kg  Energy_kcal_100_g  Fats_In_Product_g  Carbs_In_Product_g  Sugars_In_Product_g  Protein_In_Product_g  Salt_In_Product_g
activia-yoghurt-aardbei-4-x-125-g-228598STK.html 2026-06-26       Jumbo          Yoghurt  228598STK Activia_Yoghurt_Aardbei_4_x_125_g Activia            3.0             6.0     500.0           6.0               88.9               14.0                60.0                 58.5                  18.5                0.6
 activia-yoghurt-granen-4-x-125-g-302972STK.html 2026-06-26       Jumbo          Yoghurt  302972STK  Activia_Yoghurt_Granen_4_x_125_g Activia            3.0             6.0     500.0           6.0               90.6               14.5                56.5                 52.5                  19.5                0.5
 activia-yoghurt-muesli-4-x-125-g-302975STK.html 2026-06-26       Jumbo          Yoghurt  302975STK  Activia_Yoghurt_Muesli_4_x_125_g Activia            2.9             5.8     500.0           5.8               93.7               14.5                60.0                 53.5                  19.5                0.5
activia-yoghurt-naturel-4-x-125-g-491422TUB.html 2026-06-26       Jumbo          Yoghurt  491422TUB Activia_Yoghurt_Naturel_4_x_125_g Activia            2.4             4.8     500.0           4.8               66.0               17.5                23.5                 23.5                  19.5                0.5
  activia-yoghurt-pruim-4-x-125-g-709840PAK.html 2026-06-26       Jumbo          Yoghurt  709840PAK   Activia_Yoghurt_Pruim_4_x_125_g Activia            2.9             5.8     500.0           5.8               98.9               17.0                64.5                 60.0                  17.0                0.5

02. Check items per supermarket
-------------------------------

This query returned 2 rows.

Supermarket  product_count
       PLUS            163
      Jumbo            150

03. Check biggest brands per supermarket
----------------------------------------

This query returned 45 rows.

Supermarket         Brand  product_count
      Jumbo          Ísey             20
      Jumbo      Melkunie             17
      Jumbo       Campina             15
      Jumbo        Almhof             15
      Jumbo          Arla             14
      Jumbo         Alpro             11
      Jumbo         Jumbo              9
      Jumbo   Zuivelhoeve              7
      Jumbo       Optimel              7
      Jumbo         HiPRO              6
      Jumbo       Activia              6
      Jumbo        Dodoni              5
      Jumbo     Danoontje              3
      Jumbo           den              2
      Jumbo           XXL              2
      Jumbo     Halfvolle              2
      Jumbo           Den              2
      Jumbo        Danone              2
      Jumbo         Volle              1
      Jumbo           Pur              1
      Jumbo        Magere              1
      Jumbo      Katharos              1
      Jumbo          Isey              1
       PLUS        Melkan             26
       PLUS        Almhof             17
       PLUS      Melkunie             15
       PLUS       Campina             15
       PLUS          Arla             14
       PLUS       Optimel             10
       PLUS          Isey             10
       PLUS   Zuivelhoeve              8
       PLUS           XXL              6
       PLUS         Alpro              6
       PLUS       Activia              6
       PLUS    Biologisch              5
       PLUS Zuivelmeester              4
       PLUS          PLUS              4
       PLUS           Den              4
       PLUS        Danone              3
       PLUS           Pur              2
       PLUS        Elinas              2
       PLUS         Danio              2
       PLUS          BIO+              2
       PLUS        Nestlé              1
       PLUS        Dodoni              1

04. Check for empty columns
---------------------------

This query returned 2 rows.

Supermarket  total_products  products_with_price  products_with_unit_price  products_with_weight  products_with_energy  products_with_protein
      Jumbo             150                  150                       150                   150                   150                    143
       PLUS             163                  163                       163                   163                   163                    163

05. Look for the most expensive products
----------------------------------------

This query returned 5 rows.

Supermarket     Brand                                       Product_Name  Product_Price  Price_Per_kg  Weight_g
      Jumbo Danoontje        Danoontje_Yoghurt_Tussendoortje_Aardbei_70g            1.0          14.3      70.0
      Jumbo Danoontje Danoontje_Yoghurt_Tussendoortje_Appel_Aardbei_70_g            1.0          14.3      70.0
      Jumbo Danoontje         Danoontje_Yoghurt_Tussendoortje_Banaan_70g            1.0          14.3      70.0
       PLUS      Isey                             Isey_Skyr_Mandarin_pie            2.0          14.3     140.0
      Jumbo      Ísey              Ísey_Skyr_Air_Chocolate-Coconut_125_g            1.7          13.6     125.0

06. The most expensive brands
-----------------------------

This query returned 5 rows.

    Brand  Average_kg_Price
Danoontje              14.0
     Ísey              12.0
     Isey              12.0
      XXL               9.0
   Nestlé               9.0

07. Cheapest Products
---------------------

This query returned 5 rows.

Supermarket         Brand                    Product_Name  Product_Price  Price_Per_kg  Weight_g
      Jumbo        Magere              Magere_yoghurt_1_L            0.8           0.8    1000.0
       PLUS Zuivelmeester    Zuivelmeester_Magere_yoghurt            0.8           0.8    1000.0
      Jumbo     Halfvolle           Halfvolle_Yoghurt_1_L            1.0           1.0    1000.0
       PLUS Zuivelmeester Zuivelmeester_Halfvolle_Yoghurt            1.0           1.0    1000.0
       PLUS         Danio   Danio_Duo_chocolade_balletjes            1.0           1.0    1000.0

08. Checking number of house brand products compared to others
--------------------------------------------------------------

This query returned 4 rows.

Supermarket  brand_type  product_count  Average_Unit_Price
      Jumbo House Brand             13            2.261538
      Jumbo Other Brand            137            6.723358
       PLUS House Brand              9            2.633333
       PLUS Other Brand            154            5.526623

09. Checking prices of same brands at both supermarkets
-------------------------------------------------------

This query returned 45 rows.

Supermarket         Brand  product_count  AVG(Price_Per_kg)
      Jumbo       Activia              6           5.533333
       PLUS       Activia              6           6.966667
      Jumbo        Almhof             15           5.840000
       PLUS        Almhof             17           5.764706
      Jumbo         Alpro             11           4.990909
       PLUS         Alpro              6           5.133333
      Jumbo          Arla             14           4.050000
       PLUS          Arla             14           4.450000
       PLUS          BIO+              2           3.200000
       PLUS    Biologisch              5           2.220000
      Jumbo       Campina             15           2.860000
       PLUS       Campina             15           2.860000
       PLUS         Danio              2           4.750000
      Jumbo        Danone              2           9.950000
       PLUS        Danone              3           4.466667
      Jumbo     Danoontje              3          14.300000
      Jumbo           Den              2           2.850000
       PLUS           Den              4           2.575000
      Jumbo        Dodoni              5           6.560000
       PLUS        Dodoni              1           8.800000
       PLUS        Elinas              2           3.800000
      Jumbo     Halfvolle              2           1.250000
      Jumbo         HiPRO              6           8.866667
      Jumbo          Isey              1          11.100000
       PLUS          Isey             10          11.730000
      Jumbo         Jumbo              9           2.744444
      Jumbo      Katharos              1           4.000000
      Jumbo        Magere              1           0.800000
       PLUS        Melkan             26           3.561538
      Jumbo      Melkunie             17           7.823529
       PLUS      Melkunie             15           8.400000
       PLUS        Nestlé              1           8.700000
      Jumbo       Optimel              7           3.428571
       PLUS       Optimel             10           4.370000
       PLUS          PLUS              4           3.150000
      Jumbo           Pur              1           3.700000
       PLUS           Pur              2           4.050000
      Jumbo         Volle              1           1.400000
      Jumbo           XXL              2          10.000000
       PLUS           XXL              6           8.350000
      Jumbo   Zuivelhoeve              7           8.114286
       PLUS   Zuivelhoeve              8           8.500000
       PLUS Zuivelmeester              4           1.200000
      Jumbo           den              2           2.300000
      Jumbo          Ísey             20          11.705000

10. Best price for protein
--------------------------

This query returned 5 rows.

Supermarket         Brand                    Product_Name  Weight_g  Product_Price  Protein_In_Product_g  Protein_per_Euro
      Jumbo        Magere              Magere_yoghurt_1_L    1000.0            0.8                  48.0             60.00
       PLUS Zuivelmeester    Zuivelmeester_Magere_yoghurt    1000.0            0.8                  39.0             48.75
      Jumbo     Halfvolle           Halfvolle_Yoghurt_1_L    1000.0            1.0                  48.0             48.00
       PLUS Zuivelmeester Zuivelmeester_Halfvolle_Yoghurt    1000.0            1.0                  46.0             46.00
       PLUS        Melkan             Melkan_Skyr_naturel    1000.0            3.0                 110.0             36.67

11. Cheapest kcals
------------------

This query returned 5 rows.

Supermarket         Brand                            Product_Name  Weight_g  Product_Price  Energy_kcal_100_g  kcal_per_euro
       PLUS         Danio           Danio_Duo_chocolade_balletjes    1000.0            1.0              146.5         1465.0
       PLUS        Melkan Melkan_Yoghurt_Griekse_Stijl_10%_1000GR    1000.0            1.8              111.6          620.0
       PLUS        Melkan       Melkan_Griekse_stijl_passievrucht    1000.0            2.4              145.3          605.4
       PLUS        Melkan            Melkan_Griekse_stijl_aardbei    1000.0            2.4              145.3          605.4
       PLUS Zuivelmeester         Zuivelmeester_Halfvolle_Yoghurt    1000.0            1.0               55.7          557.0

12. Sugar heaviest products
---------------------------

This query returned 5 rows.

Supermarket  Brand                                                      Product_Name  Sugars_In_Product_g  Weight_g  percentage_sugar  Product_Price
      Jumbo Almhof Almhof_Hoekje_Yoghurt_Pistache_Smaak_met_Krokante_Amandelen_150_g                 26.9     150.1              17.9            1.5
       PLUS Almhof                                    Almhof_Hoekje_Venetië_pistache                 26.9     150.1              17.9            1.5
      Jumbo Danone                                 Danone_M&M's_Vanilleyoghurt_120_g                 21.1     120.0              17.6            1.3
       PLUS  Danio                                             Danio_Duo_karamelsaus                 20.4     118.0              17.3            1.0
       PLUS Nestlé                                    Nestlé_Kit_Kat_yoghurt_vanille                 39.6     230.1              17.2            2.0

13. Sugar lightest
------------------

This query returned 5 rows.

Supermarket  Brand                                                      Product_Name  Sugars_In_Product_g  Weight_g  percentage_sugar  Product_Price
      Jumbo  Alpro            Alpro_Mild_&_Creamy_No_Sugars_Soyaproduct_Nature_755_g                  0.0     755.1               0.0            3.0
      Jumbo  Alpro   Alpro_Mild_&_Creamy_Zonder_Suikers_Variatie_Op_Yoghurt_4_x_755g                  0.0    3020.2               0.0           12.0
      Jumbo  Alpro Alpro_Plantaardige_Variatie_Op_Yoghurt_Naturel_Zonder_Suiker_500g                  0.0     500.0               0.0            2.5
       PLUS  Alpro                             Alpro_Variatie_Yoghurt_Zonder_Suikers                  0.0     500.0               0.0            2.5
       PLUS Melkan                                      Melkan_Soja_yoghurt_original                  1.7     500.0               0.3            0.8

14. Highest protein, lowest sugar
---------------------------------

This query returned 5 rows.

Supermarket  Brand                                                    Product_Name  Product_Price  Protein_In_Product_g  Sugars_In_Product_g  protein_g_per_euro
      Jumbo  HiPRO                      HiPRO_Protein_Kwark_Bosvruchten_6_x__200_g           11.9                 148.8                 33.6               12.50
      Jumbo  HiPRO                            HiPRO_Protein_Kwark_Banaan_6_x_200_g           11.9                 148.8                 39.6               12.50
      Jumbo  Alpro Alpro_Mild_&_Creamy_Zonder_Suikers_Variatie_Op_Yoghurt_4_x_755g           12.0                 120.8                  0.0               10.07
       PLUS Melkan                                             Melkan_Skyr_naturel            3.0                 110.0                 47.0               36.67
      Jumbo   Arla                         Arla_Skyr_Naturel_Yoghurt_0%_vet_XL_1kg            4.0                 100.0                 40.0               25.00


```

Suggested content to include here:

* Total products collected
* Products per supermarket
* Most common brands
* Data completeness summary
* Cheapest products per kilogram
* Most expensive products per kilogram
* House-brand vs other-brand price comparison
* Best protein per euro
* Products with highest and lowest sugar percentage
* Any notable supermarket differences

## Assumptions and Data Quality Notes

This project uses public supermarket product data. Since the data comes from two different websites with different structures, several assumptions were needed.

### Product weight

Product weight was estimated using product price and price-per-unit values.

In simplified form:

```text
Weight_g = Product_Price / Price_Per_kg * 1000
```

This worked well for most products, but the raw unit-price formats were not always consistent between websites and products. Some products also had multipack formats, such as `4 x 125g`, which required extra care during interpretation.

The final dataset should therefore be seen as suitable for exploratory analysis, not as a guaranteed commercial product database.

### Brand extraction

Brand names were extracted from the first word of the product name.

This works well for brands such as:

```text
Activia
Almhof
Campina
Arla
Alpro
Optimel
```

However, this can misclassify some products. For example, generic product names such as `Halfvolle yoghurt` or `Magere yoghurt` may be treated as brands even though they are actually product descriptions. This was taken into account when querying for house brands and other brands:

### House-brand classification

House-brand products were classified using manually defined rules.

For example:

* Jumbo house-brand products include `Jumbo`, `Halfvolle`, `Volle`, and `Magere`
* PLUS house-brand products include `PLUS`, `Plus`, and `Biologisch`

This is a practical approximation. A more robust version would use a manually maintained brand mapping table.

### Nutrition values

Nutrition values were taken from the product pages. In some cases, products had missing nutrition data. Products with missing key nutrition values were excluded from specific analyses.

### Snapshot data

The data is a snapshot. Supermarket prices, product assortment, and promotions can change frequently.

## Limitations

The most important limitations of this project are:

1. **The data is not historical**
   The project currently captures a single snapshot. It does not yet track price changes over time.

2. **Brand extraction is simple**
   Brands are estimated from product names, which can create classification errors.

3. **Product weight is estimated**
   Product weight was calculated from price and unit price. This is practical, but not perfect.

4. **Promotions are not fully analyzed**
   Some products may have temporary discounts or promotional pricing that affects comparison.

5. **Website structures may change**
   If Jumbo or PLUS changes their website structure or API responses, the scraper may need to be updated.

6. **The project is category-specific**
   The project focuses on yoghurt products only. Other categories may require adjusted parsing and cleaning logic.

## How to Run the Project

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd 03.Scraping_and_Analysis_automated
```

### 2. Create a virtual environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Python packages

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers

Playwright needs an additional setup command:

```bash
playwright install
```

### 5. Run the full pipeline

From the project root, run:

```bash
python Scripts/main.py
```

### 6. View the outputs

After running the project, check:

```text
Data/Processed/supermarket_product_data_clean.csv
Data/Processed/supermarket_products.db
Reports/basic_supermarket_report.txt
```

## Requirements

The project uses the following main external packages:

```text
pandas
beautifulsoup4
lxml
playwright
```

The following libraries are part of the Python standard library and do not need to be installed separately:

```text
pathlib
json
sqlite3
datetime
subprocess
sys
time
```
## Skills Demonstrated

This project demonstrates:

* Web scraping
* Browser automation
* HTML parsing
* JSON parsing
* Data cleaning
* Data validation
* SQL analysis
* SQLite database usage
* Automated reporting
* Pipeline automation
* Project documentation
* Handling imperfect real-world data

## Future Improvements

Possible future improvements include:

1. **Historical price tracking**
   Run the scraper weekly or daily and store snapshots over time.

2. **Dashboarding**
   Build a Power BI or Streamlit dashboard on top of the SQLite database or cleaned CSV.

3. **Improved brand mapping**
   Replace first-word brand extraction with a manually maintained brand mapping table.

4. **Improved product weight extraction**
   Extract package sizes directly from product names or structured product metadata instead of estimating weight from price and unit price.

5. **Promotion analysis**
   Track discount labels and compare regular prices with promotional prices.

6. **More supermarkets**
   Add Albert Heijn, Lidl, Aldi, Dirk, or other Dutch supermarkets.

7. **More product categories**
   Expand the project beyond yoghurt to other supermarket categories.

8. **Automated data validation tests**
   Add checks for unrealistic prices, weights, missing values, and duplicate product IDs.

## Conclusion

This project shows the complete process of turning messy online product data into structured, analyzable data.

The final result is not just a scraper, but a small end-to-end data pipeline:

```text
raw website data -> parsed product data -> cleaned dataset -> SQL database -> analysis report
```

The project highlights practical data skills that are directly relevant for data analyst and junior data engineering roles: collecting data, cleaning inconsistent sources, documenting assumptions, querying data with SQL, and communicating findings clearly.
