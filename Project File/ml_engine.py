from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    model = IsolationForest(contamination=0.05, random_state=42)

    X = df[[
        "demo_ratio_5_17",
        "bio_ratio_5_17",
        "bio_ratio_adult"
    ]]

    df["anomaly_flag"] = model.fit_predict(X)
    df["anomaly_flag"] = df["anomaly_flag"].map({
        -1: "ANOMALY",
         1: "NORMAL"
    })
    return df
