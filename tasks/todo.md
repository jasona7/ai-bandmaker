# 2026-05-06 Audit Plan

## Phase 1 — Audit
- [x] Review templates/base.html, index.html, gallery.html, generate.html
- [x] Review static/css/style.css and static/js/main.js
- [x] Review createAct.py HTML emission (lines 324-625) and app.py routes
- [x] Spot-check color contrast across all foreground/background pairs (including all 4 c1/c2/c3 accent permutations on generated page)
- [x] Verify touch targets across all interactive elements
- [x] Verify landmark structure on every page (incl. generated band page)
- [x] Write findings to tasks/review.md

## Phase 2 — Fix
- [x] HIGH N15: Generated-band-page nav touch target ~16-21px
      Fix: add `display: inline-block; padding: 6px 8px;` to `.nav-bar a` in
      `createAct.py:525-527` (mirrors the 2026-05-02 N2 fix in `static/css/style.css`)
- [ ] (Medium/Low findings remain logged in review.md, deferred per task instructions)

## Phase 3 — Verify
- [x] Run `python -m py_compile app.py createAct.py`
- [x] Confirm template files still parse (Jinja2 sanity)
- [x] Confirm CSS brace matching, breakpoints, prefers-reduced-motion intact

## Phase 4 — Deliver
- [x] Branch fix/code-review-2026-05-06 off main
- [x] Commit fix + audit report
- [x] Push and open PR via `gh pr create`
