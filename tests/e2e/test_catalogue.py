"""Run with --browser chromium; outgoing WhatsApp links must never be clicked."""
import os
import re
import pytest
from playwright.sync_api import expect

@pytest.mark.smoke
def test_catalogue_loads(page, base_url):
    page.goto(base_url)
    expect(page.get_by_role("heading", name=re.compile("Make every"))).to_be_visible()
    expect(page.get_by_test_id("product-card")).to_have_count(8)

@pytest.mark.smoke
def test_search(page, base_url):
    page.goto(base_url)
    page.get_by_role("textbox", name="Search products").fill("Golden Spark")
    expect(page.get_by_test_id("product-card")).to_have_count(1)

@pytest.mark.nonprod
def test_cart_total_and_quantity(page, base_url):
    page.goto(base_url)
    page.get_by_test_id("add-starlight-fountain").click()
    expect(page.get_by_test_id("cart-total")).to_have_text("RM 39.90")
    page.get_by_role("button", name="Increase Starlight Fountain quantity").click()
    expect(page.get_by_test_id("cart-total")).to_have_text("RM 79.80")
    page.reload()
    expect(page.get_by_test_id("cart-total")).to_have_text("RM 79.80")

@pytest.mark.nonprod
def test_unavailable_is_disabled(page, base_url):
    page.goto(base_url)
    expect(page.get_by_test_id("add-aurora-show")).to_be_disabled()

@pytest.mark.nonprod
def test_whatsapp_is_prepared_but_never_sent(page, base_url):
    page.add_init_script("window.__openedWhatsApp = null; window.open = url => { window.__openedWhatsApp = url; return null; };")
    page.goto(base_url)
    page.get_by_test_id("add-golden-spark").click()
    page.get_by_role("button", name=re.compile("Prepare WhatsApp")).click()
    page.wait_for_function("() => Boolean(window.__openedWhatsApp)")
    # The popup is intercepted in-browser, so tests do not contact WhatsApp.
    assert page.evaluate("window.__openedWhatsApp").startswith("https://wa.me/")
