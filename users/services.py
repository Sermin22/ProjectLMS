import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_product_stripe():
    """Создает продукт в страйпе"""

    product = stripe.Product.create(name="Оплата курса")
    return product


def create_price_stripe(amount, product):
    """Создает цену в страйпе"""

    price = stripe.Price.create(currency="rub", unit_amount=int(float(amount) * 100), product=product.get("id"))
    return price


def create_session_stripe(prise):
    """Создает сессию на оплату в страйпе"""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/lms/courses/",
        line_items=[{"price": prise.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def payment_status(session_id):
    session = stripe.checkout.Session.retrieve(
        session_id,
    )
    return session
