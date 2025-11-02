# Utility module for interacting with the Stripe API
# Handles payment intent creation, retrieval, and webhook verification for CharityConnect

from __future__ import annotations
import stripe
from django.conf import settings

# internal setup helper
def _init():
    # Initialises the stripe SDK with API keys and version settings
    # Ensures all stripe calls use consistent authentication and configuration
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if settings.STRIPE_API_VERSION:
        stripe.api_version = settings.STRIPE_API_VERSION

# create new payment intent
def create_payment_intent(amount_cents: int, currency: str = "eur", *, metadata: dict | None = None):
    # Creates a new stripe PaymentIntent for secure checkout
    # used when donors purchase tickets or make donations
    _init()
    return stripe.PaymentIntent.create(
        amount=amount_cents,
        currency=currency,
        automatic_payment_methods={"enabled": True}, # enables stripes smart payment handling
        metadata=metadata or {},
    )

# retrieve an existing payment intent
def retrieve_payment_intent(pi_id: str):
    # retrieves details of an exisiting stripe paymentintent by its ID
    # Used to confirm payment status or update records post-transaction
    _init()
    return stripe.PaymentIntent.retrieve(pi_id)

# verify incoming stripe webhook events
def construct_event(payload: bytes, sig_header: str):
    # verifies the authenticity of incoming stripe webhook events
    # ensures all payment notifications are securely validated before processing
    _init()
    secret = settings.STRIPE_WEBHOOK_SECRET or ""
    return stripe.Webhook.construct_event(
        payload=payload,
        sig_header=sig_header,
        secret=secret,
    )
