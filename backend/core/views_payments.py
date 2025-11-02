# Payment-related API endpoints for CharityConnect
# Handles Stripe PaymentIntent creation and webhook event processing

import logging
import stripe
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .stripe_utils import create_payment_intent as _create_pi, construct_event

logger = logging.getLogger(__name__)

# create PaymentIntent endpoint
@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([]) 
def create_payment_intent(request):
    # creates a stripe PaymentIntent for secure checkout
    # used when donors make a payment or purchase tickets
    data = request.data or {}
    try:
        amount_cents = int(data.get("amount_cents"))
    except Exception:
        return Response({"error": "amount_cents (int) is required"}, status=400)

    currency = (data.get("currency") or "eur").lower()
    metadata = data.get("metadata") or {}

    try:
        # create PaymentIntent via helper utility
        pi = _create_pi(amount_cents, currency, metadata=metadata)
        client_secret = getattr(pi, "client_secret", None)
        if not client_secret:
            logger.error("Stripe PI created without client_secret: %r", pi)
            return Response({"error": "Failed to create PaymentIntent"}, status=500)
        return Response({"clientSecret": client_secret}, status=200)

    # handle stripe specific and unexpected errors
    except stripe.error.StripeError as e:
        logger.exception("Stripe error creating PI: %s", e)
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        logger.exception("Unexpected error creating PI")
        return Response({"error": "internal error"}, status=500)

# stripe webhook endpoints
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def stripe_webhook(request):
    # receives and verifies stripe webhook events
    # used to confirm payments, trigger receipts, or hadle failed transactions
    payload = request.body  
    sig = request.headers.get("Stripe-Signature", "")

    try:
        # validate the webhook signature and construct event safely
        event = construct_event(payload, sig) 
    except Exception as e:
        logger.warning("Invalid Stripe signature or payload: %s", e)
        return Response({"error": "invalid signature"}, status=400)

    event_type = event.get("type")
    logger.info("Stripe event received: %s", event_type)

    try:
        # handle relevant stripe event types
        if event_type == "payment_intent.succeeded":
            pi = event["data"]["object"]
            # TODO: mark donation/order as paid, enqueue receipt email, etc.
            logger.info("PaymentIntent succeeded: %s for %s %s",
                        pi.get("id"), pi.get("amount_received"), pi.get("currency"))

        elif event_type == "payment_intent.payment_failed":
            pi = event["data"]["object"]
            err = (pi.get("last_payment_error") or {}).get("message")
            logger.info("PaymentIntent failed: %s (%s)", pi.get("id"), err)

        elif event_type == "charge.succeeded":
            charge = event["data"]["object"]
            logger.info("Charge succeeded: %s", charge.get("id"))

        # acknowledge event receipt
        return Response({"received": True}, status=status.HTTP_200_OK)

    # log unexpected errors but still return 200 to acknowledge event receipt
    except Exception as e:
        logger.exception("Error handling Stripe event %s: %s", event_type, e)
        return Response({"received": True}, status=status.HTTP_200_OK)
