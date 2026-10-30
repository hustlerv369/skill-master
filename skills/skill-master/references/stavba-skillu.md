# Stavba skillu

## Obsah
1. Anatomie
2. Frontmatter – všechna pole
3. Postupné načítání (progressive disclosure)
4. Jak psát tělo SKILL.md
5. Vzory, které fungují
6. Argumenty a ruční spouštění
7. Kdy skill rozdělit

## 1. Anatomie

```
nazev-skillu/
├── SKILL.md          povinný: frontmatter + návod
├── references/       podrobnosti, které Claude čte jen když je potřebuje
├── scripts/          kód pro opakovanou nebo přesnou práci (spouští se, nečte)
└── assets/           šablony, obrázky, fonty – použijí se ve výstupu
```

Složka se jmenuje stejně jako `name`. Soubor se jmenuje přesně `SKILL.md`.

## 2. Frontmatter – všechna pole

Blok `---` musí být úplně na prvním řádku souboru. Když YAML nejde přečíst, skill se načte bez polí.

**Standard Agent Skills (funguje v Claude Code, claude.ai, API i v jiných nástrojích, např. Codex):**

| Pole | Povinné | Význam |
|---|---|---|
| `name` | ano* | malá písmena bez diakritiky, číslice, pomlčky; max 64 znaků; bez slov `claude` a `anthropic`; stejné jako název složky |
| `description` | ano | co dělá a kdy ho použít (viz `references/popis-a-spousteni.md`) |
| `license` | ne | licence, např. `MIT` |
| `compatibility` | ne | co skill potřebuje (Python, internet…), max 500 znaků |
| `metadata` | ne | cokoliv dalšího, např. `version`, `author` |
| `allowed-tools` | ne | nástroje, které skill smí použít bez ptaní |

\* Claude Code bez `name` použije název složky. Pro sdílení ho vždy vyplň.

**Navíc jen v Claude Code:**

| Pole | Význam |
|---|---|
| `when_to_use` | další text „kdy“, připojí se k popisu |
| `disable-model-invocation: true` | skill spustí jen uživatel přes `/nazev`. Použij u skillů s vedlejšími účinky (nasazení, odeslání, mazání) |
| `user-invocable: false` | skill se neukáže v nabídce `/`, Claude ho ale použít může (znalostní skilly) |
| `argument-hint`, `arguments` | nápověda a pojmenované argumenty pro `/nazev …` |
| `allowed-tools` / `disallowed-tools` | předschválené / zakázané nástroje, dokud skill běží |
| `model`, `effort` | model a úsilí pro daný krok |
| `context: fork` (+ `agent`) | skill poběží v samostatném subagentovi bez historie konverzace |
| `paths` | skill se nabízí jen u souborů odpovídajících vzoru |
| `shell` | `bash` (výchozí) nebo `powershell` pro příkazy ve skillu |
| `hooks` | hooky, které se zaregistrují po spuštění skillu |

Neznámá pole Claude ignoruje bez chyby – překlep tedy nic neohlásí. Proto `validuj.py`.

## 3. Postupné načítání

1. **Název + popis** – Claude je vidí vždycky (proto krátké a výstižné).
2. **Tělo SKILL.md** – načte se, až když se skill spustí. Drž ho **pod 500 řádků**.
3. **Soubory v references/, scripts/, assets/** – jen když je Claude potřebuje. Skripty se spouštějí, jejich obsah se do kontextu nedostane.

Pravidla:
- Na každý soubor odkaž **přímo ze SKILL.md** a napiš, **kdy** ho číst („Když řešíš X, přečti `references/x.md`“). Odkazy z referencí na další reference Claude často dočte jen napůl.
- Soubor delší než ~100 řádků začni obsahem (seznam kapitol).
- Pro skill s variantami (AWS / GCP / Azure, Windows / Mac) dej každou variantu do vlastního souboru. Claude si přečte jen tu svou.
- V cestách používej `/`, i na Windows.

## 4. Jak psát tělo SKILL.md

- **Rozkazovací způsob**, krátké kroky: „Přečti…“, „Spusť…“, „Ověř…“.
- **Vysvětli proč.** Model je chytrý; když ví, proč pravidlo existuje, poradí si i v situaci, kterou jsi nepopsal. Místo „NIKDY nestříhej ve slově“ napiš „Stříhej jen v tichu – řez uprostřed slova je slyšet a divák ho vnímá jako chybu.“ Řádek plný VŽDY/NIKDY velkými písmeny je varovný signál.
- **Ukaž výstup.** Šablona nebo příklad vstup → výstup řekne víc než odstavec popisu.
- **Krok ověření.** Jak poznat, že výsledek je dobrý. „Skript doběhl“ neznamená „funguje“.
- **Nic, co zastará.** Žádné „od srpna 2026 použij…“. Když je to nutné, dej starý postup do sekce „Starší postup“.
- **Konzistentní pojmy.** Jedna věc = jedno slovo v celém skillu.
- **Ne moc úzce.** Skill poběží na stovkách různých zadání, ne jen na tvých třech testech.

## 5. Vzory, které fungují

**Tabulka „kdy ano / kdy ne“** na začátku – rychle vymezí hranice:
```markdown
| Situace | Co dělat |
|---|---|
| Uživatel chce popis videa z přepisu | Postupuj podle skillu |
| Uživatel chce jen titulek | Skill nepoužívej |
```

**Kontrolní seznam** u dlouhých postupů – Claude si ho zkopíruje a odškrtává:
```markdown
Postup (zkopíruj a odškrtávej):
- [ ] 1. Inventura
- [ ] 2. Návrh a schválení
- [ ] 3. Provedení
- [ ] 4. Kontrola
```

**Plán → schválení → provedení** u čehokoliv, co mění soubory nebo něco odesílá.

**Smyčka ověření:** udělej → zkontroluj (skript, porovnání) → oprav → znovu zkontroluj.

**Šablona výstupu** v `assets/` – stejný vzhled pokaždé.

**Skript místo popisu** – když by Claude pokaždé psal stejný kód (převod, validace, výpočet), napiš ho jednou do `scripts/`. Skript má hlásit srozumitelné chyby, ne padat. Každé číslo v něm (limit, časový interval) vysvětli komentářem.

## 6. Argumenty a ruční spouštění (Claude Code)

- Uživatel může skill spustit ručně: `/nazev-skillu text`.
- V těle SKILL.md: `$ARGUMENTS` = celý text za příkazem, `$0`, `$1`… = jednotlivé argumenty (od nuly, uvozovky drží víc slov dohromady).
- Když skill nemá žádný zástupný symbol, Claude Code text přidá na konec jako `ARGUMENTS: …`.
- Doslovný dolar napiš jako `\$`.

## 7. Kdy skill rozdělit

- Jeden skill = jedna práce. Když popis potřebuje „a taky… a navíc…“, jsou to nejspíš dva skilly.
- Skilly se můžou odkazovat: „Na zvuk použij skill `audio-mix`.“
- Společná pravidla pro všechny skilly (styl, bezpečnost) patří spíš do `CLAUDE.md` než do každého skillu zvlášť.
