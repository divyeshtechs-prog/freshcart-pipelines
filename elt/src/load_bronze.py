from pathlib import Path
import pandas as pd


BRONZE_DIR = Path("elt/data/bronze")


def load_bronze(df: pd.DataFrame) -> Path:
    """Save normalized raw records into the Bronze layer."""

    BRONZE_DIR.mkdir(parents=True, exist_ok=True)

    output_path = BRONZE_DIR / "raw_orders.csv"
    df.to_csv(output_path, index=False)

    return output_path