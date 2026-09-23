from datetime import datetime
import hashlib
import sqlite3

DB_NAME = "agrichain.db"


def get_connection():
    """Membuka sambungan ke pangkalan data SQLite."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password):
    """Fungsi keselamatan untuk menukar kata laluan teks kepada format SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():
    """Membinakan jadual-jadual utama dan data asas (seed data) jika belum wujud."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Jadual Pengguna (Users & Roles)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'farmer'
        )
    """)

    # 2. Jadual Komoditi Pertanian
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS commodities (
            commodity_id INTEGER PRIMARY KEY AUTOINCREMENT,
            commodity_name TEXT NOT NULL,
            unit TEXT NOT NULL
        )
    """)

    # 3. Jadual Pembekal & Sejarah Harga
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            price_id INTEGER PRIMARY KEY AUTOINCREMENT,
            commodity_id INTEGER,
            source TEXT NOT NULL,
            location TEXT NOT NULL,
            market_level TEXT NOT NULL,
            price REAL NOT NULL,
            unit TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (commodity_id) REFERENCES commodities(commodity_id)
        )
    """)

    # 4. Jadual Kawalan Inventori
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            min_threshold REAL NOT NULL
        )
    """)

    # 5. Jadual Transaksi Kewangan (Mengandungi kolum user_id)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            trans_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    # Seed Data 1: Akaun Pengguna Default (Jika jadual kosong)
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", hash_password("admin123"), "admin"),
        )
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("petani", hash_password("petani123"), "farmer"),
        )
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("pembekal", hash_password("pembekal123"), "supplier"),
        )

    # Seed Data 2: Komoditi Asas FAMA
    cursor.execute("SELECT COUNT(*) FROM commodities")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO commodities (commodity_name, unit) VALUES (?, ?)",
            [
                ("CILI MERAH", "kg"),
                ("TOMAT", "kg"),
                ("KACANG BENDI", "kg"),
                ("BAWANG MERAH", "kg"),
                ("UREA FERTILIZER", "Bag"),
            ],
        )

    # Seed Data 3: Rekod Penawaran Pembekal
    cursor.execute("SELECT COUNT(*) FROM price_history")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            """
            INSERT INTO price_history (commodity_id, source, location, market_level, price, unit, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            [
                (
                    1,
                    "Cili Cameron Enterprise",
                    "Pahang",
                    "Borong",
                    14.50,
                    "kg",
                    "2026-03-01",
                ),
                (
                    1,
                    "Pembekal Cili Penang",
                    "Penang",
                    "Runcit",
                    19.50,
                    "kg",
                    "2026-03-01",
                ),
                (
                    2,
                    "Tomato Supply Cameron",
                    "Pahang",
                    "Borong",
                    5.80,
                    "kg",
                    "2026-03-01",
                ),
                (
                    5,
                    "Agro Chemical Penang",
                    "Penang",
                    "Borong",
                    155.00,
                    "Bag",
                    "2026-03-01",
                ),
                (
                    5,
                    "Kedah Agro Farm",
                    "Kedah",
                    "Runcit",
                    168.00,
                    "Bag",
                    "2026-03-01",
                ),
            ],
        )

    # Seed Data 4: Item Inventori
    cursor.execute("SELECT COUNT(*) FROM inventory")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            """
            INSERT INTO inventory (item_name, quantity, unit, min_threshold)
            VALUES (?, ?, ?, ?)
        """,
            [
                ("Baja NPK 15-15-15", 4.0, "Bag", 10.0),
                ("Racun Serangga", 12.0, "Liter", 5.0),
                ("Benih Cili Merah", 2.0, "Peket", 5.0),
            ],
        )

    # Seed Data 5: Transaksi Kewangan Asas (Dikaitkan kepada user_id = 2 [petani])
    cursor.execute("SELECT COUNT(*) FROM transactions")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            """
            INSERT INTO transactions (user_id, type, category, amount, description, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            [
                (
                    2,
                    "Expense",
                    "Pembelian Baja",
                    310.00,
                    "Beli 2 Bag Baja Urea",
                    "2026-03-02",
                ),
                (
                    2,
                    "Revenue",
                    "Jualan Hasil",
                    1200.00,
                    "Jualan 80kg Cili Merah",
                    "2026-03-05",
                ),
            ],
        )

    conn.commit()
    conn.close()


# --- FUNGSI AUTENTIKASI ---


def verify_user(username, password):
    """Memeriksa maklumat log masuk pengguna."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, hash_password(password)),
    )
    user = cursor.fetchone()
    conn.close()
    return user


def register_user(username, password, role="farmer"):
    """Mendaftarkan pengguna baharu berserta peranannya."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hash_password(password), role),
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


# --- FUNGSI KOMODITI & HARGA ---


def get_all_commodities():
    """Mengambil senarai semua komoditi pertanian."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM commodities ORDER BY commodity_name ASC")
    res = cursor.fetchall()
    conn.close()
    return res


def get_supplier_prices(commodity_id):
    """Mengambil tawaran harga pembekal mengikut komoditi yang dipilih."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT source as supplier_name, location, market_level, price, unit,"
        " date FROM price_history WHERE commodity_id = ?",
        (commodity_id,),
    )
    res = cursor.fetchall()
    conn.close()
    return res


# --- FUNGSI INVENTORI ---


def get_inventory():
    """Mengambil semua rekod stok inventori."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    res = cursor.fetchall()
    conn.close()
    return res


def add_inventory_item(name, qty, unit, min_thresh):
    """Menambah item baharu ke dalam inventori."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO inventory (item_name, quantity, unit, min_threshold)"
        " VALUES (?, ?, ?, ?)",
        (name, qty, unit, min_thresh),
    )
    conn.commit()
    conn.close()


# --- FUNGSI KEWANGAN (TRANSACTIONS) ---


def get_transactions(user_id=None, role="farmer"):
    """Mengambil rekod kewangan mengikut user_id (atau semua rekod jika peranan admin)."""
    conn = get_connection()
    cursor = conn.cursor()
    if role == "admin":
        cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
    else:
        cursor.execute(
            "SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC",
            (user_id,),
        )
    res = cursor.fetchall()
    conn.close()
    return res


def add_transaction(user_id, t_type, category, amount, desc):
    """Menambah rekod kewangan baharu berserta maklumat ID pengguna."""
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO transactions (user_id, type, category, amount,"
        " description, date) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, t_type, category, amount, desc, today),
    )
    conn.commit()
    conn.close()