import pandas as pd
import numpy as np

def generate_features(enrol, demo, bio):
    # --------------------------------------------------
    # 1. AGGREGATE EACH DATASET FIRST (CRITICAL)
    # --------------------------------------------------

    enrol_agg = (
        enrol
        .groupby(["state", "district", "pincode"], as_index=False)
        .agg({
            "age_0_5": "sum",
            "age_5_17": "sum",
            "age_18_greater": "sum"
        })
    )

    demo_agg = (
        demo
        .groupby(["state", "district", "pincode"], as_index=False)
        .agg({
            "demo_age_5_17": "sum",
            "demo_age_17_": "sum"
        })
    )

    bio_agg = (
        bio
        .groupby(["state", "district", "pincode"], as_index=False)
        .agg({
            "bio_age_5_17": "sum",
            "bio_age_17_": "sum"
        })
    )

    # --------------------------------------------------
    # 2. SAFE ONE-TO-ONE MERGES (NO EXPLOSION)
    # --------------------------------------------------

    df = enrol_agg.merge(demo_agg, on=["state", "district", "pincode"], how="left")
    df = df.merge(bio_agg, on=["state", "district", "pincode"], how="left")

    df.fillna(0, inplace=True)

    # --------------------------------------------------
    # 3. MEMORY-SAFE RATIOS
    # --------------------------------------------------

    df["age_5_17"] = df["age_5_17"].replace(0, np.nan)
    df["age_18_greater"] = df["age_18_greater"].replace(0, np.nan)

    df["demo_ratio_5_17"] = df["demo_age_5_17"] / df["age_5_17"]
    df["bio_ratio_5_17"]  = df["bio_age_5_17"]  / df["age_5_17"]
    df["bio_ratio_adult"] = df["bio_age_17_"]   / df["age_18_greater"]

    df.fillna(0, inplace=True)

    return df
