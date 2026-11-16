import pandas as pd
from elt.src.extract import extract_pincode


STATE_REGIONS = {
    "Tamil Nadu": "South",
    "Karnataka": "South",
    "Maharashtra": "West",
    "Uttar Pradesh": "North",
    "Madhya Pradesh": "Central",
}


def enrich_pincode(df):
    result = df.copy()
    geography = {}

    for pin in result["pincode"].astype(str).unique():
        response = extract_pincode(pin)

        if response and response[0]["Status"] == "Success":
            office = response[0]["PostOffice"][0]
            state = office["State"]

            geography[pin] = {
                "city": office["District"],
                "state": state,
                "region": STATE_REGIONS.get(state),
            }
        else:
            geography[pin] = {
                "city": None,
                "state": None,
                "region": None,
            }

    result["city"] = result["pincode"].astype(str).map(
        lambda pin: geography[pin]["city"]
    )
    result["state"] = result["pincode"].astype(str).map(
        lambda pin: geography[pin]["state"]
    )
    result["region"] = result["pincode"].astype(str).map(
        lambda pin: geography[pin]["region"]
    )

    return result