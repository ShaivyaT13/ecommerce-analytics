import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["font.size"] = 12

df = pd.read_csv("../data/cleaned/ecommerce_cleaned.csv")
df["order_date"] = pd.to_datetime(df["order_date"])

VIZ_DIR = "../visualizations"
os.makedirs(VIZ_DIR, exist_ok=True)

print(f"loaded {len(df)} rows")
print(f"dates: {df['order_date'].min().date()} to {df['order_date'].max().date()}")

# --- KPIs ---

total_rev = df["revenue"].sum()
total_profit = df["profit"].sum()
n_orders = df["order_id"].nunique()
n_customers = df["customer_id"].nunique()
aov = total_rev / n_orders

print(f"\nrevenue: ₹{total_rev:,.2f}")
print(f"profit: ₹{total_profit:,.2f}")
print(f"margin: {total_profit/total_rev:.1%}")
print(f"orders: {n_orders:,}")
print(f"customers: {n_customers}")
print(f"AOV: ₹{aov:,.2f}")

# --- category breakdown ---

cat = (
    df.groupby("category")
    .agg(orders=("order_id", "nunique"), revenue=("revenue", "sum"),
         profit=("profit", "sum"), avg_margin=("profit_margin", "mean"))
    .sort_values("revenue", ascending=False)
)
cat["share"] = cat["revenue"] / cat["revenue"].sum()
print("\n", cat)

# category chart
fig, ax = plt.subplots(figsize=(10, 6))
colors = ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#F44336"]
cat_sorted = cat.sort_values("revenue")
bars = ax.barh(cat_sorted.index, cat_sorted["revenue"],
               color=colors[:len(cat_sorted)], edgecolor="white", linewidth=0.5)
for bar, val in zip(bars, cat_sorted["revenue"]):
    ax.text(bar.get_width() + total_rev * 0.005, bar.get_y() + bar.get_height()/2,
            f"₹{val:,.0f}", va="center", fontsize=11)
ax.set_xlabel("Revenue (₹)")
ax.set_title("Revenue by Category", fontsize=14, fontweight="bold")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/category_revenue.png", dpi=150, bbox_inches="tight")
plt.show()

# margin comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
x = range(len(cat))
w = 0.35
axes[0].bar([i - w/2 for i in x], cat["revenue"], w, label="Revenue", color="#2196F3")
axes[0].bar([i + w/2 for i in x], cat["profit"], w, label="Profit", color="#4CAF50")
axes[0].set_xticks(list(x))
axes[0].set_xticklabels(cat.index, rotation=30, ha="right")
axes[0].set_title("Revenue vs Profit")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"₹{y:,.0f}"))
axes[0].legend()
axes[1].bar(list(x), cat["avg_margin"] * 100, color=colors[:len(cat)], edgecolor="white")
axes[1].set_ylabel("Avg Margin (%)")
axes[1].set_title("Profit Margin by Category")
axes[1].set_xticks(list(x))
axes[1].set_xticklabels(cat.index, rotation=30, ha="right")
plt.tight_layout()
plt.show()

# --- regions ---

reg = (
    df.groupby("region")
    .agg(customers=("customer_id", "nunique"), orders=("order_id", "nunique"),
         revenue=("revenue", "sum"), profit=("profit", "sum"),
         avg_margin=("profit_margin", "mean"))
    .sort_values("revenue", ascending=False)
)
print("\n", reg)

fig, ax = plt.subplots(figsize=(10, 6))
rcols = ["#1565C0", "#2E7D32", "#E65100", "#6A1B9A", "#757575"]
bars = ax.bar(reg.index, reg["revenue"], color=rcols[:len(reg)], edgecolor="white")
for bar, val in zip(bars, reg["revenue"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + total_rev * 0.003,
            f"₹{val:,.0f}", ha="center", fontsize=11)
ax.set_ylabel("Revenue (₹)")
ax.set_title("Revenue by Region", fontsize=14, fontweight="bold")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"₹{y:,.0f}"))
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/regional_revenue.png", dpi=150, bbox_inches="tight")
plt.show()

# --- monthly trend ---

monthly = (
    df.groupby("year_month")
    .agg(revenue=("revenue", "sum"), profit=("profit", "sum"),
         orders=("order_id", "nunique"))
    .sort_index()
)
monthly["prev"] = monthly["revenue"].shift(1)
monthly["mom_pct"] = (monthly["revenue"] - monthly["prev"]) / monthly["prev"] * 100
print("\n", monthly[["revenue", "profit", "orders", "mom_pct"]])

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(monthly.index, monthly["revenue"], color="#1565C0", marker="o",
        linewidth=2, markersize=6, label="Revenue")
ax.plot(monthly.index, monthly["profit"], color="#2E7D32", marker="s",
        linewidth=2, markersize=5, label="Profit")
ax.set_xlabel("Month")
ax.set_ylabel("Amount (₹)")
ax.set_title("Monthly Revenue & Profit", fontsize=14, fontweight="bold")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"₹{y:,.0f}"))
ax.legend(loc="upper left")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/monthly_revenue.png", dpi=150, bbox_inches="tight")
plt.show()

# --- top 10 products ---

top = (
    df.groupby("product")
    .agg(units=("quantity", "sum"), revenue=("revenue", "sum"),
         profit=("profit", "sum"), avg_margin=("profit_margin", "mean"))
    .sort_values("revenue", ascending=False)
    .head(10)
)
print("\n", top)

fig, ax = plt.subplots(figsize=(10, 7))
top_rev = top.sort_values("revenue")
bars = ax.barh(top_rev.index, top_rev["revenue"], color="#1976D2", edgecolor="white")
for bar, val in zip(bars, top_rev["revenue"]):
    ax.text(bar.get_width() + top["revenue"].max() * 0.01,
            bar.get_y() + bar.get_height()/2, f"₹{val:,.0f}", va="center", fontsize=10)
ax.set_xlabel("Revenue (₹)")
ax.set_title("Top 10 Products by Revenue", fontsize=14, fontweight="bold")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/top_products.png", dpi=150, bbox_inches="tight")
plt.show()

# --- high volume, low margin products ---

prod = (
    df.groupby("product")
    .agg(units=("quantity", "sum"), revenue=("revenue", "sum"),
         profit=("profit", "sum"), avg_margin=("profit_margin", "mean"))
)
# these sell a lot but don't make much per unit
print("\nhigh volume low margin:")
print(prod[prod["units"] > 100].sort_values("avg_margin").head(5))

# --- customers ---

top_cust = (
    df.groupby(["customer_id", "customer_name"])
    .agg(orders=("order_id", "nunique"), spend=("revenue", "sum"),
         profit=("profit", "sum"))
    .sort_values("spend", ascending=False)
    .head(10)
)
print("\ntop 10 customers:")
print(top_cust)

# repeat vs one-time
cust_orders = df.groupby("customer_id")["order_id"].nunique()
repeats = (cust_orders > 1).sum()
print(f"\nrepeat customers: {repeats}/{len(cust_orders)} ({repeats/len(cust_orders):.1%})")

# --- customer segments ---

cust = (
    df.groupby("customer_id")
    .agg(spend=("revenue", "sum"), orders=("order_id", "nunique"),
         profit=("profit", "sum"))
    .reset_index()
)

def segment(spend):
    if spend >= 5000: return "High Value"
    elif spend >= 2000: return "Medium Value"
    else: return "Low Value"

cust["seg"] = cust["spend"].apply(segment)

seg_summary = cust.groupby("seg").agg(
    n=("customer_id", "count"), revenue=("spend", "sum"), profit=("profit", "sum"),
    avg_orders=("orders", "mean")
)
seg_summary["rev_share"] = seg_summary["revenue"] / seg_summary["revenue"].sum()
print("\ncustomer segments:")
print(seg_summary)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
seg_colors = {"High Value": "#1565C0", "Medium Value": "#FF8F00", "Low Value": "#E53935"}
order = ["High Value", "Medium Value", "Low Value"]
seg_data = seg_summary.reindex(order).dropna()
axes[0].bar(seg_data.index, seg_data["n"], color=[seg_colors[s] for s in seg_data.index])
axes[0].set_title("Customers by Segment")
axes[0].set_ylabel("Count")
axes[1].pie(seg_data["revenue"], labels=seg_data.index, autopct="%1.1f%%",
            colors=[seg_colors[s] for s in seg_data.index], startangle=90)
axes[1].set_title("Revenue Share")
plt.tight_layout()
plt.show()

# --- discount distribution ---

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(df["discount"], bins=20, color="#1976D2", edgecolor="white")
ax.set_xlabel("Discount")
ax.set_ylabel("Frequency")
ax.set_title("Discount Distribution", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()
print(f"avg discount: {df['discount'].mean():.2%}")
print(f"no discount: {(df['discount'] == 0).sum()} ({(df['discount'] == 0).mean():.1%})")

# --- payment methods ---

pay = (
    df.groupby("payment_method")
    .agg(orders=("order_id", "nunique"), revenue=("revenue", "sum"))
    .sort_values("orders", ascending=False)
)
pay["pct"] = pay["orders"] / pay["orders"].sum()
print("\npayment methods:")
print(pay)
