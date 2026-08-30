SELECT
    title,
    price,
    location,
    CASE
        WHEN price < 2000 THEN 'Budget'
        WHEN price BETWEEN 2000 AND 3500 THEN 'Medium'
        ELSE 'Premium'
    END AS price_category
FROM {{ source('raw_data', 'raw_olx_houses') }}
WHERE price IS NOT NULL