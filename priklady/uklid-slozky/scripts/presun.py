#!/usr/bin/env python3
"""Provede schválený plán přesunů, nebo ho vrátí. Nikdy nic nemaže ani nepřepisuje.

Použití:
    python presun.py plan.json              # přesune podle plánu, zapíše presun-log.json
    python presun.py --zpet presun-log.json # vrátí soubory zpět
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def volne_jmeno(cil: Path) -> Path:
    """Když soubor existuje, vrátí 'nazev (2).pripona' atd. — nikdy nepřepisujeme."""
    if not cil.exists():
        return cil
    i = 2
    while True:
        kandidat = cil.with_name(f"{cil.stem} ({i}){cil.suffix}")
        if not kandidat.exists():
            return kandidat
        i += 1


def presun(src: Path, dst: Path) -> Path | None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst = volne_jmeno(dst)
    try:
        shutil.move(str(src), str(dst))
        return dst
    except (PermissionError, OSError) as e:
        print(f"Přeskočeno (soubor je otevřený nebo zamčený): {src.name} – {e}")
        return None


def main() -> int:
    args = sys.argv[1:]
    if args[:1] == ["--zpet"] and len(args) == 2:
        log = json.loads(Path(args[1]).read_text(encoding="utf-8"))
        vraceno = 0
        for z in reversed(log["presunuto"]):
            if presun(Path(z["do"]), Path(z["z"])):
                vraceno += 1
        for d in {Path(z["do"]).parent for z in log["presunuto"]}:
            try:
                d.rmdir()  # smaže jen PRÁZDNOU složku, kterou úklid vytvořil
            except OSError:
                pass
        print(f"Vráceno {vraceno} z {len(log['presunuto'])} souborů.")
        return 0
    if len(args) != 1:
        print(__doc__)
        return 2
    plan = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    root = Path(plan["slozka"])
    pred = sum(1 for p in root.rglob("*") if p.is_file())
    log = {"slozka": str(root), "presunuto": []}
    for item in plan["presuny"]:
        src = root / item["soubor"]
        if not src.is_file():
            print(f"Nenalezeno, přeskakuji: {item['soubor']}")
            continue
        dst = presun(src, root / item["cil"] / src.name)
        if dst:
            log["presunuto"].append({"z": str(src), "do": str(dst)})
    log_path = Path(args[0]).with_name("presun-log.json")
    log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    po = sum(1 for p in root.rglob("*") if p.is_file())
    print(f"Přesunuto {len(log['presunuto'])} souborů. Souborů před: {pred}, po: {po} (má být stejně).")
    print(f"Log pro vrácení: {log_path}")
    return 0 if pred == po else 1


if __name__ == "__main__":
    sys.exit(main())
