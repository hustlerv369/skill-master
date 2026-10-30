# Testování skillu

Skill, který nikdo nevyzkoušel, je jen přání. Testují se dvě věci:

1. **Spouštění** – zapne se skill tehdy, kdy má (a jen tehdy)?
2. **Práce** – je výsledek se skillem lepší než bez něj?

## Obsah
1. Testovací zadání
2. Test práce (se skillem vs. bez)
3. Test spouštění
4. Jak hodnotit
5. Iterace
6. Testování v Claude.ai

## 1. Testovací zadání

Napiš 2–3 (u důležitých skillů 5+) **realistická** zadání – tak, jak by je uživatel opravdu napsal:

- konkrétní: název souboru, čísla, kontext („šéfová chce do tabulky sloupec s marží, tržby jsou ve sloupci C“),
- různě dlouhá, některá hovorově nebo s překlepem,
- aspoň jedno okrajové (chybějící vstup, divný formát, velký soubor).

Ulož je do `evals/zadani.json` vedle skillu (ne dovnitř skillu, ať se nebalí):
```json
[
  {"id": 1, "zadani": "…", "ocekavam": "co má výsledek splnit", "soubory": []}
]
```
Ukaž je uživateli a nech ho doplnit – on ví nejlíp, co bude skill dostávat.

## 2. Test práce (se skillem vs. bez)

**V Claude Code se subagenty** (nejlepší):
- Pro každé zadání spusť ve stejném kroku dva subagenty: jednoho **se skillem** (dej mu cestu ke skillu) a jednoho **bez** (u úpravy existujícího skillu: se starou verzí – předtím si ji zkopíruj).
- Výstupy ukládej do `<nazev>-workspace/kolo-1/<zadani>/se-skillem/` a `/bez-skillu/`.
- Subagent nezná tvoji konverzaci, takže test je poctivější než když skill zkoušíš sám.

**Bez subagentů:** otevři **novou relaci** (čistý kontext) a zadej úkol tam. V relaci, kde jsi skill psal, Claude ví víc, než skill obsahuje – test by lhal.

**Na více modelech:** co stačí Opusu, nemusí stačit Haiku. Když skill poběží na menších modelech, otestuj i je.

## 3. Test spouštění

```bash
python scripts/test_spousteni.py <složka-skillu> dotazy.json --opakovani 2 --model sonnet
```

- 8–10 vět, kde se má spustit, a 8–10 záludných, kde ne (viz `references/popis-a-spousteni.md`).
- Každá věta běží v čisté dočasné složce, kde je nainstalovaný jen testovaný skill (plus tvoje osobní skilly, jako v reálu). Opakování ukáže, jestli je výsledek stabilní.
- Čerpá to limit předplatného: 20 vět × 2 = 40 krátkých běhů. Na ladění stačí `--model haiku`, finální kontrolu udělej modelem, který používáš.

## 4. Jak hodnotit

- Kde jde výsledek ověřit objektivně (soubor existuje, čísla sedí, formát odpovídá, skript projde), napiš si **kontrolu jako skript** a pouštěj ji v každém kole.
- Styl, design, texty hodnotí člověk. Ukaž uživateli výstupy vedle sebe (se skillem / bez) a zeptej se, co je lepší a proč.
- Čti i **průběh**, nejen výsledek: když Claude se skillem bloudí, čte zbytečné soubory nebo pokaždé píše stejný pomocný kód, je to signál, co ve skillu opravit.
- Kontrola, která projde vždy (se skillem i bez), nic neměří – vyhoď ji.

## 5. Iterace

1. Zobecňuj. Neopravuj skill tak, aby prošel jen tvoje tři testy. Hledej příčinu a popiš ji obecně.
2. Škrtej. Co nepomáhá, zdržuje. Kratší skill = rychlejší a levnější běh.
3. Vysvětluj proč místo zákazů.
4. Opakovaná práce → skript do `scripts/`.
5. Nové kolo testů do `kolo-2/`, porovnej s předchozím.

Skonči, když je uživatel spokojený, nebo když další kola už nic nezlepšují.

## 6. Testování v Claude.ai (web, desktop)

Nejsou tam subagenti ani `claude -p`. Postup:
- Skill zabal (`scripts/zabal.py`), nahraj a zapni.
- Otevři novou konverzaci a zadej testovací zadání.
- Výsledek porovnej s konverzací, kde je skill vypnutý.
- Test spouštění dělej ručně: pár „má / nemá“ vět v nových konverzacích.
