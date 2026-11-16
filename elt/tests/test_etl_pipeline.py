import pandas as pd

from elt.src.extract import extract_all
from elt.src.normalize import normalize_all
from elt.src.transform_silver import transform_silver
from elt.src.deduplicate import deduplicate_orders
from elt.src.enrich_fx import enrich_fx
from elt.src.enrich_customer import enrich_customer
from elt.src.enrich_pincode import enrich_pincode
from elt.src.build_gold import build_gold


def test_freshcart_baseline_pipeline():
    data = extract_all()

    raw = normalize_all(
        data["web_orders"],
        data["mobile_orders"],
    )

    clean, quarantine = transform_silver(raw)
    deduplicated = deduplicate_orders(clean)

    enriched = enrich_fx(deduplicated)
    enriched = enrich_customer(enriched)
    enriched = enrich_pincode(enriched)

    gold = build_gold(enriched)

    assert len(raw) == 8
    assert len(clean) == 6
    assert len(quarantine) == 2
    assert len(deduplicated) == 4

    assert round(gold["amount_inr"].sum(), 2) == 7785.00
    assert gold["loyalty_points"].sum() == 161

def test_unsupported_currency_is_quarantined():
    raw = pd.DataFrame([{
        "order_id": "ORD-TEST",
        "cust_email": "test@example.com",
        "cust_name": "Test Customer",
        "order_date": "2026-09-03",
        "amount": 100,
        "currency": "EUR",
        "pincode": "600041",
        "updated_at": "2026-09-03T10:00:00",
        "source": "website",
    }])

    clean, quarantine = transform_silver(raw)

    assert len(clean) == 0
    assert len(quarantine) == 1
    assert "unsupported_currency" in quarantine.iloc[0]["rejection_reason"]

def test_arjun_tier_change_applies_by_effective_date():
    orders = pd.DataFrame([
        {
            "order_id": "ORD-OLD",
            "cust_email": "arjun.k@yahoo.in",
            "order_date": "2026-08-14",
            "amount_inr": 3536,
        },
        {
            "order_id": "ORD-1002",
            "cust_email": "arjun.k@yahoo.in",
            "order_date": "2026-09-01",
            "amount_inr": 3536,
        },
    ])

    enriched = enrich_customer(orders)
    gold = build_gold(enriched)

    tiers = gold.set_index("order_id")["customer_tier"]

    assert tiers["ORD-OLD"] == "Silver"
    assert tiers["ORD-1002"] == "Gold"

    points = gold.set_index("order_id")["loyalty_points"]

    assert points["ORD-1002"] == 70