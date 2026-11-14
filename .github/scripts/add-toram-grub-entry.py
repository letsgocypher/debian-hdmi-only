#!/usr/bin/env python3
"""Add an explicit GRUB live-boot entry that copies the Debian live medium to RAM."""
from pathlib import Path
import re
import sys

cfg = Path(sys.argv[1])
text = cfg.read_text()
if "toram" in text:
    raise SystemExit("toram already present; refusing to add duplicate entries")

# Locate complete top-level GRUB menuentry blocks using brace depth.
entries = []
for match in re.finditer(r"(?m)^menuentry\s+(['\"])(.*?)\1[^\n]*\{", text):
    start = match.start()
    brace = text.find("{", match.start())
    depth = 0
    quote = None
    escaped = False
    end = None
    for i in range(brace, len(text)):
        ch = text[i]
        if quote:
            if escaped:
                escaped = False
            elif ch == "\\\\":
                escaped = True
            elif ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end is not None:
        entries.append((match.group(2), text[start:end]))

# Clone the ordinary live entry, not failsafe/rescue entries.
chosen = None
for title, block in entries:
    if "boot=live" in block and "failsafe" not in title.lower() and "failsafe" not in block.lower():
        if re.search(r"(?m)^\s*linux(?:efi)?\s+.*boot=live", block):
            chosen = (title, block)
            break

if chosen is None:
    raise SystemExit("Could not find a normal GRUB live entry; refusing to publish an ISO without a RAM option")

title, block = chosen
new_title = title + " (Copy to RAM)"
new_block = re.sub(r"^menuentry\s+(['\"]).*?\1", lambda m: m.group(0).replace(m.group(0)[len("menuentry "):], "'" + new_title + "'", 1), block, count=1)
new_block, count = re.subn(r"(?m)^(\s*linux(?:efi)?\s+[^\n]*\bboot=live[^\n]*)$", r"\1 toram", new_block, count=1)
if count != 1:
    raise SystemExit("Could not add toram to the live kernel command line")

cfg.write_text(text.rstrip() + "\n\n# Optional live session copied into RAM; USB can be removed after boot completes.\n" + new_block + "\n")
print(f"Added GRUB entry: {new_title}")
