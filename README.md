# 🛍️ E-Commerce Sales & Customer Analytics

> An end-to-end data analytics pipeline and interactive web dashboard built with Python, SQLite, Flask, and custom HTML/CSS. Analyzes ~20,000 orders across 500 customers to extract sales performance, profit margins, and customer retention metrics.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Backend-Flask-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Chart.js](https://img.shields.io/badge/Frontend-Chart.js-FF6384?logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🚀 Live Demo
**Public Link:** `https://<your-app-name>.onrender.com` *(Follow the [Deployment Guide](#-how-to-deploy-live-link) below to launch your own)*

---

## 📸 Key Features

- **Executive KPI Cards**: Real-time summary of Total Revenue, Net Profit, Profit Margin, Orders, Customers, and Average Order Value (AOV) formatted in Indian Rupees (₹).
- **Interactive Filtering**: Filter all metrics dynamically by product category and geographic region without reloading the page.
- **Visual Analytics**:
  - 18-month monthly revenue & profit trend line
  - Category-wise revenue distribution & margin comparisons
  - Regional market performance (North, West, East, South)
  - Top 10 revenue-generating products
  - Customer payment method preferences (UPI, Credit Card, Debit Card, etc.)
- **Interactive SQL Sandbox**: Run live read-only SQL queries against the underlying `ecommerce.db` database directly from the browser, with one-click presets for common analytics queries (Window Functions, CTEs, Ranking).
- **Recent Orders Stream**: Paginated line-item browser inspecting transactional records.

---

## 🏗️ Architecture

```
                      ecommerce_sales.csv (Raw Dataset)
                                     │
                                     ▼
                           ┌──────────────────┐
                           │   Data Cleaning  │
                           │     (Pandas)     │
                           └─────────┬────────┘
                                     │
                                     ▼
                         ecommerce_cleaned.csv
                                     │
                                     ▼
                           ┌──────────────────┐
                           │    SQLite DB     │
                           │   ecommerce.db   │
                           └─────────┬────────┘
                                     │
                                     ▼
                           ┌──────────────────┐
                           │   Flask API &    │
                           │ Custom HTML/CSS  │
                           └─────────┬────────┘
                                     │
                                     ▼
                           ┌──────────────────┐
                           │ Live Web App &   │
                           │  SQL Playground  │
                           └──────────────────┘
```

---

## 📊 Summary of Findings

Based on ~20,000 orders between **January 2024 and June 2025**:

| Metric | Value |
| :--- | :--- |
| **Total Revenue** | **₹60,18,372** |
| **Total Net Profit** | **₹14,34,337** |
| **Overall Profit Margin** | **23.8%** |
| **Total Processed Orders** | **19,940** |
| **Customer Count** | **500 unique buyers** |
| **Average Order Value (AOV)** | **₹301.82** |

### Key Business Insights
1. **The Volume vs. Margin Paradox**: Electronics drives **62.4%** of total gross revenue, but yields only a **31.2%** average profit margin (with Laptops sitting at just **11.0%** margin due to heavy discounting). Conversely, **Office Supplies** brings in the lowest revenue volume but boasts the highest profit margin at **55.9%**.
2. **Geographic Distribution**: Sales are well-balanced across regions (North: ₹15.8L, West: ₹15.5L, East: ₹14.9L), while the South region (₹13.7L, 113 customers) represents an under-penetrated market with high growth upside.
3. **Payment Preferences**: Digital payments dominate **89.7%** of transactions, led by UPI (30.0%) and Credit Cards (29.5%).

👉 *Read the complete analytical write-up in [`analysis_results.md`](analysis_results.md).*

---

## 📁 Repository Structure

```
ecommerce-data-analysis/
├── data/
│   ├── raw/ecommerce_sales.csv          # Raw generated data (~20K rows)
│   └── cleaned/ecommerce_cleaned.csv    # Cleaned & validated dataset
│
├── notebooks/
│   ├── 01_data_cleaning.py              # Standalone data cleaning script
│   └── 02_exploratory_analysis.py       # Standalone EDA script with charts
│
├── sql/
│   ├── schema.sql                       # Database DDL (orders, customers, products + indexes)
│   └── analysis_queries.sql             # Comprehensive SQL queries (KPIs, CTEs, Window Fns)
│
├── src/
│   ├── clean_data.py                    # Data cleaning pipeline
│   ├── generate_dataset.py              # Synthetic data generator
│   ├── generate_visualizations.py       # Matplotlib static chart generator
│   └── load_database.py                 # SQLite database ingestion loader
│
├── static/
│   ├── css/style.css                    # Custom dashboard styles & dark code editor
│   └── js/app.js                        # Chart.js integration & SQL playground logic
│
├── templates/
│   └── index.html                       # Responsive web dashboard
│
├── visualizations/                      # High-res chart exports (PNG)
│   ├── category_revenue.png
│   ├── monthly_revenue.png
│   ├── regional_revenue.png
│   └── top_products.png
│
├── app.py                               # Flask backend application
├── ecommerce.db                         # Production SQLite database
├── Procfile                             # Cloud deployment command
├── requirements.txt                     # Python dependencies
└── README.md                            # Project documentation
```

---

## ⚡ Quickstart (Run Locally)

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/ecommerce-analytics.git
cd ecommerce-analytics
```

### 2. Set up virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the application
```bash
python app.py
```
Open your browser and navigate to: **`http://localhost:5000`**

---

## 🛠️ Data Cleaning Process

The dataset was processed through a systematic cleaning pipeline (`src/clean_data.py`):

| Issue | Resolution | Rationale |
| :--- | :--- | :--- |
| **Duplicates** | Dropped identical rows | Exact duplicate transactions skew revenue aggregations. |
| **Invalid Dates** | Coerced using `errors="coerce"` and dropped `NaT` | Dates cannot be reliably imputed without corrupting time-series trends. |
| **Missing Discount** | Imputed with `0.0` | In e-commerce, missing discount values represent transactions with no promotion applied. |
| **Missing Region/Name** | Filled with `"Unknown"` | Retains financial transaction records for revenue tracking rather than discarding rows. |
| **Invalid Numeric Values** | Removed rows where `quantity <= 0`, `unit_price <= 0`, or `discount > 1.0` | Prevents corrupted financial calculations and division errors. |

---

## 💡 SQL Techniques Included

The queries in [`sql/analysis_queries.sql`](sql/analysis_queries.sql) demonstrate practical relational database querying:
- **Aggregations & Filtering**: `GROUP BY`, `HAVING`, `DISTINCT`
- **Multi-Table Joins**: `INNER JOIN` linking transactional orders to normalized customer and product tables.
- **Common Table Expressions (CTEs)**: Multi-step customer lifetime value (CLV) segmentation.
- **Window Functions**:
  - `LAG()` and `LEAD()` for Month-over-Month (MoM) revenue growth calculations.
  - `ROW_NUMBER() OVER (PARTITION BY category ...)` to isolate top-selling items per catalog category.
  - `RANK()` and `DENSE_RANK()` for monthly customer spend leaderboards.
  - Running cumulative totals using `SUM(...) OVER (ORDER BY year_month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`.
- **Conditional Logic**: `CASE WHEN` statements for customer tiering and discount impact bucketing.

---

## 🌐 How to Deploy (Live Link)

You can deploy this web dashboard for free on **[Render.com](https://render.com)** in 3 steps:

1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git push -u origin main
   ```

2. **Connect to Render**:
   - Go to [dashboard.render.com](https://dashboard.render.com) and click **New + > Web Service**.
   - Select your GitHub repository.

3. **Configure Settings**:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`
   - Click **Deploy Web Service**.

Your live URL will be ready in ~2 minutes at `https://your-service-name.onrender.com`.

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
