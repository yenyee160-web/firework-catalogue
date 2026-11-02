"""Stateless JSON catalogue and server-verified WhatsApp enquiry links."""
import json
import os
from functools import lru_cache
from pathlib import Path
from django.conf import settings
from django.http import FileResponse, HttpResponse, JsonResponse
from django.views.decorators.http import require_GET, require_POST
from .logic.enquiry import build_enquiry

DATA_FILE = Path(__file__).resolve().parent / "data" / "product.json"

@lru_cache(maxsize=1)
def read_products():
    products = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    if not isinstance(products, list) or not products:
        raise ValueError("Catalogue JSON must contain a non-empty array")
    if len({p["id"] for p in products}) != len(products):
        raise ValueError("Catalogue product IDs must be unique")
    return products

@require_GET
def health(request):
    return JsonResponse({"status": "ok", "database": False})

@require_GET
def products(request):
    return JsonResponse({"products": read_products(), "currency": "MYR"})

@require_POST
def enquiry(request):
    if len(request.body) > 16_384:
        return JsonResponse({"error": "Request too large"}, status=413)
    try:
        payload = json.loads(request.body)
        if not isinstance(payload, dict):
            raise ValueError("Expected JSON object")
        number = os.environ.get("WHATSAPP_NUMBER", "")
        if not number.isdigit() or not 8 <= len(number) <= 15:
            return JsonResponse({"error": "Business contact not configured"}, status=503)
        result = build_enquiry(payload.get("items"), read_products(), number)
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    return JsonResponse(result)

@require_GET
def index(request):
    index_file = settings.WEB_DIST / "index.html"
    if not index_file.is_file():
        return HttpResponse("Frontend not built. Run 'npm run dev' from frontend/.", status=503)
    return FileResponse(index_file.open("rb"), content_type="text/html; charset=utf-8")
