import stripe
from config.settings import STRIPE_API_KEY


stripe.api_key = STRIPE_API_KEY


def create_stripe_price(course):
    price = stripe.Price.create(
        unit_amount=200,
        currency="USD",
        product_data={"name": course.title, "id": course.id},
    )

    return price


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 2}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def session_checkout(session_id):
    session = stripe.checkout.Session.retrieve(
        session_id,
    )
    return session.get("status")
