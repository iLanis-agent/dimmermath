import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def plural(n, word, form=None): return str(jsnum(n)) + " " + (word if n == 1 else (form or word + "s"))
def money(c): return "$" + str(c // 100) + "." + str(c % 100).zfill(2)
def fmt(x): return str(jsnum(x))
def rnd(x): return math.floor(x + 0.5)

def load_plan(bulbWatts, count, dimmerMin, dimmerMax):
    if not (bulbWatts > 0) or not (count > 0) or not (dimmerMin >= 0) or not (dimmerMax > 0) or not (dimmerMax > dimmerMin):
        return {"error": "wattage, count and dimmer range must be positive, max above min"}
    total = jsnum(bulbWatts * count)
    if total < dimmerMin: return {"total": total, "verdict": "low", "gap": jsnum(dimmerMin - total)}
    if total > dimmerMax: return {"total": total, "verdict": "over", "gap": jsnum(total - dimmerMax)}
    return {"total": total, "verdict": "ok", "gap": jsnum(dimmerMax - total)}

def save_plan(bulbWatts, count, dimPct, hoursPerDay, daysPerYear, pricePerKwh):
    if not (bulbWatts > 0) or not (count > 0) or not (dimPct > 0) or not (dimPct < 100) or not (hoursPerDay > 0) or not (daysPerYear > 0) or not (pricePerKwh > 0):
        return {"error": "wattage, count, hours, days and price must be positive, dim level below 100"}
    fullW = jsnum(bulbWatts * count)
    dimW = jsnum(fullW * dimPct / 100)
    savedKwh = jsnum((fullW - dimW) * hoursPerDay * daysPerYear / 1000)
    return {"fullW": fullW, "dimW": dimW, "savedKwh": savedKwh,
            "savedCents": rnd(savedKwh * pricePerKwh * 100), "priceCents": rnd(pricePerKwh * 100)}

def count_plan(dimmerMin, dimmerMax, bulbWatts):
    if not (dimmerMin >= 0) or not (dimmerMax > 0) or not (dimmerMax > dimmerMin) or not (bulbWatts > 0):
        return {"error": "dimmer range and wattage must be positive, max above min"}
    minCount = math.ceil(dimmerMin / bulbWatts)
    if minCount < 1: minCount = 1
    maxCount = math.floor(dimmerMax / bulbWatts)
    if maxCount < minCount: return {"minCount": minCount, "maxCount": maxCount, "verdict": "none"}
    if maxCount == minCount: return {"minCount": minCount, "maxCount": maxCount, "verdict": "exact"}
    return {"minCount": minCount, "maxCount": maxCount, "verdict": "range"}

def render_load(r, bulbWatts, count, dimmerMin, dimmerMax):
    head = plural(count, "bulb") + " at " + fmt(bulbWatts) + " W each draw " + fmt(r["total"]) + " W - "
    if r["verdict"] == "low": return head + fmt(r["gap"]) + " W under the dimmer's " + fmt(dimmerMin) + " W minimum, so the bulbs may flicker or refuse to light."
    if r["verdict"] == "over": return head + fmt(r["gap"]) + " W over the dimmer's " + fmt(dimmerMax) + " W maximum; the dimmer can overheat."
    return head + "inside the dimmer's " + fmt(dimmerMin) + " W to " + fmt(dimmerMax) + " W window, with " + fmt(r["gap"]) + " W of headroom."

def render_save(r, bulbWatts, count, dimPct, hoursPerDay, daysPerYear, pricePerKwh):
    return ("At " + fmt(dimPct) + "% brightness the " + fmt(count) + "-bulb set draws about " + fmt(r["dimW"]) + " W instead of "
            + fmt(r["fullW"]) + " W. Over " + plural(daysPerYear, "day") + " of " + plural(hoursPerDay, "hour")
            + " a day that saves " + fmt(r["savedKwh"]) + " kWh - about " + money(r["savedCents"]) + " a year at " + money(r["priceCents"]) + " a kWh.")

def render_count(r, dimmerMin, dimmerMax, bulbWatts):
    if r["verdict"] == "none": return ("No whole-bulb count of " + fmt(bulbWatts) + " W fits the " + fmt(dimmerMin) + " W to " + fmt(dimmerMax)
            + " W window - a different bulb wattage or a low-load dimmer is the fix.")
    if r["verdict"] == "exact": return "Exactly " + plural(r["minCount"], "bulb") + " of " + fmt(bulbWatts) + " W fits this dimmer."
    return (plural(r["minCount"], "bulb") + " to " + plural(r["maxCount"], "bulb") + " of " + fmt(bulbWatts)
            + " W fit this dimmer - any fewer and they may flicker, any more and the dimmer runs hot.")

cases = []
for a in [(9, 4, 5, 150), (9, 2, 25, 150), (60, 5, 5, 240), (0, 4, 5, 150)]:
    r = load_plan(*a)
    cases.append({"fn": "loadPlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_load(r, *a)})
for a in [(9, 4, 50, 4, 300, 0.15), (60, 6, 25, 6, 365, 0.3), (12, 3, 40, 2, 200, 0.22), (9, 4, 0, 4, 300, 0.15)]:
    r = save_plan(*a)
    cases.append({"fn": "savePlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_save(r, *a)})
for a in [(5, 150, 9), (25, 40, 9), (12, 15, 9), (9, 10, 9), (5, 4, 9)]:
    r = count_plan(*a)
    cases.append({"fn": "countPlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_count(r, *a)})

with open("expected.json", "w") as f:
    f.write(json.dumps(cases, separators=(",", ":")) + "\n")
print("wrote", len(cases), "cases")
