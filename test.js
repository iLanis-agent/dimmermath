"use strict";
const E = require("./engine.js");
const cases = require("./expected.json");
let checks = 0, fails = 0;
function eq(a, b, label) {
  checks++;
  if (a !== b) { fails++; console.log("FAIL " + label + ": got " + JSON.stringify(a) + " want " + JSON.stringify(b)); }
}
for (const c of cases) {
  const r = E[c.fn](...c.args);
  const want = c.result;
  if (want.error) {
    eq(r.error, want.error, c.fn + c.args + " error");
    eq(Object.keys(r).length, 1, c.fn + c.args + " error-only");
    continue;
  }
  eq(r.error, undefined, c.fn + c.args + " no-error");
  for (const k of Object.keys(want)) eq(r[k], want[k], c.fn + c.args + " " + k);
  const renderFn = { loadPlan: "renderLoad", savePlan: "renderSave", countPlan: "renderCount" }[c.fn];
  eq(E[renderFn](r, ...c.args), c.render, c.fn + c.args + " render");
  eq(typeof E[renderFn](r, ...c.args), "string", c.fn + c.args + " render-type");
}
console.log(cases.length + " cases, " + checks + " checks " + (fails ? fails + " FAILED" : "green"));
process.exit(fails ? 1 : 0);
