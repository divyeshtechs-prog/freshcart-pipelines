from pathlib import Path
import pandas as pd
from elt.src.deduplicate import deduplicate_orders

SILVER_DIR = Path("elt/data/silver")


def load_silver(clean, quarantine):
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    clean_path = SILVER_DIR / "clean_orders.csv"
    quarantine_path = SILVER_DIR / "quarantine_orders.csv"

    clean.to_csv(clean_path, index=False)
    quarantine.to_csv(quarantine_path, index=False)

    deduplicated = deduplicate_orders(clean)
    deduplicated_path = SILVER_DIR / "deduplicated_orders.csv"
    deduplicated.to_csv(deduplicated_path, index=False)

    return clean_path, quarantine_path, deduplicated_path