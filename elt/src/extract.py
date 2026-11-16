from elt.src.mock_data import (
    MOCK_WEB_ORDERS,
    MOCK_MOBILE_ORDERS,
    MOCK_CRM_TIER_EVENTS,
    MOCK_FX_RESPONSES,
    mock_pincode_response,
)


def extract_all():
    """Extract raw data from all mock API sources."""

    return {
        "web_orders": MOCK_WEB_ORDERS.copy(),
        "mobile_orders": MOCK_MOBILE_ORDERS.copy(),
        "crm_tier_events": MOCK_CRM_TIER_EVENTS.copy(),
        "fx_responses": MOCK_FX_RESPONSES.copy(),
    }


def extract_pincode(pin):
    """Simulate an India Post pincode API request."""
    return mock_pincode_response(pin)