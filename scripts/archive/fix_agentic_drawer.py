#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIX AGENTIC BROWSING & ARIA-HIDDEN ACCESSIBILITY TREE ISSUE
Resolves: "ARIA hidden element must not be focusable or contain focusable elements" on #lttMobileDrawer
Enforces:
1. 'inert' attribute on #lttMobileDrawer when closed
2. visibility: hidden !important and pointer-events: none !important when closed
3. visibility: visible !important and pointer-events: auto !important when .is-open
4. JavaScript toggle updates inert and aria-hidden in sync
"""

import os
import re
import glob

BASE_DIR = '/Users/adamdimitrov/Development/budapest-adventures'

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_content = content

    # 1. Update HTML tag: add inert to #lttMobileDrawer
    # Matches <div aria-hidden="true" class="ltt-mobile-drawer" id="lttMobileDrawer"> or any variant
    content = re.sub(
        r'<div\s+([^>]*?)id=[\"\']lttMobileDrawer[\"\']([^>]*)>',
        lambda m: f'<div {m.group(1)}id="lttMobileDrawer"{m.group(2)}>'.replace('aria-hidden="true"', 'aria-hidden="true" inert') if 'inert' not in m.group(0) else m.group(0),
        content
    )

    # 2. Add visibility and pointer-events rules in CSS
    # Check if our drawer fix is already in CSS
    if '/* LTT_AGENTIC_DRAWER_ACCESSIBILITY_FIX */' not in content:
        drawer_css_fix = """
/* LTT_AGENTIC_DRAWER_ACCESSIBILITY_FIX */
.ltt-mobile-drawer:not(.is-open){visibility:hidden !important;pointer-events:none !important;display:none !important;}
.ltt-mobile-drawer.is-open{visibility:visible !important;pointer-events:auto !important;display:block !important;}
"""
        # Append before </head> or inside an existing style tag
        if '</head>' in content:
            content = content.replace('</head>', f'<style>{drawer_css_fix.strip()}</style></head>', 1)
        elif '</style>' in content:
            content = content.replace('</style>', f'{drawer_css_fix}</style>', 1)

    # 3. Update JavaScript in ltt-nav-script
    # When opening: remove inert, aria-hidden="false"
    # When closing: set inert, aria-hidden="true"
    old_open_block = "drawer.classList.add('is-open');\n        toggle.classList.add('is-active');\n        toggle.setAttribute('aria-expanded', 'true');\n        drawer.setAttribute('aria-hidden', 'false');"
    new_open_block = "drawer.classList.add('is-open');\n        toggle.classList.add('is-active');\n        toggle.setAttribute('aria-expanded', 'true');\n        drawer.setAttribute('aria-hidden', 'false');\n        drawer.removeAttribute('inert');"

    old_close_block = "drawer.classList.remove('is-open');\n        toggle.classList.remove('is-active');\n        toggle.setAttribute('aria-expanded', 'false');\n        drawer.setAttribute('aria-hidden', 'true');"
    new_close_block = "drawer.classList.remove('is-open');\n        toggle.classList.remove('is-active');\n        toggle.setAttribute('aria-expanded', 'false');\n        drawer.setAttribute('aria-hidden', 'true');\n        drawer.setAttribute('inert', '');"

    content = content.replace(old_open_block, new_open_block)
    content = content.replace(old_close_block, new_close_block)

    if content != orig_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed agentic drawer accessibility in {os.path.relpath(file_path, BASE_DIR)}")
        return True
    return False

def run_fix():
    print("=== FIXING AGENTIC BROWSING ARIA-HIDDEN ISSUE ACROSS ALL PAGES ===")
    
    # Target all html files in repo
    all_files = glob.glob(os.path.join(BASE_DIR, '**/*.html'), recursive=True)
    count = 0
    for p in all_files:
        if fix_file(p):
            count += 1
            
    print(f"\nSuccessfully applied Agentic Browsing fix to {count} files.")

if __name__ == '__main__':
    run_fix()
