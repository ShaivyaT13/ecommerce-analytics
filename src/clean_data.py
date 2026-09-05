# cleans raw ecommerce data

import os
import pandas as pd
import numpy as np


def load_raw_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"loaded {len(df)} rows, {len(df.columns)} columns")
    return df


def inspect_data(df: pd.DataFrame) -> None:
    print(f"rows: {df.shape[0]}, cols: {df.shape[1]}")
    print(df.dtypes)
    print("missing values:")
    print(df.isnull().sum())
    print(f"duplicates: {df.duplicated().sum()}")


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"dropped {before - after} duplicates")
    return df


def convert_dates(df: pd.DataFrame) -> pd.DataFrame:
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    invalid_dates = df["order_date"].isnull().sum()
    print(f"invalid dates found: {invalid_dates}")

    before = len(df)
    df = df.dropna(subset=["order_date"])
    print(f"dropped {before - len(df)} rows due to invalid dates")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    # business logic: missing discount = no discount (0)
    # missing region/name = "Unknown"
    
    df["discount"] = pd.to_numeric(df["discount"], errors="coerce")
    missing_discount = df["discount"].isnull().sum()
    df["discount"] = df["discount"].fillna(0)
    print(f"filled {missing_discount} missing discounts with 0")

    missing_region = df["region"].isnull().sum() + (df["region"] == "").sum()
    df["region"] = df["region"].replace("", np.nan).fillna("Unknown")
    print(f"filled {missing_region} missing regions with 'Unknown'")

    missing_name = df["customer_name"].isnull().sum() + (df["customer_name"] == "").sum()
    df["customer_name"] = df["customer_name"].replace("", np.nan).fillna("Unknown")
    print(f"filled {missing_name} missing names with 'Unknown'")

    return df


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)

    invalid_qty = (df["quantity"] <= 0).sum()
    df = df[df["quantity"] > 0]
    if invalid_qty:
        print(f"dropped {invalid_qty} rows with bad quantity")

    invalid_price = (df["unit_price"] <= 0).sum()
    df = df[df["unit_price"] > 0]
    if invalid_price:
        print(f"dropped {invalid_price} rows with bad price")

    invalid_discount = ((df["discount"] < 0) | (df["discount"] > 1)).sum()
    df = df[(df["discount"] >= 0) & (df["discount"] <= 1)]
    if invalid_discount:
        print(f"dropped {invalid_discount} rows with bad discount")

    return df


def derive_business_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["revenue"] = df["quantity"] * df["unit_price"] * (1 - df["discount"])
    df["total_cost"] = df["quantity"] * df["cost"]
    df["profit"] = df["revenue"] - df["total_cost"]
    df["profit_margin"] = df["profit"] / df["revenue"].replace(0, pd.NA)
    return df


def derive_time_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.month
    df["month_name"] = df["order_date"].dt.month_name()
    df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
    return df


def save_cleaned_data(df: pd.DataFrame, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"saved {len(df)} rows to {path}")


def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(project_root, "data", "raw", "ecommerce_sales.csv")
    clean_path = os.path.join(project_root, "data", "cleaned", "ecommerce_cleaned.csv")

    df = load_raw_data(raw_path)
    
    print("removing duplicates...")
    df = remove_duplicates(df)

    print("converting dates...")
    df = convert_dates(df)

    print("handling missing values...")
    df = handle_missing_values(df)

    print("validating data...")
    df = validate_data(df)

    print("adding derived columns...")
    df = derive_business_columns(df)
    df = derive_time_columns(df)

    print(f"final shape: {df.shape}")
    save_cleaned_data(df, clean_path)
    print("done")


if __name__ == "__main__":
    main()
