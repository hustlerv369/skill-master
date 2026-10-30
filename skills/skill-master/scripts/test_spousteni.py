#!/usr/bin/env python3
"""Otestuje, jestli se skill spouští na správné věty (a nespouští na špatné).

Použití:
    python test_spousteni.py <složka-skillu> <dotazy.json> [--opakovani 2] [--model sonnet] [--paralelne 3]

dotazy.json:
    [
      {"dotaz": "realistická věta uživatele…", "spustit": true},
      {"dotaz": "podobná věta, kde skill použít nemá…", "spustit": false}
    ]

Potřebuje Claude Code (příkaz `claude`) přihlášený na tvém předplatném. Každý dotaz
spustí v čisté dočasné složce, kde je nainstalovaný jen testovaný skill, a sleduje,
jestli Claude skill zavolá. Nic nemění na tvých souborech ani nastavení.
Pozor: každý běh čerpá limit předplatného. 20 dotazů × 2 opakování = 40 krátkých běhů.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TIMEOUT = 180  # s na jeden běh; Claude se rozhoduje o skillu v prvních krocích


def arg(args: list[str], name: str, default: str) -> str:
    return args[args.index(name) + 1] if name in args else default


def run_once(skill_dir: Path, query: str, model: str) -> tuple[bool, str]:
    """Vrátí (spustil_se, poznámka)."""
    claude = shutil.which("claude")
    if not claude:
        raise SystemExit("Nenašel jsem příkaz 'claude'. Nainstaluj Claude Code a přihlas se.")
    with tempfile.TemporaryDirectory(prefix="skilltest-") as tmp:
        dst = Path(tmp) / ".claude" / "skills" / skill_dir.name
        shutil.copytree(skill_dir, dst, ignore=shutil.ignore_patterns("__pycache__", "*-workspace", ".git"))
        cmd = [claude, "-p", query, "--output-format", "stream-json", "--verbose",
               "--max-turns", "2", "--model", model,
               "--setting-sources", "project", "--strict-mcp-config",
               "--disallowedTools", "Bash,Edit,Write,NotebookEdit,WebFetch,WebSearch"]
        try:
            proc = subprocess.Popen(cmd, cwd=tmp, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                    stdin=subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace")
        except OSError as e:
            return False, f"nelze spustit claude: {e}"
        hit, note, start = False, "", time.time()
        try:
            assert proc.stdout is not None
            for line in proc.stdout:
                if time.time() - start > TIMEOUT:
                    note = "časový limit"
                    break
                try:
                    ev = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = ev.get("message") if isinstance(ev, dict) else None
                content = msg.get("content") if isinstance(msg, dict) else None
                for block in content if isinstance(content, list) else []:
                    if not isinstance(block, dict) or block.get("type") != "tool_use":
                        continue
                    inp = block.get("input") or {}
                    name = block.get("name", "")
                    if name == "Skill" and skill_dir.name in json.dumps(inp, ensure_ascii=False):
                        hit = True
                    elif name == "Read" and f"{skill_dir.name}/SKILL.md" in str(inp.get("file_path", "")).replace("\\", "/"):
                        hit = True
                if hit:
                    break
        finally:
            proc.kill()
            proc.wait()
        return hit, note


def main(argv: list[str]) -> int:
    args = argv[1:]
    pos = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or not args[i - 1].startswith("--"))]
    if len(pos) != 2:
        print(__doc__)
        return 2
    skill_dir = Path(pos[0]).expanduser().resolve()
    cases = json.loads(Path(pos[1]).read_text(encoding="utf-8"))
    reps = int(arg(args, "--opakovani", "2"))
    model = arg(args, "--model", "sonnet")
    par = int(arg(args, "--paralelne", "3"))
    jobs = [(i, c) for i, c in enumerate(cases) for _ in range(reps)]
    print(f"Testuji '{skill_dir.name}': {len(cases)} dotazů × {reps} = {len(jobs)} běhů (model {model}) …")
    results: dict[int, list[bool]] = {i: [] for i in range(len(cases))}
    with ThreadPoolExecutor(max_workers=par) as ex:
        futs = [(i, ex.submit(run_once, skill_dir, c["dotaz"], model)) for i, c in jobs]
        for i, f in futs:
            try:
                hit, _ = f.result()
            except Exception as e:  # jeden rozbitý běh nesmí shodit celý test
                print(f"  běh selhal: {e}")
                hit = False
            results[i].append(hit)
    ok_total = 0
    print()
    for i, c in enumerate(cases):
        hits = sum(results[i])
        rate = hits / len(results[i])
        want = bool(c.get("spustit", True))
        passed = rate >= 0.5 if want else rate < 0.5
        ok_total += passed
        mark = "OK " if passed else "XX "
        exp = "má spustit  " if want else "nemá spustit"
        print(f"{mark} {exp}  spuštěno {hits}/{len(results[i])}  {c['dotaz'][:90]}")
    print(f"\nVÝSLEDEK: {ok_total}/{len(cases)} správně.")
    print("Když skill nereaguje, kde má: přidej do popisu slova, kterými to lidé říkají.")
    print("Když reaguje, kde nemá: dopiš do popisu, kdy ho NEpoužívat.")
    return 0 if ok_total == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
