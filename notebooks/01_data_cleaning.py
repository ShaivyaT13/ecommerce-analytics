import pandas as pd
import numpy as np

df = pd.read_csv("../data/raw/ecommerce_sales.csv")
print(f"loaded {df.shape[0]} rows, {df.shape[1]} cols")

df.head()
df.shape
df.columns.tolist()
df.info()
df.describe()
df.isnull().sum()
print(f"duplicates: {df.duplicated().sum()}")

# drop dupes
before = len(df)
df = df.drop_duplicates()
print(f"removed {before - len(df)} dupes, now {len(df)} rows")

# fix dates
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
print(f"bad dates: {df['order_date'].isnull().sum()}")
df = df.dropna(subset=["order_date"])

# missing values
# discount missing = no discount was given, so fill with 0
df["discount"] = pd.to_numeric(df["discount"], errors="coerce")
print(f"missing discounts: {df['discount'].isnull().sum()}")
df["discount"] = df["discount"].fillna(0)

# for region and name, keep the row but mark as unknown
df["region"] = df["region"].replace("", np.nan).fillna("Unknown")
df["customer_name"] = df["customer_name"].replace("", np.nan).fillna("Unknown")

print(f"nulls left:\n{df.isnull().sum()}")

# validation - get rid of nonsense rows
print(f"qty <= 0: {(df['quantity'] <= 0).sum()}")
print(f"price <= 0: {(df['unit_price'] <= 0).sum()}")
print(f"discount out of range: {((df['discount'] < 0) | (df['discount'] > 1)).sum()}")

before = len(df)
df = df[df["quantity"] > 0]
df = df[df["unit_price"] > 0]
df = df[(df["discount"] >= 0) & (df["discount"] <= 1)]
print(f"dropped {before - len(df)} bad rows")

# derived columns
df["revenue"] = df["quantity"] * df["unit_price"] * (1 - df["discount"])
df["total_cost"] = df["quantity"] * df["cost"]
df["profit"] = df["revenue"] - df["total_cost"]
df["profit_margin"] = df["profit"] / df["revenue"].replace(0, pd.NA)

# time stuff
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.month_name()
df["year_month"] = df["order_date"].dt.to_period("M").astype(str)

print(f"\nfinal shape: {df.shape}")
print(f"revenue range: {df['revenue'].min():.2f} - {df['revenue'].max():.2f}")
print(f"profit range: {df['profit'].min():.2f} - {df['profit'].max():.2f}")

df.to_csv("../data/cleaned/ecommerce_cleaned.csv", index=False)
print("saved to ../data/cleaned/ecommerce_cleaned.csv")
