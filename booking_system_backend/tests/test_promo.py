import pytest
import sys
from pathlib import Path
from datetime import date, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from models import PromoCode, User, Flight
from schemas import ErrorResponse
from services import promo as promo_service
from services import booking


def make_promo(db, code="SAVE10", percent_off=10, days_from_now=30, max_uses=100, uses=0):
    p = PromoCode(
        code=code,
        percent_off=percent_off,
        valid_from=date.today() - timedelta(days=1),
        valid_until=date.today() + timedelta(days=days_from_now),
        max_uses=max_uses,
        uses=uses,
    )
    db.add(p)
    db.commit()
    return p


class TestPromoValidation:
    def test_valid_code_applies_discount(self, db_session):
        make_promo(db_session, code="SAVE10", percent_off=10)
        result = promo_service.validate_promo(db_session, "SAVE10", 1000)
        assert result.valid is True
        assert result.percent_off == 10
        assert result.savings == 100
        assert result.discounted_price == 900

    def test_case_insensitive(self, db_session):
        make_promo(db_session, code="SAVE10", percent_off=10)
        result = promo_service.validate_promo(db_session, "save10", 1000)
        assert result.valid is True

    def test_invalid_code(self, db_session):
        result = promo_service.validate_promo(db_session, "NOPE", 1000)
        assert result.valid is False
        assert result.error is not None

    def test_expired_code(self, db_session):
        p = PromoCode(
            code="OLD",
            percent_off=10,
            valid_from=date.today() - timedelta(days=30),
            valid_until=date.today() - timedelta(days=1),
            max_uses=100,
            uses=0,
        )
        db_session.add(p)
        db_session.commit()
        result = promo_service.validate_promo(db_session, "OLD", 1000)
        assert result.valid is False
        assert "expired" in result.error.lower()

    def test_maxed_out_code(self, db_session):
        make_promo(db_session, code="FULL", max_uses=5, uses=5)
        result = promo_service.validate_promo(db_session, "FULL", 1000)
        assert result.valid is False
        assert "usage limit" in result.error.lower()


class TestPromoWithBooking:
    def test_booking_applies_promo_discount(self, db_session):
        make_promo(db_session, code="SPACE20", percent_off=20)
        db_session.add(User(name="Alice", email="alice@test.com"))
        db_session.add(Flight(
            origin="Earth", destination="Mars",
            departure_time="2099-01-01 09:00", arrival_time="2099-01-01 17:00",
            base_price=1000,
            economy_seats_available=5, business_seats_available=3, galaxium_seats_available=1,
        ))
        db_session.commit()
        user_obj = db_session.query(User).first()
        flight_obj = db_session.query(Flight).first()

        result = booking.book_flight(
            db_session, user_obj.user_id, "Alice", flight_obj.flight_id,
            seat_class="economy", promo_code="SPACE20"
        )
        assert not isinstance(result, ErrorResponse)
        assert result.price_paid == 800  # 1000 - 20%

    def test_booking_without_promo_unchanged(self, db_session):
        make_promo(db_session, code="SPACE20", percent_off=20)
        db_session.add(User(name="Bob", email="bob@test.com"))
        db_session.add(Flight(
            origin="Earth", destination="Mars",
            departure_time="2099-01-01 09:00", arrival_time="2099-01-01 17:00",
            base_price=1000,
            economy_seats_available=5, business_seats_available=3, galaxium_seats_available=1,
        ))
        db_session.commit()
        user_obj = db_session.query(User).first()
        flight_obj = db_session.query(Flight).first()

        result = booking.book_flight(
            db_session, user_obj.user_id, "Bob", flight_obj.flight_id,
            seat_class="economy"
        )
        assert not isinstance(result, ErrorResponse)
        assert result.price_paid == 1000

    def test_invalid_promo_does_not_block_booking(self, db_session):
        """An invalid promo code should be silently ignored — booking proceeds at full price."""
        db_session.add(User(name="Charlie", email="charlie@test.com"))
        db_session.add(Flight(
            origin="Earth", destination="Mars",
            departure_time="2099-01-01 09:00", arrival_time="2099-01-01 17:00",
            base_price=1000,
            economy_seats_available=5, business_seats_available=3, galaxium_seats_available=1,
        ))
        db_session.commit()
        user_obj = db_session.query(User).first()
        flight_obj = db_session.query(Flight).first()

        result = booking.book_flight(
            db_session, user_obj.user_id, "Charlie", flight_obj.flight_id,
            seat_class="economy", promo_code="BADCODE"
        )
        assert not isinstance(result, ErrorResponse)
        assert result.price_paid == 1000  # Full price — bad code ignored
