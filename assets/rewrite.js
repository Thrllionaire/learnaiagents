/* ============================================================
   Reusable rewrite drill — AI Agents course
   ------------------------------------------------------------
   For skills that are *production*, not recognition. The learner
   must type the artefact before anything is revealed; only then do
   the criteria appear, as a rubric they grade themselves against,
   and only then the model answer.

   The ordering is the whole point. Showing a rubric first turns the
   task into fill-in-the-blanks; showing a model answer first turns it
   into reading. Write blind, then judge, then compare.

   Self-grading is deliberate. Free text cannot be machine-marked
   honestly, and a keyword matcher would reward the wrong thing —
   naming the criteria explicitly and asking "did you do this?" is a
   tighter feedback loop than a brittle regex pretending to be one.

   Markup contract:

   <div class="rewrite" data-rewrite>
     <div class="rw-stage" data-stage></div>
     <div class="rw-bar">
       <span data-score></span>
       <button data-next>Next &rarr;</button>
     </div>
     <script type="application/json" data-cases>
       {
         "cases": [
           {
             "num": "Rewrite 1 of 2",
             "situation": "What happened, as HTML.",
             "current": "The string the tool returns today.",
             "placeholder": "Optional textarea placeholder.",
             "rubric": ["Criterion one.", "Criterion two."],
             "answer": "One good rewrite.",
             "note": "Optional sentence under the model answer, HTML."
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

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
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
    var cases = (data && data.cases) || [];
    if (!cases.length) return;

    var i = 0;
    var met = 0;
    var possible = 0;

    function paintScore() {
      if (!scoreEl) return;
      scoreEl.textContent = possible
        ? "Criteria met " + met + " / " + possible
        : "Case " + (i + 1) + " of " + cases.length;
    }

    function render() {
      var c = cases[i];
      stage.innerHTML = "";

      stage.appendChild(el("span", "rw-num", c.num || "Rewrite " + (i + 1)));
      stage.appendChild(el("p", "rw-situation", c.situation || ""));

      if (c.current) {
        var cur = el("div", "rw-current");
        cur.appendChild(el("h4", null, "What it says today"));
        cur.appendChild(el("pre", null, "<code>" + esc(c.current) + "</code>"));
        stage.appendChild(cur);
      }

      var ta = el("textarea");
      ta.setAttribute("placeholder", c.placeholder || "Write the replacement string…");
      stage.appendChild(ta);

      var check = el("button", "rw-check", "Check mine");
      check.disabled = true;
      stage.appendChild(check);

      ta.addEventListener("input", function () {
        check.disabled = ta.value.trim().length < 12;
      });

      check.addEventListener("click", function () {
        check.disabled = true;
        check.remove();
        ta.readOnly = true;

        var rubric = c.rubric || [];
        possible += rubric.length;

        var box = el("div", "rw-rubric");
        box.appendChild(
          el("h4", null, "Now grade it. Tick only what your own text actually does.")
        );
        var list = el("ul");
        rubric.forEach(function (item) {
          var li = el("li");
          var lab = el("label");
          var cb = el("input");
          cb.type = "checkbox";
          lab.appendChild(cb);
          lab.appendChild(el("span", null, item));
          cb.addEventListener("change", function () {
            met += cb.checked ? 1 : -1;
            li.classList.toggle("ticked", cb.checked);
            paintScore();
          });
          li.appendChild(lab);
          list.appendChild(li);
        });
        box.appendChild(list);
        stage.appendChild(box);

        var ans = el("details", "rw-answer");
        var sum = el("summary", null, "One good answer");
        ans.appendChild(sum);
        ans.appendChild(el("pre", null, "<code>" + esc(c.answer || "") + "</code>"));
        if (c.note) ans.appendChild(el("p", "rw-note", c.note));
        stage.appendChild(ans);

        if (next) next.disabled = i >= cases.length - 1;
        paintScore();
      });

      if (next) next.disabled = true;
      paintScore();
    }

    if (next) {
      next.addEventListener("click", function () {
        if (i < cases.length - 1) {
          i++;
          render();
        }
      });
    }

    render();
  }

  function init() {
    document.querySelectorAll("[data-rewrite]").forEach(wire);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
