# 2026-05-07 Audit Plan

## Phase 1 — Audit
- [x] Re-verify all prior fixes (N1–N4 from 2026-05-02, N15 from 2026-05-06, C1–C4 + H1–H9 from 2026-05-01)
- [x] Review templates/base.html, index.html, gallery.html, generate.html
- [x] Review static/css/style.css and static/js/main.js
- [x] Review createAct.py HTML emission and app.py routes
- [x] Spot-check color contrast across all foreground/background pairs (incl. all 4 c1/c2/c3 accent permutations on generated page)
- [x] Verify touch targets across all interactive elements (incl. generated-page nav post-N15 fix)
- [x] Verify landmark structure on every page
- [x] Confirm path-traversal regex still applied at both `view_band` and `band_assets` routes
- [x] Write findings to tasks/review.md

## Phase 2 — Fix
- [x] No new Critical/High findings — no code changes required.
- [ ] (Medium/Low findings remain logged in review.md, deferred per task instructions)

## Phase 3 — Verify
- [x] Run `python -m py_compile app.py createAct.py`
- [x] Confirm template files still parse (Jinja2 sanity)
- [x] Confirm CSS brace matching, breakpoints, prefers-reduced-motion intact
- [x] Re-read `createAct.py:525-529` to confirm N15 fix structurally correct

## Phase 4 — Deliver
- [x] Branch fix/code-review-2026-05-07 off main
- [x] Commit audit log (tasks/review.md + tasks/todo.md)
- [x] Push and open PR via `gh pr create`
