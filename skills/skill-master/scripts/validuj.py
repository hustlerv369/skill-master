#!/usr/bin/env python3
"""Kontrola skillu pro Claude (Skill Master).

Použití:
    python validuj.py <složka-skillu> [--prisne]

Zkontroluje SKILL.md (frontmatter, název, popis, délku), odkazy na soubory,
kódování, podezřelé klíče a hesla a typické pasti na Windows.
Chyby (CHYBA) znamenají, že skill nebude fungovat nebo je nebezpečný.
Varování (POZOR) jsou doporučení. S --prisne neprojde ani varování.
Jen standardní knihovna Pythonu 3.8+.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:  # české znaky i na starší Windows konzoli
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RESERVED = ("anthropic", "claude")
KNOWN_KEYS = {
    "name", "description", "license", "allowed-tools", "metadata", "compatibility",
    "when_to_use", "argument-hint", "arguments", "disable-model-invocation", "user-invocable",
    "disallowed-tools", "model", "effort", "context", "agent", "background", "hooks", "paths", "shell",
}
SECRET_RES = [
    (re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}"), "klíč Anthropic"),
    (re.compile(r"\bsk-[A-Za-z0-9_\-]{30,}"), "klíč typu sk-… (OpenAI apod.)"),
    (re.compile(r"AIza[0-9A-Za-z_\-]{35}"), "klíč Google"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{40,}"), "token GitHub"),
    (re.compile(r"xox[abpr]-[A-Za-z0-9\-]{20,}"), "token Slack"),
    (re.compile(r"\b\d{8,10}:AA[A-Za-z0-9_\-]{30,}"), "token Telegram bota"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "privátní klíč"),
    (re.compile(r"(?i)\b(api[_-]?key|secret|password|heslo|token)\b\s*[:=]\s*[\"'][^\"'\s]{16,}[\"']"), "heslo nebo klíč přímo v textu"),
]
TEMPLATE_MARKERS = (  # věty ze šablony assets/SKILL-sablona.md – nesmí zůstat v hotovém skillu
    "Co skill dělá jednou větou",
    "vyjmenuj slova a situace",
    "Jedna až dvě věty: k čemu skill je",
    "Přesný formát výsledku (šablona",
)
TEXT_EXT = {".md", ".txt", ".py", ".js", ".mjs", ".ts", ".json", ".yaml", ".yml", ".sh", ".ps1",
            ".html", ".css", ".csv", ".toml", ".ini", ".bat", ".cmd"}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.ok: list[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def good(self, msg: str) -> None:
        self.ok.append(msg)


def parse_frontmatter(text: str) -> tuple[dict | None, str, str | None]:
    """Vrátí (data, tělo, chyba). Zkusí PyYAML, jinak jednoduchý parser."""
    text = text.lstrip("\ufeff")
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)$", text, re.DOTALL)
    if not m:
        return None, text, "SKILL.md nezačíná blokem --- frontmatter --- (musí být úplně na prvním řádku)."
    raw, body = m.group(1), m.group(2)
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(raw)
        if not isinstance(data, dict):
            return None, body, "Frontmatter není slovník klíč: hodnota."
        return data, body, None
    except ImportError:
        pass
    except Exception as e:  # chyba YAML
        return None, body, f"Frontmatter není platný YAML: {e}"
    # jednoduchý parser: klíč: hodnota, bloky > a |, vnořené klíče přeskočí
    data: dict = {}
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#") or line.startswith((" ", "\t")):
            i += 1
            continue
        km = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", line)
        if not km:
            return None, body, f"Nesrozumitelný řádek ve frontmatteru: {line!r}"
        key, val = km.group(1), km.group(2).strip()
        if val in (">", "|", ">-", "|-", ">+", "|+"):
            block = []
            i += 1
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            data[key] = (" " if val.startswith(">") else "\n").join(b for b in block if b)
            continue
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        data[key] = val if val != "" else {}
        i += 1
    return data, body, None


def check(skill_dir: Path) -> Report:
    r = Report()
    skill_md = skill_dir / "SKILL.md"
    if not skill_dir.is_dir():
        r.err(f"Složka {skill_dir} neexistuje.")
        return r
    if not skill_md.exists():
        alt = [p.name for p in skill_dir.iterdir() if p.name.lower() == "skill.md"]
        r.err("Chybí SKILL.md" + (f" (našel jsem {alt[0]} — název musí být přesně SKILL.md)." if alt else "."))
        return r
    raw = skill_md.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        r.err("SKILL.md není v kódování UTF-8. Ulož ho jako UTF-8.")
        return r
    data, body, perr = parse_frontmatter(text)
    if perr:
        r.err(perr)
        return r
    assert data is not None

    unknown = set(data) - KNOWN_KEYS
    if unknown:
        r.warn("Neznámé klíče ve frontmatteru: " + ", ".join(sorted(unknown)) + ". Překlep? Claude je nejspíš ignoruje.")

    # --- název
    name = data.get("name")
    if name is None or name == "":
        r.warn("Chybí 'name'. Claude Code pak použije název složky, ale pro claude.ai a sdílení ho vyplň.")
        name = skill_dir.name
    name = str(name).strip()
    if not NAME_RE.match(name):
        r.err(f"Název '{name}' smí mít jen malá písmena bez diakritiky, číslice a pomlčky (např. 'popis-videa').")
    if len(name) > 64:
        r.err(f"Název je dlouhý {len(name)} znaků, maximum je 64.")
    for word in RESERVED:
        if word in name:
            r.err(f"Název obsahuje vyhrazené slovo '{word}'. Zvol jiný (např. 'pomocnik-…').")
    if name != skill_dir.name:
        r.warn(f"Název '{name}' se liší od názvu složky '{skill_dir.name}'. Sjednoť je, ať se skill dá spolehlivě najít a vyvolat.")
    else:
        r.good(f"název '{name}'")

    # --- popis
    desc = data.get("description")
    if not desc or not str(desc).strip():
        r.err("Chybí 'description'. Bez popisu Claude neví, kdy skill použít.")
    else:
        desc = " ".join(str(desc).split())
        extra = " ".join(str(data.get("when_to_use", "")).split())
        if len(desc) > 1024:
            r.err(f"Popis má {len(desc)} znaků, maximum je 1024.")
        if len(desc) + len(extra) > 1536:
            r.warn("Popis + when_to_use mají přes 1536 znaků. Claude Code v seznamu skillů zbytek usekne.")
        if re.search(r"<[^>]+>", desc):
            r.err("Popis obsahuje XML/HTML značky (<…>). Nejsou povolené.")
        if len(desc) < 80:
            r.warn(f"Popis je krátký ({len(desc)} znaků). Napiš co skill dělá A kdy ho použít, včetně slov, kterými to lidé říkají.")
        low = (desc + " " + extra).lower()
        if not re.search(r"(použij|pouzij|kdy|když|kdyz|spust|aktivuj|use when|use this|when the user|trigger)", low):
            r.warn("Popis neříká, KDY se má skill spustit. Přidej např. 'Použij, když uživatel chce…'.")
        if re.search(r"\b(já |i can |i will |you can )", low):
            r.warn("Popis piš ve třetí osobě ('Vytvoří…', 'Creates…'), ne 'já umím' / 'you can'.")
        r.good(f"popis {len(desc)} znaků")

    # --- tělo
    body_lines = body.count("\n") + 1
    if body_lines > 500:
        r.warn(f"SKILL.md má {body_lines} řádků těla. Doporučeno pod 500 — detaily přesuň do references/.")
    else:
        r.good(f"tělo {body_lines} řádků")
    if len(body.strip()) < 200:
        r.warn("Tělo SKILL.md je skoro prázdné. Popiš postup, výstup a jak ověřit výsledek.")
    leftovers = [m for m in TEMPLATE_MARKERS if m in text]
    if leftovers:
        r.err("V SKILL.md zůstal nevyplněný text ze šablony (např. „" + leftovers[0] + "“). Vyplň popis i postup.")
    if desc and re.search(r"(^|[\s(„\"])…([\s)“\",.]|$)", str(desc)):
        r.warn("Popis obsahuje samostatné „…“ – nezůstal tam zástupný text?")
    if re.search(r"\b(TODO|DOPLŇ|DOPLN|XXX|lorem ipsum)\b", body, re.I):
        r.warn("V SKILL.md zůstal zástupný text (TODO / DOPLŇ / lorem ipsum).")
    caps = re.findall(r"\b(VŽDY|NIKDY|MUST|ALWAYS|NEVER)\b", body)
    if len(caps) > 8:
        r.warn(f"{len(caps)}× VŽDY/NIKDY velkými písmeny. Místo křiku vysvětli PROČ — model se pak chová chytřeji.")

    # --- odkazy na soubory
    links = set(re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", body))
    links |= set(re.findall(r"`((?:references|scripts|assets|templates|examples|reference|skripty)/[^`\s]+)`", body))
    missing = []
    for link in sorted(links):
        if re.match(r"^(https?:|mailto:|/|[A-Za-z]:)", link) or "${" in link or "<" in link or "…" in link:
            continue
        if not (skill_dir / link).exists():
            missing.append(link)
    if missing:
        r.err("SKILL.md odkazuje na soubory, které neexistují: " + ", ".join(missing))
    elif links:
        r.good(f"odkazy na soubory ({len(links)}) existují")
    if re.search(r"\]\([^)]*\\[^)]*\)", body):
        r.warn("V odkazech jsou zpětná lomítka (\\). Používej '/', funguje všude.")

    # --- všechny soubory: kódování, tajnosti, osobní cesty, PowerShell BOM
    files = [p for p in skill_dir.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    for p in files:
        rel = p.relative_to(skill_dir).as_posix()
        if p.name in (".env",) or p.suffix in (".pem", ".key"):
            r.err(f"{rel}: soubor s tajnými údaji nepatří do skillu. Smaž ho a použij proměnnou prostředí.")
            continue
        if p.suffix.lower() not in TEXT_EXT:
            continue
        b = p.read_bytes()
        try:
            t = b.decode("utf-8")
        except UnicodeDecodeError:
            r.err(f"{rel}: není v UTF-8.")
            continue
        for rx, what in SECRET_RES:
            if rx.search(t):
                r.err(f"{rel}: vypadá to na {what}. Klíče patří do proměnné prostředí, nikdy do skillu.")
                break
        if re.search(r"[A-Za-z]:[\\/]Users[\\/][A-Za-z0-9._-]+[\\/]|/Users/[a-z][A-Za-z0-9._-]*/|/home/[a-z][A-Za-z0-9._-]*/", t):
            r.warn(f"{rel}: obsahuje cestu k osobní složce (C:\\Users\\…). U sdíleného skillu použij relativní cesty nebo ~.")
        if p.suffix.lower() == ".ps1" and not b.startswith(b"\xef\xbb\xbf") and re.search(r"[^\x00-\x7f]", t):
            r.warn(f"{rel}: PowerShell skript s diakritikou bez BOM. Windows PowerShell 5.1 ho přečte rozbitě — ulož jako 'UTF-8 with BOM'.")
    big = [p for p in files if p.stat().st_size > 5_000_000]
    for p in big:
        r.warn(f"{p.relative_to(skill_dir).as_posix()}: {p.stat().st_size // 1_000_000} MB. Velké soubory zpomalí instalaci a sdílení.")

    scripts = [p for p in files if p.suffix in (".py", ".sh", ".js", ".mjs", ".ps1")]
    for s in scripts:
        if s.relative_to(skill_dir).as_posix() not in text and s.name not in text:
            r.warn(f"Skript {s.relative_to(skill_dir).as_posix()} není v SKILL.md zmíněný. Claude o něm nebude vědět.")
    for ref in [p for p in files if p.parent.name == "references" and p.suffix == ".md"]:
        rel = ref.relative_to(skill_dir).as_posix()
        if rel not in text and ref.name not in text:
            r.warn(f"{rel} není v SKILL.md zmíněný. Claude ho nebude číst – odkaž na něj, nebo ho smaž.")
        elif "Sem patří detaily, které Claude potřebuje jen někdy" in ref.read_text(encoding="utf-8", errors="ignore"):
            r.warn(f"{rel} je nevyplněná šablona.")
    return r


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    strict = "--prisne" in argv or "--strict" in argv
    if len(args) != 1:
        print(__doc__)
        return 2
    skill_dir = Path(args[0]).expanduser().resolve()
    r = check(skill_dir)
    print(f"Kontrola skillu: {skill_dir}")
    for m in r.ok:
        print(f"  OK     {m}")
    for m in r.warnings:
        print(f"  POZOR  {m}")
    for m in r.errors:
        print(f"  CHYBA  {m}")
    if r.errors:
        print(f"\nVÝSLEDEK: neprošlo ({len(r.errors)} chyb, {len(r.warnings)} varování).")
        return 1
    if strict and r.warnings:
        print(f"\nVÝSLEDEK: neprošlo v přísném režimu ({len(r.warnings)} varování).")
        return 1
    print(f"\nVÝSLEDEK: prošlo" + (f" s {len(r.warnings)} varováními." if r.warnings else " bez výhrad."))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
