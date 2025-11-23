import sqlite3
import os

db_path = 'data/northwind.sqlite'

if not os.path.exists(db_path):
    print(f"Error: {db_path} not found.")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

views = [
    "CREATE VIEW IF NOT EXISTS orders AS SELECT * FROM Orders;",
    "CREATE VIEW IF NOT EXISTS order_items AS SELECT * FROM \"Order Details\";",
    "CREATE VIEW IF NOT EXISTS products AS SELECT * FROM Products;",
    "CREATE VIEW IF NOT EXISTS customers AS SELECT * FROM Customers;"
]

for view in views:
    try:
        cursor.execute(view)
        print(f"Executed: {view}")
    except Exception as e:
        print(f"Error executing {view}: {e}")

conn.commit()
conn.close()
print("Views created successfully.")
