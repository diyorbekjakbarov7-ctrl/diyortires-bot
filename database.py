import aiosqlite
from datetime import datetime

DB_NAME = "warehouse.db"


class Database:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name

    async def connect(self):
        return await aiosqlite.connect(self.db_name)

    async def create_tables(self):
        async with await self.connect() as db:

            await db.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                full_name TEXT,
                phone TEXT,
                created_at TEXT
            )
            """)

            await db.execute("""
            CREATE TABLE IF NOT EXISTS admins(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE
            )
            """)

            await db.execute("""
            CREATE TABLE IF NOT EXISTS categories(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
            """)

            await db.execute("""
            CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER,
                brand TEXT,
                model TEXT,
                size TEXT,
                season TEXT,
                price REAL,
                quantity INTEGER,
                description TEXT,
                FOREIGN KEY(category_id)
                REFERENCES categories(id)
            )
            """)

            await db.execute("""
            CREATE TABLE IF NOT EXISTS orders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                total REAL,
                status TEXT,
                created_at TEXT
            )
            """)

            await db.execute("""
            CREATE TABLE IF NOT EXISTS order_items(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                price REAL
            )
            """)

            await db.commit()
                async def add_user(self, telegram_id, full_name):
        async with await self.connect() as db:
            await db.execute("""
            INSERT OR IGNORE INTO users(
                telegram_id,
                full_name,
                created_at
            )
            VALUES(?,?,?)
            """, (
                telegram_id,
                full_name,
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ))
            await db.commit()

    async def update_phone(self, telegram_id, phone):
        async with await self.connect() as db:
            await db.execute("""
            UPDATE users
            SET phone=?
            WHERE telegram_id=?
            """, (phone, telegram_id))
            await db.commit()

    async def get_user(self, telegram_id):
        async with await self.connect() as db:
            cursor = await db.execute("""
            SELECT * FROM users
            WHERE telegram_id=?
            """, (telegram_id,))
            return await cursor.fetchone()

    async def get_users_count(self):
        async with await self.connect() as db:
            cursor = await db.execute("""
            SELECT COUNT(*) FROM users
            """)
            result = await cursor.fetchone()
            return result[0]
                # ==========================
    # CATEGORY CRUD
    # ==========================

    async def add_category(self, name: str):
        async with await self.connect() as db:
            await db.execute("""
                INSERT OR IGNORE INTO categories(name)
                VALUES(?)
            """, (name,))
            await db.commit()

    async def get_categories(self):
        async with await self.connect() as db:
            cursor = await db.execute("""
                SELECT id, name
                FROM categories
                ORDER BY name
            """)
            return await cursor.fetchall()

    async def get_category(self, category_id: int):
        async with await self.connect() as db:
            cursor = await db.execute("""
                SELECT id, name
                FROM categories
                WHERE id=?
            """, (category_id,))
            return await cursor.fetchone()

    async def get_category_by_name(self, name: str):
        async with await self.connect() as db:
            cursor = await db.execute("""
                SELECT id, name
                FROM categories
                WHERE name=?
            """, (name,))
            return await cursor.fetchone()

    async def update_category(self, category_id: int, new_name: str):
        async with await self.connect() as db:
            await db.execute("""
                UPDATE categories
                SET name=?
                WHERE id=?
            """, (new_name, category_id))
            await db.commit()

    async def delete_category(self, category_id: int):
        async with await self.connect() as db:
            await db.execute("""
                DELETE FROM categories
                WHERE id=?
            """, (category_id,))
            await db.commit()

    async def category_exists(self, category_id: int) -> bool:
        async with await self.connect() as db:
            cursor = await db.execute("""
                SELECT 1
                FROM categories
                WHERE id=?
            """, (category_id,))
            return await cursor.fetchone() is not None

    async def get_categories_count(self):
        async with await self.connect() as db:
            cursor = await db.execute("""
                SELECT COUNT(*)
                FROM categories
            """)
            result = await cursor.fetchone()
            return result[0]
                # ==========================
    # PRODUCTS CRUD
    # ==========================

    async def add_product(
        self,
        category_id: int,
        brand: str,
        model: str,
        size: str,
        season: str,
        price: float,
        quantity: int,
        description: str = ""
    ):
        async with await self.connect() as db:
            await db.execute("""
                INSERT INTO products(
                    category_id,
                    brand,
                    model,
                    size,
                    season,
                    price,
                    quantity,
                    description
                )
                VALUES(?,?,?,?,?,?,?,?)
            """, (
                category_id,
                brand,
                model,
                size,
                season,
                price,
                quantity,
                description
            ))
            await db.commit()


    async def get_products(self):
        async with await self.connect() as db:
            cursor = await db.execute("""
                SELECT
                    p.id,
                    c.name,
                    p.brand,
                    p.model,
                    p.size,
                    p.season,
                    p.price,
                    p.quantity,
                    p.description
                FROM products p
                LEFT JOIN categories c
                ON c.id = p.category_id
                ORDER BY p.id DESC
            """)
            return await cursor.fetchall()


    async def get_product(self, product_id: int):
        async with await self.connect() as db:
            cursor = await db.execute("""
                SELECT *
                FROM products
                WHERE id=?
            """, (product_id,))
            return await cursor.fetchone()


    async def get_products_by_category(self, category_id: int):
        async with await self.connect() as db:
            cursor = await db.execute("""
                SELECT *
                FROM products
                WHERE category_id=?
                ORDER BY brand
            """, (category_id,))
            return await cursor.fetchall()


    async def search_by_size(self, size: str):
        async with await self.connect() as db:
            cursor = await db.execute("""
                SELECT *
                FROM products
                WHERE size LIKE ?
                ORDER BY brand
            """, (f"%{size}%",))
            return await cursor.fetchall()


    async def update_product(
        self,
        product_id: int,
        category_id: int,
        brand: str,
        model: str,
        size: str,
        season: str,
        price: float,
        quantity: int,
        description: str
    ):
        async with await self.connect() as db:
            await db.execute("""
                UPDATE products
                SET
                    category_id=?,
                    brand=?,
                    model=?,
                    size=?,
                    season=?,
                    price=?,
                    quantity=?,
                    description=?
                WHERE id=?
            """, (
                category_id,
                brand,
                model,
                size,
                season,
                price,
                quantity,
                description,
                product_id
            ))
            await db.commit()


    async def update_quantity(
        self,
        product_id: int,
        quantity: int
    ):
        async with await self.connect() as db:
            await db.execute("""
                UPDATE products
                SET quantity=?
                WHERE id=?
            """, (quantity, product_id))
            await db.commit()


    async def decrease_quantity(
        self,
        product_id: int,
        amount: int
    ):
        async with await self.connect() as db:
            await db.execute("""
                UPDATE products
                SET quantity = quantity - ?
                WHERE id=?
            """, (amount, product_id))
            await db.commit()


    async def delete_product(self, product_id: int):
        async with await self.connect() as db:
            await db.execute("""
                DELETE FROM products
                WHERE id=?
            """, (product_id,))
            await db.commit()


    async def get_products_count(self):
        async with await self.connect() as db:
            cursor = await db.execute("""
                SELECT COUNT(*)
                FROM products
            """)
            result = await cursor.fetchone()
            return result[0]


    async def low_stock_products(self, limit: int = 5):
        async with await self.connect() as db:
            cursor = await db.execute("""
                SELECT
                    id,
                    brand,
                    model,
                    quantity
                FROM products
                WHERE quantity<=?
                ORDER BY quantity ASC
            """, (limit,))
            return await cursor.fetchall()
                # ==========================
    # ORDERS
    # ==========================

    async def create_order(self, user_id: int, total: float):
        async with await self.connect() as db:
            cursor = await db.execute("""
                INSERT INTO orders(
                    user_id,
                    total,
                    status,
                    created_at
                )
                VALUES(?,?,?,?)
            """, (
                user_id,
                total,
                "Yangi",
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ))

            await db.commit()
            return cursor.lastrowid


    async def add_order_item(
        self,
        order_id: int,
        product_id: int,
        quantity: int,
        price: float
    ):
        async with await self.connect() as db:
            await db.execute("""
                INSERT INTO order_items(
                    order_id,
                    product_id,
                    quantity,
                    price
                )
                VALUES(?,?,?,?)
            """, (
                order_id,
                product_id,
                quantity,
                price
            ))

            await db.commit()


    async def get_orders(self):
        async with await self.connect() as db:
            cursor = await db.execute("""
                SELECT *
                FROM orders
                ORDER BY id DESC
            """)
            return await cursor.fetchall()


    async def get_order(self, order_id: int):
        async with await self.connect() as db:
            cursor = await db.execute("""
                SELECT *
                FROM orders
                WHERE id=?
            """, (order_id,))
            return await cursor.fetchone()


    async def get_order_items(self, order_id: int):
        async with await self.connect() as db:
            cursor = await db.execute("""
                SELECT
                    oi.product_id,
                    p.brand,
                    p.model,
                    p.size,
                    oi.quantity,
                    oi.price
                FROM order_items oi
                JOIN products p
                    ON p.id = oi.product_id
                WHERE oi.order_id=?
            """, (order_id,))
            return await cursor.fetchall()


    async def update_order_status(
        self,
        order_id: int,
        status: str
    ):
        async with await self.connect() as db:
            await db.execute("""
                UPDATE orders
                SET status=?
                WHERE id=?
            """, (status, order_id))

            await db.commit()


    # ==========================
    # STATISTICS
    # ==========================

    async def get_total_income(self):
        async with await self.connect() as db:
            cursor = await db.execute("""
                SELECT COALESCE(SUM(total),0)
                FROM orders
                WHERE status='Yakunlandi'
            """)
            result = await cursor.fetchone()
            return result[0]


    async def get_orders_count(self):
        async with await self.connect() as db:
            cursor = await db.execute("""
                SELECT COUNT(*)
                FROM orders
            """)
            result = await cursor.fetchone()
            return result[0]


    async def get_completed_orders(self):
        async with await self.connect() as db:
            cursor = await db.execute("""
                SELECT COUNT(*)
                FROM orders
                WHERE status='Yakunlandi'
            """)
            result = await cursor.fetchone()
            return result[0]


    async def get_top_products(self, limit: int = 10):
        async with await self.connect() as db:
            cursor = await db.execute("""
                SELECT
                    p.brand,
                    p.model,
                    p.size,
                    SUM(oi.quantity) AS sold
                FROM order_items oi
                JOIN products p
                    ON p.id = oi.product_id
                GROUP BY oi.product_id
                ORDER BY sold DESC
                LIMIT ?
            """, (limit,))
            return await cursor.fetchall()