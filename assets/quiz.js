/* ============================================================
   Reusable quiz widget — AI Agents course
   ------------------------------------------------------------
   Markup contract:

   <div class="quiz" data-quiz>
     <p class="q"><span class="num">Check 1 of 3</span>Question text?</p>
     <div class="opts">
       <button class="opt" data-correct>Answer that is right</button>
       <button class="opt">Answer that is wrong</button>
     </div>
     <div class="feedback" data-when-correct="Why it's right."
                           data-when-wrong="Why the others miss.">
     </div>
   </div>

   Authoring rule (from the teaching skill): every option in a quiz should be
   the same number of words, and as close as possible in characters. Length is
   a tell; a longer option reads as the considered one. Keep them flat.
   ============================================================ */

(function () {
  "use strict";

  function wire(quiz) {
    var opts = Array.prototype.slice.call(quiz.querySelectorAll(".opt"));
    var feedback = quiz.querySelector(".feedback");
    if (!opts.length) return;

    opts.forEach(function (opt) {
      opt.addEventListener("click", function () {
        if (quiz.dataset.answered) return;
        quiz.dataset.answered = "1";

        var chosenIsRight = opt.hasAttribute("data-correct");

        opts.forEach(function (o) {
          o.disabled = true;
          if (o.hasAttribute("data-correct")) o.classList.add("correct");
        });
        if (!chosenIsRight) opt.classList.add("wrong");

        if (feedback) {
          var verdict = chosenIsRight ? "Correct." : "Not quite.";
          var cls = chosenIsRight ? "ok" : "no";
          var body = chosenIsRight
            ? feedback.getAttribute("data-when-correct") || ""
            : feedback.getAttribute("data-when-wrong") ||
              feedback.getAttribute("data-when-correct") || "";
          feedback.innerHTML =
            '<span class="verdict ' + cls + '">' + verdict + "</span> " + body;
          feedback.classList.add("show");
        }

        quiz.dispatchEvent(
          new CustomEvent("quiz:answered", {
            bubbles: true,
            detail: { correct: chosenIsRight }
          })
        );
      });
    });
  }

  function init() {
    document.querySelectorAll("[data-quiz]").forEach(wire);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
