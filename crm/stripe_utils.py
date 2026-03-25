import stripe
from django.conf import settings


def get_stripe():
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe


def create_checkout_session(
    product,
    quantity=1,
    success_url=None,
    cancel_url=None,
    customer_email=None,
    metadata=None,
):
    stripe_instance = get_stripe()

    checkout_session = stripe_instance.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": product.name,
                        "description": (
                            product.description[:500]
                            if product.description
                            else None
                        ),
                    },
                    "unit_amount": int(product.price * 100),
                },
                "quantity": quantity,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
        customer_email=customer_email,
        metadata=metadata or {},
        billing_address_collection="required",
    )

    return checkout_session


def create_order_bump_session(
    main_product,
    bump_products=None,
    success_url=None,
    cancel_url=None,
    customer_email=None,
    metadata=None,
):
    stripe_instance = get_stripe()

    line_items = [
        {
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": main_product.name,
                    "description": (
                        main_product.description[:500]
                        if main_product.description
                        else None
                    ),
                },
                "unit_amount": int(main_product.price * 100),
            },
            "quantity": 1,
        }
    ]

    if bump_products:
        for bump in bump_products:
            price = (
                bump.display_price
                if hasattr(bump, "display_price")
                else bump.price
            )
            line_items.append(
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"[ADD-ON] {bump.product.name}",
                            "description": (
                                bump.description[:500]
                                if bump.description
                                else None
                            ),
                        },
                        "unit_amount": int(price * 100),
                    },
                    "quantity": 1,
                }
            )

    checkout_session = stripe_instance.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
        customer_email=customer_email,
        metadata=metadata or {},
        billing_address_collection="required",
    )

    return checkout_session


def create_upsell_payment_intent(
    product,
    customer_id=None,
    metadata=None,
):
    stripe_instance = get_stripe()

    payment_intent = stripe_instance.PaymentIntent.create(
        amount=int(product.price * 100),
        currency="usd",
        customer=customer_id,
        metadata=metadata or {},
        automatic_payment_methods={"enabled": True},
    )

    return payment_intent


def retrieve_session(session_id):
    stripe_instance = get_stripe()
    return stripe_instance.checkout.Session.retrieve(session_id)


def retrieve_payment_intent(payment_intent_id):
    stripe_instance = get_stripe()
    return stripe_instance.PaymentIntent.retrieve(payment_intent_id)


def construct_webhook_event(payload, sig_header):
    stripe_instance = get_stripe()
    return stripe_instance.Webhook.construct_event(
        payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
    )
