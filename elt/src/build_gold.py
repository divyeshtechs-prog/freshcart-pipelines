from pathlib import Path
import pandas as pd

GOLD_DIR = Path("elt/data/gold")

TIER_MULTIPLIERS = {
    "Silver": 1,
    "Gold": 2,
    "Platinum": 3,
}


def build_gold(df: pd.DataFrame) -> pd.DataFrame:
    """Build the Gold orders table with revenue and loyalty points."""
    result = df.copy()

    result["tier_multiplier"] = (
        result["customer_tier"].map(TIER_MULTIPLIERS).fillna(0).astype(int)
    )

    result["loyalty_points"] = (
        (result["amount_inr"] // 100) * result["tier_multiplier"]
    ).astype(int)

    return result


def load_gold(df: pd.DataFrame) -> Path:
    GOLD_DIR.mkdir(parents=True, exist_ok=True)
    output_path = GOLD_DIR / "gold_orders.csv"
    df.to_csv(output_path, index=False)
    return output_path