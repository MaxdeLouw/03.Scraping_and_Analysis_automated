-- 01. Slice head
SELECT *
FROM supermarket_products
limit 5;

-- 02. Check items per supermarket
SELECT
    Supermarket,
    COUNT(*) AS product_count
FROM supermarket_products
GROUP BY Supermarket
ORDER BY product_count DESC;

-- 03. Check biggest brands per supermarket
SELECT
    Supermarket,
    Brand,
    COUNT(*) AS product_count
FROM supermarket_products
GROUP BY Supermarket, Brand
ORDER BY Supermarket, product_count DESC;

-- 04. Check for empty columns
SELECT
    Supermarket,
    COUNT(*) AS total_products,
    COUNT(Product_Price) AS products_with_price,
    COUNT(Price_Per_Unit) AS products_with_unit_price,
    COUNT(Weight_g) AS products_with_weight,
    COUNT(Energy_kcal_100_g) AS products_with_energy,
    COUNT(Protein_In_Product_g) AS products_with_protein
FROM supermarket_products
GROUP BY Supermarket;

-- 05. Look for the most expensive products
SELECT
    Supermarket,
    Brand,
    Product_Name,
    Product_Price,
    Price_Per_kg,
    Weight_g
FROM supermarket_products
WHERE Price_Per_kg IS NOT NULL
ORDER BY Price_Per_kg DESC
LIMIT 5;

-- 06. The most expensive brands
SELECT 
    Brand, 
    Round(AVG(Price_Per_kg)) as Average_kg_Price
FROM supermarket_products
GROUP BY Brand
ORDER BY Average_kg_Price DESC
LIMIT 5;

-- 07. Cheapest Products
SELECT
    Supermarket,
    Brand,
    Product_Name,
    Product_Price,
    Price_Per_kg,
    Weight_g
FROM supermarket_products
WHERE Price_Per_kg IS NOT NULL
ORDER BY Price_Per_kg ASC
LIMIT 5;

-- 08. Checking number of house brand products compared to others
SELECT  Supermarket,
        CASE
            WHEN Supermarket = 'Jumbo'
                AND Brand IN ('Jumbo', 'Halfvolle', 'Volle', 'Magere')
                THEN 'House Brand'

            WHEN Supermarket = 'PLUS'
                AND Brand IN ('PLUS', 'Plus', 'Biologisch')
                THEN 'House Brand'

            ELSE 'Other Brand'
        END as 'brand_type',
        Count(*) as product_count,
        AVG(Price_Per_kg) as Average_Unit_Price
FROM supermarket_products
GROUP BY 
    Supermarket,
    brand_type
ORDER BY   
    Supermarket,
    brand_type;

-- 09. Checking prices of same brands at both supermarkets
SELECT  Supermarket,
        Brand,
        COUNT(*) as product_count,
        AVG(Price_Per_kg)
FROM supermarket_products
GROUP BY
    Brand,
    Supermarket
ORDER BY
    Brand,
    Supermarket,
    product_count;

-- 10. Best price for protein
SELECT  Supermarket,
        Brand,
        Product_Name,
        Weight_g,
        Product_Price,
        Protein_In_Product_g,
        Round(Protein_In_Product_g / Product_Price,2) AS Protein_per_Euro
FROM supermarket_products
ORDER BY Protein_per_Euro DESC
limit 5;

-- 11. Cheapest kcals
SELECT
    Supermarket,
    Brand,
    Product_Name,
    Weight_g,
    Product_Price,
    Energy_kcal_100_g,
    ROUND((Energy_kcal_100_g * Weight_g / 100) / Product_Price, 1) AS kcal_per_euro
FROM supermarket_products
ORDER BY kcal_per_euro DESC
LIMIT 5;

-- 12. Sugar heaviest products
SELECT
    Supermarket,
    Brand,
    Product_Name,
    Sugars_In_Product_g,
    Weight_g,
    Round(Sugars_In_Product_g * 100/ Weight_g, 1) AS percentage_sugar,
    Product_Price
FROM supermarket_products
ORDER BY percentage_sugar DESC
LIMIT 5;

-- 13. Sugar lightest

SELECT
    Supermarket,
    Brand,
    Product_Name,
    Sugars_In_Product_g,
    Weight_g,
    Round(Sugars_In_Product_g * 100/ Weight_g, 1) AS percentage_sugar,
    Product_Price
FROM supermarket_products
WHERE Sugars_In_Product_g IS NOT NULL
ORDER BY percentage_sugar ASC
LIMIT 5;

-- 14. Highest protein, lowest sugar

SELECT
    Supermarket,
    Brand,
    Product_Name,
    Product_Price,
    Protein_In_Product_g,
    Sugars_In_Product_g,
    ROUND(Protein_In_Product_g / Product_Price, 2) AS protein_g_per_euro
FROM supermarket_products
WHERE
    Protein_In_Product_g IS NOT NULL
    AND Sugars_In_Product_g IS NOT NULL
ORDER BY
    Protein_In_Product_g DESC,
    Sugars_In_Product_g ASC
LIMIT 5;