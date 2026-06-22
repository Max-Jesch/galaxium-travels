# Implementation Plan — Issue #32: Destination Detail Pages (`/destinations/:slug`)

> **Issue:** [#32](https://github.com/IBM/galaxium-travels/issues/32) · Tier 2 · ~2 hours  
> **Branch target:** `main`

---

## 1. Goal

Add a per-destination page that gives travellers context about where they are going: physical facts, hazards, a small gallery, and a live "flights departing soon" list drawn from the existing `/flights` API.

---

## 2. Codebase snapshot (relevant to this issue)

| Area | Key findings |
|---|---|
| **API** | `GET /flights?destination=<name>` already works via `flight.list_flights()` — no backend changes needed. |
| **Frontend router** | `App.tsx` uses React Router v6 `<Routes>`. Currently three routes: `/`, `/flights`, `/bookings`. |
| **Flight data** | Seven distinct destinations seeded in `seed.py`: `Earth`, `Mars`, `Moon`, `Venus`, `Jupiter`, `Europa`, `Pluto`. |
| **`getFlights()`** | `api.ts` accepts a `destination` filter string and passes it as a query param. Ready to use. |
| **Tailwind tokens** | Custom palette: `space-dark`, `space-blue`, `cosmic-purple`, `nebula-pink`, `alien-green`, `solar-orange`, `star-white`; gradients `space-gradient`, `cosmic-gradient`. |
| **`glass-card`** | Global CSS utility (`bg-white/5 backdrop-blur-md border border-white/10 rounded-xl`). Used everywhere. |
| **Component library** | `Card`, `Button`, `LoadingSpinner` in `src/components/common/`. `motion` from `framer-motion` is standard. |
| **`FlightCard`** | Shows origin → destination + seat classes. Currently no link to a destination page. |
| **`Home.tsx`** | Four feature cards in a grid; a CTA section. Has room for a "Destinations" row between the feature grid and the CTA. |
| **`formatters.ts`** | `formatDate`, `formatTime`, `formatCurrency`, `calculateDuration` — all useful on the detail page. |
| **No backend changes** | The issue is purely frontend; the existing `/flights` endpoint with a `destination` filter covers everything. |

---

## 3. Destination data model

Each destination needs:

```ts
interface DestinationData {
  slug: string;               // URL slug, lowercase, e.g. "mars"
  name: string;               // Display name, e.g. "Mars"
  tagline: string;            // One-line marketing hook
  description: string;        // 2–3 sentence overview
  facts: {
    gravity: string;          // e.g. "3.72 m/s²"
    distanceFromEarth: string;// e.g. "~225 million km (avg)"
    typicalTransitTime: string;// e.g. "8 h"
    surfaceTemp: string;      // min/max range
    moons: string;            // count or names
    atmosphere: string;       // brief description
  };
  hazards: string[];          // 3–5 bullet points
  gallery: {
    alt: string;
    description: string;      // text caption rendered as a styled card (no real images)
    colorClass: string;       // Tailwind background tint for placeholder tile
  }[];
  accentColor: string;        // Tailwind class for destination-specific accent, e.g. "text-solar-orange"
  bgAccent: string;           // e.g. "bg-solar-orange/10"
  borderAccent: string;       // e.g. "border-solar-orange/30"
}
```

Destinations to cover: **Earth, Mars, Moon, Venus, Jupiter, Europa, Pluto**  
(one entry per unique value that appears as `origin` or `destination` in the seed flights).

---

## 4. Files to create / modify

### 4.1 New: `src/data/destinations.ts`

Static map of `slug → DestinationData` plus a lookup helper:

```ts
// lookup by slug (case-insensitive)
export const getDestinationBySlug = (slug: string): DestinationData | null
// lookup by name (used to linkify destination names in FlightCard)
export const getDestinationByName = (name: string): DestinationData | null
// all destinations for the homepage grid
export const ALL_DESTINATIONS: DestinationData[]
```

### 4.2 New: `src/pages/DestinationDetail.tsx`

Route component for `/destinations/:slug`.

**Sections (top → bottom):**

1. **Hero** — full-width `glass-card` with destination name, tagline, accent gradient badge.
2. **Facts block** — 2×3 grid of `glass-card` tiles: Gravity, Distance, Transit Time, Surface Temp, Moons, Atmosphere.
3. **Hazards** — a warning panel listing each hazard with an alert icon.
4. **Gallery** — 3-column grid of placeholder tiles (no `<img>` or external URLs; pure CSS gradient + caption text).
5. **Flights departing soon** — live list fetched with `getFlights({ destination: name })`. Shows up to 5 flights, each as a compact row with departure time, price, and a "Book" button linking to `/flights?destination=<name>`. Shows `LoadingSpinner` while fetching; shows a friendly empty state when none are found.
6. **Unknown slug** — if `getDestinationBySlug(slug)` returns `null`, render a centred 404 panel: "We haven't charted this world yet" + a Back button.

**Data fetching:** `useEffect` + `useState`, same pattern as `Flights.tsx`. Error handling with `toast.error`.

**Animations:** `motion.div` with `initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}` on each section, staggered by `transition={{ delay: index * 0.1 }}` — matches site-wide style.

### 4.3 Modify: `src/App.tsx`

Add one route:

```tsx
<Route path="/destinations/:slug" element={<DestinationDetail />} />
```

Keep the catch-all `<Route path="*" element={<Home />} />` at the bottom.

### 4.4 Modify: `src/pages/Home.tsx`

Add a **"Explore Destinations"** section between the features grid and the CTA section:

- Section heading: "Explore Our Destinations"
- Responsive grid: `grid-cols-2 md:grid-cols-3 lg:grid-cols-4` (7 items → 4+3 layout)
- Each tile: a `Card` with `hover={true}` wrapped in `<Link to={/destinations/${slug}}>`, showing destination name, accent-coloured badge, and tagline.
- Uses `ALL_DESTINATIONS` from `destinations.ts` — no API call, purely static.

### 4.5 Modify: `src/components/flights/FlightCard.tsx`

Make the destination name in the route header a `<Link>`:

```tsx
import { Link } from 'react-router-dom';
import { getDestinationByName } from '../../data/destinations';

// inside the component
const destData = getDestinationByName(flight.destination);
const destLabel = destData
  ? <Link to={`/destinations/${destData.slug}`} ...>{flight.destination}</Link>
  : <span>{flight.destination}</span>;
```

Render `{flight.origin} → {destLabel}` instead of the plain string. Style the link with `hover:text-cosmic-purple underline-offset-2` so it is visually distinct but stays on-brand.

---

## 5. Acceptance criteria mapping

| Criterion | Covered by |
|---|---|
| One destination page per existing flight destination | `destinations.ts` (7 entries) + `/destinations/:slug` route |
| Each page shows name, facts, hazards, gallery | Sections 1–4 in `DestinationDetail.tsx` |
| "Flights departing soon" pulls from real flight list | `getFlights({ destination })` in section 5 |
| Destination links from flight cards and homepage work | `FlightCard.tsx` link + `Home.tsx` grid |
| Unknown slug renders friendly not-found state | `null` check from `getDestinationBySlug` in `DestinationDetail.tsx` |

---

## 6. What is explicitly out of scope

- No backend changes — the existing `/flights` endpoint is sufficient.
- No new API service functions beyond passing `destination` to existing `getFlights()`.
- No real images (avoids external URL policy and CDN concerns).
- No user-generated content, 3D maps, or reviews (those are issue #14).
- No new Tailwind tokens — use the existing palette.

---

## 7. Implementation order

1. `src/data/destinations.ts` — pure data, no dependencies.
2. `src/pages/DestinationDetail.tsx` — depends on (1) and existing `api.ts`/components.
3. `src/App.tsx` — add the route, depends on (2).
4. `src/pages/Home.tsx` — add destinations row, depends on (1).
5. `src/components/flights/FlightCard.tsx` — add destination link, depends on (1).
6. Run `npm run lint` to confirm no TypeScript errors.

---

## 8. Risk / gotchas

| Risk | Mitigation |
|---|---|
| `/flights?destination=Moon` returns flights where `destination = "Moon"` **and** `origin = "Moon"`. The service uses `ilike('%Moon%')`, not exact match. | Filter client-side in `DestinationDetail` to keep only `flight.destination === name` before rendering the departing-soon list. |
| `react-router-dom` `Link` inside a `motion.button` (Card with `onClick`) causes nested interactive elements. | The destination tiles on Home use `Card` with `hover={true}` but no `onClick` — wrap the whole `Card` in a `Link`, not vice versa. For `FlightCard`, only the text label is a `Link`, not the whole card. |
| `framer-motion` `motion.button` vs `motion.div` in `Card` — `Card` renders `motion.button` when `onClick` is provided. | Destination tiles do not pass `onClick` to `Card`, so they render `motion.div` — safe to wrap in `<Link>`. |
| 7 destinations × future slug changes. | Slug is derived from the lowercase name (`name.toLowerCase().replace(' ', '-')`). No spaces in any current destination name so replace is a no-op; consistent and predictable. |

---

*Made with IBM Bob*
