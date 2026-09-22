# Publishing a new lesson

This course is a static HTML site published with GitHub Pages, from the `master`
branch root of `github.com/Thrllionaire/learnaiagents`. Live at:
https://thrllionaire.github.io/learnaiagents/

There is no build step — the HTML in `lessons/` and `reference/` is committed as-is
and served directly. The only "generation" step is converting the three root
markdown files (`MISSION.md`, `RESOURCES.md`, `GLOSSARY.md`) to HTML, which only
needs to happen when those files change.

## 1. Add the lesson files

New lesson HTML goes in `lessons/NNNN-slug.html`; a matching cheat sheet (if any)
goes in `reference/NNNN-slug.html`. Copy the structure of an existing lesson —
same `<head>`, same `../assets/course.css` link, same `masthead`/`footer` markup —
so the shared stylesheet and scripts apply.

Link paths from a file in `lessons/` or `reference/` back to the repo root use `../`,
e.g. `../glossary.html`, not `../GLOSSARY.md` — the site serves the generated
`.html` versions of those pages, not the raw markdown.

## 2. Regenerate glossary/resources/mission pages (only if they changed)

If you edited `GLOSSARY.md`, `RESOURCES.md`, or `MISSION.md`, rebuild the
corresponding HTML page with pandoc, wrapped to match the site's look:

```bash
cd /home/naren/dev/learnaiagents

md2html() {
  local src="$1" title="$2" out="$3"
  local body
  body=$(pandoc "$src" -f markdown -t html)
  cat > "$out" << HTML
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
<link rel="stylesheet" href="assets/course.css">
</head>
<body>
<div class="wrap">

${body}

<footer>
  <div class="pagenav">
    <a href="index.html">Home</a>
  </div>
</footer>

</div>
</body>
</html>
HTML
}

md2html MISSION.md   "Mission"   mission.html
md2html RESOURCES.md "Resources" resources.html
md2html GLOSSARY.md  "Glossary"  glossary.html
```

## 3. Update the homepage

Add a link to the new lesson (and reference page, if any) in `index.html`, under
the `<h2>Lessons</h2>` / `<h2>Reference</h2>` lists, in lesson-number order.

## 4. Commit and push

```bash
cd /home/naren/dev/learnaiagents
git add lessons/ reference/ index.html mission.html resources.html glossary.html \
        GLOSSARY.md RESOURCES.md MISSION.md
git commit -m "Add lesson NNNN: <title>"
git push
```

Only add `practice/`, `learning-records/`, and `NOTES.md` if you're fine with them
being visible in the (public) repo — they aren't linked from the site either way.

GitHub Pages rebuilds automatically on push, usually within 1-2 minutes. Check
build status with:

```bash
gh api repos/Thrllionaire/learnaiagents/pages/builds/latest
```

## 5. Verify

Open the new page and confirm it renders and links resolve:

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  https://thrllionaire.github.io/learnaiagents/lessons/NNNN-slug.html
```

A `200` means it's live.

## One-time setup (already done, for reference)

- `git init`, `gh repo create learnaiagents --public --source=. --remote=origin --push`
- `.nojekyll` added at repo root so GitHub Pages serves the HTML as-is instead of
  running it through Jekyll (which would otherwise try to process the loose
  markdown/Python files in `practice/` and `learning-records/`).
- Pages enabled via `gh api -X POST repos/Thrllionaire/learnaiagents/pages
  -f "source[branch]=master" -f "source[path]=/"`.
