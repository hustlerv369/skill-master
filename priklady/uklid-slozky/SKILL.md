---
name: uklid-slozky
description: Bezpečně roztřídí soubory v jedné složce (Stažené, Plocha, Dokumenty…) do podsložek podle typu – nejdřív inventura a návrh, přesun až po schválení, s možností vrátit zpět, nic nemaže. Použij při „uklid mi stažené“, „udělej pořádek ve složce“, „roztřiď soubory“, „organize my downloads“. Nepoužívej na mazání souborů, úklid celého disku ani systémových složek.
license: MIT
metadata:
  version: 1.0.0
  author: VojtaCode
---

# Úklid složky

Uživatel chce pořádek, ale nesmí o nic přijít. Proto: **inventura → návrh → schválení → přesun → kontrola**. Nic se nemaže a každý přesun jde vrátit.

## Postup

1. **Která složka.** Jen ta, kterou uživatel jmenoval. Systémové složky (`C:\Windows`, `Program Files`, `~/Library`…) a celý disk odmítni – je tam riziko rozbití aplikací.
2. **Inventura:**
   ```bash
   python scripts/inventura.py "<složka>" > plan.json
   ```
   Skript nic nemění. Vypíše návrh: který soubor kam (Obrázky, Dokumenty, Videa, Hudba, Archivy, Instalátory, Ostatní). Podsložky ani skryté soubory nepřesouvá.
3. **Ukaž návrh** uživateli: kolik souborů jde kam, pár příkladů a co zůstane. Zeptej se, jestli chce něco změnit (např. vlastní složku „Faktury“). Uprav `plan.json` podle něj.
4. **Přesun jen po výslovném „ano“:**
   ```bash
   python scripts/presun.py plan.json
   ```
   Když cílový soubor už existuje, skript nový přejmenuje (`soubor (2).pdf`), nikdy nepřepisuje. Zapíše `presun-log.json`.
5. **Kontrola:** porovnej počet souborů před a po (skript ho vypíše). Řekni uživateli, kde je log a jak úklid vrátit:
   ```bash
   python scripts/presun.py --zpet presun-log.json
   ```

## Hranice

- Mazání nedělej ani na požádání v rámci tohoto skillu – doporuč koš a nech to na uživateli.
- Otevřené soubory (Windows je zamkne) skript přeskočí a nahlásí. Netlač.
