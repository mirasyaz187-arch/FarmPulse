import pandas as pd

print("🔥 PRICECATCHER DATA LOADER 🔥")

URL_DATA = "https://storage.data.gov.my/pricecatcher/pricecatcher_2026-09.csv"
URL_ITEM = "https://storage.data.gov.my/pricecatcher/lookup_item.csv"
URL_PREMISE = "https://storage.data.gov.my/pricecatcher/lookup_premise.csv"


def get_pricecatcher_data():
    print("[1] Downloading PriceCatcher price data...")

    df_price = pd.read_csv(URL_DATA)

    print(f"[2] Price records: {len(df_price)}")

    print("[3] Downloading item lookup...")
    df_item = pd.read_csv(URL_ITEM)

    print("[4] Downloading premise lookup...")
    df_premise = pd.read_csv(URL_PREMISE)

    # Gabungkan nama barang
    df = df_price.merge(
        df_item,
        on="item_code",
        how="left"
    )

    # Gabungkan maklumat lokasi
    df = df.merge(
        df_premise,
        on="premise_code",
        how="left"
    )

    print("[5] Data successfully combined!")

    print(df.head())

    return df


if __name__ == "__main__":
    df = get_pricecatcher_data()

    df.to_csv(
        "pricecatcher_prices.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("✅ Saved as pricecatcher_prices.csv")