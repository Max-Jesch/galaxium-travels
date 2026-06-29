from datetime import date
from sqlalchemy.orm import Session
from models import PromoCode
from schemas import PromoValidationResult


def validate_promo(db: Session, code: str, price: int) -> PromoValidationResult:
    """Validate a promo code and return the discounted price if valid."""
    promo = db.query(PromoCode).filter(PromoCode.code == code.upper()).first()

    if not promo:
        return PromoValidationResult(valid=False, error="Invalid promo code")

    today = date.today()
    if today < promo.valid_from or today > promo.valid_until:
        return PromoValidationResult(valid=False, error="Promo code has expired")

    if promo.uses >= promo.max_uses:
        return PromoValidationResult(valid=False, error="Promo code has reached its usage limit")

    savings = int(price * promo.percent_off / 100)
    discounted_price = price - savings

    return PromoValidationResult(
        valid=True,
        code=promo.code,
        percent_off=promo.percent_off,
        discounted_price=discounted_price,
        savings=savings,
    )


def apply_promo(db: Session, code: str) -> PromoCode | None:
    """Increment the use counter for a promo code. Returns the promo if valid, None otherwise."""
    promo = db.query(PromoCode).filter(PromoCode.code == code.upper()).first()
    if not promo:
        return None
    today = date.today()
    if today < promo.valid_from or today > promo.valid_until:
        return None
    if promo.uses >= promo.max_uses:
        return None
    promo.uses += 1
    return promo
