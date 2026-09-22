/* ============================================================
   Reusable trace stepper — AI Agents course
   ------------------------------------------------------------
   Steps the learner through a sequential process one frame at a time,
   so the mechanism is watched rather than read. Used for the agent loop,
   but generic: any ordered process (workflow patterns, eval pipelines,
   context compaction) can be traced with it.

   Markup contract:

   <div class="trace" data-trace>
     <div class="trace-stage" data-stage></div>
     <div class="trace-bar">
       <button data-prev>Back</button>
       <span data-counter></span>
       <button data-next>Step</button>
     </div>
     <script type="application/json" data-frames>
       [ { "caption": "...", "html": "..." }, ... ]
     </script>
   </div>
   ============================================================ */

(function () {
  "use strict";

  function wire(root) {
    var src = root.querySelector("[data-frames]");
    var stage = root.querySelector("[data-stage]");
    var prev = root.querySelector("[data-prev]");
    var next = root.querySelector("[data-next]");
    var counter = root.querySelector("[data-counter]");
    if (!src || !stage) return;

    var frames;
    try {
      frames = JSON.parse(src.textContent);
    } catch (e) {
      return;
    }
    if (!frames || !frames.length) return;

    var i = 0;

    function render() {
      var f = frames[i];
      stage.innerHTML =
        (f.caption ? '<p class="trace-caption">' + f.caption + "</p>" : "") +
        (f.html || "");
      if (counter) counter.textContent = i + 1 + " / " + frames.length;
      if (prev) prev.disabled = i === 0;
      if (next) {
        next.disabled = i === frames.length - 1;
        next.textContent = i === frames.length - 1 ? "Done" : "Step →";
      }
      root.dispatchEvent(
        new CustomEvent("trace:step", { bubbles: true, detail: { index: i } })
      );
    }

    if (next) next.addEventListener("click", function () {
      if (i < frames.length - 1) { i++; render(); }
    });
    if (prev) prev.addEventListener("click", function () {
      if (i > 0) { i--; render(); }
    });

    root.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight" && i < frames.length - 1) { i++; render(); }
      if (e.key === "ArrowLeft" && i > 0) { i--; render(); }
    });
    root.tabIndex = 0;

    render();
  }

  function init() {
    document.querySelectorAll("[data-trace]").forEach(wire);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
