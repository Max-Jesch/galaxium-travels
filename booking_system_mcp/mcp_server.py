from fastmcp import FastMCP
from pydantic import BaseModel
from db import SessionLocal, init_db
from seed import seed
from models import User, Flight, Booking
from datetime import datetime
from starlette.requests import Request
from starlette.responses import PlainTextResponse

mcp = FastMCP("Booking System MCP")

# Pydantic models for structured output
class FlightOut(BaseModel):
    flight_id: int
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    price: int
    seats_available: int
    class Config:
        from_attributes = True

class BookingIn(BaseModel):
    user_id: int
    name: str
    flight_id: int

class BookingOut(BaseModel):
    booking_id: int
    user_id: int
    flight_id: int
    status: str
    booking_time: str
    class Config:
        from_attributes = True

class UserIn(BaseModel):
    name: str
    email: str

class UserOut(BaseModel):
    user_id: int
    name: str
    email: str
    class Config:
        from_attributes = True

@mcp.tool()
def list_flights() -> list[FlightOut]:
    """List all available flights. 
    Returns a list of flights with origin, destination, times, price, and seats available."""
    db = SessionLocal()
    flights = db.query(Flight).all()
    db.close()
    return [FlightOut.from_orm(f) for f in flights]

@mcp.tool()
def book_flight(user_id: int, name: str, flight_id: int) -> BookingOut:
    """Book a seat on a specific flight for a user. 
    Requires user_id, name, and flight_id. 
    Decrements available seats if successful. 
    Returns booking details or raises an error if booking is not possible."""
    db = SessionLocal()
    flight = db.query(Flight).filter(Flight.flight_id == flight_id).first()
    if not flight:
        db.close()
        raise Exception("Flight not found")
    if flight.seats_available < 1:
        db.close()
        raise Exception("No seats available")
    user = db.query(User).filter(User.user_id == user_id, User.name == name).first()
    if not user:
        db.close()
        raise Exception("User not found or name does not match user ID")
    flight.seats_available -= 1
    new_booking = Booking(
        user_id=user_id,
        flight_id=flight_id,
        status="booked",
        booking_time=datetime.utcnow().isoformat()
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    db.commit()
    out = BookingOut.from_orm(new_booking)
    db.close()
    return out

@mcp.tool()
def get_bookings(user_id: int) -> list[BookingOut]:
    """Retrieve all bookings for a specific user by user_id. 
    Returns a list of booking details for the user."""
    db = SessionLocal()
    bookings = db.query(Booking).filter(Booking.user_id == user_id).all()
    db.close()
    return [BookingOut.from_orm(b) for b in bookings]

@mcp.tool()
def cancel_booking(booking_id: int) -> BookingOut:
    """Cancel an existing booking by its booking_id. 
    Increments available seats for the flight if successful. 
    Returns updated booking details or raises an error if already cancelled or not found."""
    db = SessionLocal()
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        db.close()
        raise Exception("Booking not found")
    if booking.status == "cancelled":
        db.close()
        raise Exception("Booking already cancelled")
    flight = db.query(Flight).filter(Flight.flight_id == booking.flight_id).first()
    if flight:
        flight.seats_available += 1
    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)
    out = BookingOut.from_orm(booking)
    db.close()
    return out

@mcp.tool()
def register_user(name: str, email: str) -> UserOut:
    """Register a new user with a name and unique email. 
    Returns the created user's details or raises an error if the email is already registered."""
    db = SessionLocal()
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        db.close()
        raise Exception("Email already registered")
    new_user = User(name=name, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    out = UserOut.from_orm(new_user)
    db.close()
    return out

@mcp.tool()
def get_user_id(name: str, email: str) -> UserOut:
    """Retrieve a user's information, including user_id, by providing both name and email. 
    Returns user details or raises an error if not found."""
    db = SessionLocal()
    user = db.query(User).filter(User.name == name, User.email == email).first()
    if not user:
        db.close()
        raise Exception("User not found")
    out = UserOut.from_orm(user)
    db.close()
    return out

@mcp.custom_route("/", methods=["GET"])
async def root_health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

# Initialize DB and seed data on startup
init_db()
seed()

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8080)