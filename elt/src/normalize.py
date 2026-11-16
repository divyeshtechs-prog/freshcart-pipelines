import pandas as pd


def normalize_web_orders(records):
    """Convert website orders into a common tabular structure."""

    normalized = []

    for record in records:
        normalized.append({
            "order_id": record.get("order_id"),
            "cust_email": record.get("cust_email"),
            "cust_name": record.get("cust_name"),
            "order_date": record.get("order_date"),
            "amount": record.get("amount"),
            "currency": record.get("currency"),
            "pincode": record.get("pincode"),
            "updated_at": record.get("updated_at"),
            "source": "website",
        })

    return pd.DataFrame(normalized)


def normalize_mobile_orders(records):
    """Flatten nested mobile orders into the same structure."""

    normalized = []

    for record in records:
        customer = record.get("customer", {})
        total = record.get("total", {})

        normalized.append({
            "order_id": record.get("orderId"),
            "cust_email": customer.get("email"),
            "cust_name": customer.get("name"),
            "order_date": record.get("orderDate"),
            "amount": total.get("value"),
            "currency": total.get("currency"),
            "pincode": record.get("deliveryPin"),
            "updated_at": record.get("updatedAt"),
            "source": "mobile",
        })

    return pd.DataFrame(normalized)


def normalize_all(web_records, mobile_records):
    """Combine both sources into one standardized dataset."""

    web_df = normalize_web_orders(web_records)
    mobile_df = normalize_mobile_orders(mobile_records)

    return pd.concat([web_df, mobile_df], ignore_index=True)