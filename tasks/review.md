# UX & Accessibility Code Review
**Date**: 2026-04-29
**Reviewer**: Jennifer Mitchelle (Senior UX Design Critic, Swords, Ireland)
**Branch**: fix/code-review-2026-04-29

## 2026-04-29 Audit (Jennifer Mitchelle, UX)

Twenty-sixth periodic review. **One new HIGH finding (J-001) — a regression introduced by yesterday's N-033 fix.** Re-audit performed against 9 source files (app.py 284, createAct.py 827, migrate_legacy_pages.py 152, base.html 63, index.html 97, generate.html 519, gallery.html 63, style.css 724, main.js 19 = 2748 total — note: prior cycle's 2596 figure excluded migrate_legacy_pages.py from the count) plus all 12 generated fan pages. Tooling checks (Python AST, pyflakes on all 3 .py files, Jinja2 compile, CSS brace balance, Flask `test_client` on 8 routes including 2 adversarial). Heading-hierarchy grep across all 12 fan pages (`grep -n '<h[1-6]'`) — this is the audit step that surfaced J-001.

**J-001 is a direct regression of the N-033 fix shipped in 78a18f4 on 2026-04-28.** Before that fix, the 8 v1 fan pages had no `<h1>` element (the band name was in a bare `<marquee>`), and section headers were already `<h3>` — so the visible "heading skip" was h0→h3, which is technically still a 1.3.1 violation but presents to AT as "no top-level heading" (which is what N-033 named). Yesterday's fix added a real `<h1 class="band-title">` wrapping the marquee. That correctly satisfies the missing-h1 leg of WCAG 1.3.1, but it now exposes an h1→h3 skip across the 8 v1 pages because the `<h3 class="section-header">` elements were left untouched. The page now has a top-level heading but the next heading is two levels deeper, which AT screen-reader rotors render as a broken outline.

| Severity | Count | Change |
|---|---|---|
| Critical | 0 | — |
| High | 1 | +1 (J-001 new — regression of N-033) |
| Medium | 6 | — (N-002, N-004, N-009, N-012, N-016, N-019) |
| Low | 22 | — |

Per the workflow, J-001 was fixed in Phase 2 of this same cycle.

### Phase 1 — Audit findings by category

**Critical**: 0 (none)
**High**: 1 new — **J-001** (regression introduced by N-033 fix; see below)
**Medium**: 0 new (6 carried — N-002, N-004, N-009, N-012, N-016, N-019)
**Low**: 0 new (22 carried — N-005, N-006, N-007, N-008, N-010, N-011, N-014, N-017, N-018, N-020, N-022, N-025, N-026, N-027, N-029, N-030, N-032, N-034, N-035, N-036, N-037, N-038, N-039)

#### J-001 — HIGH — Heading-hierarchy skip (h1 → h3) on 8 v1 fan pages
- **Severity**: HIGH
- **WCAG**: SC 1.3.1 Info and Relationships (Level A), SC 2.4.6 Headings and Labels (Level AA)
- **Files** (40 total occurrences — 5 per page × 8 pages):
  - `ChãoDeCorais/home.html:228, 246, 260, 296, 373`
  - `EtherealTrampleweed/home.html:228, 248, 262, 305, 377`
  - `EucalyptusSaints/home.html:228, 246, 260, 296, 376`
  - `Inu-k-trkadeka/home.html:228, 246, 260, 296, 368`
  - `MidnightParlor/home.html:228, 246, 260, 296, 370`
  - `MyopicSunflowers/home.html:228, 246, 260, 296, 368`
  - `NightshadeVanguard/home.html:228, 246, 260, 296, 375`
  - `TheLuminescentUndertow/home.html:213, 240, 251, 294, 374`
- **Origin**: regression introduced by commit `78a18f4` (2026-04-28, N-033 fix). The fix wrapped the band-name `<marquee>` in `<h1 class="band-title">` but did not adjust the existing `<h3 class="section-header">` elements that mark the page sections (Backstory, Band Photo, Members, Discography, Guestbook).
- **User impact**: Screen-reader users navigating by heading rotor (a primary AT pattern) jump from a top-level h1 (band name) directly to h3, signalling that two structural levels are missing. AT may announce this as "heading level 3" without context, breaking the page outline. Sighted users see no visual change — the bug is purely structural/semantic.
- **Why this didn't appear in prior reviews**: Before 78a18f4, v1 pages had NO `<h1>` at all, so the audit framed the issue as "missing h1" (N-033) rather than "broken heading hierarchy". Now that h1 is present, the h1→h3 skip becomes the visible failure. The per-page heading inventory done in past audits counted `<h1>`, `<marquee>`, and `<h2>` markers but did not enumerate all `<h[1-6]>` levels in sequence — that's the audit improvement that surfaced this on 2026-04-29.
- **Recommended fix (applied in Phase 2)**: Promote the 5 `<h3 class="section-header">` elements on each of the 8 v1 pages to `<h2 class="section-header">`. Visual styling is governed by the `.section-header` CSS class (defined in each page's embedded `<style>` block at line 38 in EtherealTrampleweed; same shape across all 8) and is independent of the heading level — so the substitution is purely semantic and preserves all visual output. Verified per-page that there are zero existing `<h2>` elements (so the change is unambiguous) and exactly 5 `<h3>` elements per page (all of them `section-header`).
- **Rejected alternatives**:
  - Demote `<h1>` to `<h2>` and unwrap N-033's contribution → regresses N-033 (would re-fail SC 2.4.6).
  - Insert a synthetic `<h2>` before each `<h3>` → adds visual noise without solving the issue.
  - Add `aria-level="2"` to the h3 elements → works for AT but leaves the DOM hierarchy broken; element-level promotion is the canonical fix.

### Phase 2 — Fix applied this cycle

**J-001 (HIGH, Resolved)**: Extended `migrate_legacy_pages.py` with a new patch step (`J001_SECTION_HEADER_RE`) that promotes `<h3 class="section-header">…</h3>` to `<h2 class="section-header">…</h2>`. The regex matches both opening and closing tags so the surrounding inner content is preserved verbatim. The patch is gated on `'<h3 class="section-header"' in content` — once a v1 page has been migrated, the gate is false, so a re-run is a no-op (idempotency verified — see Phase 3). The 4 legacy pages (`TheVelvetEchoes`, `MoonlitReverie`, `EchoesOfTheMirage`, `**VelvetEchoes`) use `<h2 class="section-title">` (different class name), so their section headers don't match the regex and are correctly left alone.

The script was re-run after the patch was added; 8 v1 pages were patched (one substitution path per page; 5 h3→h2 swaps each = 40 line edits), and the 4 legacy pages reported "no changes needed". Idempotency was verified by a third run that reported "no changes needed" on all 12 pages.

`createAct.py` v2 template (line 657 emits `<h1 class="band-title">`; lines 676, 683, 696, 703, 708 emit `<h2 class="section-header">`) was inspected and confirmed to ALREADY use `<h2>` correctly. So future v2-generated pages are unaffected by both N-033 and J-001 — no template change is required, only a one-time retroactive patch on the 8 pre-existing v1 pages. DALL-E credits are NOT consumed.

**While I was in `migrate_legacy_pages.py`**, I also removed an unused `import sys` (line 20 in the prior file) — pyflakes flagged it as a pre-existing issue introduced when the script was originally created in commit 5d0042f. This is a one-line cleanup and did not warrant its own finding.

Files changed (10):
- `migrate_legacy_pages.py` — added `J001_SECTION_HEADER_RE` module-level regex and a new patch step in `patch_html()` (gated on `'<h3 class="section-header"' in content`); updated docstring to list J-001; removed unused `import sys`.
- `ChãoDeCorais/home.html` — 5 `<h3 class="section-header">` → `<h2 class="section-header">` (and matching `</h3>` → `</h2>`).
- `EtherealTrampleweed/home.html` — same.
- `EucalyptusSaints/home.html` — same.
- `Inu-k-trkadeka/home.html` — same.
- `MidnightParlor/home.html` — same.
- `MyopicSunflowers/home.html` — same.
- `NightshadeVanguard/home.html` — same.
- `TheLuminescentUndertow/home.html` — same.
- `tasks/review.md` — this entry.

### Phase 3 — Verification this cycle

| Check | Result |
|---|---|
| Python AST parse on app.py, createAct.py, migrate_legacy_pages.py | PASS |
| `pyflakes` on app.py + createAct.py + migrate_legacy_pages.py | 3 warnings → still N-037 (`flask.session`, `datetime.datetime`, `datetime.timedelta`); migrate_legacy_pages.py now CLEAN (was: 1 unused-`sys` warning, fixed in this PR as drive-by) |
| Jinja2 compile on 4 top-level templates | PASS (base/index/generate/gallery all compile) |
| CSS brace balance | 128/128 (unchanged — J-001 fix did not touch CSS) |
| Flask `test_client` on 8 routes (incl. `/band/$(evil)/` 400 and `/band/%2E%2E%2Fetc/` 404) | 8/8 as expected (200×6, 400×1, 404×2) — no regression |
| Per-page `<h1>` count after fix (12 fan pages) | 12/12 (unchanged — N-033 fix preserved) |
| Per-page `<h3 class="section-header">` count after fix (8 v1 pages) | 0/8 (was 5/8 each) — fix correctly applied |
| Per-page `<h2 class="section-header">` count after fix (8 v1 pages) | 5/8 each (40 total) — fix correctly applied |
| Per-page heading-sequence read after fix (sampled 3 v1 pages: EtherealTrampleweed, MidnightParlor, TheLuminescentUndertow) | h1, h2, h2, h2, h2, h2 — correct outline |
| Legacy page heading sequence (4 pages) | Unchanged: h1, h2, h2, h2 — still correct |
| Idempotency re-run of migrate_legacy_pages.py | 0 patches on third run (all 12 pages: "no changes needed") |
| Spot-render via Flask `test_client` on 7 ASCII v1 pages | All 7 returned 200 and contained `<h2 class="section-header">~ The Story ~</h2>` (correct nesting) |
| Source file line counts | app.py 284, createAct.py 827, migrate_legacy_pages.py 165 (was 152, +13 for new regex/patch step), base.html 63, index.html 97, generate.html 519, gallery.html 63, style.css 724, main.js 19 = 2761 total (was 2748) |

No regressions. All Phase 1 expected outcomes confirmed in Phase 3. The 4 legacy pages and the v2 template are correctly skipped by the new patch step.

### Phase 4 — Delivery

- Branch `fix/code-review-2026-04-29` created from `main` (NOT from yesterday's branch).
- Single commit covers the 8 modified `home.html` files, the change to `migrate_legacy_pages.py`, and this `tasks/review.md` update.
- PR opened against `main` titled "Fix J-001: promote v1 fan-page section headers from h3 to h2".

Recommendation priority ordering for next cycle: **N-009 (Medium — gallery responsive)** is the longest-aged unfixed Medium and remains the top candidate. N-002, N-004, N-012, N-016, N-019 round out the remaining 5 Medium findings. No findings face an aging-escalation deadline in the next 10 days; recommend continuing the periodic re-audit cadence.

---

## Status of Previous Issues (carried forward — unchanged)

| Prior ID | Issue | Status |
|---|---|---|
| N-001 | Color contrast failure in accent color tuple (#ff6666) | **RESOLVED** |
| N-002 | Residual inline styles in generated fan pages | Open (Medium) — `createAct.py:710,713,731` |
| N-003 | Guestbook links use `href="#"` with no indication | **RESOLVED** |
| N-004 | Legacy generated pages still accessible via direct URL without band_info.json check | Open (Medium) — `app.py:95-104` |
| N-005 | `<hr>` elements use deprecated HTML attributes | Open (Low) — `createAct.py:677,684,697,704,709` |
| N-006 | Feature grid boxes lack equal height content alignment | Open (Low) — `static/css/style.css:304` |
| N-007 | `role="form"` on `<form>` element is redundant | Open (Low) — `templates/generate.html:18` |
| N-008 | No `<meta name="description">` on any page | Open (Low) — `templates/base.html:3-8` |
| N-009 | Gallery table lacks responsive handling for narrow viewports | Open (Medium) — `static/css/style.css:449-492`, `templates/gallery.html:14-47` (WCAG 1.4.10) |
| N-010 | Generated fan page nav pipe separators not hidden from AT | Open (Low) — `createAct.py:666` |
| N-011 | Blink animation timing mismatch (`linear` vs `step-start`) | Open (Low) — `createAct.py:584` |
| N-012 | Band directory path validation blocks non-ASCII band names | Open (Medium) — `app.py:36` |
| N-014 | Inline `import re` inside functions in createAct.py | Open (Low) — `createAct.py:115,252` |
| N-016 | Inconsistent path resolution between gallery and view_band routes | Open (Medium) — `app.py:66-86,95-104` |
| N-017 | No focus management after gallery page load | Open (Low) — `templates/gallery.html` |
| N-018 | Fixed polling interval with no backoff | Open (Low) — `templates/generate.html:355` |
| N-019 | Generated fan pages use `!important` overrides in responsive styles | Open (Medium) — `createAct.py:624,627,630` |
| N-020 | Generated fan page `<br>` tag after decorative stars in header | Open (Low) — `createAct.py:656` |
| N-021 | Generated fan pages have no focus indicator styles | **RESOLVED** |
| N-022 | Generated fan page body has no explicit line-height | Open (Low) — `createAct.py:408-415` |
| N-023 | Gallery displays zero bands because no `band_info.json` files exist | **RESOLVED** |
| N-024 | Older generated pages use `#666666` text | **RESOLVED** |
| N-025 | Older generated pages use deprecated `<marquee>` element | Open (Low) — 8 of 12 pages (WCAG 2.2.2 mitigated by prefers-reduced-motion) |
| N-026 | Older generated pages use `<a name="">` anchors instead of `id` | Open (Low) — 8 pages |
| N-027 | Older generated pages heading hierarchy issues | Open (Low) — narrowed to legacy v0 pages only; v1 issue tracked separately |
| N-028 | Dead gallery links from special-character band names | **RESOLVED** |
| N-029 | Legacy-format fan pages have fixed-position footer that occludes content | Open (Low) — 4 legacy pages |
| N-030 | Legacy-format fan pages render empty band members section | Open (Low) — 4 legacy pages |
| N-031 | All 12 existing fan pages lack skip links, landmarks, prefers-reduced-motion | **RESOLVED** |
| N-032 | `band_assets` route does not validate `filename` parameter | Open (Low) — `app.py:107-112` |
| N-033 | v1 fan pages have no `<h1>` element — band name inside `<marquee>` | **RESOLVED** (2026-04-28, commit 78a18f4) |
| N-034 | Legacy fan pages lack `aria-label` on `<nav>` element | Open (Low) — 4 legacy pages |
| N-035 | Legacy fan pages have fixed-width band photo that overflows on narrow viewports | Open (Low) — 4 legacy pages (WCAG 1.4.10) |
| N-036 | Focus is not moved to a visible element after resetInterface / cancelGeneration | Open (Low) — `templates/generate.html:471-511` |
| N-037 | Unused imports in app.py | Open (Low) — `app.py:1,9` (`flask.session`, `datetime.datetime`, `datetime.timedelta`) |
| N-038 | Skip-link target naming divergence between v1 migrated pages and createAct.py v2 template | Open (Low) — `createAct.py:650,673,735` |
| N-039 | 4 legacy fan pages lack a "Back to Top" link | Open (Low) — 4 legacy pages |
| **J-001** | **Heading-hierarchy skip (h1 → h3) on 8 v1 fan pages** | **RESOLVED** (2026-04-29, this cycle) |

---

## Metrics

- Total tracked issues: 37 (N-001 through N-039 plus J-001, excluding invalidated N-013)
- Critical: 0 | High: 0 | Medium: 6 | Low: 22 (after this cycle's fix)
- Resolved cumulative: N-001, N-003, N-021, N-023, N-024, N-028, N-031, N-033, J-001 (9 total; +1 this cycle)
- Escalated this cycle: J-001 surfaced as HIGH on first detection (regression of recent fix; severity reflects WCAG Level A failure on user-facing pages).
- New this review: J-001 (1 finding).
- Cycles without new findings: 6 of the last 11 (2026-04-16, 2026-04-23, 2026-04-24, 2026-04-25, 2026-04-26, 2026-04-27); 2026-04-28 and 2026-04-29 both had findings (N-033 and J-001 respectively).
- Open medium issues aging: N-002, N-004, N-009, N-012, N-016, N-019 are all 19+ days old.

## Verification — exact commands run

| Command | Result |
|---|---|
| `venv/bin/python -c "import ast; ast.parse(open('app.py').read()); ast.parse(open('createAct.py').read()); ast.parse(open('migrate_legacy_pages.py').read())"` | PASS |
| `venv/bin/python -m pyflakes app.py createAct.py migrate_legacy_pages.py` | 3 warnings (all N-037 — app.py only) |
| `venv/bin/python -c "from jinja2 import …; env.get_template(t)"` for 4 templates | PASS |
| CSS brace count | 128/128 |
| `OPENAI_API_KEY=fake-test-key venv/bin/python -c "..."` Flask `test_client` on 8 routes | 8/8 expected (200/200/200/200/404/400/404/200) |
| `grep -c '<h1' */home.html` across 12 pages | 12/12 |
| `grep -c '<h3 class="section-header"' */home.html` across 8 v1 pages | 0/8 after fix |
| `grep -c '<h2 class="section-header"' */home.html` across 8 v1 pages | 5/8 each = 40 total after fix |
| `venv/bin/python migrate_legacy_pages.py` (third idempotent run) | "no changes needed" on all 12 pages |
