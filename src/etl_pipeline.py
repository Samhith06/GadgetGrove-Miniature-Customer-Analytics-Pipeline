import sqlite3
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
VIS_DIR = os.path.join(BASE_DIR, "visualizations")

db_path = os.path.join(DATA_DIR, "shop.db")
conn = sqlite3.connect(db_path)

orders = pd.read_sql("""
SELECT o.order_id,o.customer_id,o.product_id,o.order_date,o.quantity,
       p.product_name,p.category,p.price
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
""", conn)

client = MongoClient("mongodb://localhost:27017/")
db = client["GreenField"]

reviews = pd.DataFrame(list(db.reviews.find()))

orders["customer_id"] = orders["customer_id"].astype(str)
orders["product_id"] = orders["product_id"].astype(str)

reviews["customer_id"] = reviews["customer_id"].astype(str)
reviews["product_id"] = reviews["product_id"].astype(str)

df = pd.merge(orders, reviews, how="left", on=["customer_id","product_id"])

df["rating"] = df["rating"].fillna(0)
df["is_satisfied"] = df["rating"] >= 4
df["total_price"] = df["quantity"] * df["price"]

# Complex Transformation: Customer Lifetime Value (CLV)
clv_df = df.groupby("customer_id")["total_price"].sum().reset_index()
clv_df.rename(columns={"total_price": "customer_lifetime_value"}, inplace=True)
df = pd.merge(df, clv_df, how="left", on="customer_id")

print(df)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_product_report(
product_key INTEGER PRIMARY KEY,
product_name TEXT,
category TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_sales_reviews(
sale_id INTEGER PRIMARY KEY,
order_id INTEGER,
product_key INTEGER,
customer_id INTEGER,
order_date DATE,
quantity INTEGER,
total_price REAL,
rating REAL,
is_satisfied BOOLEAN,
customer_lifetime_value REAL
)
""")

products = df[["product_id","product_name","category"]].drop_duplicates()

products.columns = ["product_key","product_name","category"]

products.to_sql("dim_product_report",conn,if_exists="replace",index=False)

fact = df[["order_id","product_id","customer_id","order_date","quantity","total_price",
"rating","is_satisfied","customer_lifetime_value"]]

fact.columns = ["order_id","product_key","customer_id","order_date","quantity",
"total_price","rating","is_satisfied","customer_lifetime_value"]

fact.insert(0,"sale_id",range(1,len(fact)+1))

fact.to_sql("fact_sales_reviews",conn,if_exists="replace",index=False)

# Visualization
print("Generating visualization...")
# Calculate mean rating per category
avg_rating_per_cat = df.groupby('category')['rating'].mean().reset_index()

plt.figure(figsize=(8, 5))
plt.bar(avg_rating_per_cat['category'], avg_rating_per_cat['rating'], color='skyblue', edgecolor='black')
plt.title('Average Product Rating by Category')
plt.xlabel('Category')
plt.ylabel('Average Rating (0-5)')
plt.ylim(0, 5)

# Save the figure as an image
plt.tight_layout()
chart1_path = os.path.join(VIS_DIR, 'category_ratings_chart.png')
plt.savefig(chart1_path)
print(f"Data visualization saved to '{chart1_path}'")

# Visualization 2: Top Customers by Customer Lifetime Value
plt.figure(figsize=(8, 5))
top_customers = clv_df.sort_values(by='customer_lifetime_value', ascending=False).head(5)
plt.bar(top_customers['customer_id'].astype(str), top_customers['customer_lifetime_value'], color='lightgreen', edgecolor='black')
plt.title('Top 5 Customers by Lifetime Value (CLV)')
plt.xlabel('Customer ID')
plt.ylabel('Lifetime Value ($)')

plt.tight_layout()
chart2_path = os.path.join(VIS_DIR, 'top_customers_clv_chart.png')
plt.savefig(chart2_path)
print(f"Data visualization saved to '{chart2_path}'")
