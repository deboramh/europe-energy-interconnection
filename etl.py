import sqlite3

import pandas as pd

MONTH_MAP = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


def extract(filepath):
    df = pd.read_csv(filepath)
    print(f"[extract] {len(df)} linhas, {df['Country'].nunique()} países")
    return df


def transform(df):
    df.columns = ["country", "hour", "res_penetration_pct", "net_position_pct"]
    df["hour"] = df["hour"].astype(int)
    df["res_penetration_pct"] = df["res_penetration_pct"].astype(float)
    df["net_position_pct"] = df["net_position_pct"].astype(float)
    df["trade_status"] = df["net_position_pct"].apply(
        lambda x: "exporter" if x > 0 else "importer"
    )
    pt = df[df["country"] == "Portugal"].copy()
    print(f"[transform] Portugal: {len(pt)} horas")
    return df, pt


def load(df_all, df_pt, db_path="data/processed/energy.db"):
    conn = sqlite3.connect(db_path)
    df_all.to_sql("country_hourly_2024", conn, if_exists="replace", index=False)
    df_pt.to_sql("portugal_hourly_2024", conn, if_exists="replace", index=False)
    conn.close()
    print(f"[load] Guardado em {db_path}")


def extract_monthly(filepath):
    df = pd.read_csv(filepath)
    print(f"[extract_monthly] {len(df)} linhas, {df['Country'].nunique()} países")
    return df


def transform_monthly(df):
    df.columns = ["country", "month", "res_penetration_pct", "net_position_pct"]
    df["month_num"] = df["month"].map(MONTH_MAP)
    df["res_penetration_pct"] = df["res_penetration_pct"].astype(float)
    df["net_position_pct"] = df["net_position_pct"].astype(float)
    df["trade_status"] = df["net_position_pct"].apply(
        lambda x: "exporter" if x > 0 else "importer"
    )
    pt = df[df["country"] == "Portugal"].copy()
    print(f"[transform_monthly] Portugal: {len(pt)} meses")
    return df, pt


def extract_ntc(filepath):
    df = pd.read_csv(filepath)
    print(f"[extract_ntc] {len(df)} linhas, {df['Border'].nunique()} fronteiras")
    return df


def transform_ntc(df):
    df.columns = [
        "border",
        "from_country",
        "to_country",
        "year",
        "ntc_forward_mw",
        "ntc_backward_mw",
    ]
    df = df[df["year"] == 2024].copy()
    df["capacity_asymmetry_mw"] = df["ntc_forward_mw"] - df["ntc_backward_mw"]
    pt = df[df["border"].str.contains("PT")].copy()
    print(
        f"[transform_ntc] {len(df)} fronteiras em 2024, Portugal: {len(pt)} fronteira(s)"
    )
    return df, pt


def load_ntc(df_all, df_pt, db_path="data/processed/energy.db"):
    conn = sqlite3.connect(db_path)
    df_all.to_sql("borders_ntc_2024", conn, if_exists="replace", index=False)
    df_pt.to_sql("portugal_ntc_2024", conn, if_exists="replace", index=False)
    conn.close()
    print(f"[load_ntc] Guardado em {db_path}")


def load_monthly(df_all, df_pt, db_path="data/processed/energy.db"):
    conn = sqlite3.connect(db_path)
    df_all.to_sql("country_monthly_2024", conn, if_exists="replace", index=False)
    df_pt.to_sql("portugal_monthly_2024", conn, if_exists="replace", index=False)
    conn.close()
    print(f"[load_monthly] Guardado em {db_path}")


def extract_flows(filepath):
    df = pd.read_csv(filepath)
    print(
        f"[extract_flows] {len(df)} linhas, {df['Country From'].nunique()} países de origem"
    )
    return df


def transform_flows(df):
    df.columns = ["country_from", "hour", "country_to", "flow_pct"]
    df["hour"] = df["hour"].astype(int)
    df["flow_pct"] = df["flow_pct"].astype(float)
    df["flow_direction"] = df["flow_pct"].apply(
        lambda x: "export" if x > 0 else "import"
    )
    pt = df[
        df["country_from"].str.contains("PT|Portugal", case=False)
        | df["country_to"].str.contains("PT|Portugal", case=False)
    ].copy()
    print(f"[transform_flows] {len(df)} linhas, Portugal: {len(pt)} linha(s)")
    return df, pt


def load_flows(df_all, df_pt, db_path="data/processed/energy.db"):
    conn = sqlite3.connect(db_path)
    df_all.to_sql("flows_hourly_2024", conn, if_exists="replace", index=False)
    df_pt.to_sql("portugal_flows_hourly_2024", conn, if_exists="replace", index=False)
    conn.close()
    print(f"[load_flows] Guardado em {db_path}")


def extract_imp_pot(filepath):
    df = pd.read_csv(filepath)
    print(f"[extract_imp_pot] {len(df)} linhas, {df['Country'].nunique()} países")
    return df


def transform_imp_pot(df):
    df.columns = [
        "country",
        "current_2024_mw",
        "reference_mw",
        "projects_mw",
        "needs_mw",
    ]
    print(f"[transform_imp_pot] {len(df)} países")
    return df


def load_imp_pot(df, db_path="data/processed/energy.db"):
    conn = sqlite3.connect(db_path)
    df.to_sql("import_potential_2030", conn, if_exists="replace", index=False)
    conn.close()
    print(f"[load_imp_pot] Guardado em {db_path}")


if __name__ == "__main__":
    # Horário
    df = extract(
        "data/raw/europe_interconnection_data/country indicators/country_hourly_chart_2024.csv"
    )
    df_all, df_pt = transform(df)
    load(df_all, df_pt)
    print("\nPortugal — perfil horário:")
    print(df_pt.to_string(index=False))

    print("\n" + "=" * 50 + "\n")

    # Mensal
    df_m = extract_monthly(
        "data/raw/europe_interconnection_data/country indicators/country_monthly_chart_2024.csv"
    )
    df_all_m, df_pt_m = transform_monthly(df_m)
    load_monthly(df_all_m, df_pt_m)
    print("\nPortugal — perfil mensal:")
    print(df_pt_m.to_string(index=False))

    print("\n" + "=" * 50 + "\n")

    # Capacidade de interligação
    df_n = extract_ntc(
        "data/raw/europe_interconnection_data/Interconnectors/REF_NTC.csv"
    )
    df_all_n, df_pt_n = transform_ntc(df_n)
    load_ntc(df_all_n, df_pt_n)
    print("\nPortugal — capacidade de interligação:")
    print(df_pt_n.to_string(index=False))

    print("\n" + "=" * 50 + "\n")

    # Fluxos transfronteiriços
    df_f = extract_flows(
        "data/raw/europe_interconnection_data/Flow indicators/flows_hourly_chart_2024.csv"
    )
    df_all_f, df_pt_f = transform_flows(df_f)
    load_flows(df_all_f, df_pt_f)
    print("\nPortugal — fluxos horários:")
    print(df_pt_f.to_string(index=False))

    print("\n" + "=" * 50 + "\n")

    # Potencial de importação
    df_imp = extract_imp_pot(
        "data/raw/europe_interconnection_data/Import potential/imp_pot_chart_2030.csv"
    )
    df_imp = transform_imp_pot(df_imp)
    load_imp_pot(df_imp)
    print("\nPotencial de importação 2030:")
    print(df_imp.to_string(index=False))
