# UX & Accessibility Code Review
**Date**: 2026-04-26
**Reviewer**: Jennifer Mitchelle (Senior UX Design Critic, Swords, Ireland)
**Branch**: fix/code-review-2026-04-13

## 2026-04-26 Audit (Jennifer Mitchelle, UX)

Twenty-third periodic review. **No code changes since 2026-04-25.** Re-audit performed against 8 source files (line counts unchanged: 2596 total — exact match to last cycle, MD5 hashes confirm zero drift) plus all 12 generated fan pages. Rotation this cycle: deep-read of `**VelvetEchoes` (legacy, full 245-line read — first full deep-read since 2026-04-22; previously only grep-surveyed) plus structural body sampling on `ChãoDeCorais` (v1) and `MyopicSunflowers` (v1) at lines 180-280. Cross-page grep sweep across 11 structural markers; tooling checks (Python AST, pyflakes, Jinja2 compile, CSS brace balance, CSS custom-property reference audit, Flask `test_client` on 8 routes including 2 adversarial). v2 template structural lines 575-742 in `createAct.py` re-inspected to re-validate N-002, N-005, N-019, N-038 line references.

**No new issues identified this cycle.** All 7 previously resolved issues remain verified. Open count is unchanged: 7 Medium, 22 Low. This is now the **fifth** "no new findings" cycle in the last 9 (2026-04-16, 2026-04-23, 2026-04-24, 2026-04-25, 2026-04-26). Codebase is genuinely stable; the audit surface is saturated for the current state.

**Aging watch — N-033 is now 8 days old.** Threshold for escalation to High remains 10 days (2026-04-28 — 2 cycles away). Strong recommend: fix in the next remediation pass before auto-escalation. Mechanical fix is well-understood (wrap `<marquee>` in `<h1>` on 8 v1 pages or modify v2 template line 657 — already correctly uses `<h1>`, so the migration script `migrate_legacy_pages.py` is the natural vehicle for a structural pass over the 8 v1 pages).

| Severity | Count | Change |
|---|---|---|
| Critical | 0 | — |
| High | 0 | — |
| Medium | 7 | — |
| Low | 22 | — |

### Phase 1 — Audit findings by category

**Critical**: 0 (none)
**High**: 0 (none)
**Medium**: 0 new (7 carried — N-002, N-004, N-009, N-012, N-016, N-019, N-033)
**Low**: 0 new (22 carried — N-005, N-006, N-007, N-008, N-010, N-011, N-014, N-017, N-018, N-020, N-022, N-025, N-026, N-027, N-029, N-030, N-032, N-034, N-035, N-036, N-037, N-038, N-039)

Per the instructions, no Critical or High issues were identified this cycle, so Phase 2 makes **zero code changes**. All carried Medium and Low findings remain logged unchanged with their existing recommended fixes. Phase 3 verification is recorded below.

### Verification this cycle (Phase 3)
| Check | Result |
|---|---|
| Python AST parse on app.py and createAct.py | PASS |
| `pyflakes` on app.py + createAct.py | 3 warnings → still N-037 (`flask.session`, `datetime.datetime`, `datetime.timedelta`) |
| Jinja2 compile on 4 top-level templates | PASS (base/index/generate/gallery all compile) |
| CSS brace balance | 128/128 |
| CSS custom-property reference audit | 21 referenced / 24 defined — 3 unreferenced (`--space-2xl`, `--space-lg`, `--space-xl`); 0 missing definitions |
| Flask `test_client` on 8 routes (incl. `/band/$(evil)/` 400 and `/band/%2E%2E%2Fetc/` 404) | 8/8 as expected (200×5, 400×1, 404×2) |
| Structural marker grep across 12 fan pages, 11 markers | All match prior-cycle figures: skip-link 12/12, lang="en" 12/12, viewport 12/12, DOCTYPE 12/12, h1 4/12, marquee 8/12, href="#" 0/12, id="main-content" 12/12, id="main" 0/12, Back to Top 8/12, prefers-reduced-motion 16 total |
| Source file line counts | 2596 total — exact match to 2026-04-25 |
| MD5 hashes on all 8 source files | match prior cycle (no drift) |
| `**VelvetEchoes` deep-read (legacy, 245 lines) | Confirms N-029 (footer fixed-bottom at line 86-94), N-030 (empty members section at lines 168-175), N-034 (plain `<nav>` at line 145), N-035 (`width: 600px` at line 96), N-039 (no Back-to-Top) all unchanged |
| `ChãoDeCorais` + `MyopicSunflowers` v1 sampling (lines 180-280) | Confirms N-005 (`<hr color="#00ff00" size="2" noshade>` deprecated attrs), N-026 (`<a name=...>`), N-033 (band name in `<marquee>` with no `<h1>`), N-002 (inline `style=` on member rows) all unchanged |
| createAct.py v2 template lines 575-742 re-inspection | Confirms N-002 (inline styles at 710,713,731), N-005 (deprecated `<hr color="..." size="2" noshade>` at 677,684,697,704,709), N-011 (`linear` at 584 vs CSS `step-start`), N-019 (3× `!important` at 624,627,630), N-038 (`#main`/`id="main"` at 650,673,735) all unchanged |

No code changes this cycle. Only `tasks/review.md` updated. Recommendation priority ordering unchanged from 2026-04-25 — N-033 remains top priority with hard escalation deadline at 2026-04-28 (now 2 cycles away).

---

## 2026-04-25 Audit (prior cycle — preserved for history)

Twenty-second periodic review. **No code changes since 2026-04-24.** Re-audit performed against 8 source files (line counts unchanged: 2596 total — exact match to last cycle) plus all 12 generated fan pages. Rotation this cycle: deep-read of MoonlitReverie (legacy, full 231-line read) and TheVelvetEchoes (legacy, full 235-line read) — neither was deep-read last cycle — plus structural body sampling on EucalyptusSaints (v1) and Inu-K-Trkadeka (v1) at lines 180-260. Cross-page grep sweep across 13 structural markers; tooling checks (Python AST, pyflakes, Jinja2 compile, CSS brace balance, Flask `test_client` on 8 routes including 2 adversarial). MD5 hashes captured on all 8 source files for future drift detection.

**No new issues identified this cycle.** All 7 previously resolved issues remain verified. Open count is unchanged: 7 Medium, 22 Low. This is now the **fourth** "no new findings" cycle in the last 8 (2026-04-16, 2026-04-23, 2026-04-24, 2026-04-25). Codebase is genuinely stable; the audit surface is saturated for the current state.

**Aging watch — N-033 is now 7 days old.** Threshold for escalation to High is 10 days (2026-04-28). Recommend addressing within 3 cycles before auto-escalation triggers.

| Severity | Count | Change |
|---|---|---|
| Critical | 0 | — |
| High | 0 | — |
| Medium | 7 | — |
| Low | 22 | — |

### Verification this cycle
| Check | Result |
|---|---|
| Python AST parse on app.py and createAct.py | PASS |
| `pyflakes` on app.py + createAct.py | 3 warnings → still N-037 |
| Jinja2 compile on 4 templates | PASS |
| CSS brace balance | 128/128 |
| Flask `test_client` on 8 routes (incl. `/band/$(evil)/` 400 and `/band/%2E%2E%2Fetc/` 404) | 8/8 expected |
| Structural marker grep across 12 fan pages | 13/13 markers match prior cycle exactly |
| Source file line counts | 2596 total — exact match to 2026-04-24 |
| MoonlitReverie deep-read (legacy) | Confirms N-029, N-030, N-034, N-035, N-039 patterns |
| TheVelvetEchoes deep-read (legacy) | Confirms same 5 legacy patterns |
| EucalyptusSaints + Inu-K-Trkadeka v1 sampling | Confirms N-005, N-026, N-033 unchanged |

No code changes this cycle. Only `tasks/review.md` updated. Recommendation priority ordering unchanged from 2026-04-24 — N-033 remains top priority with hard escalation deadline at 2026-04-28.

---

## 2026-04-24 Audit (prior cycle — preserved for history)

## Summary

Twenty-first periodic review of the AI Band Generator. No code changes have been made since the prior review (2026-04-23). This cycle performed a fresh deep re-audit of all key source files and rotated the fan-page spot-check subset to EchoesOfTheMirage (legacy), EtherealTrampleweed (v1), TheLuminescentUndertow (v1), and MidnightParlor (v1) — three v1 pages that were **not** deep-read last cycle. Full grep verification across all 12 pages was performed against 13 structural markers (including a new `id="main"` / `id="main-content"` check to re-validate N-038), plus tooling checks (pyflakes, CSS brace balance, Flask test-client smoke tests with two extra adversarial routes, Jinja template compilation, Python AST parse).

The deep re-audit identified **no new issues** this cycle. All 7 previously resolved issues (N-001, N-003, N-021, N-023, N-024, N-028, N-031) remain verified as resolved. The 7 existing Medium issues and 22 existing Low issues (through N-039) carry forward unchanged. Total open count remains 7 Medium and 22 Low.

`tasks/review-recheck.md` is an untracked file from an earlier (2026-04-01) review session on a different branch. Left untouched.

**Files reviewed:**
- `templates/base.html` (63 lines), `templates/index.html` (97 lines), `templates/generate.html` (519 lines), `templates/gallery.html` (63 lines)
- `static/css/style.css` (724 lines), `static/js/main.js` (19 lines)
- `app.py` (284 lines), `createAct.py` (827 lines)
- Generated fan pages (this cycle's rotation): EchoesOfTheMirage (legacy) — full 269-line read; EtherealTrampleweed (v1) — structural body read lines 180-259; TheLuminescentUndertow (v1) — structural body read lines 180-259; MidnightParlor (v1) — structural body read lines 180-259. Remaining 8 pages: targeted grep sweep on structural markers.
- `migrate_legacy_pages.py` (inspected header lines 1-60; documents N-021/N-023/N-024 migration flow — confirms the script exists but only targets those 3 closed issues; does not address N-027/N-029/N-030/N-033/N-034/N-035/N-039).
- Grep verification across all 12 pages for: `Back to Top`, `class="skip-link"`, `lang="en"`, `name="viewport"`, `<!DOCTYPE`, `<marquee`, `<a name=`, `href="#"`, `bgcolor=`, `font color=`, `<h1`, `id="main-content"`, `id="main"`.
- Tooling: Python `ast.parse` on both source files (PASS); `pyflakes` on both (3 unused imports in app.py — still N-037); Flask `test_client` route smoke tests (`/`, `/gallery`, `/generate`, `/band/TheVelvetEchoes/`, `/band/Inu-k-trkadeka/`, `/band/NonExistent/`, `/band/$(evil)/`, `/band/%2E%2E%2Fetc/` — 200/200/200/200/200/404/400/404 as expected; 400 on injection attempt, 404 on URL-encoded path traversal); Jinja2 template compilation on all 4 templates (PASS); CSS brace balance (128/128 matched); line counts (2596 total, exact match to last cycle).
- `tasks/review.md` (prior review document, reviewed for context).

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 7 |
| Low | 22 |

---

## Status of Previous Issues

| Prior ID | Issue | Status |
|---|---|---|
| N-001 | Color contrast failure in accent color tuple (#ff6666) | **RESOLVED** |
| N-002 | Residual inline styles in generated fan pages | Open (Medium) |
| N-003 | Guestbook links use `href="#"` with no indication | **RESOLVED** — re-verified 0 matches across 12 pages |
| N-004 | Legacy generated pages still accessible via direct URL without band_info.json check | Open (Medium) |
| N-005 | `<hr>` elements use deprecated HTML attributes | Open (Low) |
| N-006 | Feature grid boxes lack equal height content alignment | Open (Low) |
| N-007 | `role="form"` on `<form>` element is redundant | Open (Low) — re-verified at generate.html:18 |
| N-008 | No `<meta name="description">` on any page | Open (Low) |
| N-009 | Gallery table lacks responsive handling for narrow viewports | Open (Medium) |
| N-010 | Generated fan page nav pipe separators not hidden from AT | Open (Low) |
| N-011 | Blink animation timing mismatch (`linear` vs `step-start`) | Open (Low) |
| N-012 | Band directory path validation blocks non-ASCII band names | Open (Medium) |
| N-014 | Inline `import re` inside functions in createAct.py | Open (Low) |
| N-015 | Inline style on visitor count in generated pages | Subsumed under N-002 |
| N-016 | Inconsistent path resolution between gallery and view_band routes | Open (Medium) |
| N-017 | No focus management after gallery page load | Open (Low) |
| N-018 | Fixed polling interval with no backoff | Open (Low) |
| N-019 | Generated fan pages use `!important` overrides in responsive styles | Open (Medium) |
| N-020 | Generated fan page `<br>` tag after decorative stars in header | Open (Low) |
| N-021 | Generated fan pages have no focus indicator styles | **RESOLVED** |
| N-022 | Generated fan page body has no explicit line-height | Open (Low) |
| N-023 | Gallery displays zero bands because no `band_info.json` files exist | **RESOLVED** |
| N-024 | Older generated pages use `#666666` text | **RESOLVED** |
| N-025 | Older generated pages use deprecated `<marquee>` element | Open (Low) — 8 of 12 pages |
| N-026 | Older generated pages use `<a name="">` anchors instead of `id` | Open (Low) — 8 pages |
| N-027 | Older generated pages heading hierarchy issues | Open (Low) — narrowed; v1 issue tracked as N-033 |
| N-028 | Dead gallery links from special-character band names | **RESOLVED** |
| N-029 | Legacy-format fan pages have fixed-position footer that occludes content | Open (Low) |
| N-030 | Legacy-format fan pages render empty band members section | Open (Low) |
| N-031 | All 12 existing fan pages lack skip links, landmarks, and prefers-reduced-motion | **RESOLVED** |
| N-032 | `band_assets` route does not validate `filename` parameter | Open (Low) |
| N-033 | v1 fan pages have no `<h1>` element — band name inside `<marquee>` | Open (Medium) |
| N-034 | Legacy fan pages lack `aria-label` on `<nav>` element | Open (Low) |
| N-035 | Legacy fan pages have fixed-width band photo that overflows on narrow viewports | Open (Low) |
| N-036 | Focus is not moved to a visible element after resetInterface / cancelGeneration | Open (Low) |
| N-037 | Unused imports in app.py | Open (Low) |
| N-038 | Skip-link target naming divergence between v1 migrated pages and createAct.py v2 template | Open (Low) |
| N-039 | 4 legacy fan pages lack a "Back to Top" link | Open (Low) |

---

## Escalation Assessment

### Medium Issues Re-evaluated

All 7 Medium issues were re-assessed for escalation to High. N-002, N-004, N-009, N-012, N-016, N-019 are now 18+ days old; N-033 is 6 days old.

- **N-002**: Unchanged. Three inline `style` attributes in v2 template at createAct.py:710,713,731 (re-verified this cycle via grep). Cosmetic guestbook/footer only. Not escalating.
- **N-004**: Unchanged. `view_band()` relies on `SAFE_BAND_NAME` regex and `send_from_directory` scoping for safety. Functional correctness, not security. Not escalating.
- **N-009**: Unchanged. Table is cramped below 400px but does not overflow. Not escalating.
- **N-012**: Unchanged. `ChãoDeCorais` and `**VelvetEchoes` remain unreachable via gallery but data is not lost. Not escalating.
- **N-016**: Unchanged. Latent only in non-standard deployments. Not escalating.
- **N-019**: Unchanged. Three `!important` declarations at createAct.py:624,627,630 that override nothing in the current CSS cascade. Not escalating.
- **N-033**: Unchanged. Still the top-priority Medium. Band name in `<marquee>` on 8 v1 pages (re-verified this cycle on EtherealTrampleweed line 206, MidnightParlor line 206, TheLuminescentUndertow line 191; `<h1>` count = 0 on all 8 v1 pages). WCAG SC 1.3.1 Level A. Not escalating this cycle — remains flagged as highest-priority Medium for the next remediation pass. Aging watch: 6 days old, still within norms. If it reaches 10+ days unremediated, re-examine for escalation.

### Low Issues Re-evaluated for Escalation

All 22 existing Low issues were reassessed. None warrant escalation.

- **N-029, N-030, N-034, N-035, N-039**: All legacy-page tech debt (4 pages). Cumulatively 5 distinct issues on the same 4 files. Recommendation stands: rather than piecemeal fixes, the cleanest remediation is to re-generate the 4 legacy pages via the v2 template pipeline. This cycle's inspection of `migrate_legacy_pages.py` confirms it only migrates N-021/N-023/N-024 (focus-visible CSS, band_info.json, #666666 text) — it does **not** regenerate page structure. A full regeneration would require running `createAct.py` against each legacy name (expensive — burns DALL-E credits) OR writing a new structural-migration pass. Flagged for a dedicated remediation PR. Not escalating any individual issue.
- **N-038**: Re-verified this cycle. `createAct.py:650,673,735` uses `#main` and `id="main"`; all 8 v1 migrated pages use `#main-content` and `id="main-content"`. New v2-generated pages would introduce this divergence again. Still Low (each page is internally consistent). Flagged for fix whenever v2 template is next edited.

No escalations this cycle.

---

## New Issues

None this cycle. This is the **third** "no new findings" cycle in the last 7 (2026-04-16, 2026-04-23, 2026-04-24). The rotation this cycle covered a full legacy page (EchoesOfTheMirage) previously only grep-surveyed, plus three v1 pages (EtherealTrampleweed, TheLuminescentUndertow, MidnightParlor) not deep-read last cycle. Cross-page grep sweep added `id="main"` and `id="main-content"` markers (re-validating N-038). Adversarial Flask routes (`/band/$(evil)/`, `/band/%2E%2E%2Fetc/`) added to smoke test — both correctly return 400/404. There is genuinely nothing new to report. The audit surface is saturated for the current codebase state; further issues will only surface when code changes land.

Stability indicators this cycle:
- Line counts of all 8 source files match last cycle exactly (2596 total — no drift).
- Fan page marker counts unchanged: 12/12 on skip-link/lang/viewport/DOCTYPE/id="main-content"; 8/12 on Back-to-Top/marquee/`<a name=`; 4/12 on `<h1>`; 0/12 on `href="#"`/bgcolor/font-color/`id="main"`.
- Flask routes 8/8 return expected status codes (200×5, 404×2, 400×1).

---

## Medium Issues (carried forward)

### N-002: Residual inline styles in generated fan pages
- **File**: `createAct.py:710,713,731`

### N-004: Legacy generated pages still accessible via direct URL without band_info.json check
- **File**: `app.py:95-104`

### N-009: Gallery table lacks responsive handling for narrow viewports
- **File**: `static/css/style.css:449-492`, `templates/gallery.html:14-47`
- **WCAG**: SC 1.4.10 Reflow, Level AA

### N-012: Band directory path validation blocks non-ASCII and special-character band names
- **File**: `app.py:36`

### N-016: Inconsistent path resolution between gallery and view_band routes
- **File**: `app.py:66-86,95-104`

### N-019: Generated fan pages use `!important` overrides in responsive styles
- **File**: `createAct.py:624,627,630`

### N-033: v1 fan pages have no `<h1>` element
- **Files**: 8 of 12 generated pages (all v1: `ChãoDeCorais`, `EtherealTrampleweed`, `EucalyptusSaints`, `Inu-k-trkadeka`, `MidnightParlor`, `MyopicSunflowers`, `NightshadeVanguard`, `TheLuminescentUndertow`)
- **WCAG**: SC 1.3.1 Info and Relationships, Level A; SC 2.4.6 Headings and Labels, Level AA

---

## Low Issues (carried forward)

### N-005: `<hr>` elements use deprecated HTML attributes
- **File**: `createAct.py:677,684,697,704,709`

### N-006: Feature grid boxes lack equal height content alignment
- **File**: `static/css/style.css:304`

### N-007: `role="form"` on `<form>` element is redundant
- **File**: `templates/generate.html:18`

### N-008: No `<meta name="description">` on any page
- **File**: `templates/base.html:3-8`

### N-010: Generated fan page nav pipe separators not hidden from AT
- **File**: `createAct.py:666` (v2 template); same pattern in all 8 v1 pages

### N-011: Blink animation timing mismatch between main app and generated pages
- **File**: `createAct.py:584` (`linear`) vs `static/css/style.css:650` (`step-start`)

### N-014: Inline `import re` inside functions in createAct.py
- **File**: `createAct.py:115,252`

### N-015: Inline style on visitor count in generated pages
- Subsumed under N-002

### N-017: No focus management after gallery page load
- **File**: `templates/gallery.html`

### N-018: Fixed polling interval with no backoff
- **File**: `templates/generate.html:355`

### N-020: Generated fan page `<br>` tag after decorative stars
- **File**: `createAct.py:656`

### N-022: Generated fan page body has no explicit line-height
- **File**: `createAct.py:408-415`

### N-025: Older generated pages use deprecated `<marquee>` element
- **Files**: 8 of 12 generated pages
- **WCAG**: SC 2.2.2 Pause, Stop, Hide, Level A (mitigated by prefers-reduced-motion)

### N-026: Older generated pages use `<a name="">` anchors instead of `id`
- **Files**: 8 of 12 generated pages (re-verified this cycle: grep count is 5 per v1 page, 0 per legacy page)

### N-027: Older generated pages heading hierarchy issues
- **Files**: Narrowed to legacy pages only; v1 heading issue tracked as N-033

### N-029: Legacy-format fan pages have fixed-position footer that occludes content
- **Files**: 4 legacy pages (EchoesOfTheMirage re-verified this cycle at lines 86-94)

### N-030: Legacy-format fan pages render empty band members section
- **Files**: 4 legacy pages (EchoesOfTheMirage re-verified this cycle at lines 167-171)

### N-032: `band_assets` route does not validate `filename` parameter
- **File**: `app.py:107-112`

### N-034: Legacy fan pages lack `aria-label` on `<nav>` element
- **Files**: 4 legacy pages (EchoesOfTheMirage re-verified this cycle at line 145: plain `<nav>` with no aria-label)

### N-035: Legacy fan pages have fixed-width band photo that overflows on narrow viewports
- **Files**: 4 legacy pages (EchoesOfTheMirage re-verified this cycle at lines 95-100: `width: 600px`)
- **WCAG**: SC 1.4.10 Reflow, Level AA

### N-036: Focus is not moved to a visible element after resetInterface / cancelGeneration
- **File**: `templates/generate.html:471-511`
- **WCAG**: SC 2.4.3 Focus Order, Level A (advisory)

### N-037: Unused imports in app.py
- **File**: `app.py:1,9` (re-verified this cycle: `flask.session`, `datetime.datetime`, `datetime.timedelta`)

### N-038: Skip-link target naming divergence between v1 migrated pages and createAct.py v2 template
- **Files**: `createAct.py:650,673,735` (`#main` / `id="main"` / `href="#main"`) vs. all 8 v1 migrated fan pages (`#main-content` / `id="main-content"`)

### N-039: 4 legacy fan pages lack a "Back to Top" link
- **Files**: `TheVelvetEchoes/home.html`, `MoonlitReverie/home.html`, `EchoesOfTheMirage/home.html`, `**VelvetEchoes/home.html` (re-verified this cycle: `grep -c 'Back to Top'` returns 0 on all 4, 1 on all 8 v1 pages)

---

## Positive Observations

1. **v2 template quality remains excellent**: `lang="en"`, viewport meta, skip link, semantic `<header>`/`<main>`/`<footer>`/`<nav>`, correct heading hierarchy (h1 > h2), `focus-visible`, `prefers-reduced-motion`, ARIA labels, XSS escaping via `html.escape()`, and CSS custom properties.
2. **Main app accessibility remains strong**: Skip link, ARIA progressbar with `aria-valuenow` updates (re-verified at generate.html:191,406,506), `aria-live` regions (`polite` for progress, `assertive` for error), focus management on forward state transitions (`progressTitle`/`successDisplay h3`/`errorDisplay h3`), `focus-visible` on all interactive elements, `prefers-reduced-motion`, scoped table headers, `fieldset`/`legend`, 44x44px touch targets on `.retro-button-small` and `.dice-btn`.
3. **All color contrast ratios pass WCAG AA** (re-verified from prior cycle).
4. **Design token system** well-organized in `:root` (29 tokens: colors, fonts, spacing scale).
5. **Error resilience**: Consecutive network error counter (threshold 3 → user message, 5 → full abort) with graceful degradation.
6. **Security**: CSRF origin/referer checks, per-IP rate limiting (5/hour), `SAFE_BAND_NAME` regex on routes, XSS escaping (verified `html.escape()` on `band_name`, members, tracks, titles), thread-safe `generation_lock`. Adversarial routes `/band/$(evil)/` and `/band/%2E%2E%2Fetc/` correctly return 400 and 404 respectively.
7. **Responsive design**: Three-tier responsive strategy (base + 640px + 768px breakpoints); flex column-fallback on feature grid.
8. **Fan-page baseline compliance**: All 12 fan pages have consistent `lang="en"`, alt text, skip-links, viewport meta, DOCTYPE, and main landmark with `id="main-content"` (12/12 on these six items per this cycle's grep sweep). "Back to Top" stands at 8/12 (N-039 tracks the gap).
9. **Flask routes smoke-test cleanly**: 8/8 routes returned expected status codes under `test_client`.
10. **CSS brace balance**: 128 open / 128 close — clean.
11. **No `href="#"`, `bgcolor`, or `font color=` anywhere** in served pages (re-verified 0/12 on all three markers).
12. **`SAFE_BAND_NAME` regex correctly behaves as designed**: 10/12 directories pass; 2 (`**VelvetEchoes`, `ChãoDeCorais`) blocked. Both blocked names also fail the gallery's `SAFE_BAND_NAME` filter (added per N-028 fix), so they don't generate dead links. Recovery path for these two pages remains rename-or-skip (N-012).
13. **Codebase stability**: Line counts of all 8 source files match exactly to last cycle's figures (2596 total), confirming no drift has occurred since 2026-04-23.

---

## Verification

Commands run as part of this audit (all from project root, with venv activated where indicated):

| Command | Result |
|---|---|
| `venv/bin/python -c "import ast; ast.parse(..)"` on app.py and createAct.py | PASS (syntax clean) |
| `venv/bin/python -c "from jinja2 import ..."` on 4 templates | PASS (all 4 compile) |
| `venv/bin/python -m pyflakes app.py createAct.py` | 3 warnings in app.py → still N-037 |
| Flask `test_client` on 8 routes | PASS (200/200/200/200/200/404/400/404 as expected) |
| CSS brace count (`open=128 close=128`) | PASS |
| `grep -c 'Back to Top' */home.html` across 12 pages | 8/12 (4 legacy zeroes → N-039 confirmed) |
| `grep -c 'class="skip-link"' */home.html` across 12 pages | 12/12 — N-031 still holds |
| `grep -c 'lang="en"' */home.html` across 12 pages | 12/12 |
| `grep -c 'name="viewport"' */home.html` across 12 pages | 12/12 |
| `grep -c '<!DOCTYPE' */home.html` across 12 pages | 12/12 |
| `grep -c '<h1' */home.html` across 12 pages | 4/12 (4 legacy have h1; 8 v1 have 0 → N-033 confirmed) |
| `grep -c '<marquee' */home.html` across 12 pages | 8/12 (all 8 v1 have 1 marquee → N-025 confirmed) |
| `grep -c 'href="#"' */home.html` across 12 pages | 0/12 — N-003 still holds |
| `grep -c 'id="main-content"' */home.html` across 12 pages | 12/12 (all pages consistent) |
| `grep -c 'id="main"' */home.html` across 12 pages | 0/12 (confirms no v2 pages generated post-N-038) |
| `SAFE_BAND_NAME` regex against actual directory inventory | 10/12 pass (as designed) |

No code changes were made this cycle (no new findings above the Low threshold). Only `tasks/review.md` is updated.

---

## Metrics

- Total tracked issues: 36 (N-001 through N-039, excluding invalidated N-013)
- Critical: 0 | High: 0 | Medium: 7 | Low: 22
- Resolved cumulative: N-001, N-003, N-021, N-023, N-024, N-028, N-031 (7 total; +0 this cycle)
- Escalated this cycle: none
- New this review: none
- Previously invalid: N-013 (`json` import is used in gallery route)
- Open medium issues aging: N-002, N-004, N-009, N-012, N-016, N-019 are all 18+ days old; N-033 is 6 days old
- Cycles without new findings: 3 of the last 7 (2026-04-16, 2026-04-23, 2026-04-24)
- **Recommendation**: Priority ordering unchanged from 2026-04-23 —
  1. **N-033** (missing `<h1>` in v1 pages) remains the top Medium and a WCAG Level A issue. 6 days old. Fix by modifying the v2 template's `<marquee>` line in `createAct.py:584` to wrap in `<h1>` (e.g., `<h1 class="band-title"><marquee scrollamount="3">{band_name}</marquee></h1>`) and then either (a) re-generating the 8 v1 pages or (b) running a targeted find-and-replace migration across the 8 pages. Visual appearance is preserved; only semantic structure changes. **If this is not addressed by 2026-04-28 (10 days), escalate to High.**
  2. **Legacy-page consolidation** (N-027, N-029, N-030, N-034, N-035, N-039) — 6 Low issues against the same 4 legacy pages. `migrate_legacy_pages.py` does not regenerate structure (confirmed this cycle by reading lines 1-60), so this needs either a new migration pass or manual re-generation.
  3. **N-037** (3-line unused-import cleanup in app.py) and **N-038** (3-character fix in createAct.py v2 template: change `main` to `main-content` at lines 650, 673, 735) are trivial 5-minute wins.
  4. **N-002** (remove 3 inline styles) and **N-019** (remove 3 superfluous `!important` declarations) in createAct.py v2 template — same file, pair them in one PR.
  5. **N-036** (single-line focus fix in generate.html).
  6. **N-009** (gallery table responsive — medium effort, WCAG AA).
