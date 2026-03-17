DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Products;

-- Customers table
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    registration_date DATE
);

-- Products table
CREATE TABLE IF NOT EXISTS Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
);

-- Orders table
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    order_date DATE,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Insert Customers
INSERT INTO Customers (customer_name, registration_date) VALUES
('Alice Johnson', '2024-01-15'),
('Bob Smith', '2024-02-10'),
('Charlie Brown', '2024-03-05'),
('Diana Prince', '2024-03-20'),
('Ethan Hunt', '2024-04-01'),
('Fiona Gallagher', '2024-04-15'),
('George Miller', '2024-05-02'),
('Hannah Davis', '2024-05-18'),
('Ian Wright', '2024-06-01'),
('Julia Roberts', '2024-06-10');

-- Insert Products
INSERT INTO Products (product_name, category, price) VALUES
('Laptop', 'Electronics', 75000),
('Smartphone', 'Electronics', 45000),
('Headphones', 'Accessories', 3000),
('Office Chair', 'Furniture', 12000),
('Coffee Maker', 'Appliances', 5000);

-- Insert Orders
INSERT INTO Orders (customer_id, product_id, order_date, quantity) VALUES
(1,1,'2024-07-01',1),
(1,3,'2024-07-02',2),
(2,2,'2024-07-03',1),
(2,5,'2024-07-04',1),
(3,4,'2024-07-05',1),
(3,1,'2024-07-06',1),
(4,2,'2024-07-07',2),
(4,3,'2024-07-08',1),
(5,5,'2024-07-09',1),
(5,1,'2024-07-10',1),
(6,2,'2024-07-11',1),
(6,4,'2024-07-12',1),
(7,3,'2024-07-13',3),
(7,5,'2024-07-14',1),
(8,1,'2024-07-15',1),
(8,2,'2024-07-16',1),
(9,4,'2024-07-17',2),
(9,3,'2024-07-18',1),
(10,5,'2024-07-19',1),
(10,2,'2024-07-20',1);