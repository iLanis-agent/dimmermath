(function (root) {
  "use strict";
  function plural(n, word, form) { return n + " " + (n === 1 ? word : (form || word + "s")); }
  function money(c) { return "$" + Math.floor(c / 100) + "." + ("0" + (c % 100)).slice(-2); }

  function loadPlan(bulbWatts, count, dimmerMin, dimmerMax) {
    if (!(bulbWatts > 0) || !(count > 0) || !(dimmerMin >= 0) || !(dimmerMax > 0) || !(dimmerMax > dimmerMin)) return { error: "wattage, count and dimmer range must be positive, max above min" };
    var total = bulbWatts * count;
    if (total < dimmerMin) return { total: total, verdict: "low", gap: dimmerMin - total };
    if (total > dimmerMax) return { total: total, verdict: "over", gap: total - dimmerMax };
    return { total: total, verdict: "ok", gap: dimmerMax - total };
  }

  function savePlan(bulbWatts, count, dimPct, hoursPerDay, daysPerYear, pricePerKwh) {
    if (!(bulbWatts > 0) || !(count > 0) || !(dimPct > 0) || !(dimPct < 100) || !(hoursPerDay > 0) || !(daysPerYear > 0) || !(pricePerKwh > 0)) return { error: "wattage, count, hours, days and price must be positive, dim level below 100" };
    var fullW = bulbWatts * count;
    var dimW = fullW * dimPct / 100;
    var savedKwh = (fullW - dimW) * hoursPerDay * daysPerYear / 1000;
    var savedCents = Math.round(savedKwh * pricePerKwh * 100);
    var priceCents = Math.round(pricePerKwh * 100);
    return { fullW: fullW, dimW: dimW, savedKwh: savedKwh, savedCents: savedCents, priceCents: priceCents };
  }

  function countPlan(dimmerMin, dimmerMax, bulbWatts) {
    if (!(dimmerMin >= 0) || !(dimmerMax > 0) || !(dimmerMax > dimmerMin) || !(bulbWatts > 0)) return { error: "dimmer range and wattage must be positive, max above min" };
    var minCount = Math.ceil(dimmerMin / bulbWatts);
    if (minCount < 1) minCount = 1;
    var maxCount = Math.floor(dimmerMax / bulbWatts);
    if (maxCount < minCount) return { minCount: minCount, maxCount: maxCount, verdict: "none" };
    if (maxCount === minCount) return { minCount: minCount, maxCount: maxCount, verdict: "exact" };
    return { minCount: minCount, maxCount: maxCount, verdict: "range" };
  }

  function renderLoad(r, bulbWatts, count, dimmerMin, dimmerMax) {
    var head = plural(count, "bulb") + " at " + bulbWatts + " W each draw " + r.total + " W - ";
    if (r.verdict === "low") return head + r.gap + " W under the dimmer's " + dimmerMin + " W minimum, so the bulbs may flicker or refuse to light.";
    if (r.verdict === "over") return head + r.gap + " W over the dimmer's " + dimmerMax + " W maximum; the dimmer can overheat.";
    return head + "inside the dimmer's " + dimmerMin + " W to " + dimmerMax + " W window, with " + r.gap + " W of headroom.";
  }

  function renderSave(r, bulbWatts, count, dimPct, hoursPerDay, daysPerYear, pricePerKwh) {
    return "At " + dimPct + "% brightness the " + count + "-bulb set draws about " + r.dimW + " W instead of " + r.fullW + " W. Over " + plural(daysPerYear, "day") + " of " + hoursPerDay + " hours a day that saves " + r.savedKwh + " kWh - about " + money(r.savedCents) + " a year at " + money(r.priceCents) + " a kWh.";
  }

  function renderCount(r, dimmerMin, dimmerMax, bulbWatts) {
    if (r.verdict === "none") return "No whole-bulb count of " + bulbWatts + " W fits the " + dimmerMin + " W to " + dimmerMax + " W window - a different bulb wattage or a low-load dimmer is the fix.";
    if (r.verdict === "exact") return "Exactly " + plural(r.minCount, "bulb") + " of " + bulbWatts + " W fits this dimmer.";
    return plural(r.minCount, "bulb") + " to " + plural(r.maxCount, "bulb") + " of " + bulbWatts + " W fit this dimmer - any fewer and they may flicker, any more and the dimmer runs hot.";
  }

  var api = { loadPlan: loadPlan, savePlan: savePlan, countPlan: countPlan, renderLoad: renderLoad, renderSave: renderSave, renderCount: renderCount };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.DimmerMath = api;
})(this);
