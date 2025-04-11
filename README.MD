# Overview

This application is a simple inventory management system. It allows you to add, update, and delete items in the inventory. It also allows you to filter items by date range. This tool was created for the purpose of increasing my knowledge of Python and SQLite.

# Relational Database

I am utilizing the SQLite relational database to accomplish this task.

I created a database called "inventory.db" with two tables, "categories" and "items". The "categories" table has an "id" and a "name" column. The "items" table has an "id", "name", "quantity", "price", "category_id", and "date_added" column. The "category_id" column is a foreign key that references the "id" column in the "categories" table.

# Development Environment

- Visual Studio Code
- Python 3.12.9
- SQLite 3

# Useful Websites

- [SQLite](https://docs.python.org/3/library/sqlite3.html)
- [Python](https://www.python.org/)

# Future Work

- Have the ability to delete a category and its items
- Allow the user to update any items other than quantity
- Add a "description" column to the "items" table