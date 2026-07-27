import aiosqlite

DB_NAME = "tires.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS tires (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            size TEXT NOT NULL,
            dot TEXT,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
        """)
        await db.commit()


async def add_tire(brand, model, size, dot, price, quantity):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO tires
            (brand, model, size, dot, price, quantity)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (brand, model, size, dot, price, quantity)
        )
        await db.commit()


async def get_all_tires():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
        SELECT id, brand, model, size, dot, price, quantity
        FROM tires
        """)
        return await cursor.fetchall()
