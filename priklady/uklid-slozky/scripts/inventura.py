#!/usr/bin/env python3
"""Inventura složky: navrhne, kam který soubor přesunout. Nic nemění.

Použití: python inventura.py <složka> > plan.json
"""
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

KATEGORIE = {
    "Obrázky": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic", ".svg", ".bmp", ".tif", ".tiff"},
    "Dokumenty": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".ods", ".txt", ".md", ".csv", ".rtf"},
    "Videa": {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v"},
    "Hudba": {".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"},
    "Archivy": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Instalátory": {".exe", ".msi", ".dmg", ".pkg", ".deb", ".appimage"},
}


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).expanduser().resolve()
    if not root.is_dir():
        print(f"Složka {root} neexistuje.", file=sys.stderr)
        return 1
    plan = []
    for p in sorted(root.iterdir()):
        if not p.is_file() or p.name.startswith("."):
            continue  # podsložky a skryté soubory necháváme být
        cil = next((k for k, ext in KATEGORIE.items() if p.suffix.lower() in ext), "Ostatní")
        plan.append({"soubor": p.name, "cil": cil})
    souhrn = {}
    for item in plan:
        souhrn[item["cil"]] = souhrn.get(item["cil"], 0) + 1
    print(json.dumps({"slozka": str(root), "souhrn": souhrn, "presuny": plan}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
