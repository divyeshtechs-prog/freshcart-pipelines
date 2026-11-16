import pandas as pd
from elt.src.mock_data import MOCK_FX_RESPONSES


def enrich_fx(df):
    """Convert all order amounts into INR using daily FX rates."""

    result = df.copy()

    # Build date-wise exchange rate lookup
    fx_rates = {}

    for response in MOCK_FX_RESPONSES:
        for date, rates in response["rates"].items():
            fx_rates[date] = rates["INR"]

    # Preserve original amount and currency
    result["original_amount"] = result["amount"]
    result["original_currency"] = result["currency"]

    # Convert USD orders using their order date
    result["amount_inr"] = result.apply(
        lambda row: (
            row["amount"] * fx_rates[row["order_date"]]
            if row["currency"] == "USD"
            else row["amount"]
        ),
        axis=1,
    )

    result["currency"] = "INR"

    return result