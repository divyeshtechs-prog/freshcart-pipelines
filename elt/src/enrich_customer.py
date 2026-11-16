import pandas as pd
from elt.src.mock_data import MOCK_CRM_TIER_EVENTS


def enrich_customer(df):
    """Attach the customer tier effective on each order date."""

    result = df.copy()

    events = pd.DataFrame(MOCK_CRM_TIER_EVENTS)

    events["effective_from"] = pd.to_datetime(
        events["effective_from"]
    )

    result["order_date"] = pd.to_datetime(result["order_date"])

    result["cust_email"] = result["cust_email"].str.strip().str.lower()
    events["email"] = events["email"].str.strip().str.lower()

    enriched = []

    for _, order in result.iterrows():
        matching = events[
            (events["email"] == order["cust_email"])
            & (events["effective_from"] <= order["order_date"])
        ].sort_values("effective_from")

        order_data = order.to_dict()

        if not matching.empty:
            latest_event = matching.iloc[-1]
            order_data["cust_id"] = latest_event["cust_id"]
            order_data["customer_tier"] = latest_event["tier"]
        else:
            order_data["cust_id"] = None
            order_data["customer_tier"] = "Unknown"

        enriched.append(order_data)

    return pd.DataFrame(enriched)