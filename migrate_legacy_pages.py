#!/usr/bin/env python3
"""
One-time migration script for legacy generated fan pages.

Fixes:
  N-023 (CRITICAL): Creates band_info.json for all band directories missing it.
  N-021 (HIGH):     Injects focus-visible CSS into existing pages' <style> blocks.
  N-024 (MEDIUM):   Replaces #666666 with #888888 for WCAG AA contrast compliance.
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
    """N-021 + N-024: Patch home.html with focus-visible and contrast fix."""
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
