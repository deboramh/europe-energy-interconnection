import sqlite3

import pandas as pd


# ── EXTRACT ────────────────────────────────────────────────
def extract(filepath):
    df = pd.read_csv(filepath)
    print(f"[extract] {len(df)} linhas, {df['Country'].nunique()} países")
    return df


# ── TRANSFORM ──────────────────────────────────────────────
def transform(df):
    # Renomear colunas
    df.columns = ["country", "hour", "res_penetration_pct", "net_position_pct"]

    # Garantir tipos corretos
    df["hour"] = df["hour"].astype(int)
    df["res_penetration_pct"] = df["res_penetration_pct"].astype(float)
    df["net_position_pct"] = df["net_position_pct"].astype(float)

    # Classificar cada hora como importador ou exportador
    df["trade_status"] = df["net_position_pct"].apply(
        lambda x: "exporter" if x > 0 else "importer"
    )

    # Filtrar só Portugal
    pt = df[df["country"] == "Portugal"].copy()
    print(f"[transform] Portugal: {len(pt)} horas")
    return df, pt


# ── LOAD ───────────────────────────────────────────────────
def load(df_all, df_pt, db_path="data/processed/energy.db"):
    conn = sqlite3.connect(db_path)
    df_all.to_sql("country_hourly_2024", conn, if_exists="replace", index=False)
    df_pt.to_sql("portugal_hourly_2024", conn, if_exists="replace", index=False)
    conn.close()
    print(f"[load] Guardado em {db_path}")


# ── MAIN ───────────────────────────────────────────────────
if __name__ == "__main__":
    filepath = "data/raw/europe_interconnection_data/country indicators/country_hourly_chart_2024.csv"
    df = extract(filepath)
    df_all, df_pt = transform(df)
    load(df_all, df_pt)

    # Preview Portugal
    print("\nPortugal — perfil horário:")
    print(df_pt.to_string(index=False))
