import re
import pandas as pd


def clean_email(value):
    if pd.isna(value):
        return None
    return str(value).strip().lower()


def clean_amount(value):
    if pd.isna(value):
        return None

    cleaned = str(value).replace(",", "").replace("₹", "").strip()

    try:
        return float(cleaned)
    except ValueError:
        return None


def clean_date(value):
    if pd.isna(value):
        return pd.NaT

    value = str(value).strip()

    if re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        return pd.to_datetime(value, format="%Y-%m-%d", errors="coerce")

    return pd.to_datetime(value, dayfirst=True, errors="coerce")

def valid_email(value):
    return bool(
        re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", str(value))
    )


def valid_pincode(value):
    return bool(re.fullmatch(r"\d{6}", str(value)))


def transform_silver(df):
    """Clean and validate normalized orders."""

    result = df.copy()

    # 1. Standardize text fields
    result["cust_email"] = result["cust_email"].apply(clean_email)
    result["cust_name"] = result["cust_name"].astype(str).str.strip().str.title()
    result["currency"] = result["currency"].astype(str).str.strip().str.upper()
    result["pincode"] = result["pincode"].astype(str).str.strip()

    # 2. Standardize dates and amounts
    result["order_date"] = result["order_date"].apply(clean_date)
    #7-G
    result["updated_at"] = pd.to_datetime(
    result["updated_at"].astype(str).str.replace("T", " ", regex=False),
    errors="coerce",
)
    result["amount"] = result["amount"].apply(clean_amount)

    # 3. Convert dates into a consistent format
    result["order_date"] = result["order_date"].dt.strftime("%Y-%m-%d")

    # 4. Validate records
    result["rejection_reason"] = ""

    result.loc[
        ~result["cust_email"].apply(valid_email),
        "rejection_reason"
    ] += "invalid_email;"

    result.loc[
        result["amount"].notna() & (result["amount"] <= 0),
        "rejection_reason"
    ] += "invalid_amount;"

    result.loc[
        ~result["currency"].isin(["INR", "USD"]),
        "rejection_reason"
    ] += "unsupported_currency;"

    result.loc[
        ~result["pincode"].apply(valid_pincode),
        "rejection_reason"
    ] += "invalid_pincode;"

    # Missing amount is temporarily retained because another
    # copy of the same order may contain the correct amount.

    # 5. Separate clean and rejected records
    clean = result[result["rejection_reason"] == ""].copy()
    quarantine = result[result["rejection_reason"] != ""].copy()

    return clean, quarantine