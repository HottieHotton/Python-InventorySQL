import sqlite3
from datetime import datetime

# Connect to or create the database
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Create tables and seed data if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    category_id INTEGER,
    date_added TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
""")

def seed_data():
    # Check if there are any categories
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        print("Seeding categories...")
        categories = ["Electronics", "Books", "Groceries"]
        for name in categories:
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    
    # Check if there are any items
    cursor.execute("SELECT COUNT(*) FROM items")
    if cursor.fetchone()[0] == 0:
        print("Seeding items...")
        # Get category IDs
        cursor.execute("SELECT id FROM categories WHERE name = 'Electronics'")
        electronics_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM categories WHERE name = 'Books'")
        books_id = cursor.fetchone()[0]

        today = datetime.now().strftime("%Y-%m-%d")
        items = [
            ("Laptop", 5, 999.99, electronics_id, today),
            ("Mouse", 15, 19.99, electronics_id, today),
            ("Python 101", 7, 29.99, books_id, today),
        ]
        cursor.executemany("""
            INSERT INTO items (name, quantity, price, category_id, date_added)
            VALUES (?, ?, ?, ?, ?)
        """, items)
    
    conn.commit()

# Add A Category
def insert_category():
    name = input("Enter category name: ")
    cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    conn.commit()
    print("Category added.")

# Add an Item
def insert_item():
    name = input("Item name: ")
    quantity = int(input("Quantity: "))
    price = float(input("Price: "))
    list_categories()
    category_id = int(input("Category ID: "))
    date_now = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        INSERT INTO items (name, quantity, price, category_id, date_added)
        VALUES (?, ?, ?, ?, ?)
    """, (name, quantity, price, category_id, date_now))
    conn.commit()
    print("Item added.")

# Update an Item
def update_item():
    item_id = int(input("Item ID to update: "))
    new_quantity = int(input("New quantity: "))
    cursor.execute("UPDATE items SET quantity = ? WHERE id = ?", (new_quantity, item_id))
    conn.commit()
    print("Item updated.")

# Delete an Item
def delete_item():
    item_id = int(input("Item ID to delete: "))
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    print("Item deleted.")

# List Inventory
def list_inventory():
    print("\nInventory List (with Categories):")
    cursor.execute("""
        SELECT items.id, items.name, items.quantity, items.price, categories.name
        FROM items
        LEFT JOIN categories ON items.category_id = categories.id
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(f"[{row[0]}] {row[1]} - Qty: {row[2]}, Price: ${row[3]:.2f}, Category: {row[4]}")

# List Categories
def list_categories():
    cursor.execute("SELECT * FROM categories")
    print("\nCategories:")
    for cat in cursor.fetchall():
        print(f"[{cat[0]}] {cat[1]}")

# Filter Items by Date
def filter_by_date():
    start = input("Start date (YYYY-MM-DD): ")
    end = input("End date (YYYY-MM-DD): ")
    cursor.execute("""
        SELECT name, date_added FROM items
        WHERE date(date_added) BETWEEN date(?) AND date(?)
    """, (start, end))
    rows = cursor.fetchall()
    print(f"\nItems added between {start} and {end}:")
    for row in rows:
        print(f"{row[0]} - Added on {row[1]}")

# Show Inventory Summary
def summarize_inventory():
    cursor.execute("SELECT SUM(quantity), AVG(price) FROM items")
    total_qty, avg_price = cursor.fetchone()
    print(f"\nSummary:\nTotal Quantity: {total_qty or 0}, Average Price: ${avg_price or 0:.2f}")

# Command Line Menu
def main_menu():
    while True:
        print("\n==== Inventory Menu ====")
        print("1. Add Category")
        print("2. Add Item")
        print("3. Update Item Quantity")
        print("4. Delete Item")
        print("5. List Inventory")
        print("6. List Categories")
        print("7. Filter Items by Date Range")
        print("8. Show Inventory Summary")
        print("9. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            insert_category()
        elif choice == "2":
            insert_item()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            list_inventory()
        elif choice == "6":
            list_categories()
        elif choice == "7":
            filter_by_date()
        elif choice == "8":
            summarize_inventory()
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid option. Try again.")

    conn.close()

# Run the app
if __name__ == "__main__":
    seed_data()
    main_menu()
