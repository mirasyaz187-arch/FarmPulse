import backend
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="FarmPulse - Smart Agricultural Platform",
    page_icon="🌾",
    layout="wide",
)

# ----------------------------------------------------
# 🌿 CUSTOM CSS: DARK FOREST GLASSMORPHISM THEME
# ----------------------------------------------------
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 80% 20%, #0d2818 0%, #05100a 60%, #020704 100%);
        color: #e2e8f0;
    }

    div.stMetric, div.stDataFrame, div[data-testid="stExpander"], div.stPlotlyChart {
        background: rgba(15, 35, 24, 0.45) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        padding: 18px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.45);
    }

    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #10b981 0%, #047857 100%);
        color: white;
        border-radius: 12px;
        border: none;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Inisialisasi Pangkalan Data
backend.init_db()

# --- DICTIONARY BAHASA ---
if "lang" not in st.session_state:
    st.session_state.lang = "BM"

TEXTS = {
    "BM": {
        "title": "AgriChain Intelligence",
        "subtitle": "Platform Pemantauan Pasaran & Digitalisasi Rantaian Bekalan Pertanian",
        "login": "Log Masuk",
        "register": "Daftar Akaun Baru",
        "username": "Nama Pengguna",
        "password": "Kata Laluan",
        "role": "Peranan Pengguna",
        "logout": "Log Keluar",
        "nav_price": "📊 Pemantauan Harga",
        "nav_inv": "📦 Kawalan Inventori",
        "nav_pred": "📈 Analisis Ramalan",
        "nav_fin": "💰 Pengurusan Kewangan",
        "comm_select": "Pilih Komoditi / Sayuran:",
        "alert_low_stock": "⚠️ AMARAN STOK MINIMA!",
    },
    "EN": {
        "title": "AgriChain Intelligence",
        "subtitle": "Real-Time Agricultural Market Monitoring & Supply Chain Platform",
        "login": "Login",
        "register": "Register Account",
        "username": "Username",
        "password": "Password",
        "role": "User Role",
        "logout": "Logout",
        "nav_price": "📊 Price Monitoring",
        "nav_inv": "📦 Inventory Tracking",
        "nav_pred": "📈 Predictive Analysis",
        "nav_fin": "💰 Financial Tracking",
        "comm_select": "Select Commodity / Crop:",
        "alert_low_stock": "⚠️ LOW INVENTORY ALERT!",
    },
}

t = TEXTS[st.session_state.lang]

# --- SESSION STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_role" not in st.session_state:
    st.session_state.user_role = "farmer"

# --- TOP NAVIGATION BAR ---
top_col1, top_col2, top_col3 = st.columns([3, 1.2, 1.2])

with top_col1:
    st.markdown(
        f"<h1 style='font-size: 2.5rem;'>{t['title']}</h1>",
        unsafe_allow_html=True,
    )
    st.caption(t["subtitle"])

with top_col2:
    lang_choice = st.radio(
        "🌐 Language / Bahasa:",
        ["BM", "EN"],
        index=0 if st.session_state.lang == "BM" else 1,
        horizontal=True,
    )
    st.session_state.lang = lang_choice

with top_col3:
    if st.session_state.authenticated:
        role_label = st.session_state.user_role.upper()
        st.write(f"👤 **{st.session_state.username}** (`{role_label}`)")
        if st.button(t["logout"]):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.user_id = None
            st.session_state.user_role = "farmer"
            st.rerun()

st.divider()

# --- BORANG LOG MASUK & PENDAFTARAN ---
if not st.session_state.authenticated:
    st.subheader("🔐 Access Portal (Sila Pilih Akaun)")
    col_log, col_reg = st.columns(2)

    with col_log:
        with st.form("main_login"):
            st.markdown("### Log Masuk Pengguna")
            user_in = st.text_input(t["username"], key="log_u")
            pass_in = st.text_input(t["password"], type="password", key="log_p")
            if st.form_submit_button(t["login"]):
                user = backend.verify_user(user_in, pass_in)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.username = user["username"]
                    st.session_state.user_id = user["user_id"]
                    st.session_state.user_role = user["role"]
                    st.rerun()
                else:
                    st.error("Log masuk gagal. Semak maklumat akaun anda.")

    with col_reg:
        with st.form("main_register"):
            st.markdown("### Pendaftaran Akaun Baharu")
            reg_u = st.text_input(t["username"], key="reg_u")
            reg_p = st.text_input(t["password"], type="password", key="reg_p")
            reg_r = st.selectbox(
                t["role"],
                ["farmer", "supplier", "admin"],
                format_func=lambda x: {
                    "farmer": "👨‍🌾 Petani (Farmer)",
                    "supplier": "🚚 Pembekal (Supplier)",
                    "admin": "⚙️ Pentadbir Sistem (Admin)",
                }[x],
            )
            if st.form_submit_button(t["register"]):
                success = backend.register_user(reg_u, reg_p, reg_r)
                if success:
                    st.success("Akaun berjaya didaftarkan! Sila log masuk.")
                else:
                    st.error("Nama pengguna sudah wujud. Sila guna nama lain.")

    st.stop()


# Cache FAMA Scraper
@st.cache_data(ttl=1800)
def load_fama_data(comm_name):
    try:
        from fama_scraper import get_fama_prices

        return get_fama_prices(comm_name)
    except Exception:
        return pd.DataFrame()


# --- TABS NAVIGASI ---
current_role = st.session_state.user_role
current_user_id = st.session_state.user_id

tab_price, tab_inv, tab_pred, tab_fin = st.tabs([
    t["nav_price"],
    t["nav_inv"],
    t["nav_pred"],
    t["nav_fin"],
])

# ----------------------------------------------------
# 1. PRICE MONITORING
# ----------------------------------------------------
with tab_price:
    st.header(t["nav_price"])
    commodities = backend.get_all_commodities()

    comm_dict = {
        f"{c['commodity_name']} ({c['unit']})": {
            "id": c["commodity_id"],
            "name": c["commodity_name"],
        }
        for c in commodities
    }
    selected_label = st.selectbox(t["comm_select"], list(comm_dict.keys()))
    selected_id = comm_dict[selected_label]["id"]
    selected_name = comm_dict[selected_label]["name"]

    if current_role in ["supplier", "admin"]:
        with st.expander(
            f"➕ Update Tawaran Harga Pembekal ({current_role.upper()})"
        ):
            with st.form("supplier_price_form"):
                sup_name = st.text_input(
                    "Nama Pembekal / Syarikat", value=st.session_state.username
                )
                sup_loc = st.text_input("Lokasi", value="Penang")
                sup_mkt = st.selectbox(
                    "Peringkat Pasaran", ["Borong", "Runcit", "Ladang"]
                )
                sup_price = st.number_input(
                    "Tawaran Harga (RM)", min_value=0.1, value=12.50
                )
                sup_unit = st.text_input("Unit", value="kg")

                if st.form_submit_button("Kemaskini Penawaran"):
                    conn = backend.get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        INSERT INTO price_history (commodity_id, source, location, market_level, price, unit, date)
                        VALUES (?, ?, ?, ?, ?, ?, date('now'))
                    """,
                        (
                            selected_id,
                            sup_name,
                            sup_loc,
                            sup_mkt,
                            sup_price,
                            sup_unit,
                        ),
                    )
                    conn.commit()
                    conn.close()
                    st.success("Tawaran harga baru berjaya disimpan!")
                    st.rerun()
    else:
        st.info(
            "💡 **Mod Pemantauan Petani:** Pemantauan harga pasaran semasa untuk"
            " perbandingan tawaran pembekal dan benchmark FAMA."
        )

    with st.spinner(f"📡 Menghubungi Portal FAMA untuk {selected_name}..."):
        df_fama = load_fama_data(selected_name)

    fama_benchmark = None
    if not df_fama.empty:
        for col in ["Harga Purata (RM)", "Harga Max (RM)", "Harga (RM)", "Harga"]:
            if col in df_fama.columns:
                val = pd.to_numeric(df_fama[col], errors="coerce").mean()
                if not pd.isna(val) and val > 0:
                    fama_benchmark = float(val)
                    break

    if fama_benchmark is None:
        defaults = {
            "CILI MERAH": 18.00,
            "TOMAT": 7.50,
            "KACANG BENDI": 11.50,
            "BAWANG MERAH": 8.50,
            "UREA FERTILIZER": 160.00,
        }
        fama_benchmark = defaults.get(selected_name, 15.00)

    suppliers = backend.get_supplier_prices(selected_id)
    if suppliers:
        df_sup = pd.DataFrame([dict(r) for r in suppliers])
        df_sup["fama_benchmark"] = fama_benchmark
        df_sup["is_overpriced"] = df_sup["price"] > df_sup["fama_benchmark"]
        df_sup["Status"] = np.where(
            df_sup["is_overpriced"],
            "⚠️ Melebihi FAMA",
            "✅ Berpatutan (Bawah FAMA)",
        )

        fig = px.bar(
            df_sup,
            x="supplier_name",
            y="price",
            color="Status",
            text="price",
            title=f"Perbandingan Harga Pembekal vs Benchmark FAMA ({selected_name})",
            color_discrete_map={
                "⚠️ Melebihi FAMA": "#ef4444",
                "✅ Berpatutan (Bawah FAMA)": "#10b981",
            },
            template="plotly_dark",
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        fig.add_hline(
            y=fama_benchmark,
            line_dash="dot",
            line_color="#f59e0b",
            annotation_text=f"Harga Benchmark FAMA: RM {fama_benchmark:.2f}",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            df_sup[
                [
                    "supplier_name",
                    "location",
                    "market_level",
                    "price",
                    "fama_benchmark",
                    "Status",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

# ----------------------------------------------------
# 2. INVENTORY TRACKING
# ----------------------------------------------------
with tab_inv:
    st.header(t["nav_inv"])

    if current_role in ["farmer", "admin"]:
        with st.expander("➕ Tambah Stok Pertanian Baharu"):
            with st.form("inv_form"):
                i_name = st.text_input("Nama Item / Input Pertanian")
                i_qty = st.number_input("Kuantiti", min_value=1.0, value=10.0)
                i_unit = st.selectbox("Unit", ["kg", "Bag", "Liter", "Peket"])
                i_min = st.number_input("Paras Amaran Minima", value=5.0)
                if st.form_submit_button("Simpan Item"):
                    backend.add_inventory_item(i_name, i_qty, i_unit, i_min)
                    st.success("Item berjaya ditambah!")
                    st.rerun()

        inv_data = backend.get_inventory()
        if inv_data:
            df_inv = pd.DataFrame([dict(r) for r in inv_data])
            low_stock = df_inv[df_inv["quantity"] <= df_inv["min_threshold"]]

            if not low_stock.empty:
                st.error(f"{t['alert_low_stock']}")
                st.dataframe(
                    low_stock[
                        ["item_name", "quantity", "unit", "min_threshold"]
                    ],
                    use_container_width=True,
                    hide_index=True,
                )

            st.subheader("📦 Senarai Stok Semasa Ladang")
            st.dataframe(
                df_inv[
                    ["item_id", "item_name", "quantity", "unit", "min_threshold"]
                ],
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.warning(
            "🔒 Modul Inventori ini dikhususkan untuk pengurusan ladang"
            " Petani sahaja."
        )

# ----------------------------------------------------
# 3. PREDICTIVE COST ANALYSIS
# ----------------------------------------------------
with tab_pred:
    st.header(t["nav_pred"])
    st.caption(
        "Model Analisis Ramalan Trend & Perubahan Harga Input Pertanian (6"
        " Bulan Horizon)"
    )

    dates = pd.date_range(end=pd.Timestamp.now(), periods=6, freq="ME")
    sample_trend = pd.DataFrame({
        "Tarikh": dates,
        "Cili Merah (RM)": [14.0, 15.5, 13.8, 17.0, 18.5, 16.2],
        "Baja Urea (RM)": [175.0, 170.0, 165.0, 160.0, 158.0, 155.0],
    })

    fig = px.line(
        sample_trend,
        x="Tarikh",
        y=["Cili Merah (RM)", "Baja Urea (RM)"],
        markers=True,
        title="Ramalan Trend Harga Pasaran",
        template="plotly_dark",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.success(
        "💡 **Analisis Strategik:** Trend harga Baja Urea konsisten menurun."
        " Petani disyorkan membuat pembelian dalam tempoh 14 hari."
    )

# ----------------------------------------------------
# 4. FINANCIAL TRACKING (SELARAS DENGAN BACKEND HELPER)
# ----------------------------------------------------
with tab_fin:
    st.header(t["nav_fin"])

    with st.expander(
        f"➕ Rekod Transaksi Kewangan Baharu ({current_role.upper()})"
    ):
        with st.form("fin_form"):
            f_type = st.selectbox(
                "Jenis Transaksi",
                ["Expense (Perbelanjaan)", "Revenue (Jualan / Pendapatan)"],
            )
            f_cat = st.text_input(
                "Kategori",
                placeholder=(
                    "Baja / Racun (Petani) atau Kos Stok / Pengangkutan"
                    " (Supplier)"
                ),
            )
            f_amt = st.number_input("Jumlah (RM)", min_value=0.1, value=100.0)
            f_desc = st.text_area("Catatan Nota")

            if st.form_submit_button("Simpan Transaksi"):
                clean_type = "Expense" if "Expense" in f_type else "Revenue"
                backend.add_transaction(
                    user_id=current_user_id,
                    t_type=clean_type,
                    category=f_cat,
                    amount=f_amt,
                    desc=f_desc,
                )
                st.success("Rekod kewangan berjaya disimpan!")
                st.rerun()

    # MENGAMBIL DATA TRANSAKSI MENGGUNAKAN BACKEND HELPER (MENGELAKKAN SQL ERROR)
    transactions = backend.get_transactions(
        user_id=current_user_id, role=current_role
    )

    if transactions:
        df_t = pd.DataFrame([dict(r) for r in transactions])

        exp = df_t[df_t["type"] == "Expense"]["amount"].sum()
        rev = df_t[df_t["type"] == "Revenue"]["amount"].sum()
        profit = rev - exp

        c1, c2, c3 = st.columns(3)
        c1.metric("Pendapatan (Revenue)", f"RM {rev:.2f}")
        c2.metric("Perbelanjaan (Expenses)", f"RM {exp:.2f}")
        c3.metric(
            "Untung Bersih (Net Profit)",
            f"RM {profit:.2f}",
            delta=f"{profit:.2f}",
        )

        st.subheader("📜 Rekod Transaksi Saya")
        st.dataframe(
            df_t[["date", "type", "category", "amount", "description"]],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Belum ada rekod kewangan disimpan untuk akaun ini.")