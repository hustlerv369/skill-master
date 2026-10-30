#!/usr/bin/env python3
"""Nainstaluje skill do Claude Code (Skill Master).

Použití:
    python nainstaluj.py <složka-skillu>                 # pro tebe, ve všech projektech (~/.claude/skills)
    python nainstaluj.py <složka-skillu> --projekt <dir> # jen pro jeden projekt (<dir>/.claude/skills)
    python nainstaluj.py <složka-skillu> --codex         # navíc pro OpenAI Codex (~/.agents/skills)

Nejdřív skill zkontroluje. Existující verzi nepřepíše natvrdo: uloží ji vedle jako
<nazev>.zaloha-<datum-cas>. Nic nemaže.
"""
from __future__ import annotations

import shutil
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validuj import check  # noqa: E402

IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".git", ".env", "*-workspace")


def install(src: Path, base: Path) -> None:
    dst = base / src.name
    if dst.exists() and dst.resolve() == src:
        print(f"Skill už leží v {dst}. Není co kopírovat.")
        return
    base.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        backup = dst.with_name(f"{dst.name}.zaloha-{time.strftime('%Y%m%d-%H%M%S')}")
        shutil.move(str(dst), str(backup))
        print(f"Předchozí verzi jsem uložil do {backup}")
    shutil.copytree(src, dst, ignore=IGNORE)
    print(f"Nainstalováno: {dst}")


def main(argv: list[str]) -> int:
    args = argv[1:]
    if not args or args[0].startswith("-"):
        print(__doc__)
        return 2
    src = Path(args[0]).expanduser().resolve()
    if "--projekt" in args:
        base = Path(args[args.index("--projekt") + 1]).expanduser().resolve() / ".claude" / "skills"
    else:
        base = Path.home() / ".claude" / "skills"
    r = check(src)
    if r.errors:
        print("Skill neprošel kontrolou, neinstaluji:")
        for e in r.errors:
            print("  CHYBA  " + e)
        return 1
    bases = [base]
    if "--codex" in args:
        bases.append(Path.home() / ".agents" / "skills")
    for b in bases:
        install(src, b)
    print("Claude Code nový skill pozná sám. Když ho nevidí, napiš v Claude Code /reload-skills nebo otevři novou relaci.")
    print(f"Vyzkoušej ho: napiš úkol, na který se má spustit, nebo /{src.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
