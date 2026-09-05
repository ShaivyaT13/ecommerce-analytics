import os
import sqlite3
import pandas as pd


def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, "data", "cleaned", "ecommerce_cleaned.csv")
    db_path = os.path.join(project_root, "ecommerce.db")

    print("loading data...")
    df = pd.read_csv(csv_path)
    print(f"read {len(df)} rows")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    df.to_sql("orders", conn, if_exists="replace", index=False)
    print(f"created orders table with {len(df)} rows")

    customers = (
        df.groupby("customer_id")
        .agg(
            customer_name=("customer_name", "first"),
            region=("region", "first"),
            city=("city", "first"),
        )
        .reset_index()
    )
    customers.to_sql("customers", conn, if_exists="replace", index=False)
    print(f"created customers table with {len(customers)} rows")

    products = (
        df.groupby("product")
        .agg(
            category=("category", "first"),
            unit_price=("unit_price", "first"),
            cost=("cost", "first"),
        )
        .reset_index()
    )
    products.to_sql("products", conn, if_exists="replace", index=False)
    print(f"created products table with {len(products)} rows")

    for table in ["orders", "customers", "products"]:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table} has {count} rows")

    conn.close()
    print("db saved")


if __name__ == "__main__":
    main()
