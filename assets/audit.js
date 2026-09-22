/* ============================================================
   Reusable audit widget — AI Agents course
   ------------------------------------------------------------
   Shows one artefact (a tool definition, a prompt, an eval case)
   and a flat list of candidate criticisms. The learner picks the
   ones that are real. Some are not — spotting a non-problem is as
   much of the skill as spotting a problem, so wrong picks get their
   own sentence rather than a buzzer.

   Multi-select by design: real review is "find the N things", not
   "choose the one right answer". Nothing is disabled until it is
   clicked, so the learner commits before seeing any feedback.

   Markup contract:

   <div class="audit" data-audit>
     <div class="audit-stage">
       <p class="audit-task"><span class="num">Audit</span>Find the three real flaws.</p>
       <pre><code>... the artefact ...</code></pre>
       <div class="opts">
         <button class="aopt" data-flaw
                 data-why="Why this is genuinely wrong.">Criticism text</button>
         <button class="aopt"
                 data-why="Why this one is fine as written.">Criticism text</button>
       </div>
       <div class="audit-notes" data-notes></div>
     </div>
     <div class="audit-bar">
       <span data-found></span>
       <button data-reveal>Reveal the rest</button>
     </div>
   </div>

   Authoring rule: keep the options close to the same length. A longer
   option reads as the considered one and gives the answer away.
   ============================================================ */

(function () {
  "use strict";

  function wire(root) {
    var opts = Array.prototype.slice.call(root.querySelectorAll(".aopt"));
    var notes = root.querySelector("[data-notes]");
    var foundEl = root.querySelector("[data-found]");
    var reveal = root.querySelector("[data-reveal]");
    if (!opts.length) return;

    var total = opts.filter(function (o) {
      return o.hasAttribute("data-flaw");
    }).length;
    var found = 0;

    function paint() {
      if (foundEl) {
        foundEl.textContent = "Flaws found " + found + " / " + total;
      }
      if (reveal && found >= total) reveal.disabled = true;
    }

    function note(opt, silent) {
      if (!notes) return;
      var isFlaw = opt.hasAttribute("data-flaw");
      var row = document.createElement("p");
      row.className = "audit-note";
      row.innerHTML =
        '<span class="verdict ' + (isFlaw ? "ok" : "no") + '">' +
        (isFlaw ? (silent ? "Missed:" : "A real flaw:") : "Not a flaw:") +
        "</span> " + (opt.getAttribute("data-why") || "");
      notes.appendChild(row);
      notes.classList.add("show");
    }

    function settle(opt, silent) {
      if (opt.disabled) return;
      opt.disabled = true;
      var isFlaw = opt.hasAttribute("data-flaw");
      opt.classList.add(isFlaw ? "is-flaw" : "is-fine");
      if (isFlaw) found++;
      note(opt, silent);
    }

    opts.forEach(function (opt) {
      opt.addEventListener("click", function () {
        settle(opt, false);
        paint();
      });
    });

    if (reveal) {
      reveal.addEventListener("click", function () {
        opts.forEach(function (opt) {
          if (opt.hasAttribute("data-flaw")) settle(opt, true);
        });
        reveal.disabled = true;
        paint();
      });
    }

    paint();
  }

  function init() {
    document.querySelectorAll("[data-audit]").forEach(wire);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
