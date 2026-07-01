# Beginner Implementation Tasks

Pick one of the three tasks below and paste the starter prompt into Bob to get going.

## Before you start

For the best experience, install the [GitHub CLI](https://cli.github.com) and log in:

```bash
gh auth login
```

This lets Bob read the issue and open a pull request for you automatically.
It works without it, but the experience is smoother with it.

---

## Task 1 — Homepage search widget

> **Starter prompt:**
> ```
> Look at https://github.com/IBM/galaxium-travels/issues/35 and help me plan and implement this.
> ```

A search form (From / To / Date / Passengers) on the homepage hero that navigates to
`/flights?from=...&to=...` with URL params. No backend, no database — just a form and
URL navigation.

---

## Task 2 — Flight status chip

> **Starter prompt:**
> ```
> Look at https://github.com/IBM/galaxium-travels/issues/36 and help me plan and implement this.
> ```

A small coloured badge on every flight card showing the current status (Scheduled,
Check-in Open, Boarding, Departed, Arrived) derived from the departure timestamp.
No backend — just a new utility file and two small component changes.

---

## Task 3 — Destination conditions widget

> **Starter prompt:**
> ```
> Look at https://github.com/IBM/galaxium-travels/issues/39 and help me plan and implement this.
> ```

A widget showing space-weather conditions (solar flare index, dust-storm forecast,
orbital debris risk) on destination pages. Purely frontend — a new data file and a
new component, nothing existing changes.
