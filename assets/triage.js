/* ============================================================
   Reusable triage classifier — AI Agents course
   ------------------------------------------------------------
   Presents a series of scenarios against ONE fixed set of options,
   and gives per-option feedback rather than just right/wrong. The
   wrong answers are where the learning is: choosing "agent" when the
   answer is "workflow" is a different mistake from choosing "plain
   code", and deserves a different sentence.

   Because the option set is identical on every case, option length
   carries no per-case tell — which is what the authoring rule about
   equal-length answers is actually protecting against.

   Generic: any repeated judgement call can be drilled with it
   (workflow vs. agent, tool-or-not, eval type, context strategy).

   Markup contract:

   <div class="triage" data-triage>
     <div class="triage-stage" data-stage></div>
     <div class="triage-bar">
       <span data-score></span>
       <button data-next>Next &rarr;</button>
     </div>
     <script type="application/json" data-cases>
       {
         "options": [ { "id": "code", "label": "No LLM: plain code" }, ... ],
         "cases": [
           {
             "prompt": "Scenario text, may contain HTML.",
             "answer": "code",
             "why": { "code": "Feedback if they pick this.", ... }
           }
         ]
       }
     </script>
   </div>
   ============================================================ */

(function () {
  "use strict";

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }

  function wire(root) {
    var src = root.querySelector("[data-cases]");
    var stage = root.querySelector("[data-stage]");
    var next = root.querySelector("[data-next]");
    var scoreEl = root.querySelector("[data-score]");
    if (!src || !stage) return;

    var data;
    try {
      data = JSON.parse(src.textContent);
    } catch (e) {
      return;
    }
    var options = data && data.options;
    var cases = data && data.cases;
    if (!options || !options.length || !cases || !cases.length) return;

    var i = 0;
    var right = 0;
    var answered = 0;

    function updateScore() {
      if (!scoreEl) return;
      scoreEl.textContent =
        "Case " + (i + 1) + " of " + cases.length +
        (answered ? "  ·  " + right + "/" + answered + " right" : "");
    }

    function renderDone() {
      stage.innerHTML = "";
      var pct = Math.round((right / cases.length) * 100);
      var verdict =
        right === cases.length
          ? "Clean sweep. The rule is in your hands now — the next step is defending it out loud."
          : right >= cases.length - 1
          ? "Solid. Re-read the one you missed; the misses are the part that sticks."
          : "Worth a second pass. Every miss here is a design review you would have lost.";
      stage.appendChild(
        el(
          "div",
          "triage-done",
          "<strong>" + right + " of " + cases.length + " (" + pct + "%).</strong> " + verdict
        )
      );
      if (next) next.disabled = true;
      if (scoreEl) scoreEl.textContent = "Complete";
      root.dispatchEvent(
        new CustomEvent("triage:complete", {
          bubbles: true,
          detail: { right: right, total: cases.length }
        })
      );
    }

    function render() {
      var c = cases[i];
      stage.innerHTML = "";

      var num = el("span", "triage-num", "Scenario " + (i + 1));
      var q = el("p", "triage-prompt", c.prompt);
      q.insertBefore(num, q.firstChild);
      stage.appendChild(q);

      var opts = el("div", "opts");
      var feedback = el("div", "triage-feedback");
      var locked = false;

      options.forEach(function (o) {
        var b = el("button", "opt", o.label);
        b.type = "button";
        b.dataset.id = o.id;
        b.addEventListener("click", function () {
          if (locked) return;
          locked = true;
          answered++;

          var correct = o.id === c.answer;
          if (correct) right++;

          Array.prototype.forEach.call(opts.children, function (btn) {
            btn.disabled = true;
            if (btn.dataset.id === c.answer) btn.classList.add("correct");
          });
          if (!correct) b.classList.add("wrong");

          var verdict = correct ? "Correct." : "Not quite.";
          var cls = correct ? "ok" : "no";
          var body = (c.why && c.why[o.id]) || "";
          if (!correct && c.why && c.why[c.answer]) {
            body +=
              ' <span class="triage-actual">The answer is <em>' +
              labelFor(c.answer) +
              "</em>: " +
              c.why[c.answer] +
              "</span>";
          }
          feedback.innerHTML =
            '<span class="verdict ' + cls + '">' + verdict + "</span> " + body;
          feedback.classList.add("show");

          if (next) next.disabled = false;
          updateScore();
        });
        opts.appendChild(b);
      });

      stage.appendChild(opts);
      stage.appendChild(feedback);

      if (next) {
        next.disabled = true;
        next.textContent = i === cases.length - 1 ? "See score →" : "Next →";
      }
      updateScore();
    }

    function labelFor(id) {
      for (var k = 0; k < options.length; k++) {
        if (options[k].id === id) return options[k].label;
      }
      return id;
    }

    if (next) {
      next.addEventListener("click", function () {
        if (i < cases.length - 1) {
          i++;
          render();
        } else {
          renderDone();
        }
      });
    }

    render();
  }

  function init() {
    document.querySelectorAll("[data-triage]").forEach(wire);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
