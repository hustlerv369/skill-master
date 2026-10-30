#!/usr/bin/env python3
"""Zabalí skill do ZIPu pro nahrání do Claude (web / desktop aplikace) nebo pro sdílení.

Použití:
    python zabal.py <složka-skillu> [--vystup <složka>]

Nejdřív spustí validuj.py. Když skill neprojde, nic nezabalí.
ZIP obsahuje složku skillu jako kořen (<nazev>/SKILL.md …), bez __pycache__,
.git, .env a dočasných souborů.
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validuj import check  # noqa: E402

SKIP_DIRS = {"__pycache__", ".git", "node_modules", ".venv", "venv", ".pytest_cache"}
SKIP_FILES = {".env", ".DS_Store", "Thumbs.db"}


def main(argv: list[str]) -> int:
    args = argv[1:]
    if not args or args[0].startswith("-"):
        print(__doc__)
        return 2
    skill_dir = Path(args[0]).expanduser().resolve()
    out_dir = Path(args[args.index("--vystup") + 1]).expanduser() if "--vystup" in args else skill_dir.parent
    r = check(skill_dir)
    if r.errors:
        print("Skill neprošel kontrolou, nebalím. Spusť: python validuj.py " + str(skill_dir))
        for e in r.errors:
            print("  CHYBA  " + e)
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / f"{skill_dir.name}.zip"
    n = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(skill_dir.rglob("*")):
            rel = p.relative_to(skill_dir)
            if any(part in SKIP_DIRS for part in rel.parts) or p.name in SKIP_FILES or p.suffix in (".pyc", ".tmp", ".log"):
                continue
            if p.is_file():
                z.write(p, (Path(skill_dir.name) / rel).as_posix())
                n += 1
    print(f"Zabaleno {n} souborů: {zip_path}")
    if r.warnings:
        print(f"(Kontrola našla {len(r.warnings)} varování — doporučuji je projít.)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
