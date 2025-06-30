from models import Base, User, Flight
from db import engine, SessionLocal

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Clear existing data
    db.query(User).delete()
    db.query(Flight).delete()
    db.commit()
    # Add demo users
    users = [
        User(name="Alice", email="alice@example.com"),
        User(name="Bob", email="bob@example.com"),
    ]
    db.add_all(users)
    # Add demo flights
    flights = [
        Flight(
            origin="Earth",
            destination="Mars",
            departure_time="2099-01-01T09:00:00Z",
            arrival_time="2099-01-01T17:00:00Z",
            price=1000000,
            seats_available=5
        ),
        Flight(
            origin="Earth",
            destination="Moon",
            departure_time="2099-01-02T10:00:00Z",
            arrival_time="2099-01-02T14:00:00Z",
            price=500000,
            seats_available=3
        ),
    ]
    db.add_all(flights)
    db.commit()
    db.close()
    print("Database seeded!")

if __name__ == "__main__":
    seed() 