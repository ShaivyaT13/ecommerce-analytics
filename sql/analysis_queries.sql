-- KPIs

-- total revenue
SELECT 
    ROUND(SUM(revenue), 2) AS total_revenue
FROM orders;

-- total profit
SELECT 
    ROUND(SUM(profit), 2) AS total_profit
FROM orders;

-- total orders
SELECT 
    COUNT(DISTINCT order_id) AS total_orders
FROM orders;

-- total customers
SELECT 
    COUNT(DISTINCT customer_id) AS total_customers
FROM orders;

-- average order value
SELECT 
    ROUND(SUM(revenue) * 1.0 / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM orders;

-- executive KPI summary dashboard
SELECT 
    COUNT(DISTINCT order_id)                                AS total_orders,
    COUNT(DISTINCT customer_id)                             AS total_customers,
    SUM(quantity)                                           AS total_items_sold,
    ROUND(SUM(revenue), 2)                                  AS total_revenue,
    ROUND(SUM(total_cost), 2)                               AS total_cost,
    ROUND(SUM(profit), 2)                                   AS total_profit,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2)            AS overall_profit_margin_pct,
    ROUND(SUM(revenue) * 1.0 / COUNT(DISTINCT order_id), 2) AS avg_order_value
FROM orders;

-- category analysis

-- revenue and profit by category
SELECT 
    category,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2)  AS total_profit
FROM orders
GROUP BY category
ORDER BY total_revenue DESC;

-- detailed category analysis
SELECT 
    category,
    COUNT(DISTINCT order_id)                     AS total_orders,
    SUM(quantity)                                AS units_sold,
    ROUND(SUM(revenue), 2)                       AS total_revenue,
    ROUND(SUM(total_cost), 2)                    AS total_cost,
    ROUND(SUM(profit), 2)                        AS total_profit,
    ROUND(AVG(profit_margin) * 100, 2)           AS avg_line_item_margin_pct,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2) AS overall_category_margin_pct
FROM orders
GROUP BY category
ORDER BY total_revenue DESC;

-- regional analysis

-- revenue, profit, and customer count by region
SELECT 
    region,
    COUNT(DISTINCT customer_id)                             AS total_customers,
    COUNT(DISTINCT order_id)                                AS total_orders,
    ROUND(SUM(revenue), 2)                                  AS total_revenue,
    ROUND(SUM(profit), 2)                                   AS total_profit,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2)            AS profit_margin_pct,
    ROUND(SUM(revenue) * 1.0 / COUNT(DISTINCT customer_id), 2) AS revenue_per_customer
FROM orders
GROUP BY region
ORDER BY total_revenue DESC;

-- regional and city performance drilldown
SELECT 
    region,
    city,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT order_id)    AS total_orders,
    ROUND(SUM(revenue), 2)      AS total_revenue,
    ROUND(SUM(profit), 2)       AS total_profit
FROM orders
GROUP BY region, city
ORDER BY region ASC, total_revenue DESC;

-- product analysis

-- top 10 products by revenue
SELECT 
    product,
    category,
    SUM(quantity)                                AS total_units_sold,
    ROUND(SUM(revenue), 2)                       AS total_revenue,
    ROUND(SUM(profit), 2)                        AS total_profit,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2) AS profit_margin_pct
FROM orders
GROUP BY product, category
ORDER BY total_revenue DESC
LIMIT 10;

-- high-volume low-profit products
SELECT 
    product,
    category,
    SUM(quantity)                                AS total_quantity_sold,
    ROUND(SUM(revenue), 2)                       AS total_revenue,
    ROUND(SUM(profit), 2)                        AS total_profit,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2) AS profit_margin_pct
FROM orders
GROUP BY product, category
HAVING SUM(quantity) > 100
ORDER BY total_profit ASC;

-- customer analysis

-- top 10 customers by spend
SELECT 
    customer_id,
    customer_name,
    region,
    city,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity)            AS total_items_purchased,
    ROUND(SUM(revenue), 2)   AS total_spend,
    ROUND(SUM(profit), 2)    AS total_profit_contributed
FROM orders
GROUP BY customer_id, customer_name, region, city
ORDER BY total_spend DESC
LIMIT 10;

-- average order value per customer
SELECT 
    customer_id,
    customer_name,
    COUNT(DISTINCT order_id)                                AS order_count,
    ROUND(SUM(revenue), 2)                                  AS total_spend,
    ROUND(SUM(revenue) * 1.0 / COUNT(DISTINCT order_id), 2) AS avg_order_value
FROM orders
GROUP BY customer_id, customer_name
ORDER BY avg_order_value DESC;

-- repeat customers
SELECT 
    customer_id,
    customer_name,
    COUNT(DISTINCT order_id) AS repeat_order_count,
    SUM(quantity)            AS total_units_bought,
    ROUND(SUM(revenue), 2)   AS total_spend,
    ROUND(SUM(profit), 2)    AS total_profit,
    MIN(order_date)          AS first_order_date,
    MAX(order_date)          AS latest_order_date
FROM orders
GROUP BY customer_id, customer_name
HAVING COUNT(DISTINCT order_id) > 1
ORDER BY repeat_order_count DESC, total_spend DESC;

-- monthly trends

-- monthly revenue and profit
SELECT 
    year_month,
    year,
    month,
    month_name,
    COUNT(DISTINCT order_id)                     AS total_orders,
    SUM(quantity)                                AS total_units_sold,
    ROUND(SUM(revenue), 2)                       AS monthly_revenue,
    ROUND(SUM(total_cost), 2)                    AS monthly_cost,
    ROUND(SUM(profit), 2)                        AS monthly_profit,
    ROUND((SUM(profit) / SUM(revenue)) * 100, 2) AS profit_margin_pct
FROM orders
GROUP BY year_month, year, month, month_name
ORDER BY year_month ASC;

-- month-over-month growth
WITH monthly_summary AS (
    SELECT 
        year_month,
        ROUND(SUM(revenue), 2) AS monthly_revenue,
        ROUND(SUM(profit), 2)  AS monthly_profit
    FROM orders
    GROUP BY year_month
)
SELECT 
    year_month,
    monthly_revenue,
    LAG(monthly_revenue, 1) OVER (ORDER BY year_month) AS prev_month_revenue,
    ROUND(monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year_month), 2) AS mom_revenue_change,
    ROUND(
        ((monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year_month))
         / LAG(monthly_revenue, 1) OVER (ORDER BY year_month)) * 100.0,
        2
    ) AS mom_revenue_growth_pct,
    monthly_profit,
    LAG(monthly_profit, 1) OVER (ORDER BY year_month) AS prev_month_profit,
    ROUND(monthly_profit - LAG(monthly_profit, 1) OVER (ORDER BY year_month), 2) AS mom_profit_change,
    ROUND(
        ((monthly_profit - LAG(monthly_profit, 1) OVER (ORDER BY year_month))
         / LAG(monthly_profit, 1) OVER (ORDER BY year_month)) * 100.0,
        2
    ) AS mom_profit_growth_pct
FROM monthly_summary
ORDER BY year_month ASC;

-- advanced queries

-- joins

-- revenue by customer
SELECT 
    c.customer_id,
    c.customer_name,
    c.region,
    c.city,
    COUNT(DISTINCT o.order_id)                                 AS total_orders,
    SUM(o.quantity)                                            AS total_items_bought,
    ROUND(SUM(o.revenue), 2)                                   AS total_revenue,
    ROUND(SUM(o.profit), 2)                                    AS total_profit,
    ROUND(SUM(o.revenue) * 1.0 / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
FROM customers c
INNER JOIN orders o 
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.region, c.city
ORDER BY total_revenue DESC;

-- product performance
SELECT 
    p.product,
    p.category,
    p.unit_price                                       AS catalog_unit_price,
    p.cost                                             AS catalog_unit_cost,
    COUNT(DISTINCT o.order_id)                         AS total_orders,
    SUM(o.quantity)                                    AS total_units_sold,
    ROUND(SUM(o.revenue), 2)                           AS total_revenue,
    ROUND(SUM(o.profit), 2)                            AS total_profit,
    ROUND((SUM(o.profit) / SUM(o.revenue)) * 100.0, 2) AS realized_profit_margin_pct
FROM products p
INNER JOIN orders o 
    ON p.product = o.product
GROUP BY p.product, p.category, p.unit_price, p.cost
ORDER BY total_revenue DESC;

-- CTEs

-- customer segmentation
WITH customer_totals AS (
    SELECT 
        customer_id,
        customer_name,
        region,
        city,
        COUNT(DISTINCT order_id) AS total_orders,
        ROUND(SUM(revenue), 2)   AS total_spend,
        ROUND(SUM(profit), 2)    AS total_profit
    FROM orders
    GROUP BY customer_id, customer_name, region, city
),
customer_segments AS (
    SELECT 
        customer_id,
        customer_name,
        region,
        city,
        total_orders,
        total_spend,
        total_profit,
        CASE 
            WHEN total_spend >= 5000 THEN 'High Value'
            WHEN total_spend >= 2000 THEN 'Medium Value'
            ELSE 'Low Value'
        END AS customer_segment
    FROM customer_totals
)
SELECT 
    customer_segment,
    COUNT(customer_id)                                         AS total_customers,
    ROUND(SUM(total_spend), 2)                                 AS segment_revenue,
    ROUND(AVG(total_spend), 2)                                 AS avg_spend_per_customer,
    ROUND(SUM(total_profit), 2)                                AS segment_profit,
    ROUND((SUM(total_profit) / SUM(total_spend)) * 100.0, 2)   AS segment_profit_margin_pct
FROM customer_segments
GROUP BY customer_segment
ORDER BY segment_revenue DESC;

-- customer-level segmentation detail
WITH customer_spending AS (
    SELECT 
        customer_id,
        customer_name,
        region,
        city,
        COUNT(DISTINCT order_id) AS total_orders,
        ROUND(SUM(revenue), 2)   AS total_spend,
        ROUND(SUM(profit), 2)    AS total_profit
    FROM orders
    GROUP BY customer_id, customer_name, region, city
)
SELECT 
    customer_id,
    customer_name,
    region,
    city,
    total_orders,
    total_spend,
    total_profit,
    CASE 
        WHEN total_spend >= 5000 THEN 'High Value'
        WHEN total_spend >= 2000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment
FROM customer_spending
ORDER BY total_spend DESC;

-- window functions

-- rank customers by month
WITH monthly_customer_spend AS (
    SELECT 
        year_month,
        customer_id,
        customer_name,
        COUNT(DISTINCT order_id) AS monthly_orders,
        ROUND(SUM(revenue), 2)   AS monthly_revenue
    FROM orders
    GROUP BY year_month, customer_id, customer_name
)
SELECT 
    year_month,
    customer_id,
    customer_name,
    monthly_orders,
    monthly_revenue,
    RANK() OVER (
        PARTITION BY year_month 
        ORDER BY monthly_revenue DESC
    ) AS monthly_spend_rank
FROM monthly_customer_spend
ORDER BY year_month ASC, monthly_spend_rank ASC;

-- running total revenue
WITH monthly_totals AS (
    SELECT 
        year_month,
        COUNT(DISTINCT order_id) AS total_orders,
        ROUND(SUM(revenue), 2)   AS monthly_revenue,
        ROUND(SUM(profit), 2)    AS monthly_profit
    FROM orders
    GROUP BY year_month
)
SELECT 
    year_month,
    total_orders,
    monthly_revenue,
    ROUND(SUM(monthly_revenue) OVER (
        ORDER BY year_month 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS running_total_revenue,
    monthly_profit,
    ROUND(SUM(monthly_profit) OVER (
        ORDER BY year_month 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS running_total_profit
FROM monthly_totals
ORDER BY year_month ASC;

-- top product per category
WITH ranked_products_by_category AS (
    SELECT 
        category,
        product,
        SUM(quantity)          AS units_sold,
        ROUND(SUM(revenue), 2) AS total_revenue,
        ROUND(SUM(profit), 2)  AS total_profit,
        ROW_NUMBER() OVER (
            PARTITION BY category 
            ORDER BY SUM(revenue) DESC
        ) AS rank_in_category
    FROM orders
    GROUP BY category, product
)
SELECT 
    category,
    product,
    units_sold,
    total_revenue,
    total_profit
FROM ranked_products_by_category
WHERE rank_in_category = 1
ORDER BY total_revenue DESC;

-- overall customer ranking
WITH customer_spend_summary AS (
    SELECT 
        customer_id,
        customer_name,
        region,
        city,
        COUNT(DISTINCT order_id) AS total_orders,
        ROUND(SUM(revenue), 2)   AS total_spend
    FROM orders
    GROUP BY customer_id, customer_name, region, city
)
SELECT 
    DENSE_RANK() OVER (
        ORDER BY total_spend DESC
    ) AS dense_rank_by_spend,
    customer_id,
    customer_name,
    region,
    city,
    total_orders,
    total_spend
FROM customer_spend_summary
ORDER BY dense_rank_by_spend ASC;

-- compare consecutive months
WITH monthly_revenue_data AS (
    SELECT 
        year_month,
        ROUND(SUM(revenue), 2) AS current_month_revenue,
        ROUND(SUM(profit), 2)  AS current_month_profit
    FROM orders
    GROUP BY year_month
)
SELECT 
    year_month,
    LAG(current_month_revenue, 1) OVER (ORDER BY year_month)  AS prev_month_revenue,
    current_month_revenue,
    LEAD(current_month_revenue, 1) OVER (ORDER BY year_month) AS next_month_revenue,
    ROUND(
        current_month_revenue - LAG(current_month_revenue, 1) OVER (ORDER BY year_month), 
        2
    ) AS diff_from_previous_month,
    ROUND(
        LEAD(current_month_revenue, 1) OVER (ORDER BY year_month) - current_month_revenue, 
        2
    ) AS diff_to_next_month
FROM monthly_revenue_data
ORDER BY year_month ASC;

-- case statements

-- customer tier classification
SELECT 
    customer_id,
    customer_name,
    region,
    city,
    COUNT(DISTINCT order_id) AS order_count,
    ROUND(SUM(revenue), 2)   AS total_spend,
    CASE 
        WHEN SUM(revenue) >= 7500 THEN 'Platinum'
        WHEN SUM(revenue) >= 4000 THEN 'Gold'
        WHEN SUM(revenue) >= 1500 THEN 'Silver'
        ELSE 'Bronze'
    END AS customer_tier
FROM orders
GROUP BY customer_id, customer_name, region, city
ORDER BY total_spend DESC;

-- customer tier aggregation
WITH customer_spend_tiers AS (
    SELECT 
        customer_id,
        customer_name,
        ROUND(SUM(revenue), 2) AS total_spend,
        CASE 
            WHEN SUM(revenue) >= 7500 THEN 'Platinum'
            WHEN SUM(revenue) >= 4000 THEN 'Gold'
            WHEN SUM(revenue) >= 1500 THEN 'Silver'
            ELSE 'Bronze'
        END AS customer_tier
    FROM orders
    GROUP BY customer_id, customer_name
)
SELECT 
    customer_tier,
    COUNT(customer_id)         AS total_customers,
    ROUND(SUM(total_spend), 2) AS tier_revenue,
    ROUND(AVG(total_spend), 2) AS avg_spend_per_customer
FROM customer_spend_tiers
GROUP BY customer_tier
ORDER BY 
    CASE customer_tier
        WHEN 'Platinum' THEN 1
        WHEN 'Gold'     THEN 2
        WHEN 'Silver'   THEN 3
        WHEN 'Bronze'   THEN 4
    END;

-- discount tier analysis
SELECT 
    CASE 
        WHEN discount = 0      THEN '0% No Discount'
        WHEN discount <= 0.10  THEN '1% - 10% Low Discount'
        WHEN discount <= 0.20  THEN '11% - 20% Medium Discount'
        ELSE '> 20% High Discount'
    END AS discount_tier,
    COUNT(order_id)                              AS total_orders,
    SUM(quantity)                                AS total_units_sold,
    ROUND(SUM(revenue), 2)                       AS total_revenue,
    ROUND(SUM(profit), 2)                        AS total_profit,
    ROUND(AVG(discount) * 100.0, 1)              AS avg_discount_pct,
    ROUND((SUM(profit) / SUM(revenue)) * 100.0, 2) AS profit_margin_pct
FROM orders
GROUP BY discount_tier
ORDER BY total_revenue DESC;
