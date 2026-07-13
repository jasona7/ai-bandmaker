# UX / Accessibility / Design-System Review — 2026-07-13

**Reviewer:** Jennifer Mitchelle (UX Design Critic). Every finding independently re-verified against the
code by the orchestrator; H-A and M-A were reproduced by executing the real `generate.html` script
against a stub DOM, before and after the fix.
**Branch:** `fix/code-review-2026-07-13` (audit #29)
**Scope:** `templates/`, `static/`, `createAct.py`, `app.py`, and the generated band pages.
**Standard:** WCAG 2.2 AA.

---

## ⚠ The finding that outranks every finding below

**Nothing this audit loop produces is reaching `main`.**

```
PRs merged, all time ................. 0
PRs open ............................ 19   (oldest: 2026-04-02)
Commits on this branch not on main .. 36
Commits on main not on this branch ... 0
```

`main` today still has **zero HTML escaping** in `createAct.py`. The stored-injection fix, the
`aria-live` scoping fix, the WCAG fixes from PRs #10/#11/#14, the hang-at-0% fix, the CANCEL fix —
none of it has ever landed. Users are running code that none of these 29 audits has improved.

**Good news, and it is genuinely good:** the daily branches are *stacked*. This branch is a strict
superset of `main` (zero commits on main that aren't here), and it already contains PRs **#10 → #19**.
Verified by ancestry check:

| PR branch | contained in this branch? |
|---|---|
| `fix/code-review-2026-05-02` (#10) | ✅ |
| `fix/code-review-2026-05-09` (#14) | ✅ |
| `fix/code-review-2026-07-08` (#17) | ✅ |
| `fix/code-review-2026-07-10` (#18) | ✅ |
| `fix/code-review` (#1) | ❌ diverged |
| `fix/code-review-2026-04-05` (#2) | ❌ diverged |
| `fix/code-review-2026-04-12` (#4) | ❌ diverged |

So **one merge of this branch into `main` lands ten PRs' worth of accumulated fixes.** PRs #1–#4 and
#8/#9 predate the "retro overhaul" that landed on `main` and rewrote these files; they need separate
triage. (PR #9's own title — *"Restore accessibility, security & UX fixes lost in retro overhaul"* —
records that the overhaul already destroyed one round of fixes once.)

**Recommended action, in priority order:**
1. Merge this branch into `main`. Close #10–#19 as absorbed.
2. Triage #1–#4, #8, #9 against current `main` — most are likely obsolete post-overhaul.
3. Only then run audit #30.

Auditing harder cannot fix a delivery problem. **The highest-value action available is not another
audit — it is merging.**

---

## Summary of counts

| Severity | Count | Status |
|----------|-------|--------|
| CRITICAL | 0 | — |
| HIGH | 1 | **H-A fixed this run** |
| MEDIUM | 1 new + 4 carried | M-A **fixed** (subsumed by the H-A fix); rest logged, unfixed per scope |
| LOW | 2 new + 7 carried | Logged, unfixed per scope |

**Note:** The 1996 GeoCities aesthetic (blink text, "under construction", visitor counter, table
layout, neon palette, Comic Sans, tiled starfield) is intentional and is NOT flagged. Contrast and
motion defects *inside* that aesthetic are still flagged.

---

## HIGH

### H-A — CANCEL during the in-flight POST leaks an unclearable poller that steals focus every 1.5s, then destroys the success screen — **NEW** ✅ FIXED

**Files:** `templates/generate.html` — `:141` (`showProgress()` ran *before* the fetch), `:150-151`
(`.then` assigns id + starts polling), `:163` (`startStatusCheck` never cleared an existing interval),
`:299` (`var idToCancel = currentGenerationId`)
**WCAG:** 2.4.3 Focus Order (A); effectively 2.1.2 No Keyboard Trap (A); 3.3.1 Error Identification (A)

This is a **regression introduced by `1faf73e`** — the commit that added the CANCEL fix — not something
28 audits missed in stable code. It is exactly the composed-severity class the last audit warned about:
three individually-trivial JS gaps that compose into the primary task's final step becoming unreachable.

`showProgress()` was called *before* `fetch('/api/generate')`, so `[ CANCEL ]` was live and clickable
for the entire POST round-trip — a window in which `currentGenerationId` is still `null`. Reproduced by
executing the real script:

```
1. click GENERATE  (POST in flight, CANCEL is visible)
2. click CANCEL    (while POST still in flight)
   -> /api/cancel sent?  *** NO -- worker keeps running, full paid generation ***
3. POST lands -> poller starts AFTER the user cancelled       (live intervals: I1)
4. click GENERATE again                                       (live intervals: I1, I2)
   -> ORPHANED: statusCheckInterval only holds the newest handle; I1 is unreachable
5. generation 2 completes -> FOCUS -> successTitle
6. three more ticks    -> FOCUS -> successTitle x3   (every 1.5s, forever)
7. later, entry pruned -> orphan replaces the success panel with a false error
```

Composed user-facing failure:
1. **The H1 CANCEL fix was bypassed.** `idToCancel` was `null`, so no `/api/cancel` was sent and the
   worker ran to completion — a full paid GPT+DALL·E generation and a ghost band in the gallery. The
   exact defect `1faf73e` was written to eliminate.
2. **The orphaned interval could never be cleared** — `statusCheckInterval` holds one handle.
3. **Focus yanked to `#successTitle` every 1.5 seconds, indefinitely.** A keyboard user **cannot Tab to
   `[ VIEW BAND PAGE ]`** — focus is stolen back before they reach it. The primary task dead-ends.
4. **The orphan later replaced the success panel with a false error**, destroying the VIEW button.

**Root cause (why this class keeps recurring):** `generate.html`'s state machine had **no single source
of truth**. `currentGenerationId`, `statusCheckInterval`, `currentDirectory` and the step-table DOM were
four independent mutable states written from three entry points. Every HIGH for three consecutive audits
has been two of them disagreeing.

**Fix applied — structural, not symptomatic.** Introduced a monotonic **`runToken`** identifying the run
the UI belongs to:
- `resetInterface()` bumps `runToken` and stops the poller — one teardown, one owner.
- `startGeneration()` calls `resetInterface()` first, then captures its token; the `.then`/`.catch` bail
  out if the token changed, so an abandoned run can never resurrect the UI.
- If the run is abandoned while the POST is in flight, the `.then` now **cancels the id the server just
  returned**, closing the window in which no id existed to cancel.
- `startStatusCheck()` calls `stopStatusCheck()` first — an orphan poller can no longer form.
- `stopStatusCheck()` nulls the handle (previously `if (statusCheckInterval)` stayed permanently truthy
  after the first run).

**Verification:** differential test against the real script. Pre-fix: 7 failures (no `/api/cancel` sent,
2 live pollers, focus stolen 3 extra times, 7 stale step rows). Post-fix: 8/8 checks pass.

---

## MEDIUM

### M-A — After `[ TRY AGAIN ]`, the step table reports steps that never ran as complete — **NEW** ✅ FIXED
**Files:** `templates/generate.html:135` (retry → `startGeneration`), `:229-245` (`updateProgress` has no
`else`; indicators only ever advance)
**Heuristic:** Nielsen #1, Visibility of System Status

`resetInterface()` was the only code that cleared step indicators, and it was **not** on the retry path.
Run #1 fails at 50%, user clicks TRY AGAIN, the new run is at 10% — but the table still reads:

```
[X] Creating Profile      screen-reader: (complete)
[X] Setting Up Directory  screen-reader: (complete)
[X] Writing Backstory     screen-reader: (complete)
[>] Identifying Members   screen-reader: (in progress)
```

Screen-reader users are told "(complete)" for work that has not happened, and because the loop never
regresses an indicator it stays wrong for the entire new run. **Fixed for free** by the H-A fix, since
`startGeneration()` now calls `resetInterface()` first. (Logged as MEDIUM; fixed only because the correct
HIGH fix subsumes it — not scope creep.)

### Carried forward — logged, unfixed per scope
- **`bandPreview.innerHTML` interpolates the unescaped model-authored band name** — `generate.html:275-277`.
  Self-XSS; also mis-renders a legitimate name containing `&` or `<`. `createAct.py` has `esc()` on every
  other sink; this is the one gap. Logged since 2026-05.
- **Discography collapses to one mislabeled album** — `createAct.py:237`. The `album:` prefix test misses
  GPT-4o's markdown (`### Album 1: "..."`); subsequent headers match neither branch and are silently
  dropped. Breaks a feature advertised at `generate.html:21`. Artifacts on disk:
  `TheVelvetEchoes/home.html`, `MoonlitReverie/home.html` (3 raw-markdown lines each).
- **`resetInterface()` drops keyboard focus to `<body>`** — WCAG 2.4.3 (A). One line. Logged 7 audits running.
- **Polling has no ceiling; `.catch` only `console.error`s** — `generate.html:201-203`. A run of failing
  polls spins silently forever.

---

## LOW

- **NEW — `h3[tabindex]:focus { outline: none }` out-specifies the focus-visible rule.**
  `static/css/style.css:53-56` is specificity `(0,2,1)`; `[tabindex]:focus-visible` at `:45` is `(0,2,0)`.
  The higher one wins, so the comment at `:50-52` ("`:focus-visible` above still applies") **is false** —
  a keyboard user pressing Enter on GENERATE has focus moved to `#progressTitle` with no visible
  indicator. `main:focus` `(0,1,1)` *loses* to `(0,2,0)`, so `<main>` behaves the opposite way. Inconsistent.
- **NEW — failed runs leak their output directory.** `app.py:337` calls `cleanup_partial_output()` only in
  the `GenerationCancelled` handler; the generic `except` at `:345-352` does not. A DALL·E rate-limit or
  content-policy rejection (common) leaves an orphan dir that consumes the band's slug, so the retry
  becomes `TheVelvetEchoes1` and the gallery renders "The Velvet Echoes**1**" (`app.py:139`).
- Pending step indicator `#666666` on `#0a0a1a` = **3.41:1** — `style.css:369`. WCAG 1.4.3 (AA).
  `#909090` → 6.14:1. *(All 12 palette pairs re-derived; this is the only failure. Prior contrast work is sound.)*
- Blinking "Under Construction" has no pause/stop/hide — `base.html:49`. WCAG 2.2.2 (A).
  `prefers-reduced-motion` mitigates; a finite `animation-iteration-count` would close it outright.
- `h2` → `h4` heading skip — `index.html:85, 91, 97`. WCAG 1.3.1 (A). *Carried, 7 audits.*
- Generated members table has no `<th>`/`scope` — `createAct.py:621-623`. WCAG 1.3.1 (A).
- Backstory renders as an unbroken wall (newlines collapse) — `createAct.py:605`.
- Bare unstyled 404 text — `app.py:158`.
- ASCII bar wraps below ~360px — cosmetic; it is `aria-hidden`.

---

## Correction to a prior audit (WCAG 2.2-specific)

The previous `review.md` **L4** recommended dropping the redundant `[ VIEW ]` link in the gallery.
**Do not do that** — it would *introduce* a WCAG 2.2 **SC 2.5.8 Target Size (Minimum, AA)** failure. The
band-name link (`gallery.html:31`) is ~**23.1px** tall (1.1em × 1.5 line-height), under the 24×24
minimum, and as a lone target in a table cell it does not qualify for the inline exception. It currently
passes **only** via 2.5.8's *Equivalent* exception — the `[ VIEW ]` link (`min-height:32px`,
`style.css:311`) is the conforming equivalent control. **The redundancy is load-bearing.** Keep both;
just add `aria-label="View {{ band.name }}"`.

## WCAG 2.2 new criteria — clean
Prior audits were all 2.1. Checked the five additions: **2.4.11** Focus Not Obscured — pass (no
`position:fixed/sticky` in current source; only stale on-disk legacy pages have it). **2.5.7** Dragging —
N/A. **2.5.8** Target Size — pass (see correction above; `.retro-button` ≈47px, `.retro-button-small`
32px, nav links 32px). **3.2.6 / 3.3.7 / 3.3.8** — N/A (no help mechanism, no forms, no auth).

---

## Verification performed

| Check | Result |
|---|---|
| `python -m py_compile app.py createAct.py` | ✅ |
| Jinja parse: base / index / generate / gallery | ✅ |
| Flask boot; `GET /`, `/generate`, `/gallery` | ✅ 200, 200, 200 |
| H-A + M-A differential test, pre-fix (real script, stub DOM) | ❌ 7 failures — bug reproduced |
| H-A + M-A differential test, post-fix | ✅ 8/8 pass |
