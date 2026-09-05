import os
import sqlite3
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "ecommerce.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/filters")
def get_filters():
    conn = get_db()
    categories = [r[0] for r in conn.execute("SELECT DISTINCT category FROM orders ORDER BY category").fetchall()]
    regions = [r[0] for r in conn.execute("SELECT DISTINCT region FROM orders WHERE region != 'Unknown' ORDER BY region").fetchall()]
    conn.close()
    return jsonify({"categories": categories, "regions": regions})


@app.route("/api/kpis")
def get_kpis():
    cat = request.args.get("category", "")
    reg = request.args.get("region", "")

    where_clauses = []
    params = []
    if cat:
        where_clauses.append("category = ?")
        params.append(cat)
    if reg:
        where_clauses.append("region = ?")
        params.append(reg)

    where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    query = f"""
        SELECT 
            ROUND(COALESCE(SUM(revenue), 0), 2) AS total_revenue,
            ROUND(COALESCE(SUM(profit), 0), 2) AS total_profit,
            COUNT(DISTINCT order_id) AS total_orders,
            COUNT(DISTINCT customer_id) AS total_customers,
            ROUND(COALESCE(SUM(revenue) * 1.0 / NULLIF(COUNT(DISTINCT order_id), 0), 0), 2) AS avg_order_value
        FROM orders
        {where_sql}
    """

    conn = get_db()
    row = conn.execute(query, params).fetchone()
    conn.close()

    rev = row["total_revenue"]
    profit = row["total_profit"]
    margin = round((profit / rev * 100), 1) if rev > 0 else 0.0

    return jsonify({
        "revenue": rev,
        "profit": profit,
        "margin": margin,
        "orders": row["total_orders"],
        "customers": row["total_customers"],
        "aov": row["avg_order_value"]
    })


@app.route("/api/charts/category")
def chart_category():
    conn = get_db()
    rows = conn.execute("""
        SELECT category, 
               ROUND(SUM(revenue), 2) AS revenue, 
               ROUND(SUM(profit), 2) AS profit,
               ROUND(AVG(profit_margin) * 100, 1) AS margin
        FROM orders 
        GROUP BY category 
        ORDER BY revenue DESC
    """).fetchall()
    conn.close()

    return jsonify({
        "labels": [r["category"] for r in rows],
        "revenue": [r["revenue"] for r in rows],
        "profit": [r["profit"] for r in rows],
        "margin": [r["margin"] for r in rows]
    })


@app.route("/api/charts/region")
def chart_region():
    conn = get_db()
    rows = conn.execute("""
        SELECT region, 
               ROUND(SUM(revenue), 2) AS revenue, 
               ROUND(SUM(profit), 2) AS profit
        FROM orders 
        WHERE region != 'Unknown'
        GROUP BY region 
        ORDER BY revenue DESC
    """).fetchall()
    conn.close()

    return jsonify({
        "labels": [r["region"] for r in rows],
        "revenue": [r["revenue"] for r in rows],
        "profit": [r["profit"] for r in rows]
    })


@app.route("/api/charts/monthly")
def chart_monthly():
    conn = get_db()
    rows = conn.execute("""
        SELECT year_month, 
               ROUND(SUM(revenue), 2) AS revenue, 
               ROUND(SUM(profit), 2) AS profit
        FROM orders 
        GROUP BY year_month 
        ORDER BY year_month ASC
    """).fetchall()
    conn.close()

    return jsonify({
        "labels": [r["year_month"] for r in rows],
        "revenue": [r["revenue"] for r in rows],
        "profit": [r["profit"] for r in rows]
    })


@app.route("/api/charts/top-products")
def chart_top_products():
    conn = get_db()
    rows = conn.execute("""
        SELECT product, 
               ROUND(SUM(revenue), 2) AS revenue,
               SUM(quantity) AS units
        FROM orders 
        GROUP BY product 
        ORDER BY revenue DESC 
        LIMIT 10
    """).fetchall()
    conn.close()

    return jsonify({
        "labels": [r["product"] for r in rows],
        "revenue": [r["revenue"] for r in rows],
        "units": [r["units"] for r in rows]
    })


@app.route("/api/charts/payment")
def chart_payment():
    conn = get_db()
    rows = conn.execute("""
        SELECT payment_method, 
               COUNT(DISTINCT order_id) AS orders,
               ROUND(SUM(revenue), 2) AS revenue
        FROM orders 
        GROUP BY payment_method 
        ORDER BY orders DESC
    """).fetchall()
    conn.close()

    return jsonify({
        "labels": [r["payment_method"] for r in rows],
        "orders": [r["orders"] for r in rows],
        "revenue": [r["revenue"] for r in rows]
    })


@app.route("/api/orders")
def get_orders():
    limit = min(int(request.args.get("limit", 20)), 100)
    offset = int(request.args.get("offset", 0))

    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    rows = conn.execute("""
        SELECT order_id, order_date, customer_name, region, category, product, quantity, unit_price, discount, revenue, profit
        FROM orders 
        ORDER BY order_date DESC 
        LIMIT ? OFFSET ?
    """, (limit, offset)).fetchall()
    conn.close()

    return jsonify({
        "total": total,
        "orders": [dict(r) for r in rows]
    })


@app.route("/api/sql", methods=["POST"])
def run_sql():
    data = request.get_json() or {}
    query = (data.get("query") or "").strip()

    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    # Only allow SELECT statements for safety
    first_word = query.split()[0].upper() if query.split() else ""
    if first_word not in ("SELECT", "WITH"):
        return jsonify({"error": "Only SELECT / read-only queries are permitted"}), 400

    for blocked in ("INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "ATTACH", "DETACH"):
        if f" {blocked} " in f" {query.upper()} ":
            return jsonify({"error": f"Statement '{blocked}' is not allowed"}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        conn.close()

        results = [[item for item in row] for row in rows[:100]]
        return jsonify({
            "columns": columns,
            "rows": results,
            "total_returned": len(rows),
            "truncated": len(rows) > 100
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
