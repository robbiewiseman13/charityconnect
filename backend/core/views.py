# core/views.py — aggregator so backend/urls.py can import from here
from django.http import JsonResponse
from .views_payments import create_payment_intent, stripe_webhook  # noqa: F401
create_payment_intent_view = create_payment_intent  # <- alias so urls.py works
from .views_ai import ai_suggest_event  # noqa: F401

def health(request):
    return JsonResponse({"status": "ok"})
