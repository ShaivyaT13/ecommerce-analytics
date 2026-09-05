# generates fake ecommerce data with some messy rows thrown in

import csv
import random
import os
from datetime import datetime, timedelta

random.seed(42)

REGIONS_CITIES = {
    "North": ["Delhi", "Jaipur", "Lucknow", "Chandigarh"],
    "South": ["Bangalore", "Chennai", "Hyderabad", "Kochi"],
    "East": ["Kolkata", "Patna", "Bhubaneswar"],
    "West": ["Mumbai", "Pune", "Ahmedabad", "Surat"],
}

FIRST_NAMES = [
    "Rahul", "Amit", "Priya", "Sneha", "Vikram", "Anjali", "Ravi", "Pooja",
    "Suresh", "Neha", "Arun", "Kavita", "Deepak", "Sunita", "Manoj",
    "Meena", "Rajesh", "Swati", "Sanjay", "Divya", "Nikhil", "Rina",
    "Kiran", "Lakshmi", "Ashok", "Geeta", "Vivek", "Anita", "Ramesh",
    "Shweta", "Gaurav", "Rekha", "Pankaj", "Suman", "Tarun", "Nisha",
    "Alok", "Preeti", "Hemant", "Jyoti", "Rohit", "Sarita", "Harsh",
    "Usha", "Mohan", "Pallavi", "Dinesh", "Rashmi", "Yogesh", "Vandana",
]

LAST_NAMES = [
    "Sharma", "Kumar", "Singh", "Gupta", "Patel", "Reddy", "Nair",
    "Verma", "Joshi", "Mehta", "Shah", "Rao", "Das", "Mishra",
    "Chopra", "Iyer", "Pillai", "Bose", "Mukherjee", "Dutta",
]

PRODUCTS = {
    "Electronics": [
        ("Laptop", 800, 650),
        ("Smartphone", 500, 380),
        ("Tablet", 350, 260),
        ("Mouse", 25, 12),
        ("Keyboard", 45, 22),
        ("Headphones", 80, 45),
        ("Monitor", 300, 220),
        ("USB Drive", 15, 7),
    ],
    "Furniture": [
        ("Office Chair", 150, 100),
        ("Desk", 200, 140),
        ("Bookshelf", 120, 80),
        ("Filing Cabinet", 90, 55),
        ("Standing Desk", 350, 250),
    ],
    "Clothing": [
        ("T-Shirt", 20, 8),
        ("Jeans", 45, 22),
        ("Jacket", 80, 45),
        ("Sneakers", 65, 35),
        ("Formal Shirt", 35, 18),
    ],
    "Office Supplies": [
        ("Notebook Pack", 10, 4),
        ("Pen Set", 8, 3),
        ("Printer Paper", 12, 5),
        ("Stapler", 6, 2),
        ("Whiteboard", 40, 20),
    ],
    "Food & Beverages": [
        ("Coffee Beans 1kg", 15, 8),
        ("Tea Box", 10, 5),
        ("Protein Bars (12pk)", 25, 14),
        ("Mixed Nuts 500g", 12, 6),
        ("Energy Drink (6pk)", 18, 10),
    ],
}

PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Cash", "Net Banking"]

ALL_PRODUCTS = []
for category, items in PRODUCTS.items():
    for product_name, price, cost in items:
        ALL_PRODUCTS.append((category, product_name, price, cost))

customers = []
for i in range(1, 501):
    cid = f"C{i:03d}"
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    name = f"{first} {last}"
    region = random.choice(list(REGIONS_CITIES.keys()))
    city = random.choice(REGIONS_CITIES[region])
    customers.append((cid, name, region, city))

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 6, 30)
DATE_RANGE_DAYS = (END_DATE - START_DATE).days

NUM_ORDERS = 20000

rows = []
order_id = 10001

for _ in range(NUM_ORDERS):
    cid, cname, region, city = random.choice(customers)

    days_offset = random.randint(0, DATE_RANGE_DAYS)
    order_date = START_DATE + timedelta(days=days_offset)
    order_date_str = order_date.strftime("%Y-%m-%d")

    category, product, unit_price, cost = random.choice(ALL_PRODUCTS)

    quantity = random.choices(
        population=[1, 2, 3, 4, 5, 6, 7, 8, 10],
        weights=[35, 25, 15, 10, 5, 4, 3, 2, 1],
        k=1,
    )[0]

    # ~60% get no discount
    if random.random() < 0.60:
        discount = 0.0
    else:
        discount = round(random.choice([0.05, 0.10, 0.15, 0.20, 0.25, 0.30]), 2)

    payment = random.choices(
        population=PAYMENT_METHODS,
        weights=[30, 20, 30, 10, 10],
        k=1,
    )[0]

    rows.append([
        order_id, order_date_str, cid, cname, region, city,
        category, product, quantity, unit_price, discount, cost, payment,
    ])

    order_id += 1

dup_indices = random.sample(range(len(rows)), 200)
for idx in dup_indices:
    rows.append(list(rows[idx]))

missing_disc_indices = random.sample(range(len(rows)), 300)
for idx in missing_disc_indices:
    rows[idx][10] = ""

missing_region_indices = random.sample(range(len(rows)), 50)
for idx in missing_region_indices:
    rows[idx][4] = ""

missing_name_indices = random.sample(range(len(rows)), 30)
for idx in missing_name_indices:
    rows[idx][3] = ""

invalid_date_indices = random.sample(range(len(rows)), 20)
for idx in invalid_date_indices:
    rows[idx][1] = random.choice(["not-a-date", "invalid", "2025-13-45", "N/A"])

neg_qty_indices = random.sample(range(len(rows)), 15)
for idx in neg_qty_indices:
    rows[idx][8] = -abs(rows[idx][8]) if isinstance(rows[idx][8], int) else -1

neg_price_indices = random.sample(range(len(rows)), 10)
for idx in neg_price_indices:
    rows[idx][9] = -abs(rows[idx][9]) if isinstance(rows[idx][9], (int, float)) else -10

bad_disc_indices = random.sample(range(len(rows)), 15)
for idx in bad_disc_indices:
    rows[idx][10] = round(random.choice([-0.1, 1.5, 2.0, -0.5, 1.2]), 2)

random.shuffle(rows)

HEADER = [
    "order_id", "order_date", "customer_id", "customer_name", "region",
    "city", "category", "product", "quantity", "unit_price", "discount",
    "cost", "payment_method",
]

output_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "raw", "ecommerce_sales.csv",
)

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(HEADER)
    writer.writerows(rows)

print(f"wrote {len(rows)} rows to {output_path}")
