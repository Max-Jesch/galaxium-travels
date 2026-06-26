# Backend Test Fix Plan

15 failing tests across 5 issues. All changes are confined to
`booking_system_backend/`. Validate after each step with:

```bash
cd booking_system_backend && pytest
```

---

## Issue 1 — Stale test fixtures use renamed Flight model columns

**Failing tests (9):** `TestBookingService`, `TestBookEndpoint`,
`TestCancelEndpoint`, `TestBookingsEndpoint`

**Root cause:** The `Flight` ORM model replaced `price` → `base_price`
and the single `seats_available` → `economy_seats_available`,
`business_seats_available`, `galaxium_seats_available`. The `Booking`
model also added required columns `seat_class` and `price_paid`. The
fixtures in these four test groups were never updated.

### Changes

**`tests/test_services.py`**

- Lines 274–281, 309–316, 328–334, 346–353, 366–373, 405–412, 435–442:
  Replace `price=…` with `base_price=…` and `seats_available=N` with
  `economy_seats_available=N, business_seats_available=3,
  galaxium_seats_available=1` on every stale `Flight(…)` constructor.
- Lines 294, 394: Replace `flight_obj.seats_available` assertions with
  `flight_obj.economy_seats_available`.
- Lines 379–384, 418–424, 448–453: Add `seat_class="economy"` and
  `price_paid=1000000` to bare `Booking(…)` constructors (columns are
  `nullable=False`).

**`tests/test_rest.py`**

- Lines 282–289, 332–339, 374–381: Same `Flight(…)` column rename.
- Lines 343–348, 385–390: Same `Booking(…)` additions.

**`tests/conftest.py`**

- Lines 82–89: Update `sample_flight_data` fixture:
  `price` → `base_price`, `seats_available` →
  `economy_seats_available` / `business_seats_available` /
  `galaxium_seats_available`.

---

## Issue 2 — route_category filter matches origin OR destination; tests expect destination-only

**Failing tests (2):** `TestFlightService::test_list_flights_filter_by_route_category`,
`TestFlightsEndpoint::test_get_flights_with_route_category_filter`

**Root cause:** Both tests seed `Earth→Mars` and `Earth→Jupiter`, filter
by `inner_planets = ['Earth', 'Mars', 'Venus', 'Mercury']`, and assert
exactly 1 result with `destination == "Mars"`. The current filter at
`services/flight.py:174–178` uses
`or_(Flight.origin.in_(…), Flight.destination.in_(…))`, so
`Earth→Jupiter` also matches because `origin="Earth"` is in
`inner_planets`.

### Change

**`services/flight.py` lines 174–178**

```python
# Before
query = query.filter(
    or_(
        Flight.origin.in_(destinations),
        Flight.destination.in_(destinations)
    )
)

# After
query = query.filter(Flight.destination.in_(destinations))
```

> `or_` is still used in the `departure_time_period == 'night'` branch,
> so leave the import.

---

## Issue 3 — Date-range filter breaks with mixed timestamp formats

**Failing tests (2):** `TestFlightFiltering::test_filter_by_date_range`,
`TestFlightFiltering::test_combined_filters`

**Root cause:** `datetime.fromisoformat()` succeeds on a plain
`"YYYY-MM-DD"` string (it is valid ISO-8601), so the "fallback" branch
is never reached for these inputs. The from-date boundary is then
serialised as `"2026-03-01T00:00:00"` with a `T` separator. SQLite
compares strings lexicographically: `'T'` (0x54) > `' '` (0x20), so
`"2026-03-01 09:00" >= "2026-03-01T00:00:00"` evaluates to **false**,
silently dropping rows that should match.

Fixing the service alone is not enough: the 12 existing `Flight`
constructors in `TestFlightService` and `TestFlightsEndpoint` store
`departure_time` as `"2099-01-01T09:00:00Z"` (ISO with `T`). After
unifying to space-separated boundaries, the to-boundary
`"2099-01-15 23:59"` would fail to match `"2099-01-15T09:00:00Z"` for
the same reason (`'T' > ' '`). Those seeds must also be normalised.

### Changes

**`services/flight.py` lines 96–118** — Replace the two try/except
branches with a single, unified path:

```python
# Before
if departure_date_from:
    try:
        date_from = datetime.fromisoformat(departure_date_from.replace('Z', '+00:00'))
        query = query.filter(Flight.departure_time >= date_from.isoformat())
    except ValueError:
        query = query.filter(Flight.departure_time >= departure_date_from)

if departure_date_to:
    try:
        date_to = datetime.fromisoformat(departure_date_to.replace('Z', '+00:00'))
        date_to = date_to + timedelta(days=1)
        query = query.filter(Flight.departure_time < date_to.isoformat())
    except ValueError:
        query = query.filter(Flight.departure_time <= f'{departure_date_to} 23:59')

# After
if departure_date_from:
    query = query.filter(Flight.departure_time >= f'{departure_date_from[:10]} 00:00')

if departure_date_to:
    query = query.filter(Flight.departure_time <= f'{departure_date_to[:10]} 23:59')
```

Also remove the now-unused `timedelta` import if nothing else uses it.

**`tests/test_services.py`** — Normalise all ISO `departure_time` /
`arrival_time` seeds in `TestFlightService` (~lines 25, 43–44, 47–48,
62–63, 66–67, 81–88, 97–98, ...) to `"YYYY-MM-DD HH:MM"` format
(e.g. `"2099-01-01T09:00:00Z"` → `"2099-01-01 09:00"`).

**`tests/test_rest.py`** — Same normalisation for all ISO seeds in
`TestFlightsEndpoint` (~lines 24–25, 43–44, 47–48, 64–65, 69–70,
85–86, 90–91, ...).

> The 9 stale fixtures fixed in Issue 1 also use ISO timestamps. Normalise
> those at the same time — it is one pass through both files.

---

## Issue 4 — Extract _flight_to_out() helper into services/flight.py

**Failing tests:** none (prevents future breakage / duplication)

**Root cause:** `FlightOut.model_validate(flight_obj)` always fails
because `economy_price`, `business_price`, and `galaxium_price` are
computed values, not ORM columns. The conversion is currently inlined as
a 14-line dict literal inside the result loop at
`services/flight.py:211–225`. Any future call site would have to
duplicate it.

### Change

**`services/flight.py`** — Extract the block into a module-level helper
before `list_flights`, then call it from the loop:

```python
def _flight_to_out(f: Flight) -> FlightOut:
    return FlightOut(
        flight_id=f.flight_id,
        origin=f.origin,
        destination=f.destination,
        departure_time=f.departure_time,
        arrival_time=f.arrival_time,
        base_price=f.base_price,
        economy_seats_available=f.economy_seats_available,
        business_seats_available=f.business_seats_available,
        galaxium_seats_available=f.galaxium_seats_available,
        economy_price=f.base_price,
        business_price=int(f.base_price * 2.5),
        galaxium_price=f.base_price * 5,
    )
```

Replace the `flight_dict` block in the loop with:

```python
result.append((_flight_to_out(f), duration_hours, f))
```

---

## Issue 5 — Pydantic v2 deprecation: class Config → model_config

**Failing tests:** none (will become an error in Pydantic v3)

**Root cause:** `FlightOut`, `BookingOut`, and `UserOut` in `schemas.py`
use the Pydantic v1-style `class Config: from_attributes = True`.

### Change

**`schemas.py`**

```python
# Add to imports
from pydantic import BaseModel, EmailStr, ConfigDict

# Replace in each of the three schema classes
class Config:
    from_attributes = True
# →
model_config = ConfigDict(from_attributes=True)
```

---

## Execution order

| Step | Issue | Files touched | Tests fixed |
|------|-------|---------------|-------------|
| 1 | Issue 1 | `tests/test_services.py`, `tests/test_rest.py`, `tests/conftest.py` | 9 |
| 2 | Issue 3 | `services/flight.py`, `tests/test_services.py`, `tests/test_rest.py` | 2 |
| 3 | Issue 2 | `services/flight.py` | 2 |
| 4 | Issue 4 | `services/flight.py` | 0 |
| 5 | Issue 5 | `schemas.py` | 0 |

Run `pytest` after steps 1, 2, and 3 to confirm the 13 previously
failing tests now pass before continuing with the non-critical cleanups.
