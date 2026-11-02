import pytest
from catalogue.logic.enquiry import build_enquiry

PRODUCTS = [{"id": "sample", "name": "Sample", "price_sen": 350, "available": True}]

def test_total_and_encoding():
    result = build_enquiry([{"id": "sample", "quantity": 2}], PRODUCTS, "60123456789")
    assert result["total_sen"] == 700
    assert "Sample%20x2" in result["url"]
    assert "No%20order%20is%20placed" in result["url"]

@pytest.mark.parametrize("items", [[], None, [{"id": "sample", "quantity": 0}],
    [{"id": "sample", "quantity": True}], [{"id": "missing", "quantity": 1}],
    [{"id": "sample", "quantity": 1}] * 2])
def test_rejects_bad_input(items):
    with pytest.raises(ValueError):
        build_enquiry(items, PRODUCTS, "60123456789")
