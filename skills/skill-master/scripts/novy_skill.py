#!/usr/bin/env python3
"""Založí kostru nového skillu ze šablony (Skill Master).

Použití:
    python novy_skill.py <nazev-skillu> [--kam <složka>] [--s-referencemi] [--se-skripty]

Výchozí <složka> je aktuální adresář. Vznikne <složka>/<nazev-skillu>/SKILL.md
a podle přepínačů i references/ a scripts/. Existující složku nepřepíše.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "SKILL-sablona.md"


def main(argv: list[str]) -> int:
    args = argv[1:]
    if not args or args[0].startswith("-"):
        print(__doc__)
        return 2
    name = args[0]
    target = Path.cwd()
    if "--kam" in args:
        target = Path(args[args.index("--kam") + 1]).expanduser()
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        print("Název smí mít jen malá písmena bez diakritiky, číslice a pomlčky, max 64 znaků. Např. 'popis-videa'.")
        return 2
    if "claude" in name or "anthropic" in name:
        print("Slova 'claude' a 'anthropic' jsou v názvu skillu vyhrazená. Zvol jiné.")
        return 2
    skill_dir = target / name
    if skill_dir.exists():
        print(f"{skill_dir} už existuje. Nic jsem nepřepsal.")
        return 1
    skill_dir.mkdir(parents=True)
    text = TEMPLATE.read_text(encoding="utf-8").replace("{{NAZEV}}", name)
    (skill_dir / "SKILL.md").write_text(text, encoding="utf-8", newline="\n")
    if "--s-referencemi" in args:
        (skill_dir / "references").mkdir()
        (skill_dir / "references" / "podrobnosti.md").write_text(
            "# Podrobnosti\n\nSem patří detaily, které Claude potřebuje jen někdy.\n"
            "V SKILL.md napiš, KDY má tento soubor číst.\n", encoding="utf-8", newline="\n")
    if "--se-skripty" in args:
        (skill_dir / "scripts").mkdir()
        (skill_dir / "scripts" / "hlavni.py").write_text(
            '#!/usr/bin/env python3\n"""Co skript dělá, jaké má vstupy a výstupy."""\n'
            "import sys\n\n\ndef main() -> int:\n    print('hotovo')\n    return 0\n\n\n"
            "if __name__ == '__main__':\n    sys.exit(main())\n", encoding="utf-8", newline="\n")
    extra = []
    if "--s-referencemi" in args:
        extra.append("- Když potřebuješ podrobnosti k …, přečti `references/podrobnosti.md`.")
    if "--se-skripty" in args:
        extra.append("- Hlavní práci udělej skriptem: `python scripts/hlavni.py` (popiš vstupy a výstup).")
    if extra:
        with (skill_dir / "SKILL.md").open("a", encoding="utf-8", newline="\n") as f:
            f.write("\n## Soubory skillu\n\n" + "\n".join(extra) + "\n")
    print(f"Založeno: {skill_dir}")
    print("Další krok: vyplň v SKILL.md popis (description) a postup, pak spusť validuj.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
