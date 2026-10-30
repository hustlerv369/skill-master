# Instalace a sdílení skillu

## Claude Code

| Kam | Cesta | Pro koho |
|---|---|---|
| osobní | `~/.claude/skills/<nazev>/SKILL.md` | ty, ve všech projektech |
| projekt | `<projekt>/.claude/skills/<nazev>/SKILL.md` | každý, kdo pracuje v projektu (dá se commitnout do gitu) |
| plugin | `<plugin>/skills/<nazev>/SKILL.md` | kdo si nainstaluje plugin; volá se `/plugin:nazev` |

- Při stejném názvu má přednost osobní skill před projektovým.
- Změny ve skillu Claude Code pozná sám, bez restartu. Když vytvoříš úplně novou složku `skills`, která při startu neexistovala, napiš `/reload-skills`.
- Instalace jedním příkazem: `python scripts/nainstaluj.py <složka-skillu>` (záloha předchozí verze, nic nemaže). Pro jeden projekt přidej `--projekt <cesta>`.

## Claude.ai a desktopová aplikace

1. `python scripts/zabal.py <složka-skillu>` → vznikne `<nazev>.zip` (uvnitř složka `<nazev>/SKILL.md`).
2. V Claude: **Customize → Skills → „+“ → Create skill → Upload a skill**, vyber ZIP a skill zapni.
3. Musí být zapnuté spouštění kódu / „Create and edit files“ (Nastavení → Capabilities).
4. Skilly nahrané na claude.ai jsou jen tvoje; každý člověk si je nahrává sám.

Názvy menu se občas mění. Když položku nenajdeš, hledej „Skills“ v nastavení.

## OpenAI Codex a další nástroje

Formát skillu je otevřený standard (agentskills.io). OpenAI Codex čte skilly z:
- `~/.agents/skills/<nazev>/` (pro tebe),
- `<projekt>/.agents/skills/<nazev>/` (pro projekt).

`python scripts/nainstaluj.py <složka-skillu> --codex` nainstaluje skill zároveň pro Claude Code i Codex.
Funkce jen pro Claude Code (`context: fork`, `hooks`…) jinde nefungují – drž se standardních polí, pokud má skill běžet všude.

## Sdílení přes GitHub (plugin marketplace)

Nejpohodlnější pro komunitu: repozitář, který je zároveň **marketplace pluginů**.

```
muj-repozitar/
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
└── skills/
    └── nazev-skillu/SKILL.md
```

`marketplace.json`:
```json
{
  "name": "muj-repozitar",
  "owner": {"name": "Tvoje jméno"},
  "plugins": [{"name": "muj-plugin", "source": "./", "description": "…"}]
}
```

`plugin.json`:
```json
{"name": "muj-plugin", "description": "…", "version": "1.0.0", "author": {"name": "Tvoje jméno"}}
```

Uživatel pak v Claude Code napíše:
```
/plugin marketplace add tvuj-github/muj-repozitar
/plugin install muj-plugin@muj-repozitar
```

Před zveřejněním:
- `python scripts/validuj.py <skill> --prisne`,
- žádné klíče, osobní cesty ani soukromá data (validátor je hledá, ale přečti to i očima),
- README: co skill dělá, jak nainstalovat, ukázka použití, licence.

## Verze

- Do `metadata` dej `version: 1.0.0` a veď krátký `CHANGELOG.md`.
- Při úpravě existujícího skillu **neměň `name`** – jinak vznikne druhý skill vedle starého.
