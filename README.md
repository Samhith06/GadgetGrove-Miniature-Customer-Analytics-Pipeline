# GadgetGrove Miniature Customer Analytics Pipeline

## Setup Instructions

### Prerequisites

- Python 3.8+
- SQLite3
- MongoDB running locally on port `localhost:27017`
- Pip packages: `pandas`, `pymongo`

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

_(If you do not have a requirements.txt, you can install manually: `pip install pandas pymongo`)_

### 2. Generate Data and Setup Databases

To initialize both the SQLite relational database and the MongoDB Document store, run:

```bash
python src/generate_data.py
```

This script will:

1. Run `setup_sql.sql` to create and populate the `shop.db` SQLite database with Customers, Products, and Orders.
2. Connect to the local MongoDB instance on port `27017`.
3. Create and populate the `GreenField.reviews` collection with product reviews.
4. Export the reviews to `reviews_export.json` automatically.

### 3. Run the ETL Pipeline

Extract the data from both databases, transform it, and load it into a star schema for analytics.

```bash
python src/etl_pipeline.py
```

This script will output the merged dataframe into the console and create the `dim_product_report` and `fact_sales_reviews` tables inside `shop.db`.

### 4. Architecture Diagram

```mermaid
flowchart TD
    A[User/Analyst] -->|Run scripts| B[Local Python ETL]
    subgraph "Source Systems"
      C1[SQLite (shop.db): Customers, Products, Orders]
      C2[MongoDB (GreenField.reviews): reviews]
    end
    B -->|Read via sqlite3| C1
    B -->|Read via pymongo| C2
    B --> D[Transform in pandas]
    D --> E[Load star schema into SQLite]
    E --> F1[dim_product_report]
    E --> F2[fact_sales_reviews]
    D --> G[Generate charts with matplotlib]
    G --> H[visualizations/category_ratings_chart.png]
    G --> I[visualizations/top_customers_clv_chart.png]
    B --> J[data/reviews_export.json]
    E --> K[data/shop.db]
```

### 5. Artifacts and Project Structure

- `src/generate_data.py`: Central data setup script.
- `src/etl_pipeline.py`: Python ETL pipeline script.
- `sql/setup_sql.sql`: SQL DDL and Insert statements.
- `data/reviews_export.json`: Exported JSON of the MongoDB collection.
- `data/shop.db`: SQLite database.
- `visualizations/`: Generated output graphs.
- `Project_Report.md`: Comprehensive project report.

_(For the PDF requirement of the report, export `Project_Report.md` to PDF using a markdown viewer or browser)._
