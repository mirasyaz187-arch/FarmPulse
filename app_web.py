from fastapi import FastAPI, Query
import pandas as pd

app = FastAPI(
    title="FarmPulse API",
    description="Agricultural Price Monitoring API",
    version="1.0"
)

print("🔥 FARMPULSE API STARTING...")


# ==========================================
# LOAD DATA
# ==========================================

try:
    df_prices = pd.read_csv("agrichain_prices.csv")

    df_prices["date"] = pd.to_datetime(
        df_prices["date"],
        errors="coerce"
    )

    print("✅ Agricultural price data loaded!")
    print(f"Total records: {len(df_prices)}")

except Exception as e:
    print("❌ Failed to load agrichain_prices.csv")
    print(e)

    df_prices = pd.DataFrame()


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "message": "FarmPulse Agricultural Price API is running!",
        "records": len(df_prices)
    }


# ==========================================
# 1. COMMODITY LIST
# ==========================================

@app.get("/api/commodities")
def get_commodities():

    if df_prices.empty:
        return {
            "status": "error",
            "data": []
        }

    commodities = (
        df_prices[
            [
                "item_code",
                "item",
                "unit",
                "item_category"
            ]
        ]
        .drop_duplicates()
        .sort_values("item")
    )

    return {
        "status": "success",
        "count": len(commodities),
        "data": commodities.to_dict(
            orient="records"
        )
    }


# ==========================================
# 2. STATE LIST
# ==========================================

@app.get("/api/states")
def get_states():

    if df_prices.empty:
        return {
            "status": "error",
            "data": []
        }

    states = (
        df_prices["state"]
        .dropna()
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    return {
        "status": "success",
        "count": len(states),
        "data": states
    }


# ==========================================
# 3. CURRENT / LATEST PRICE
# ==========================================

@app.get("/api/current-price")
def get_current_price(
    item: str,
    state: str | None = Query(default=None)
):

    if df_prices.empty:
        return {
            "status": "error",
            "data": []
        }

    result = df_prices[
        df_prices["item"].str.contains(
            item,
            case=False,
            na=False
        )
    ].copy()

    if state:
        result = result[
            result["state"].str.contains(
                state,
                case=False,
                na=False
            )
        ]

    if result.empty:
        return {
            "status": "error",
            "message": "No price data found",
            "data": []
        }

    # Latest available date
    latest_date = result["date"].max()

    result = result[
        result["date"] == latest_date
    ].copy()

    return {
        "status": "success",
        "item": item.upper(),
        "latest_date": latest_date.strftime(
            "%Y-%m-%d"
        ),

        "lowest_price": float(
            result["price"].min()
        ),

        "highest_price": float(
            result["price"].max()
        ),

        "average_price": round(
            float(result["price"].mean()),
            2
        ),

        "count": len(result),

        "data": result.to_dict(
            orient="records"
        )
    }


# ==========================================
# 4. PRICE COMPARISON
# ==========================================

@app.get("/api/price-comparison")
def price_comparison(
    item: str,
    state: str | None = Query(default=None)
):

    if df_prices.empty:
        return {
            "status": "error",
            "data": []
        }

    result = df_prices[
        df_prices["item"].str.contains(
            item,
            case=False,
            na=False
        )
    ].copy()

    if state:
        result = result[
            result["state"].str.contains(
                state,
                case=False,
                na=False
            )
        ]

    if result.empty:
        return {
            "status": "error",
            "message": "No price data found",
            "data": []
        }

    # Latest available date
    latest_date = result["date"].max()

    result = result[
        result["date"] == latest_date
    ].copy()

    # Lowest price first
    result = result.sort_values(
        "price"
    )

    return {
        "status": "success",
        "item": item.upper(),
        "latest_date": latest_date.strftime(
            "%Y-%m-%d"
        ),

        "lowest_price": float(
            result["price"].min()
        ),

        "highest_price": float(
            result["price"].max()
        ),

        "average_price": round(
            float(result["price"].mean()),
            2
        ),

        "data": result.to_dict(
            orient="records"
        )
    }


# ==========================================
# 5. PRICE HISTORY
# ==========================================

@app.get("/api/price-history")
def price_history(
    item: str,
    state: str | None = Query(default=None),
    limit: int = Query(
        default=100,
        le=1000
    )
):

    if df_prices.empty:
        return {
            "status": "error",
            "data": []
        }

    result = df_prices[
        df_prices["item"].str.contains(
            item,
            case=False,
            na=False
        )
    ].copy()

    if state:
        result = result[
            result["state"].str.contains(
                state,
                case=False,
                na=False
            )
        ]

    if result.empty:
        return {
            "status": "error",
            "message": "No historical data found",
            "data": []
        }

    # Average price by date
    history = (
        result
        .groupby("date")["price"]
        .mean()
        .reset_index()
        .sort_values(
            "date",
            ascending=False
        )
        .head(limit)
    )

    history["price"] = history["price"].round(2)

    return {
        "status": "success",
        "item": item.upper(),
        "count": len(history),
        "data": history.to_dict(
            orient="records"
        )
    }