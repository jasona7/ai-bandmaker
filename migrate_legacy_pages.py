#!/usr/bin/env python3
"""
One-time migration script for legacy generated fan pages.

Fixes:
  N-023 (CRITICAL): Creates band_info.json for all band directories missing it.
  N-021 (HIGH):     Injects focus-visible CSS into existing pages' <style> blocks.
  N-024 (MEDIUM):   Replaces #666666 with #888888 for WCAG AA contrast compliance.
  N-033 (HIGH):     Wraps the v1-template <marquee> band-name heading in an
                    <h1 class="band-title"> element so v1 fan pages have a
                    proper top-level heading (WCAG SC 1.3.1 / SC 2.4.6). The
                    marquee element is preserved inside the <h1> so the
                    visual animation behavior is unchanged. Idempotent: a
                    second run is a no-op once the <h1> is in place.
"""

import json
import os
import re
import sys
from datetime import datetime


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Directories to skip (not band directories)
SKIP_DIRS = {
    'static', 'templates', 'examples', 'venv', '__pycache__',
    'logs', 'media', 'tasks', '.git',
}

FOCUS_VISIBLE_CSS = """
    /* N-021 migration: keyboard focus indicators */
    a:focus-visible {
      outline: 2px solid #ffff00;
      outline-offset: 2px;
    }
    """

# N-033 migration: v1 fan pages render the band name inside <marquee> with no
# surrounding heading element, violating WCAG SC 1.3.1 (Info and Relationships)
# and SC 2.4.6 (Headings and Labels). The shape is uniform across the 8 v1
# pages: an indented line "<marquee scrollamount=\"3\">{band_name}</marquee>"
# in the page header table. We wrap that exact element in an <h1> so the page
# now has a proper top-level heading while preserving the marquee animation.
# The marquee tag content has no '<' inside, so [^<]+ is safe.
N033_MARQUEE_RE = re.compile(r'<marquee scrollamount="3">([^<]+)</marquee>')


def find_band_directories():
    """Find all directories containing a home.html file."""
    bands = []
    for entry in os.listdir(PROJECT_ROOT):
        if entry in SKIP_DIRS or entry.startswith('.'):
            continue
        full_path = os.path.join(PROJECT_ROOT, entry)
        if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, 'home.html')):
            bands.append((entry, full_path))
    return bands


def derive_display_name(dir_name):
    """Derive a display name from a CamelCase directory name."""
    return re.sub(r'([A-Z])', r' \1', dir_name).strip()


def create_band_info(dir_name, band_path):
    """N-023: Create band_info.json if missing."""
    info_path = os.path.join(band_path, 'band_info.json')
    if os.path.exists(info_path):
        return False

    info = {
        'display_name': derive_display_name(dir_name),
        'template_version': 1,
        'generated_at': datetime.now().isoformat(),
        'migrated': True,
    }
    with open(info_path, 'w') as f:
        json.dump(info, f, indent=2)
    return True


def patch_html(band_path):
    """N-021 + N-024 + N-033: Patch home.html for accessibility fixes."""
    html_path = os.path.join(band_path, 'home.html')
    with open(html_path, 'r') as f:
        content = f.read()

    changed = False

    # N-021: Inject focus-visible CSS before </style>
    if 'focus-visible' not in content and '</style>' in content:
        content = content.replace('</style>', FOCUS_VISIBLE_CSS + '</style>', 1)
        changed = True

    # N-024: Fix contrast — #666666 on #000000 fails WCAG AA (3.66:1)
    if '#666666' in content:
        content = content.replace('#666666', '#888888')
        changed = True

    # N-033: Wrap v1 <marquee scrollamount="3">{band_name}</marquee> in <h1>.
    # Idempotency: only the 8 v1 pages contain this exact element shape; the
    # 4 legacy pages already have <h1> and have no <marquee>. We additionally
    # gate on the absence of '<h1 class="band-title">' so a re-run is a no-op
    # even if someone re-ran createAct.py and re-introduced an unwrapped
    # marquee (defense-in-depth; createAct.py v2 already emits <h1>).
    if 'class="band-title"' not in content and N033_MARQUEE_RE.search(content):
        content = N033_MARQUEE_RE.sub(
            r'<h1 class="band-title"><marquee scrollamount="3">\1</marquee></h1>',
            content,
            count=1,
        )
        changed = True

    if changed:
        with open(html_path, 'w') as f:
            f.write(content)

    return changed


def main():
    bands = find_band_directories()
    if not bands:
        print("No band directories found.")
        return

    print(f"Found {len(bands)} band directories.\n")

    info_created = 0
    html_patched = 0

    for dir_name, band_path in sorted(bands):
        actions = []

        if create_band_info(dir_name, band_path):
            info_created += 1
            actions.append("band_info.json created")

        if patch_html(band_path):
            html_patched += 1
            actions.append("home.html patched")

        status = ", ".join(actions) if actions else "no changes needed"
        print(f"  {dir_name}: {status}")

    print(f"\nDone. Created {info_created} band_info.json files, patched {html_patched} HTML files.")


if __name__ == '__main__':
    main()
