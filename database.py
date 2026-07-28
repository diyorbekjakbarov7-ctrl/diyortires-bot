import sqlite3

DB_NAME = "warehouse.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            action TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def add_product(name, price, quantity):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO products (name, price, quantity)
        VALUES (?, ?, ?)
        """,
        (name, price, quantity)
    )

    product_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO history (product_id, action, quantity)
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
        "SELECT * FROM products ORDER BY id DESC"
    )

    products = cursor.fetchall()

    conn.close()

    return products


def sell_product(name, quantity):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM products
        WHERE name = ?
        """,
        (name,)
    )

    product = cursor.fetchone()

    if not product:
        conn.close()
        return False, "Tovar topilmadi"


    if product["quantity"] < quantity:
        conn.close()
        return False, "Omborda yetarli emas"


    new_quantity = product["quantity"] - quantity


    cursor.execute(
        """
        UPDATE products
        SET quantity = ?
        WHERE id = ?
        """,
        (new_quantity, product["id"])
    )


    cursor.execute(
        """
        INSERT INTO history
        (product_id, action, quantity)
        VALUES (?, ?, ?)
        """,
        (product["id"], "SELL", quantity)
    )


    conn.commit()
    conn.close()


    return True, new_quantity