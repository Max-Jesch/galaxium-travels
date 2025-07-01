# Galaxium Travels Infrastructure

This repository contains infrastructure and demo applications for the imaginary space travel company, **Galaxium Travels**. It is designed to showcase agentic and generative AI capabilities in a modular, easy-to-deploy way.

The main repo is this https://github.com/Max-Jesch/galaxium-travels

#TODO:
- deploy this on code engine. Create the easiest possible startup script! 

## Repository Structure

```
galaxium-travels-infrastructure/
  booking_system/    # FastAPI + SQLite demo booking system
  HR_database/       # HR database app (details inside)
  README.md          # This file
```

## Applications

### 1. Booking System
- **Path:** `booking_system/`
- **Description:** A mock space travel booking system built with FastAPI and SQLite. Demonstrates core booking flows and is ready for agentic integration.
- **Features:**
  - List available flights
  - Book a flight
  - View user bookings
  - Cancel a booking
  - Auto-seeded demo data on startup
- **See:** [`booking_system/README.md`](booking_system/README.md) for setup, usage, and deployment instructions.

### 2. HR Database
- **Path:** `HR_database/`
- **Description:** (Details and instructions inside the app directory.)

## Prerequisites
- Python 3.9+
- [pip](https://pip.pypa.io/en/stable/)
- (Optional) [Fly.io CLI](https://fly.io/docs/hands-on/install-flyctl/) for cloud deployment

## Local Development
Each app is self-contained. To run an app locally:
1. `cd` into the app directory (e.g., `cd booking_system`)
2. Follow the instructions in that app's `README.md`

## Deployment
- Each app can be deployed independently to Fly.io or another platform.
- See the per-app `README.md` for deployment steps and configuration.

## Contributing
Feel free to fork, open issues, or submit pull requests for improvements or new demo apps!

---

**This repository is for demonstration and prototyping purposes only.** 