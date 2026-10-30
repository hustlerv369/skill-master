# Popis (description) a spouštění skillu

Popis je nejdůležitější řádek celého skillu. Claude na začátku každé relace vidí jen
**název a popis** všech skillů. Podle popisu se rozhodne, jestli si skill otevře.
Špatný popis = skill, který nikdy nepoběží, i kdyby jeho obsah byl geniální.

## Obsah
1. Jak se Claude rozhoduje
2. Recept na popis
3. Česká specifika
4. Příklady: špatně → dobře
5. Limity délky
6. Jak popis ladit

## 1. Jak se Claude rozhoduje

- Skill si Claude otevře, když úkol odpovídá popisu **a** zároveň je natolik složitý, že mu skill pomůže. Jednoduchá věc („přečti tenhle soubor“) skill nespustí, i když popis sedí.
- Claude má sklon skilly spíš **nepoužívat**. Proto má být popis konkrétní a trochu „dotěrný“: vyjmenuj situace, kdy se má skill použít, i když uživatel nevysloví přesné slovo.
- Čím víc skillů máš nainstalovaných, tím hůř si Claude vybírá. U desítek až stovek skillů může i dobře popsaný skill zůstat stranou – důležité skilly pak volej ručně (`/nazev`) a nepoužívané vypni.
- Skilly mezi sebou soupeří. Když máš dva podobné, popis musí říct, čím se liší a kdy který.

## 2. Recept na popis

Napiš ho ve **třetí osobě** a ve třech částech:

1. **Co dělá** – jedna věta se slovesem: „Vytvoří…“, „Zkontroluje…“, „Převede…“.
2. **Kdy ho použít** – „Použij, když uživatel chce…“ a vyjmenuj slova a situace, jak je lidé opravdu píšou. Klidně česky i anglicky, hovorově, s typickými názvy souborů nebo nástrojů.
3. **Kdy ne** (u skillů, které by se mohly plést) – „Nepoužívej na…“, „Není pro…“.

Popis neříká, **jak** skill funguje uvnitř. To patří do těla SKILL.md. Popis jen pomáhá vybrat.

## 3. Česká specifika

- Lidé píšou s diakritikou i bez ní a s překlepy: „udelej popisek“, „popis k videu“, „description“. Uveď hlavní varianty.
- Uveď česká i anglická klíčová slova, pokud se v oboru používá angličtina (commit, deploy, thumbnail, prompt).
- Skloňování: Claude rozumí tvarům slov, nemusíš vypisovat všechny pády. Stačí základní tvar a typická spojení.
- **Název** skillu je bez diakritiky (`popis-videa`), **popis** s diakritikou normálně.

## 4. Příklady: špatně → dobře

**Špatně:** `Pomáhá s videi.`
Proč: nic konkrétního, Claude neví kdy.

**Dobře:**
```yaml
description: Napíše popisek k YouTube videu – háček, shrnutí, kapitoly s časy a odkazy – z přepisu nebo scénáře. Použij, když uživatel chce popis videa, popisek, description, kapitoly, timestampy nebo text pod video, i když to napíše hovorově („hoď mi tam popisek“). Nepoužívej na titulek ani thumbnail.
```

**Špatně:** `I can help you clean your Downloads folder.`
Proč: první osoba, chybí kdy.

**Dobře:**
```yaml
description: Bezpečně roztřídí soubory v jedné složce (Stažené, Plocha…) – nejdřív inventura a návrh, přesun až po schválení, nic nemaže. Použij při „uklid mi stažené“, „udělej pořádek ve složce“, „roztřiď soubory“, „organize my downloads“. Ne pro mazání souborů ani úklid celého disku.
```

## 5. Limity délky

| Kde | Limit |
|---|---|
| Specifikace Agent Skills a Claude API | popis 1–1024 znaků, bez XML značek `< >` |
| Claude Code | popis + `when_to_use` dohromady se v seznamu ořízne na 1536 znaků |
| Claude.ai (nahrání ZIPu) | starší nápověda uvádí 200 znaků; když nahrání selže, popis zkrať |

Prakticky: drž se kolem **250–600 znaků**. Nejdůležitější slova dej na začátek, kdyby se konec ořízl.

V Claude Code můžeš část „kdy“ dát do pole `when_to_use` (přidá se k popisu). Pro přenositelnost
na claude.ai a jiné nástroje je ale bezpečnější mít vše v `description`.

## 6. Jak popis ladit

1. Napiš 8–10 vět, na které se skill **má** spustit (různé formulace, hovorové, s kontextem).
2. Napiš 8–10 vět, na které se **nemá** spustit – a ať jsou záludné: podobná témata, stejná slova, jiný cíl. „Napiš fibonacciho funkci“ jako negativní test pro skill na popisky nic netestuje.
3. Spusť `scripts/test_spousteni.py` (jen Claude Code). Uvidíš, kde skill mlčí a kde se plete.
4. Uprav popis: chybějící situace přidej, matoucí odliš větou „Nepoužívej na…“.
5. Opakuj, dokud neprojde většina. Nezkoušej trefit každý test za každou cenu – popis musí fungovat i na věty, které jsi nenapsal.
