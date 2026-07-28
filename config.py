import os
import logging

# ==========================
# BOT CONFIG
# ==========================

# Render Environment Variable
BOT_TOKEN = os.getenv("BOT_TOKEN", "TOKENINGIZNI_BU_YERGA_YOZING")

# Admin ID lar (vergul bilan ajratiladi)
# Render'da:
# ADMIN_IDS=123456789,987654321
_admins = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [
    int(admin.strip())
    for admin in _admins.split(",")
    if admin.strip().isdigit()
]

# SQLite Database
DATABASE_NAME = os.getenv("DATABASE_NAME", "warehouse.db")

# ==========================
# LOGGING
# ==========================

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("TireWarehouseBot")

# ==========================
# BOT SETTINGS
# ==========================

BOT_NAME = "Shina Ombori Bot"

DEFAULT_ORDER_STATUS = "Yangi"

LOW_STOCK_LIMIT = 5

CURRENCY = "so'm"

SEARCH_LIMIT = 20

# ==========================
# TEXTS
# ==========================

START_TEXT = (
    "👋 Assalomu alaykum!\n\n"
    "Shina Ombori botiga xush kelibsiz.\n"
    "Kerakli bo'limni tanlang."
)

ADMIN_TEXT = (
    "🛠 Admin paneliga xush kelibsiz."
)

CONTACT_TEXT = (
    "📞 Telefon raqamingizni yuboring."
)