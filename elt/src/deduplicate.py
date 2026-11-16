""" 

def deduplicate_orders(df: pd.DataFrame) -> pd.DataFrame:
   # Keep the latest record for each order ID.

    result = df.copy()

    # 7A- result["updated_at"] = pd.to_datetime(result["updated_at"])
    # 7B-
    result["updated_at"] = pd.to_datetime(
    result["updated_at"], format="mixed", errors="coerce"
    )
    result = result.sort_values(
        by="updated_at",
        ascending=False
    )

    result = result.drop_duplicates(
        subset=["order_id"],
        keep="first"
    )

    return result.sort_values("order_id").reset_index(drop=True)"""

import pandas as pd


def deduplicate_orders(df: pd.DataFrame) -> pd.DataFrame:
    #Keep the latest record, preferring mobile when timestamps tie.

    result = df.copy()

    result["updated_at"] = pd.to_datetime(
        result["updated_at"], format="mixed"
    )

    result["source_priority"] = result["source"].map({
        "website": 1,
        "mobile": 2,
    })

    result = result.sort_values(
        by=["updated_at", "source_priority"],
        ascending=[False, False],
        kind="stable",
    )

    result = result.drop_duplicates(
        subset=["order_id"],
        keep="first",
    )

    return (
        result.drop(columns=["source_priority"])
        .sort_values("order_id")
        .reset_index(drop=True)
    )