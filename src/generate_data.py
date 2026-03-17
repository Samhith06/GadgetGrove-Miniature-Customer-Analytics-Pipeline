import sqlite3
import json
from pymongo import MongoClient
import random
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SQL_DIR = os.path.join(BASE_DIR, "sql")
def setup_sql():
    # SQL Connection
    print("Setting up SQL Database...")
    db_path = os.path.join(DATA_DIR, "shop.db")
    sql_path = os.path.join(SQL_DIR, "setup_sql.sql")
    conn = sqlite3.connect(db_path)
    with open(sql_path, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("SQL setup complete.")

def setup_nosql():
    print("Setting up NoSQL Database (MongoDB)...")
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        client.admin.command('ping') # test connection
        db = client["GreenField"]
        collection = db["reviews"]
        collection.drop()
        reviews_data = [
            {"review_id": "r1", "product_id": "1", "customer_id": "1", "rating": 5, "review_text": "Great laptop!"},
            {"review_id": "r2", "product_id": "3", "customer_id": "1", "rating": 4, "review_text": "Good headphones, comfortable."},
            {"review_id": "r3", "product_id": "2", "customer_id": "2", "rating": 5, "review_text": "Amazing smartphone."},
            {"review_id": "r4", "product_id": "5", "customer_id": "2", "rating": 2, "review_text": "Coffee maker broke after a week."},
            {"review_id": "r5", "product_id": "4", "customer_id": "3", "rating": 4, "review_text": "Very comfortable chair."},
            {"review_id": "r6", "product_id": "1", "customer_id": "3", "rating": 5, "review_text": "Smooth performance."},
            {"review_id": "r7", "product_id": "2", "customer_id": "4", "rating": 3, "review_text": "Okay phone, battery could be better."},
            {"review_id": "r8", "product_id": "5", "customer_id": "5", "rating": 5, "review_text": "Makes great coffee."},
            {"review_id": "r9", "product_id": "1", "customer_id": "5", "rating": 5, "review_text": "Love it."},
            {"review_id": "r10", "product_id": "2", "customer_id": "6", "rating": 4, "review_text": "Nice features."},
            {"review_id": "r11", "product_id": "4", "customer_id": "6", "rating": 1, "review_text": "Wheels broke off."},
            {"review_id": "r12", "product_id": "3", "customer_id": "7", "rating": 3, "review_text": "Average sound quality."},
            {"review_id": "r13", "product_id": "5", "customer_id": "7", "rating": 4, "review_text": "Good value."},
            {"review_id": "r14", "product_id": "1", "customer_id": "8", "rating": 5, "review_text": "Best laptop I've ever owned."},
            {"review_id": "r15", "product_id": "4", "customer_id": "9", "rating": 5, "review_text": "Perfect for my home office."},
            {"review_id": "r16", "product_id": "3", "customer_id": "9", "rating": 2, "review_text": "Too tight on my ears."},
            {"review_id": "r17", "product_id": "5", "customer_id": "10", "rating": 4, "review_text": "Works as expected."},
        ]

        collection.insert_many(reviews_data)
        print(f"Inserted {len(reviews_data)} reviews into MongoDB.")

        # Export to JSON as per deliverable 4
        export_data = list(collection.find({}, {'_id': False}))
        export_path = os.path.join(DATA_DIR, "reviews_export.json")
        with open(export_path, "w") as f:
            json.dump(export_data, f, indent=4)
        print("Exported MongoDB reviews to reviews_export.json (in data directory)")

    except Exception as e:
        print(f"MongoDB connection/operation failed: {e}")

if __name__ == "__main__":
    setup_sql()
    setup_nosql()
