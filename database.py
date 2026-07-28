import sqlite3
import os

DB_FOLDER = "data"
DB_NAME = os.path.join(DB_FOLDER, "warehouse.db")


def get_connection():
    os.makedirs(DB_FOLDER, exist_ok=True)

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Mahsulotlar
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tarix
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            action TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)

    conn.commit()
    conn.close()


def add_product(name, price, quantity):
    conn = get_connection()
    cursor = conn.cursor()

    # Mahsulot mavjudmi?
    cursor.execute(
        "SELECT * FROM products WHERE name=?",
        (name,)
    )

    product = cursor.fetchone()

    if product:
        new_quantity = product["quantity"] + quantity

        cursor.execute(
            """
            UPDATE products
            SET
                price=?,
                quantity=?
            WHERE id=?
            """,
            (price, new_quantity, product["id"])
        )

        product_id = product["id"]

    else:
        cursor.execute(
            """
            INSERT INTO products
            (name, price, quantity)
            VALUES (?, ?, ?)
            """,
            (name, price, quantity)
        )

        product_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO history
        (product_id, action, quantity)
        VALUES (?, ?, ?)
        """,
        (product_id, "ADD", quantity)
    )

    conn.commit()
    conn.close()


def get_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM products
        ORDER BY name
        """
    )

    products = cursor.fetchall()

    conn.close()

    return products