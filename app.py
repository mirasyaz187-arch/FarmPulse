import builtins
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import sys


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Farm Pulse",
    layout="wide",
    initial_sidebar_state="expanded"  # <-- Pastikan "expanded"
)


# =========================================================
# CONFIGURATION
# =========================================================

BASE_URL = "http://127.0.0.1:8000"


# =========================================================
# LOAD CSS
# =========================================================
def load_css():
    try:
        with open("style.css", "r", encoding="utf-8") as f:
            css = f.read()

        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True
        )

    except OSError:
        st.warning(
            "style.css not found. "
            "Please make sure style.css is in the same folder as app.py."
        )


load_css()


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"


# =========================================================
# LANGUAGE TRANSLATIONS
# =========================================================

if "language" not in st.session_state:
    st.session_state.language = "English"

translations = {
    "English": {
        "nav_dashboard": "Dashboard",
        "nav_price": "Price Monitoring",
        "nav_fertilizer": "Fertilizer Prices",
        "nav_inventory": "Inventory",
        "total_commodities": "Total Commodities",
        "inventory_items": "Inventory Items",
        "low_stock": "Low Stock",
        "api_status": "FarmPulse API",
    },
    "Malay": {
        "nav_dashboard": "Papan Pemuka",
        "nav_price": "Pemantauan Harga",
        "nav_fertilizer": "Harga Baja",
        "nav_inventory": "Inventori",
        "total_commodities": "Jumlah Komoditi",
        "inventory_items": "Item Inventori",
        "low_stock": "Stok Rendah",
        "api_status": "API FarmPulse",
    }
}

def t(key):
    lang = st.session_state.get("language", "English")
    return translations.get(lang, translations["English"]).get(key, key)


# =========================================================
# API HELPER FUNCTIONS
# =========================================================

def api_get(endpoint, params=None):

    try:

        response = requests.get(
            BASE_URL + endpoint,
            params=params,
            timeout=15
        )

        if response.status_code == 200:

            return response.json()

        return None

    except Exception:

        return None


def api_post(endpoint, data):

    try:

        response = requests.post(
            BASE_URL + endpoint,
            json=data,
            timeout=15
        )

        if response.status_code == 200:

            return response.json()

        return None

    except Exception:

        return None


# =========================================================
# LOGIN PAGE
# =========================================================

# =========================================================
# LOGIN PAGE (SPLIT SCREEN)
# =========================================================
def login_page():

    st.markdown('<div class="login-spacer"></div>', unsafe_allow_html=True)

    left, right = st.columns([1.15, 0.85], gap="large")

    # =========================
    # LEFT SIDE
    # =========================
    with left:

        st.markdown("""
        <div class="auth-image">
        <div class="auth-image-content">

        <div class="auth-brand">
                    🌱 FARMPULSE
        </div>

        <h1 class="auth-image-title">
                    Smart Farming,<br>
                    Better Harvest.
        </h1>

        <p class="auth-image-description">
                    Monitor your farm, track important data,
                    and make smarter agricultural decisions
                    with FarmPulse.
        </p>

        <div class="auth-feature">
                    🌱
        <span class="auth-feature-text">
                        Smart Agricultural Monitoring
        </span>
        </div>

        <div class="auth-feature">
                    📊
        <span class="auth-feature-text">
                        Real-time Farm Data
        </span>
        </div>

        <div class="auth-feature">
                    🤖
        <span class="auth-feature-text">
                        Intelligent Farm Insights
        </span>
        </div>

        </div>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # RIGHT SIDE
    # =========================
    with right:

        st.markdown("""
        <div class="auth-header">

        <div class="auth-welcome">
                Welcome Back
        </div>

        <h2 class="auth-title">
                Login to FarmPulse
        </h2>

        <p class="auth-description">
                Access your agricultural monitoring dashboard.
        </p>

        </div>
        """, unsafe_allow_html=True)

        phone = st.text_input(
            "Phone Number",
            placeholder="Enter your phone number"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        remember = st.checkbox("Remember me")

        if st.button(
            "Login",
            type="primary",
            use_container_width=True
        ):

            if not phone or not password:
                st.warning(
                    "Please enter your phone number and password."
                )

            else:

                result = api_post(
                    "/api/auth/login",
                    {
                        "phone": phone.strip(),
                        "password": password
                    }
                )

                if result:

                    st.session_state.logged_in = True
                    st.session_state.user = result.get(
                        "user", {}
                    )

                    st.session_state.page = "Dashboard"

                    st.rerun()

        st.markdown("""
        <div class="auth-switch-text">
            Don't have an account?
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Create New Account",
            use_container_width=True
        ):
            st.session_state.auth_page = "register"
            st.rerun()

        st.markdown("""
        <div class="auth-footer">
            © 2026 FarmPulse · Smart Agricultural Monitoring
        </div>
        """, unsafe_allow_html=True) 

def register_page():

    st.markdown('<div class="login-spacer"></div>', unsafe_allow_html=True)

    left, right = st.columns([1.15, 0.85], gap="large")

    # =========================
    # LEFT SIDE
    # =========================
    with left:

        st.markdown("""
        <div class="auth-image">
        <div class="auth-image-content">

        <div class="auth-brand">
                    🌱 FARMPULSE
        </div>

        <h1 class="auth-image-title">
                    Grow Smarter,<br>
                    Farm Better.
        </h1>

        <p class="auth-image-description">
                    Join FarmPulse and simplify the way
                    you monitor and manage your agricultural
                    activities.
        </p>

        <div class="auth-feature">
                    🌱
        <span class="auth-feature-text">
                        Smart Agricultural Monitoring
        </span>
        </div>

        <div class="auth-feature">
                    📊
        <span class="auth-feature-text">
                        Track Your Farm Data
        </span>
        </div>

        <div class="auth-feature">
                    🤖
        <span class="auth-feature-text">
                        Make Data-driven Decisions
        </span>
        </div>

        </div>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # RIGHT SIDE
    # =========================
    with right:

        st.markdown("""
        <div class="auth-header">

        <div class="auth-welcome">
                Get Started
        </div>

        <h2 class="auth-title">
                Create Account
        </h2>

        <p class="auth-description">
                Create your FarmPulse account to get started.
        </p>

        </div>
        """, unsafe_allow_html=True)

        name = st.text_input(
            "Full Name",
            placeholder="Enter your full name"
        )

        phone = st.text_input(
            "Phone Number",
            placeholder="Enter your phone number"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm your password"
        )

        role = st.selectbox(
            "Role",
            ["Farmer", "Admin"]
        )

        if st.button(
            "Create Account",
            type="primary",
            use_container_width=True
        ):

            if not name or not phone or not password or not confirm_password:

                st.warning(
                    "Please fill in all fields."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                result = api_post(
                    "/api/auth/register",
                    {
                        "name": name.strip(),
                        "phone": phone.strip(),
                        "password": password,
                        "role": role.lower()
                    }
                )

                if result:

                    st.success(
                        "Account created successfully!"
                    )

                    st.session_state.auth_page = "login"

                    st.rerun()

        st.markdown("""
        <div class="auth-switch-text">
            Already have an account?
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Back to Login",
            use_container_width=True
        ):

            st.session_state.auth_page = "login"
            st.rerun()

        st.markdown("""
        <div class="auth-footer">
            © 2026 FarmPulse · Smart Agricultural Monitoring
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

def sidebar():

    user = st.session_state.get("user")

    if not user:
        return

    user_name = user.get(
        "name",
        "User"
    )

    user_role = str(
        user.get(
            "role",
            "farmer"
        )
    ).lower()

    with st.sidebar:

        st.markdown(
            """
            <div style="
                text-align:center;
                padding:10px 0 20px 0;
            ">

            <div style="
                    font-size:42px;
            ">
                    🌱
            </div>

            <div style="
                    font-size:26px;
                    font-weight:700;
                    color:#166534;
            ">
                    FarmPulse
            </div>

            <div style="
                    color:#64748b;
                    font-size:13px;
            ">
                    Smart Agricultural Monitoring
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        st.markdown(
            f"""
            <div style="
                background:#f0fdf4;
                border:1px solid #bbf7d0;
                padding:14px;
                border-radius:12px;
                margin-bottom:15px;
            ">

            <div style="
                    font-size:14px;
                    color:#64748b;
            ">
                    Signed in as
            </div>

            <div style="
                    font-size:17px;
                    font-weight:600;
                    color:#166534;
            ">
                    {user_name}
            </div>

            <div style="
                    font-size:13px;
                    color:#64748b;
                    margin-top:3px;
            ">
                    Role: {user_role.title()}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # =================================================
        # ROLE-BASED MENU
        # =================================================

        # =================================================
        # ROLE-BASED MENU (DENGAN SOKONGAN BAHASA)
        # =================================================

        # Kamus label menu mengikut bahasa
        menu_labels = {
            "English": {
                "Dashboard": "Dashboard",
                "Price Monitoring": "Price Monitoring",
                "Fertilizer Prices": "Fertilizer Prices",
                "Inventory": "Inventory",
                "Supplier Products": "Supplier Products",
                "User Management": "User Management",
                "System Overview": "System Overview",
                "Financial Tracking": "Financial Tracking"
            },
            "Malay": {
                "Dashboard": "Papan Pemuka",
                "Price Monitoring": "Pemantauan Harga",
                "Fertilizer Prices": "Harga Baja",
                "Inventory": "Inventori",
                "Supplier Products": "Produk Pembekal",
                "User Management": "Pengurusan Pengguna",
                "System Overview": "Gambaran Keseluruhan Sistem",
                "Financial Tracking": "Penjejakan Kewangan"
            }
        }

        current_lang = st.session_state.get("language", "English")

        if user_role == "farmer":
            raw_menu = [
                "Dashboard",
                "Price Monitoring",
                "Fertilizer Prices",
                "Inventory",
                "Financial Tracking"
            ]
        elif user_role == "supplier":
            raw_menu = [
                "Dashboard",
                "Price Monitoring",
                "Fertilizer Prices",
                "Supplier Products",
                "Financial Tracking"
            ]
        elif user_role == "admin":
            raw_menu = [
                "Dashboard",
                "User Management",
                "System Overview"
            ]
        else:
            raw_menu = [
                "Dashboard"
            ]

        # Tukar nama menu mengikut bahasa yang dipilih (tapi kekalkan nilai asal untuk routing)
        display_to_raw = {
            menu_labels[current_lang].get(item, item): item 
            for item in raw_menu
        }
        display_menu = list(display_to_raw.keys())

        current_page = st.session_state.get("page", "Dashboard")
        
        # Cari label paparan semasa
        current_display = next(
            (k for k, v in display_to_raw.items() if v == current_page), 
            display_menu[0]
        )
        current_index = display_menu.index(current_display) if current_display in display_menu else 0
        selected_display = st.radio(
            "Navigation" if current_lang == "English" else "Navigasi",
            display_menu,
            index=current_index
        )

        # Tukar kembali kepada nilai asal untuk routing di bawah
        st.session_state.page = display_to_raw[selected_display]

        st.divider()

        # =================================================
        # PEMILIH BAHASA (LANGUAGE SELECTOR)
        # =================================================
        selected_lang = st.selectbox(
            "🌐 Language / Bahasa",
            ["English", "Malay"],
            index=0 if current_lang == "English" else 1,
            key="sidebar_language_select"
        )

        if selected_lang != current_lang:
            st.session_state.language = selected_lang
            st.rerun()

        st.divider()
         

        # =================================================
        # API STATUS
        # =================================================

        try:

            response = requests.get(
                BASE_URL + "/",
                timeout=3
            )

            if response.status_code == 200:

                st.success(
                    "🟢 API Connected"
                )

            else:

                st.error(
                    "🔴 API Error"
                )

        except Exception:

            st.error(
                "🔴 API Offline"
            )

        st.divider()

        # =================================================
        # LOGOUT
        # =================================================

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False

            st.session_state.user = None

            st.session_state.page = "Dashboard"

            st.session_state.auth_page = "login"

            st.rerun()


# =========================================================
# DASHBOARD
# =========================================================

# =========================================================
# DASHBOARD
# =========================================================

def dashboard():
    user = st.session_state.get("user")

    if not user:
        return

    user_name = user.get("name", "User")
    user_role = str(
        user.get("role", "farmer")
    ).lower()

    # =====================================================
    # GET INVENTORY
    # =====================================================

    inventory = []

    if user_role == "farmer":
        inventory = get_inventory()

    total_items = len(inventory)

    total_inventory_value = sum(
        float(
            item.get("total_value", 0) or 0
        )
        for item in inventory
    )

    low_stock_items = []

    for item in inventory:
        try:
            quantity = float(
                item.get("quantity", 0) or 0
            )

            low_stock = float(
                item.get("low_stock", 0) or 0
            )

            if quantity <= low_stock:
                low_stock_items.append(item)

        except Exception:
            pass

    # =====================================================
    # GET COMMODITIES
    # =====================================================

    commodities_response = api_get(
        "/api/commodities"
    )

    states_response = api_get(
        "/api/states"
    )

    product_names = []
    state_names = []

    # -----------------------------------------------------
    # PRODUCTS
    # -----------------------------------------------------

    if isinstance(
        commodities_response,
        dict
    ):
        product_list = (
            commodities_response.get("commodities")
            or commodities_response.get("data")
            or []
        )
    else:
        product_list = commodities_response or []

    for product in product_list:

        if isinstance(product, dict):

            name = (
                product.get("item")
                or product.get("name")
                or product.get("commodity")
            )

        else:
            name = product

        if name:
            product_names.append(
                str(name)
            )

    product_names = sorted(
        list(set(product_names))
    )

    # -----------------------------------------------------
    # STATES
    # -----------------------------------------------------

    if isinstance(
        states_response,
        dict
    ):
        state_list = (
            states_response.get("states")
            or states_response.get("data")
            or []
        )
    else:
        state_list = states_response or []

    for state in state_list:

        if isinstance(state, dict):

            name = (
                state.get("state")
                or state.get("name")
            )

        else:
            name = state

        if name:
            state_names.append(
                str(name)
            )

    state_names = sorted(
        list(set(state_names))
    )

    

    # =====================================================
    # API STATUS
    # =====================================================

    api_online = False

    try:

        api_response = requests.get(
            BASE_URL + "/",
            timeout=3
        )

        if api_response.status_code == 200:
            api_online = True

    except Exception:
        api_online = False

    # =====================================================
    # TOP COMMODITIES
    # =====================================================

    commodity_rows = []

    # Limit to 10 products so dashboard stays clean
    dashboard_products = product_names[:10]

    for product in dashboard_products:

        try:

            price_response = api_get(
                "/api/current-price",
                params={
                    "item": product
                }
            )

            if price_response:

                lowest = price_response.get(
                    "lowest_price"
                )

                average = price_response.get(
                    "average_price"
                )

                highest = price_response.get(
                    "highest_price"
                )

                latest_date = price_response.get(
                    "latest_date",
                    "N/A"
                )

                latest_data = price_response.get(
                    "data",
                    []
                )

                state = "Malaysia"

                # Try to get state from latest data
                if latest_data:

                    first_row = latest_data[0]

                    if isinstance(
                        first_row,
                        dict
                    ):

                        state = (
                            first_row.get("state")
                            or first_row.get("State")
                            or "Malaysia"
                        )

                # Prefer average price
                display_price = average

                if display_price is None:
                    display_price = lowest

                commodity_rows.append(
                    {
                        "Commodity": product,
                        "State": state,
                        "Price": display_price,
                        "Lowest": lowest,
                        "Highest": highest,
                        "Date": latest_date
                    }
                )

        except Exception:
            continue

    commodity_df = pd.DataFrame(
        commodity_rows
    )

    # =====================================================
    # HERO SECTION
    # =====================================================

    st.markdown(
        f"""
        <div class="dashboard-hero">

        <div class="hero-content">

        <div class="hero-greeting">
                    Good morning, {user_name}! 👋
        </div>

        <div class="hero-description">
                    Here's the latest agricultural prices
                    and market insights for you.
        </div>

        </div>

        <div class="hero-illustration">

        <div class="hero-sun"></div>

        <div class="hero-mountain mountain-one"></div>
                <div class="hero-mountain mountain-two"></div>

        <div class="hero-field field-one"></div>
        <div class="hero-field field-two"></div>

        <div class="hero-farmer">
                    🧑‍🌾
        </div>

        </div>

        <div class="hero-quote">
                “Better data,<br>
                smarter decisions,<br>
                stronger farmers.”
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # SEARCH BAR
    # =====================================================

    search_query = st.text_input(
        "🔍 Search",
        placeholder="Search commodity or state...",
        label_visibility="collapsed"
    )

    if search_query:
        query = search_query.strip().lower()

        matched_products = [
            product for product in product_names
            if query in product.lower()
        ]

        matched_states = [
            state for state in state_names
            if query in state.lower()
        ]

        if matched_products:
            st.markdown("### 🌱 Commodity Results")

            for product in matched_products[:10]:
                st.write(f"🌱 **{product}**")

        if matched_states:
            st.markdown("### 📍 State Results")

            for state in matched_states[:10]:
                st.write(f"📍 **{state}**")

        if not matched_products and not matched_states:
            st.info("No matching commodity or state found.")

    # =====================================================
    # PAPARAN UI DASHBOARD (TAMBAHAN YANG KURANG)
    # =====================================================
    
    # Header dengan Ikon Loceng Notifikasi Amaran Stok Rendah
    col_title, col_notif = st.columns([8, 1])
    
    with col_title:
        st.markdown(f"### Selamat Datang, {user_name}! 👋")
        st.markdown(f"Peranan: **{user_role.capitalize()}**")
        
    with col_notif:
        # Ikon loceng interaktif menggunakan data low_stock_items sedia ada anda
        with st.popover("🔔"):
            st.markdown("### Amaran Stok Rendah")
            if low_stock_items:
                for item in low_stock_items:
                    item_name = item.get("name", "Item")
                    qty = item.get("quantity", 0)
                    st.warning(f"⚠️ **{item_name}** tinggal {qty} unit sahaja!")
            else:
                st.success("Semua stok mencukupi!")

    st.markdown("---")

    # Metrik Utama Dashboard
    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Item Inventori", f"{total_items} Item")
    col2.metric("Jumlah Nilai Inventori", f"RM {total_inventory_value:,.2f}")
    col3.metric("Amaran Stok Kritikal", f"{len(low_stock_items)} Item")

    st.markdown("---")
    
    # Contoh Butang Muat Turun CSV (Data Inventori)
    if inventory:
        df_inventory = pd.DataFrame(inventory)
        csv_inventory = df_inventory.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Muat Turun Laporan Inventori (CSV)",
            data=csv_inventory,
            file_name="laporan_inventori_farmpulse.csv",
            mime="text/csv"
        )

    # =====================================================
    # SUMMARY CARDS
    # =====================================================

    card1, card2, card3, card4 = st.columns(4)

    with card1:

        st.markdown(
            f"""
            <div class="summary-card summary-green">

            <div class="summary-icon">
                    🌾
            </div>

            <div class="summary-content">

            <div class="summary-label">
                        Total Commodities
            </div>

            <div class="summary-number">
                        {len(product_names)}
            </div>

            <div class="summary-change positive">
                        ● Live agricultural data
            </div>

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with card2:

        st.markdown(
            f"""
            <div class="summary-card summary-blue">

            <div class="summary-icon">
                    📦
            </div>

            <div class="summary-content">

            <div class="summary-label">
                        Inventory Items
            </div>

            <div class="summary-number">
                        {total_items}
            </div>

            <div class="summary-change positive">
                        ● Your farm inventory
            </div>

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with card3:

        st.markdown(
            f"""
            <div class="summary-card summary-yellow">

            <div class="summary-icon">
                    ⚠️
            </div>

            <div class="summary-content">

            <div class="summary-label">
                        Low Stock
            </div>

            <div class="summary-number">
                        {len(low_stock_items)}
            </div>

            <div class="summary-change warning-text">
                        ● Needs attention
            </div>

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with card4:

        api_status_text = (
            "Online"
            if api_online
            else "Offline"
        )

        api_class = (
            "positive"
            if api_online
            else "negative"
        )

        st.markdown(
            f"""
            <div class="summary-card summary-purple">

            <div class="summary-icon">
                    🟢
            </div>

            <div class="summary-content">

            <div class="summary-label">
                        FarmPulse API
            </div>

            <div class="summary-number api-number">
                        {api_status_text}
            </div>

            <div class="summary-change {api_class}">
                        ● System status
            </div>

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # =====================================================
    # MAIN DASHBOARD ROW
    # =====================================================

    left_col, middle_col, right_col = st.columns(
        [5, 3.2, 2.4]
    )

    # =====================================================
    # LIVE COMMODITY PRICES
    # =====================================================

    with left_col:

        st.markdown(
            """
            <div class="dashboard-panel">

            <div class="panel-header">

            <div>
            <h3>
                            🌾 Live Commodity Prices
            </h3>

            <p>
                            Latest available agricultural market prices
            </p>
            </div>

            <div class="view-all">
                        Live Data →
            </div>

            </div>

            """,
            unsafe_allow_html=True
        )

        if not commodity_df.empty:

            display_df = commodity_df.copy()

            display_df["Price"] = display_df[
                "Price"
            ].apply(
                lambda x:
                f"RM {float(x):,.2f}"
                if pd.notna(x)
                else "N/A"
            )

            display_df = display_df[
                [
                    "Commodity",
                    "State",
                    "Price",
                    "Date"
                ]
            ]

            display_df.columns = [
                "Commodity",
                "State",
                "Price (RM)",
                "Latest"
            ]

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                height=280
            )

        else:

            st.info(
                "No commodity price data available."
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    # =====================================================
    # PRICE TREND
    # =====================================================

    with middle_col:

        st.markdown(
            """
            <div class="dashboard-panel">

            <div class="panel-header">

            <div>
            <h3>
                            📈 Price Trend
            </h3>

            <p>
                            Agricultural price movement
            </p>
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if product_names:

            trend_product = st.selectbox(
            "Select Commodity",
        product_names,
    key="dashboard_trend_product"
)

            trend_response = api_get(
                "/api/price-history",
                params={
                    "item": trend_product,
                    "limit": 30
                }
            )

            if trend_response:

                trend_data = trend_response.get(
                    "data",
                    []
                )

                if trend_data:

                    trend_df = pd.DataFrame(
                        trend_data
                    )

                    date_column = None
                    price_column = None

                    for col in trend_df.columns:

                        lower_col = str(
                            col
                        ).lower()

                        if "date" in lower_col:
                            date_column = col

                        if "price" in lower_col:
                            price_column = col

                    if (
                        date_column
                        and price_column
                    ):

                        trend_df[
                            date_column
                        ] = pd.to_datetime(
                            trend_df[
                                date_column
                            ],
                            errors="coerce"
                        )

                        trend_df[
                            price_column
                        ] = pd.to_numeric(
                            trend_df[
                                price_column
                            ],
                            errors="coerce"
                        )

                        trend_df = (
                            trend_df
                            .dropna(
                                subset=[
                                    date_column,
                                    price_column
                                ]
                            )
                            .sort_values(
                                date_column
                            )
                        )

                        if not trend_df.empty:

                            st.caption(
                                f"Showing: {trend_product}"
                            )

                            st.line_chart(
                                trend_df.set_index(
                                    date_column
                                )[price_column],
                                height=220
                            )

                            latest_trend_price = (
                                trend_df.iloc[-1][
                                    price_column
                                ]
                            )

                            st.markdown(
                                f"""
                                <div class="current-price-box">

                                <span>
                                        Current Price
                                </span>

                                <strong>
                                        RM {float(latest_trend_price):,.2f}
                                </strong>

                                <small>
                                        {trend_product}
                                </small>

                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        else:

                            st.info(
                                "No trend data available."
                            )

                    else:

                        st.info(
                            "Price history format unavailable."
                        )

                else:

                    st.info(
                        "No historical data available."
                    )

            else:

                st.info(
                    "Unable to load price trend."
                )

        else:

            st.info(
                "No commodities available."
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    # =====================================================
    # QUICK ACTIONS
    # =====================================================

    with right_col:

        st.markdown(
            """
            <div class="dashboard-panel quick-panel">

            <div class="panel-header">

            <div>
            <h3>
                            ⚡ Quick Actions
            </h3>

            <p>
                            Frequently used features
            </p>
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # LIVE PRICES
        # -------------------------------------------------

        if st.button(
            "🌾  Check Live Prices",
            key="dashboard_live_prices",
            use_container_width=True
        ):

            st.session_state.page = (
                "Price Monitoring"
            )

            st.rerun()

        st.caption(
            "View real-time agricultural prices"
        )

        # -------------------------------------------------
        # INVENTORY
        # -------------------------------------------------

        if user_role == "farmer":

            if st.button(
                "📦  Add Inventory",
                key="dashboard_inventory",
                use_container_width=True
            ):

                st.session_state.page = (
                    "Inventory"
                )

                st.rerun()

            st.caption(
                "Record your farm stock and usage"
            )

        # -------------------------------------------------
        # FERTILIZER
        # -------------------------------------------------

        if st.button(
            "🌱  Fertilizer Prices",
            key="dashboard_fertilizer",
            use_container_width=True
        ):

            st.session_state.page = (
                "Fertilizer Prices"
            )

            st.rerun()

        st.caption(
            "View Malaysian fertilizer prices"
        )

        # -------------------------------------------------
        # PRICE PREDICTION
        # -------------------------------------------------

        if st.button(
            "🔮  View Predictions",
            key="dashboard_prediction",
            use_container_width=True
        ):

            st.session_state.page = (
                "Price Monitoring"
            )

            st.rerun()

        st.caption(
            "See future price estimates"
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    # =====================================================
    # SECOND DASHBOARD ROW
    # =====================================================

    st.write("")

    state_col, inventory_col, activity_col = st.columns(
        [3, 4, 3]
    )

    # =====================================================
    # STATE OVERVIEW
    # =====================================================

    with state_col:

        st.markdown(
            """
            <div class="dashboard-panel small-panel">

            <div class="panel-header">

            <div>
            <h3>
                            📍 Price by State
            </h3>

            <p>
                            Available market locations
            </p>
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if state_names:

            # Show maximum 10 states
            for index, state in enumerate(
                state_names[:10]
            ):

                percentage = (
                    90 - (index * 8)
                )

                st.markdown(
                    f"""
                    <div class="state-row">

                    <div class="state-name">
                            <span class="state-dot"></span>
                            {state}
                    </div>

                    <div class="state-bar-container">

                    <div
                                class="state-bar"
                                style="width:{percentage}%"
                    ></div>

                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "No state information available."
            )

        st.markdown(
        "</div>",
            unsafe_allow_html=True
        )

    # =====================================================
    # INVENTORY STATUS
    # =====================================================

    with inventory_col:

        st.markdown(
            """
            <div class="dashboard-panel small-panel">

            <div class="panel-header">

            <div>
            <h3>
                            📦 Inventory Status
            </h3>

            <p>
                            Current farm stock overview
            </p>
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if inventory:

            for item in inventory[:10]:

                item_name = item.get(
                    "item_name",
                    "Unknown"
                )

                quantity = float(
                    item.get(
                        "quantity",
                        0
                    ) or 0
                )

                low_stock = float(
                    item.get(
                        "low_stock",
                        0
                    ) or 0
                )

                if low_stock > 0:

                    percentage = (
                        quantity /
                        low_stock *
                        100
                    )

                else:

                    percentage = 100

                percentage = min(
                    max(
                        percentage,
                        5
                    ),
                    100
                )

                if quantity <= low_stock:

                    status_text = "Low stock"
                    status_class = "inventory-low"

                else:

                    status_text = "Good"
                    status_class = "inventory-good"

                st.markdown(
                    f"""
                    <div class="inventory-status-row">

                    <div class="inventory-icon">
                            📦
                    </div>

                    <div class="inventory-details">

                    <div class="inventory-name">
                                {item_name}
                    </div>

                    <div class="inventory-meta">
                                {quantity:g}
                                {item.get("unit", "")}
                                ·
                    <span class="{status_class}">
                                    {status_text}
                    </span>
                    </div>

                    <div class="inventory-progress">

                    <div
                                    class="inventory-progress-fill"
                                    style="width:{percentage}%">
                    </div>

                    </div>

                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.markdown(
                """
                <div class="empty-dashboard">

                <div class="empty-icon">
                        📦
                </div>

                <strong>
                        No inventory yet
                </strong>

                <span>
                        Add your first farm input
                        to see stock status here.
                </span>

                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    # =====================================================
    # RECENT ACTIVITY
    # =====================================================

    with activity_col:

        st.markdown(
            """
            <div class="dashboard-panel small-panel">

            <div class="panel-header">

            <div>
            <h3>
                            📰 Recent Activity
            </h3>

            <p>
                            Latest FarmPulse updates
            </p>
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        activity_items = []

        if commodity_df is not None and not commodity_df.empty:

            first_product = commodity_df.iloc[0]

            activity_items.append(
                {
                    "icon": "🌾",
                    "title": "Commodity prices updated",
                    "description": (
                        f"Latest data available for "
                        f"{first_product['Commodity']}."
                    )
                }
            )

        activity_items.append(
            {
                "icon": "🌱",
                "title": "Fertilizer price data",
                "description":
                    "Malaysian fertilizer price history is available."
            }
        )

        if inventory:

            activity_items.append(
                {
                    "icon": "📦",
                    "title": "Inventory updated",
                    "description":
                        f"You currently have {total_items} inventory item(s)."
                }
            )

        else:

            activity_items.append(
                {
                    "icon": "📦",
                    "title": "Inventory ready",
                    "description":
                        "Start recording your farm inputs."
                }
            )

        if low_stock_items:

            activity_items.append(
                {
                    "icon": "⚠️",
                    "title": "Low stock alert",
                    "description":
                        f"{len(low_stock_items)} item(s) need attention."
                }
            )

        else:

            activity_items.append(
                {
                    "icon": "✅",
                    "title": "Inventory status",
                    "description":
                        "No low-stock items detected."
                }
            )

        for activity in activity_items[:4]:

            st.markdown(
                f"""
                <div class="activity-row">

                <div class="activity-icon">
                        {activity["icon"]}
                </div>

                <div class="activity-content">

                <strong>
                            {activity["title"]}
                </strong>

                <span>
                            {activity["description"]}
                </span>

                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    # =====================================================
    # FARM PROFILE / ACCOUNT INFO
    # =====================================================

    st.write("")

    profile_col, insight_col = st.columns(
        [1, 2]
    )

    with profile_col:

        st.markdown(
            f"""
            <div class="profile-card">

            <div class="profile-card-header">

            <div class="profile-large-avatar">
                        👤
            </div>

            <div>

            <h3>
                            {user_name}
            </h3>

            <span>
                            {user_role.title()}
            </span>

            </div>

            </div>

            <div class="profile-divider"></div>

            <div class="profile-detail">
            <span>Account Role</span>
            <strong>
            {user_role.title()}
            </strong>
            </div>

            <div class="profile-detail">
            <span>Inventory Value</span>
            <strong>
                        RM {total_inventory_value:,.2f}
            </strong>
            </div>

            <div class="profile-detail">
            <span>System</span>
            <strong>
                        FarmPulse
            </strong>
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with insight_col:

        st.markdown(
            """
            <div class="insight-banner">

            <div class="insight-icon">
                    🌱
            </div>

            <div class="insight-text">

            <strong>
                        FarmPulse Insight
            </strong>

            <p>
                        Use current agricultural prices,
                        historical trends and inventory
                        information to support better
                        farm cost planning.
            </p>

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # DASHBOARD FOOTER
    # =====================================================

    st.markdown(
        """
        <div class="dashboard-bottom-footer">

        <span>
                © 2026 FarmPulse
        </span>

        <span>
                Smart Agricultural Monitoring System
        </span>

        </div>
        """,
        unsafe_allow_html=True
    )

    
# =========================================================
# PRICE MONITORING
# =========================================================
# DO NOT MODIFY THIS PRICE MONITORING LOGIC.
# =========================================================

def price_monitoring():

    st.markdown(
        '<div class="main-title">🌾 Price Monitoring & Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Monitor agricultural prices, analyse trends, compare states and predict future prices.'
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # GET PRODUCTS
    # =====================================================

    commodities = api_get(
        "/api/commodities"
    )

    states = api_get(
        "/api/states"
    )

    if not commodities:

        st.error(
            "Unable to load agricultural products."
        )

        return

    if not states:

        st.error(
            "Unable to load states."
        )

        return

    # =====================================================
    # EXTRACT PRODUCT NAMES
    # =====================================================

    if isinstance(
        commodities,
        dict
    ):

        product_list = (
            commodities.get("commodities")
            or commodities.get("data")
            or []
        )

    else:

        product_list = commodities

    if isinstance(
        states,
        dict
    ):

        state_list = (
            states.get("states")
            or states.get("data")
            or []
        )

    else:

        state_list = states

    product_names = []

    for product in product_list:

        if isinstance(
            product,
            dict
        ):

            name = (
                product.get("item")
                or product.get("name")
                or product.get("commodity")
            )

        else:

            name = product

        if name:
            product_names.append(name)

    state_names = []

    for state in state_list:

        if isinstance(
            state,
            dict
        ):

            name = (
                state.get("state")
                or state.get("name")
            )

        else:

            name = state

        if name:
            state_names.append(name)

    product_names = sorted(
        list(
            set(product_names)
        )
    )

    state_names = sorted(
        list(
            set(state_names)
        )
    )

    # =====================================================
    # FILTER
    # =====================================================

    st.markdown(
        "### 🔎 Select Agricultural Product"
    )

    col1, col2 = st.columns(2)

    with col1:

        selected_product = st.selectbox(
            "Agricultural Product",
            product_names
        )

    with col2:

        selected_state = st.selectbox(
            "State",
            ["All States"] + state_names
        )

    # =====================================================
    # VIEW PRICE
    # =====================================================

    if st.button(
        "🔍 View Price",
        type="primary"
    ):

        st.session_state.price_product = (
            selected_product
        )

        st.session_state.price_state = (
            selected_state
        )

    if (
        "price_product"
        not in st.session_state
    ):

        return

    selected_product = (
        st.session_state.price_product
    )

    selected_state = (
        st.session_state.price_state
    )

    st.divider()

    # =====================================================
    # CURRENT PRICE
    # =====================================================

    current_params = {
        "item": selected_product
    }

    if selected_state != "All States":

        current_params["state"] = (
            selected_state
        )

    current_price = api_get(
        "/api/current-price",
        params=current_params
    )

    if current_price:

        st.markdown(
            "### 💰 Current Price"
        )

        lowest_price = current_price.get(
            "lowest_price"
        )

        average_price = current_price.get(
            "average_price"
        )

        highest_price = current_price.get(
            "highest_price"
        )

        latest_date = current_price.get(
            "latest_date"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            if lowest_price is not None:

                st.metric(
                    "Lowest Price",
                    f"RM {float(lowest_price):.2f}"
                )

            else:

                st.metric(
                    "Lowest Price",
                    "N/A"
                )

        with col2:

            if average_price is not None:

                st.metric(
                    "Average Price",
                    f"RM {float(average_price):.2f}"
                )

            else:

                st.metric(
                    "Average Price",
                    "N/A"
                )

        with col3:

            if highest_price is not None:

                st.metric(
                    "Highest Price",
                    f"RM {float(highest_price):.2f}"
                )

            else:

                st.metric(
                    "Highest Price",
                    "N/A"
                )

        with col4:

            st.metric(
                "Latest Date",
                latest_date or "N/A"
            )

        # =================================================
        # LATEST PRICE TABLE
        # =================================================

        latest_data = current_price.get(
            "data",
            []
        )

        if latest_data:

            st.markdown(
                "#### Latest Price Data"
            )

            latest_df = pd.DataFrame(
                latest_data
            )

            st.dataframe(
                latest_df,
                use_container_width=True,
                hide_index=True
            )

    else:

        st.warning(
            "No current price data available."
        )

    # =====================================================
    # HISTORICAL PRICE
    # =====================================================

    st.divider()

    st.markdown(
        "### 📈 Historical Price Trend"
    )

    history_params = {
        "item": selected_product,
        "limit": 100
    }

    if selected_state != "All States":

        history_params["state"] = (
            selected_state
        )

    history = api_get(
        "/api/price-history",
        params=history_params
    )

    if history:

        history_data = history.get(
            "data",
            []
        )

        if history_data:

            history_df = pd.DataFrame(
                history_data
            )

            date_column = None
            price_column = None

            for col in history_df.columns:

                lower_col = str(
                    col
                ).lower()

                if (
                    "date"
                    in lower_col
                ):

                    date_column = col

                if (
                    "price"
                    in lower_col
                ):

                    price_column = col

            if (
                date_column
                and price_column
            ):

                history_df[
                    date_column
                ] = pd.to_datetime(
                    history_df[
                        date_column
                    ],
                    errors="coerce"
                )

                history_df[
                    price_column
                ] = pd.to_numeric(
                    history_df[
                        price_column
                    ],
                    errors="coerce"
                )

                history_df = (
                    history_df
                    .dropna(
                        subset=[
                            date_column,
                            price_column
                        ]
                    )
                    .sort_values(
                        date_column
                    )
                )

                st.line_chart(
                    history_df.set_index(
                        date_column
                    )[price_column]
                )

            st.dataframe(
                history_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "No historical price data available."
            )

    else:

        st.warning(
            "Unable to load historical price data."
        )

    # =====================================================
    # STATE COMPARISON
    # =====================================================

    st.divider()

    st.markdown(
        "### 🗺️ State Price Comparison"
    )

    comparison = api_get(
        "/api/price-comparison",
        params={
            "item": selected_product
        }
    )

    if comparison:

        comparison_data = comparison.get(
            "data",
            []
        )

        if comparison_data:

            comparison_df = pd.DataFrame(
                comparison_data
            )

            state_column = None
            price_column = None

            for col in comparison_df.columns:

                lower_col = str(
                    col
                ).lower()

                if (
                    "state"
                    in lower_col
                ):

                    state_column = col

                if (
                    "price"
                    in lower_col
                    or "average"
                    in lower_col
                ):

                    price_column = col

            if (
                state_column
                and price_column
            ):

                comparison_df[
                    price_column
                ] = pd.to_numeric(
                    comparison_df[
                        price_column
                    ],
                    errors="coerce"
                )

                chart_df = (
                    comparison_df
                    .dropna(
                        subset=[
                            state_column,
                            price_column
                        ]
                    )
                    .set_index(
                        state_column
                    )
                )

                st.bar_chart(
                    chart_df[
                        price_column
                    ]
                )

            st.dataframe(
                comparison_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "No state comparison data available."
            )

    else:

        st.warning(
            "Unable to load state comparison."
        )

    # =====================================================
    # FUTURE PRICE PREDICTION
    # =====================================================

    st.divider()

    st.markdown(
        "### 🔮 Future Price Prediction"
    )

    prediction_days = st.slider(
        "Prediction Period (Days)",
        min_value=1,
        max_value=30,
        value=7
    )

    prediction_params = {
        "item": selected_product,
        "days": prediction_days
    }

    if selected_state != "All States":

        prediction_params["state"] = (
            selected_state
        )

    prediction = api_get(
        "/api/predict-price",
        params=prediction_params
    )

    if prediction:

        prediction_data = prediction.get(
            "data",
            []
        )

        if prediction_data:

            prediction_df = pd.DataFrame(
                prediction_data
            )

            prediction_price_column = None
            prediction_date_column = None

            for col in prediction_df.columns:

                lower_col = str(
                    col
                ).lower()

                if (
                    "predict"
                    in lower_col
                    or "forecast"
                    in lower_col
                ):

                    prediction_price_column = col

                if (
                    "date"
                    in lower_col
                ):

                    prediction_date_column = col

            if (
                prediction_price_column
                is None
            ):

                possible_price_columns = [
                    col
                    for col in prediction_df.columns
                    if "price" in str(col).lower()
                ]

                if possible_price_columns:

                    prediction_price_column = (
                        possible_price_columns[-1]
                    )

            if (
                prediction_date_column
                and prediction_price_column
            ):

                prediction_df[
                    prediction_date_column
                ] = pd.to_datetime(
                    prediction_df[
                        prediction_date_column
                    ],
                    errors="coerce"
                )

                prediction_df[
                    prediction_price_column
                ] = pd.to_numeric(
                    prediction_df[
                        prediction_price_column
                    ],
                    errors="coerce"
                )

                chart_df = (
                    prediction_df
                    .dropna(
                        subset=[
                            prediction_date_column,
                            prediction_price_column
                        ]
                    )
                    .sort_values(
                        prediction_date_column
                    )
                )

                if not chart_df.empty:

                    st.line_chart(
                        chart_df.set_index(
                            prediction_date_column
                        )[prediction_price_column]
                    )

            st.dataframe(
                prediction_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "No prediction data available."
            )

    else:

        st.warning(
            "Unable to load price prediction."
        )


# =========================================================
# =========================================================
# FERTILIZER PRICE HISTORY
# =========================================================

def fertilizer_price_history():

    st.markdown(
        '<div class="main-title">🌱 Fertilizer Price History</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'View historical Malaysian fertilizer prices and cost trends.'
        '</div>',
        unsafe_allow_html=True
    )

    # =====================================================
    # GET FERTILIZER DATA FROM API
    # =====================================================

    fertilizer_response = api_get(
        "/api/fertilizer"
    )

    if not fertilizer_response:

        st.error(
            "Unable to load fertilizer price data."
        )

        return

    if not fertilizer_response.get("success"):

        st.error(
            fertilizer_response.get(
                "message",
                "Fertilizer data is unavailable."
            )
        )

        return

    fertilizer_data = fertilizer_response.get(
        "data",
        []
    )

    if not fertilizer_data:

        st.warning(
            "No fertilizer price data available."
        )

        return

    # =====================================================
    # CONVERT TO DATAFRAME
    # =====================================================

    fertilizer_df = pd.DataFrame(
        fertilizer_data
    )

    fertilizer_df["date"] = pd.to_datetime(
        fertilizer_df["date"],
        errors="coerce"
    )

    fertilizer_df["price"] = pd.to_numeric(
        fertilizer_df["price"],
        errors="coerce"
    )

    fertilizer_df = fertilizer_df.dropna(
        subset=[
            "date",
            "price"
        ]
    )

    fertilizer_df = fertilizer_df.sort_values(
        "date"
    )

    # =====================================================
    # FERTILIZER FILTER
    # =====================================================

    st.markdown(
        "### 🔎 Select Fertilizer"
    )

    fertilizer_list = sorted(
        fertilizer_df[
            "fertilizer"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    if not fertilizer_list:

        st.warning(
            "No fertilizer types available."
        )

        return

    selected_fertilizer = st.selectbox(
        "Fertilizer",
        fertilizer_list
    )

    # =====================================================
    # FILTER SELECTED FERTILIZER
    # =====================================================

    filtered_fertilizer = fertilizer_df[
        fertilizer_df["fertilizer"]
        == selected_fertilizer
    ].copy()

    if filtered_fertilizer.empty:

        st.warning(
            "No historical price data available "
            "for this fertilizer."
        )

        return

    filtered_fertilizer = (
        filtered_fertilizer
        .sort_values("date")
        .reset_index(drop=True)
    )

    # =====================================================
    # PRICE ANALYSIS
    # =====================================================

    st.markdown(
        "### 📊 Price Analysis"
    )

    latest_price = (
        filtered_fertilizer
        .iloc[-1]["price"]
    )

    highest_price = (
        filtered_fertilizer["price"]
        .max()
    )

    lowest_price = (
        filtered_fertilizer["price"]
        .min()
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Latest Price",
            f"RM {latest_price:.2f}"
        )

    with col2:

        st.metric(
            "Highest Price",
            f"RM {highest_price:.2f}"
        )

    with col3:

        st.metric(
            "Lowest Price",
            f"RM {lowest_price:.2f}"
        )

    st.caption(
        "Historical Malaysian fertilizer price data "
        "(RM/50kg bag)."
    )

    # =====================================================
    # PRICE TABLE
    # =====================================================

    st.markdown(
        "### 📋 Price Data"
    )

    display_df = filtered_fertilizer.copy()

    display_df["date"] = (
        display_df["date"]
        .dt.strftime("%Y-%m-%d")
    )

    columns_to_show = [
        "date",
        "fertilizer",
        "price",
        "unit",
        "country",
        "source"
    ]

    available_columns = [
        col
        for col in columns_to_show
        if col in display_df.columns
    ]

    st.dataframe(
        display_df[
            available_columns
        ],
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # PRICE TREND
    # =====================================================

    st.markdown(
        "### 📈 Price Trend"
    )

    chart_df = filtered_fertilizer[
        [
            "date",
            "price"
        ]
    ].copy()

    chart_df = chart_df.set_index(
        "date"
    )

    st.line_chart(
        chart_df["price"]
    )



# FIREBASE INVENTORY
# =========================================================

def get_inventory():

    user = st.session_state.user

    if not user:
        return []

    user_id = user.get("id")

    if not user_id:
        return []

    try:

        api_folder = r"C:\python1\FarmPulse_API"

        if api_folder not in sys.path:

            sys.path.append(
                api_folder
            )

        # firebase_config is provided by the sibling API project and is added
        # to sys.path immediately above.  It is not part of this project, so
        # tell static analysis not to flag the runtime import.
        import firebase_config  # type: ignore[import-not-found]

        db = firebase_config.db

    except Exception:

        return []

    try:

        inventory_ref = (
            db.collection("inventory")
            .where(
                "user_id",
                "==",
                user_id
            )
        )

        docs = inventory_ref.stream()

        inventory = []

        for doc in docs:

            data = doc.to_dict()

            data["id"] = doc.id

            inventory.append(
                data
            )

        return inventory

    except Exception as e:

        st.error(
            f"Firebase error: {e}"
        )

        return []


# =========================================================
# ADD INVENTORY
# =========================================================

def add_inventory(
    item_name,
    category,
    quantity,
    unit,
    low_stock,
    unit_cost
):

    user = st.session_state.user

    if not user:
        return False

    user_id = user.get("id")

    if not user_id:
        return False

    try:

        api_folder = r"C:\python1\FarmPulse_API"

        if api_folder not in sys.path:

            sys.path.append(
                api_folder
            )

        # The API project's directory is added to sys.path immediately above;
        # the module is intentionally imported from that external project.
        import firebase_config  # type: ignore[import-not-found]

        db = firebase_config.db

    except Exception as e:

        st.error(
            f"Unable to connect to Firebase: {e}"
        )

        return False

    try:

        total_value = (
            quantity * unit_cost
        )

        inventory_data = {

            "user_id": user_id,

            "item_name": item_name,

            "category": category,

            "quantity": quantity,

            "unit": unit,

            "low_stock": low_stock,

            "unit_cost": unit_cost,

            "total_value": total_value,

            "date": datetime.now().strftime(
                "%Y-%m-%d"
            ),

            "created_at": datetime.now().isoformat()

        }

        db.collection(
            "inventory"
        ).add(
            inventory_data
        )

        return True

    except Exception as e:

        st.error(
            f"Firebase error: {e}"
        )

        return False


# =========================================================
# DELETE INVENTORY
# =========================================================

def delete_inventory(doc_id):

    try:

        api_folder = r"C:\python1\FarmPulse_API"

        if api_folder not in sys.path:

            sys.path.append(
                api_folder
            )

        import importlib

        firebase_config = importlib.import_module(
            "firebase_config"
        )

        db = firebase_config.db

    except Exception as e:

        st.error(
            f"Unable to connect to Firebase: {e}"
        )

        return False

    try:

        db.collection(
            "inventory"
        ).document(
            doc_id
        ).delete()

        return True

    except Exception as e:

        st.error(
            f"Firebase error: {e}"
        )

        return False


# =========================================================
# INVENTORY PAGE
# =========================================================

def inventory_page():

    user = st.session_state.get(
        "user"
    )

    if not user:
        return

    user_role = str(
        user.get(
            "role",
            "farmer"
        )
    ).lower()

    if user_role != "farmer":

        st.error(
            "Access denied. Inventory is available for farmers only."
        )

        return

    st.markdown(
        '<div class="main-title">📦 Inventory Management</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Track farm inputs, stock levels and inventory value.'
        '</div>',
        unsafe_allow_html=True
    )

    inventory = get_inventory()

    # =====================================================
    # SUMMARY
    # =====================================================

    total_items = len(
        inventory
    )

    total_value = sum(
        float(
            item.get(
                "total_value",
                0
            ) or 0
        )
        for item in inventory
    )

    low_stock_items = []

    for item in inventory:

        quantity = float(
            item.get(
                "quantity",
                0
            ) or 0
        )

        low_stock = float(
            item.get(
                "low_stock",
                0
            ) or 0
        )

        if quantity <= low_stock:

            low_stock_items.append(
                item
            )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📦 Total Items",
            total_items
        )

    with col2:

        st.metric(
            "💰 Total Inventory Value",
            f"RM {total_value:,.2f}"
        )

    with col3:

        st.metric(
            "⚠️ Low Stock",
            len(low_stock_items)
        )

    st.divider()

    # =====================================================
    # LOW STOCK WARNING
    # =====================================================

    if low_stock_items:

        st.markdown(
            '<div class="low-stock">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### ⚠️ Low Stock Alert"
        )

        st.write(
            "The following inventory items are at or below "
            "their minimum stock level:"
        )

        for item in low_stock_items:

            st.write(
                f"🔴 **{item.get('item_name', 'Unknown')}** "
                f"— {item.get('quantity', 0)} "
                f"{item.get('unit', '')}"
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

        st.write("")

    # =====================================================
    # ADD INVENTORY
    # =====================================================

    st.markdown(
        "### ➕ Add Inventory"
    )

    with st.form(
        "inventory_form",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(2)

        with col1:

            item_name = st.text_input(
                "Item Name",
                placeholder="e.g. Urea Fertilizer"
            )

            category = st.selectbox(
                "Category",
                [
                    "Fertilizer",
                    "Seed",
                    "Animal Feed",
                    "Pesticide",
                    "Equipment",
                    "Other"
                ]
            )

            quantity = st.number_input(
                "Quantity",
                min_value=0.0,
                value=0.0,
                step=0.1
            )

            unit = st.selectbox(
                "Unit",
                [
                    "kg",
                    "g",
                    "ton",
                    "liter",
                    "unit",
                    "bag",
                    "bottle"
                ]
            )

        with col2:

            low_stock = st.number_input(
                "Low Stock Level",
                min_value=0.0,
                value=0.0,
                step=0.1
            )

            unit_cost = st.number_input(
                "Unit Cost (RM)",
                min_value=0.0,
                value=0.0,
                step=0.01
            )

            total_preview = (
                quantity * unit_cost
            )

            st.metric(
                "Total Value",
                f"RM {total_preview:,.2f}"
            )

        st.write("")

        save_inventory = st.form_submit_button(
            "💾 Save Inventory",
            use_container_width=True,
            type="primary"
        )

        if save_inventory:

            if not item_name.strip():

                st.warning(
                    "Please enter an item name."
                )

            elif quantity <= 0:

                st.warning(
                    "Quantity must be greater than 0."
                )

            elif unit_cost < 0:

                st.warning(
                    "Unit cost cannot be negative."
                )

            else:

                success = add_inventory(
                    item_name=item_name.strip(),
                    category=category,
                    quantity=quantity,
                    unit=unit,
                    low_stock=low_stock,
                    unit_cost=unit_cost
                )

                if success:

                    st.success(
                        "Inventory saved successfully!"
                    )

                    st.rerun()

    st.divider()

    # =====================================================
    # INVENTORY TABLE
    # =====================================================

    st.markdown(
        "### 📋 My Inventory"
    )

    if inventory:

        inventory_rows = []

        for item in inventory:

            inventory_rows.append(
                {
                    "Item": item.get(
                        "item_name",
                        ""
                    ),

                    "Category": item.get(
                        "category",
                        ""
                    ),

                    "Quantity": item.get(
                        "quantity",
                        0
                    ),

                    "Unit": item.get(
                        "unit",
                        ""
                    ),

                    "Unit Cost (RM)": item.get(
                        "unit_cost",
                        0
                    ),

                    "Total Value (RM)": item.get(
                        "total_value",
                        0
                    ),

                    "Date": item.get(
                        "date",
                        ""
                    )
                }
            )

        inventory_df = pd.DataFrame(
            inventory_rows
        )

        st.dataframe(
            inventory_df,
            use_container_width=True,
            hide_index=True
        )

        # =================================================
        # DELETE INVENTORY
        # =================================================

        st.markdown(
            "### 🗑️ Delete Inventory"
        )

        inventory_options = {}

        for item in inventory:

            item_id = item.get(
                "id"
            )

            item_name = item.get(
                "item_name",
                "Unknown"
            )

            if item_id:

                inventory_options[
                    f"{item_name} — {item_id}"
                ] = item_id

        if inventory_options:

            selected_delete = st.selectbox(
                "Select item to delete",
                list(
                    inventory_options.keys()
                )
            )

            if st.button(
                "🗑️ Delete Selected Item",
                type="secondary"
            ):

                doc_id = inventory_options[
                    selected_delete
                ]

                success = delete_inventory(
                    doc_id
                )

                if success:

                    st.success(
                        "Inventory item deleted successfully!"
                    )

                    st.rerun()

    else:

        st.info(
            "No inventory records yet. "
            "Add your first inventory item above."
        )


# =========================================================
# SUPPLIER PRODUCTS
# =========================================================

def supplier_products():

    st.markdown(
        '<div class="main-title">📦 Supplier Products</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Manage agricultural products supplied to farmers.'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Supplier product management module is ready "
        "for the next development stage."
    )


# =========================================================
# USER MANAGEMENT
# =========================================================

def user_management():

    st.markdown(
        '<div class="main-title">👥 User Management</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Manage FarmPulse users and their roles.'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Admin user management module is ready "
        "for the next development stage."
    )


# =========================================================
# SYSTEM OVERVIEW
# =========================================================

def system_overview():

    st.markdown(
        '<div class="main-title">📊 System Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Monitor the current FarmPulse system status.'
        '</div>',
        unsafe_allow_html=True
    )

    system_status = api_get(
        "/"
    )

    if system_status:

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "🟢 API Status",
                "Online"
            )

        with col2:

            st.metric(
                "📊 Price Records",
                system_status.get(
                    "total_records",
                    "N/A"
                )
            )

        st.success(
            "FarmPulse API is running normally."
        )

    else:

        st.error(
            "FarmPulse API is currently unavailable."
        )


# =========================================================
# FINANCIAL TRACKING
# =========================================================

def financial_tracking():

    st.markdown(
        """
        <div class="finance-page-header">

        <div class="finance-title-row">

        <div class="finance-icon">
                    💰
        </div>

        <div>
        <div class="finance-title">
                        Financial Tracking
        </div>

        <div class="finance-subtitle">
                        Track your income, expenses and keep your farm finances in check.
        </div>
        </div>

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # DEMO TRANSACTIONS
    # =====================================================

    if "financial_transactions" not in st.session_state:

        st.session_state.financial_transactions = [

            {
                "date": "22 Sep 2026",
                "type": "Income",
                "category": "Vegetable Sales",
                "description": "Carrot harvest sales",
                "amount": 500.00
            },

            {
                "date": "20 Sep 2026",
                "type": "Expense",
                "category": "Fertilizer",
                "description": "NPK fertilizer",
                "amount": 150.00
            },

            {
                "date": "18 Sep 2026",
                "type": "Expense",
                "category": "Fuel",
                "description": "Tractor fuel",
                "amount": 80.00
            },

            {
                "date": "15 Sep 2026",
                "type": "Income",
                "category": "Vegetable Sales",
                "description": "Lettuce sales",
                "amount": 320.00
            },

            {
                "date": "12 Sep 2026",
                "type": "Expense",
                "category": "Seeds",
                "description": "Tomato seeds",
                "amount": 120.00
            },

            {
                "date": "10 Sep 2026",
                "type": "Expense",
                "category": "Labour",
                "description": "Field worker",
                "amount": 200.00
            }
        ]

    transactions = st.session_state.financial_transactions

    # =====================================================
    # CALCULATIONS
    # =====================================================

    total_income = sum(
        item["amount"]
        for item in transactions
        if item["type"] == "Income"
    )

    total_expenses = sum(
        item["amount"]
        for item in transactions
        if item["type"] == "Expense"
    )

    net_balance = total_income - total_expenses

    # =====================================================
    # SUMMARY CARDS
    # =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="finance-summary-card income-card">

            <div class="finance-card-icon">
                    💰
            </div>

            <div class="finance-card-content">

            <div class="finance-card-label">
                        Total Income
            </div>

            <div class="finance-card-value">
                        RM {total_income:,.2f}
            </div>

            <div class="finance-card-note income-note">
                        ↑ Income recorded
            </div>

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="finance-summary-card expense-card">

            <div class="finance-card-icon">
                    💸
            </div>

            <div class="finance-card-content">

            <div class="finance-card-label">
                        Total Expenses
            </div>

            <div class="finance-card-value">
                        RM {total_expenses:,.2f}
            </div>

            <div class="finance-card-note expense-note">
                        ↑ Expenses recorded
            </div>

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        balance_class = (
            "balance-positive"
            if net_balance >= 0
            else "balance-negative"
        )

        balance_icon = (
            "⚖️"
            if net_balance >= 0
            else "⚠️"
        )

        st.markdown(
            f"""
            <div class="finance-summary-card balance-card">

            <div class="finance-card-icon">
                    {balance_icon}
            </div>

            <div class="finance-card-content">

            <div class="finance-card-label">
                        Net Balance
            </div>

            <div class="finance-card-value">
                        RM {net_balance:,.2f}
            </div>

            <div class="finance-card-note {balance_class}">
                        Income − Expenses
            </div>

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div class='finance-space'></div>", unsafe_allow_html=True)

    # =====================================================
    # CHARTS + ADD TRANSACTION
    # =====================================================

    chart_col, breakdown_col, form_col = st.columns(
        [1.6, 1, 0.95],
        gap="medium"
    )

    # =====================================================
    # INCOME VS EXPENSES
    # =====================================================

    with chart_col:

        st.markdown(
            """
            <div class="finance-panel">

            <div class="finance-panel-title">
                    Income vs Expenses
            </div>

            <div class="finance-panel-subtitle">
                    Financial movement
            </div>

            """,
            unsafe_allow_html=True
        )

        income_data = [
            700,
            550,
            650,
            830
        ]

        expense_data = [
            420,
            350,
            380,
            450
        ]

        fig = go.Figure()

        fig.add_bar(
            x=["Sep 1–7", "Sep 8–14", "Sep 15–21", "Sep 22–30"],
            y=income_data,
            name="Income",
            marker_color="#299b72"
        )

        fig.add_bar(
            x=["Sep 1–7", "Sep 8–14", "Sep 15–21", "Sep 22–30"],
            y=expense_data,
            name="Expenses",
            marker_color="#f26b72"
        )

        fig.update_layout(
            height=270,
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(
                family="Plus Jakarta Sans"
            ),
            legend=dict(
                orientation="h",
                y=1.08,
                x=0.65
            ),
            xaxis=dict(
                showgrid=False
            ),
            yaxis=dict(
                title="RM",
                gridcolor="#edf1ef"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # EXPENSE BREAKDOWN
    # =====================================================

    with breakdown_col:

        st.markdown(
            """
            <div class="finance-panel">

            <div class="finance-panel-title">
                    Expense Breakdown
            </div>

            <div class="finance-panel-subtitle">
                    By category
            </div>

            """,
            unsafe_allow_html=True
        )

        expense_categories = {}

        for item in transactions:

            if item["type"] == "Expense":

                category = item["category"]

                expense_categories[category] = (
                    expense_categories.get(category, 0)
                    + item["amount"]
                )

        if expense_categories:

            labels = list(
                expense_categories.keys()
            )

            values = list(
                expense_categories.values()
            )

            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=labels,
                        values=values,
                        hole=0.62,
                        textinfo="percent",
                        hovertemplate=(
                            "%{label}<br>"
                            "RM %{value:,.2f}"
                            "<extra></extra>"
                        )
                    )
                ]
            )

            fig.update_layout(
                height=270,
                margin=dict(
                    l=5,
                    r=5,
                    t=15,
                    b=5
                ),
                showlegend=True,
                legend=dict(
                    font=dict(size=10)
                ),
                paper_bgcolor="white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # ADD NEW TRANSACTION
    # =====================================================

    with form_col:

        st.markdown(
            """
            <div class="finance-form-panel">

            <div class="finance-form-title">
                    ➕ Add New Transaction
            </div>

            """,
            unsafe_allow_html=True
        )

        transaction_type = st.radio(
            "Transaction Type",
            ["Income", "Expense"],
            horizontal=True,
            key="finance_type"
        )

        if transaction_type == "Income":

            categories = [
                "Vegetable Sales",
                "Fruit Sales",
                "Crop Sales",
                "Other Income"
            ]

        else:

            categories = [
                "Fertilizer",
                "Seeds",
                "Fuel",
                "Labour",
                "Equipment",
                "Maintenance",
                "Other Expense"
            ]

        category = st.selectbox(
            "Category",
            categories,
            key="finance_category"
        )

        amount = st.number_input(
            "Amount (RM)",
            min_value=0.00,
            step=10.00,
            format="%.2f",
            key="finance_amount"
        )

        transaction_date = st.date_input(
            "Date",
            key="finance_date"
        )

        description = st.text_area(
            "Description",
            placeholder="Enter description (optional)",
            key="finance_description"
        )

        if st.button(
            "💾 Save Transaction",
            use_container_width=True,
            type="primary"
        ):

            if amount <= 0:

                st.warning(
                    "Please enter a valid amount."
                )

            else:

                new_transaction = {

                    "date": transaction_date.strftime(
                        "%d %b %Y"
                    ),

                    "type": transaction_type,

                    "category": category,

                    "description": (
                        description.strip()
                        if description
                        else "-"
                    ),

                    "amount": float(amount)
                }

                st.session_state.financial_transactions.insert(
                    0,
                    new_transaction
                )

                st.success(
                    "Transaction saved successfully."
                )

                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # RECENT TRANSACTIONS
    # =====================================================

    st.markdown(
        """
        <div class="finance-transactions-panel">

        <div class="finance-panel-header-row">

        <div>

        <div class="finance-panel-title">
                        Recent Transactions
        </div>

        <div class="finance-panel-subtitle">
                        Latest financial records
        </div>

        </div>

        </div>

        """,
        unsafe_allow_html=True
    )

    for transaction in transactions[:6]:

        if transaction["type"] == "Income":

            badge_class = "transaction-income"
            amount_class = "amount-income"
            amount_prefix = "+"

        else:

            badge_class = "transaction-expense"
            amount_class = "amount-expense"
            amount_prefix = "-"

        st.markdown(
            f"""
            <div class="transaction-row">

            <div class="transaction-date">
                    {transaction["date"]}
            </div>

            <div>
                    <span class="transaction-badge {badge_class}">
                        {transaction["type"]}
            </span>
            </div>

            <div class="transaction-category">
                    {transaction["category"]}
            </div>

            <div class="transaction-description">
                    {transaction["description"]}
            </div>

            <div class="transaction-amount {amount_class}">
                    {amount_prefix} RM {transaction["amount"]:,.2f}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)



# =========================================================
# MAIN APPLICATION
# =========================================================

if not st.session_state.logged_in:

    if st.session_state.auth_page == "register":

        register_page()

    else:

        login_page()

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

sidebar()


# =========================================================
# CURRENT USER
# =========================================================

current_page = st.session_state.page

user_data = (
    st.session_state.get("user")
    or {}
)

user_role = str(
    user_data.get(
        "role",
        "farmer"
    )
).lower()


# =========================================================
# PAGE ROUTING
# =========================================================

if current_page == "Dashboard":

    dashboard()

elif current_page == "Price Monitoring":

    price_monitoring()

elif current_page == "Fertilizer Prices":

    fertilizer_price_history()

elif current_page == "Inventory":

    inventory_page()

elif current_page == "Financial Tracking":

    financial_tracking()

elif current_page == "Supplier Products":

    if user_role == "supplier":

        supplier_products()

    else:

        st.error(
            "Access denied."
        )

elif current_page == "User Management":

    if user_role == "admin":

        user_management()

    else:

        st.error(
            "Access denied."
        )

elif current_page == "System Overview":

    if user_role == "admin":

        system_overview()

    else:

        st.error(
            "Access denied."
        )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#94a3b8;
        padding:10px;
    ">
        🌱 FarmPulse —
        Smart Agricultural Monitoring System
    </div>
    """,
    unsafe_allow_html=True
)
