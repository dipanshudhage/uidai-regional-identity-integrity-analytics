def calculate_risk(df):
    df["risk_score"] = (
        2.0 * df["bio_ratio_5_17"] +
        1.5 * df["demo_ratio_5_17"] +
        1.0 * df["bio_ratio_adult"]
    )

    def label(score):
        if score < 0.5:
            return "LOW"
        elif score < 1.2:
            return "MEDIUM"
        else:
            return "HIGH"

    df["risk_level"] = df["risk_score"].apply(label)
    return df
