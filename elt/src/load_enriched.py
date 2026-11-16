from pathlib import Path
import pandas as pd


ENRICHED_DIR = Path("elt/data/silver")


def load_enriched(df: pd.DataFrame) -> Path:
    ENRICHED_DIR.mkdir(parents=True, exist_ok=True)

    output_path = ENRICHED_DIR / "enriched_orders.csv"
    df.to_csv(output_path, index=False)

    return output_path