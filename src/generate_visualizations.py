import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, "data", "cleaned", "ecommerce_cleaned.csv")
    viz_dir = os.path.join(project_root, "visualizations")
    os.makedirs(viz_dir, exist_ok=True)

    print("loading data...")
    df = pd.read_csv(csv_path)
    df["order_date"] = pd.to_datetime(df["order_date"])
    print(f"loaded {len(df)} rows")

    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["font.size"] = 12

    total_revenue = df["revenue"].sum()

    print("saving category_revenue.png...")
    cat = (
        df.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=True)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#F44336"]
    bars = ax.barh(
        cat["category"], cat["revenue"],
        color=colors[: len(cat)], edgecolor="white", linewidth=0.5,
    )
    for bar, val in zip(bars, cat["revenue"]):
        ax.text(
            bar.get_width() + total_revenue * 0.005,
            bar.get_y() + bar.get_height() / 2,
            f"₹{val:,.0f}", va="center", fontsize=11,
        )
    ax.set_xlabel("Revenue (₹)")
    ax.set_title("Revenue by Product Category", fontsize=14, fontweight="bold")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, "category_revenue.png"), dpi=150, bbox_inches="tight")
    plt.close()

    print("saving regional_revenue.png...")
    region = (
        df[df["region"] != "Unknown"]
        .groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    region_colors = ["#1565C0", "#2E7D32", "#E65100", "#6A1B9A"]
    bars = ax.bar(
        region["region"], region["revenue"],
        color=region_colors[: len(region)], edgecolor="white", linewidth=0.5,
    )
    for bar, val in zip(bars, region["revenue"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + total_revenue * 0.003,
            f"₹{val:,.0f}", ha="center", fontsize=11,
        )
    ax.set_xlabel("Region")
    ax.set_ylabel("Revenue (₹)")
    ax.set_title("Revenue by Region", fontsize=14, fontweight="bold")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"₹{y:,.0f}"))
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, "regional_revenue.png"), dpi=150, bbox_inches="tight")
    plt.close()

    print("saving monthly_revenue.png...")
    monthly = (
        df.groupby("year_month")
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
        .sort_index()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(
        monthly["year_month"], monthly["revenue"],
        color="#1565C0", marker="o", linewidth=2, markersize=6, label="Revenue",
    )
    ax.plot(
        monthly["year_month"], monthly["profit"],
        color="#2E7D32", marker="s", linewidth=2, markersize=5, label="Profit",
    )
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount (₹)")
    ax.set_title("Monthly Revenue & Profit Trend", fontsize=14, fontweight="bold")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"₹{y:,.0f}"))
    ax.legend(loc="upper left")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, "monthly_revenue.png"), dpi=150, bbox_inches="tight")
    plt.close()

    print("saving top_products.png...")
    top = (
        df.groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values(ascending=True)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 7))
    bars = ax.barh(
        top["product"], top["revenue"],
        color="#1976D2", edgecolor="white", linewidth=0.5,
    )
    for bar, val in zip(bars, top["revenue"]):
        ax.text(
            bar.get_width() + top["revenue"].max() * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"₹{val:,.0f}", va="center", fontsize=10,
        )
    ax.set_xlabel("Revenue (₹)")
    ax.set_title("Top 10 Products by Revenue", fontsize=14, fontweight="bold")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, "top_products.png"), dpi=150, bbox_inches="tight")
    plt.close()

    print(f"saved visualizations to {viz_dir}")


if __name__ == "__main__":
    main()
