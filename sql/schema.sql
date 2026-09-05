-- drop existing tables to allow clean re-creation
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;

-- main orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id        INTEGER PRIMARY KEY,
    order_date      TEXT,
    customer_id     TEXT,
    customer_name   TEXT,
    region          TEXT,
    city            TEXT,
    category        TEXT,
    product         TEXT,
    quantity        INTEGER,
    unit_price      REAL,
    discount        REAL,
    cost            REAL,
    payment_method  TEXT,
    revenue         REAL,
    total_cost      REAL,
    profit          REAL,
    profit_margin   REAL,
    year            INTEGER,
    month           INTEGER,
    month_name      TEXT,
    year_month      TEXT
);

-- customers lookup
CREATE TABLE IF NOT EXISTS customers (
    customer_id     TEXT PRIMARY KEY,
    customer_name   TEXT,
    region          TEXT,
    city            TEXT
);

-- products lookup
CREATE TABLE IF NOT EXISTS products (
    product         TEXT PRIMARY KEY,
    category        TEXT,
    unit_price      REAL,
    cost            REAL
);

-- indexes for common queries
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_product     ON orders(product);
CREATE INDEX IF NOT EXISTS idx_orders_category    ON orders(category);
CREATE INDEX IF NOT EXISTS idx_orders_region      ON orders(region);
CREATE INDEX IF NOT EXISTS idx_orders_order_date  ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_year_month  ON orders(year_month);
