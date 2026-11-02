import json
from django.test import Client

client = Client()

def test_health():
    response = client.get("/api/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": False}

def test_catalogue_is_stateless():
    response = client.get("/api/products/")
    assert response.status_code == 200
    products = response.json()["products"]
    assert len(products) == 8
    assert all("price_sen" in item for item in products)

def test_method_restrictions():
    assert client.post("/api/products/").status_code == 405
    assert client.get("/api/enquiry/").status_code == 405

def test_checkout_enquiry(monkeypatch):
    monkeypatch.setenv("WHATSAPP_NUMBER", "60123456789")
    result = client.post("/api/enquiry/",
        data=json.dumps({"items": [{"id": "starlight-fountain", "quantity": 2, "price_sen": 1}]}),
        content_type="application/json")
    assert result.status_code == 200
    assert result.json()["total_sen"] == 7980
    assert result.json()["url"].startswith("https://wa.me/60123456789?text=")

def test_reject_invalid_quantities_and_duplicate_items(monkeypatch):
    monkeypatch.setenv("WHATSAPP_NUMBER", "60123456789")
    for items in [
        [{"id": "starlight-fountain", "quantity": True}],
        [{"id": "starlight-fountain", "quantity": 0}],
        [{"id": "starlight-fountain", "quantity": 26}],
        [{"id": "missing", "quantity": 1}],
        [{"id": "aurora-show", "quantity": 1}],
        [{"id": "starlight-fountain", "quantity": 1}] * 2,
    ]:
        response = client.post("/api/enquiry/", data=json.dumps({"items": items}), content_type="application/json")
        assert response.status_code == 400, items

def test_malformed_request(monkeypatch):
    monkeypatch.setenv("WHATSAPP_NUMBER", "60123456789")
    assert client.post("/api/enquiry/", data="{", content_type="application/json").status_code == 400
