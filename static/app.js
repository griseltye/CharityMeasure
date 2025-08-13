(function () {
  const INPUT_IDS = Array.from({length: 8}, (_, i) => `d${8 + i}`); // d8..d15
  const YESNO_ID = "d19";

  const el = id => document.getElementById(id);

  function readScores() {
    return INPUT_IDS.map(id => {
      const v = parseInt(el(id)?.value || "0", 10);
      return isNaN(v) ? 0 : v;
    });
  }

  async function recalc() {
    const payload = {
      scores: readScores(),
      yn: (el(YESNO_ID)?.value || '').trim().toUpperCase()
    };

    try {
      const res = await fetch('/calc', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      // Row 16 & 17
      if (el("r16_left_val")) el("r16_left_val").textContent = (data.d16 ?? 0).toString();
      if (el("r16_mid_val"))  el("r16_mid_val").textContent  = (data.d16 ?? 0).toString();
      if (el("b17_val"))      el("b17_val").textContent      = (data.b17 ?? 81).toString();

      // Row 18/19
      if (el("r18_score")) el("r18_score").textContent = (data.d16 ?? 0).toString();
      if (el("r18_text"))  el("r18_text").textContent  = data.e18 || "";
      if (el("r19_msg"))   el("r19_msg").textContent   = data.r19_msg || "";

      // Row 20 labels/values
      if (el("r20_left"))         el("r20_left").textContent = (data.row20?.banner || "JESUS ADDS TO YOUR EFFORT");
      if (el("r20_header_adds"))  el("r20_header_adds").textContent = (data.row20?.adds_label || "JESUS ADDS");
      if (el("r20_mid"))          el("r20_mid").textContent  = Math.round((data.d20 ?? 0));
      if (el("r20_short"))        el("r20_short").textContent = (data.row20?.points_short_glory ?? 16).toString();

      // Row 21
      if (el("r21_left")) el("r21_left").textContent = (data.row21?.label || "YOUR SCORE WITH JESUS ADDED");
      if (el("r21_mid"))  el("r21_mid").textContent  = Math.round((data.d21 ?? 0));

      // Row 22
      if (el("r22_left"))  el("r22_left").textContent  = data.row22?.left || "";
      if (el("r22_right")) el("r22_right").textContent = data.row22?.right || "";

    } catch (e) {
      console.error("calc error", e);
    }
  }

  // Wire up events
  INPUT_IDS.forEach(id => { const node = el(id); if (node) node.addEventListener("input", recalc); });
  if (el(YESNO_ID)) el(YESNO_ID).addEventListener("input", recalc);

  // Kickoff
  recalc();
})();