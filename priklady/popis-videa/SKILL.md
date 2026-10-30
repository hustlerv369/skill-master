---
name: popis-videa
description: Napíše popisek k YouTube videu – háček, shrnutí, kapitoly s časy, odkazy a hashtagy – z přepisu, titulků (SRT/VTT) nebo scénáře. Použij, když uživatel chce popis videa, popisek, description, kapitoly, timestampy, časové značky nebo text pod video, i hovorově („hoď mi tam popisek“, „udělej kapitoly“). Nepoužívej na titulek videa, thumbnail ani scénář.
license: MIT
metadata:
  version: 1.0.0
  author: VojtaCode
---

# Popis videa

Dobrý popisek prodá video ve vyhledávání i pod přehrávačem: první dvě věty rozhodnou, jestli někdo klikne na „Zobrazit víc“, kapitoly pomůžou divákovi i Googlu.

## Postup

1. **Vstup.** Najdi přepis, titulky (SRT/VTT) nebo scénář. Když chybí, zeptej se. Bez časů v přepisu kapitoly **nevymýšlej** – nabídni je doplnit, až budou časy známé (vymyšlené časy diváka pošlou na špatné místo).
2. **Pochop video.** Hlavní slib (co se divák naučí), 3–5 klíčových momentů, zmíněné nástroje a odkazy.
3. **Napiš popisek** podle šablony níže. Tón převezmi z přepisu (tykání/vykání, slang). Žádné „V tomto videu se podíváme…“ – začni rovnou přínosem.
4. **Kapitoly:** první musí být `00:00`, každá aspoň 10 s dlouhá, aspoň tři kapitoly (jinak je YouTube nezobrazí). Názvy 2–5 slov, co se v té části stane.
5. **Ověř:** časy jsou vzestupně a odpovídají přepisu, odkazy jsou jen ty, které zazněly nebo které dodal uživatel, nic není vymyšlené.

## Šablona

```
<Háček: 1–2 věty, co divák získá – hlavní klíčové slovo co nejdřív.>

<Shrnutí: 2–4 věty, pro koho to je a co přesně uvidí.>

⏱️ Kapitoly
00:00 <Úvod>
01:23 <…>

🔗 Odkazy
<nástroj>: <odkaz>

#<tag1> #<tag2> #<tag3>
```

## Příklad

Vstup: přepis 12minutového videa o tom, jak si v Claude Code udělat vlastní skill, časy v SRT.
Výstup začíná: „Naučím tě udělat si vlastní skill pro Claude za 10 minut – a to i když neprogramuješ.“ Následuje shrnutí, 6 kapitol od `00:00 Co je skill` po `10:41 Sdílení na GitHubu`, odkazy z videa a tři hashtagy.
