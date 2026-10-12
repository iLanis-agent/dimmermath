# Dimmer math

Why the LED bulbs flicker on the old dimmer, what a dim level saves over the year, and how many bulbs fit the dimmer's load window. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/dimmermath/

## The three tools

- **Load plan** - `loadPlan(bulbWatts, count, dimmerMin, dimmerMax)`: total wattage against the dimmer window, with the gap and a verdict.
- **Savings plan** - `savePlan(bulbWatts, count, dimPct, hoursPerDay, daysPerYear, pricePerKwh)`: dimmed wattage, kilowatt-hours and money saved per year.
- **Bulb-count plan** - `countPlan(dimmerMin, dimmerMax, bulbWatts)`: the fewest and most bulbs that fit the window.

## Labeled norms (illustrative estimates, not rules)

- Labeled approximation: LED draw tracks the dim level roughly linearly; real drivers vary. Labeled reference: many LED dimmers want a 5 W to 150 W load; older leading-edge dimmers often a 25 W minimum; LED-rated trailing-edge dimmers flicker less. The dimmer's datasheet and a licensed electrician's advice win.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (13 cases, 72 checks)

Regenerate the oracle expectations: `python3 oracle.py`
