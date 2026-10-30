# Skill Master 🛠️

**Česky provede tvorbou skillů pro Claude – od nápadu po otestovaný skill, který můžeš sdílet.**

Skill je složka s návodem (`SKILL.md`), kterou si Claude načte, když ji potřebuje. Naučíš ho tím svůj postup jednou a používá ho pořád. Skill Master je skill na tvorbu skillů: zeptá se tě na pár věcí, napíše popis, podle kterého se skill bude spolehlivě spouštět, a celý skill zkontroluje, otestuje, zabalí a nainstaluje.

Funguje v **Claude Code**, v **Claude.ai / desktopové aplikaci** a skilly z něj běží i v **OpenAI Codex** (stejný otevřený formát Agent Skills).

Od [VojtaCode](https://www.youtube.com/@VojtaCode) pro českou komunitu. Zdarma, open source.

---

## Co umí

- **Vytvoří skill z nápadu** – nebo z práce, kterou jsi s Claudem právě udělal („tohle si ulož jako skill“).
- **Napíše popis, který se spouští.** Popis rozhoduje, jestli Claude skill vůbec použije. Skill Master ho staví podle toho, jak lidé opravdu píšou – česky, anglicky, hovorově, bez diakritiky.
- **Zkontroluje skill** (`validuj.py`) – název, popis, délku, odkazy na soubory, kódování, zapomenuté klíče a hesla, osobní cesty, zbytky šablony, pasti na Windows.
- **Otestuje spouštění** (`test_spousteni.py`) – pustí tvoje věty v čistém Claude Code a ukáže, kde se skill zapnul a kde ne.
- **Otestuje práci** – se skillem vs. bez skillu, ať víš, že opravdu pomáhá.
- **Zabalí a nainstaluje** – ZIP pro Claude.ai, instalace do Claude Code i Codexu se zálohou předchozí verze.
- **Ohlídá bezpečnost** – klíče jen z proměnných prostředí, nevratné akce jen po tvém „ano“, obsah webu jako data, ne pokyny.

## Instalace

### Claude Code – jako plugin (doporučeno)

V Claude Code napiš:
```
/plugin marketplace add hustlerv369/skill-master
/plugin install skill-master@skill-master
```

### Claude Code – ručně

```bash
git clone https://github.com/hustlerv369/skill-master.git
cd skill-master
python skills/skill-master/scripts/nainstaluj.py skills/skill-master
```
Skill se zkopíruje do `~/.claude/skills/skill-master`. Přidej `--codex` a nainstaluje se i pro OpenAI Codex (`~/.agents/skills`).

### Claude.ai a desktopová aplikace

1. Stáhni `skill-master.zip` z [Releases](https://github.com/hustlerv369/skill-master/releases) (nebo si ho vyrob: `python skills/skill-master/scripts/zabal.py skills/skill-master`).
2. V Claude: **Customize → Skills → „+“ → Upload a skill**, vyber ZIP a zapni ho.
3. Musí být zapnuté spouštění kódu („Code execution“ / „Create and edit files“ v nastavení).

### Nejjednodušší: řekni to Claudovi

Vlož do Claude Code:
> Nainstaluj mi skill Skill Master z https://github.com/hustlerv369/skill-master. Nejdřív si přečti README a celý skill, ať víš, co instaluješ, a pak ho nainstaluj podle návodu.

## Jak ho používat

Stačí normálně napsat, co chceš:

- „Chci si udělat skill, který mi z přepisu porady udělá zápis s úkoly.“
- „Tohle, co jsme teď dělali, si ulož jako skill.“
- „Můj skill na faktury se nikdy nespustí, proč?“
- „Zkontroluj mi tenhle SKILL.md.“
- „Zabal mi skill do ZIPu pro kamaráda.“
- „Chci svoje skilly sdílet na GitHubu jako plugin.“

Nebo ho zavolej přímo: `/skill-master` (při instalaci jako plugin `/skill-master:skill-master`).

> **Máš hodně skillů?** Když jich máš desítky až stovky, Claude si podle popisu vybírá hůř. V našem testu se v prostředí s 300+ skilly Skill Master sám nespustil. Ruční zavolání přes `/` fungovalo vždycky. Nepoužívané skilly si vypni.

Postup, kterým tě provede:

1. **Záměr** – co má skill dělat, kdy se spustit, kdy ne, rizika.
2. **Návrh** – název, struktura, kde poběží.
3. **Popis** – aby se skill spouštěl, kdy má.
4. **Obsah** – návod, skripty, šablony, bezpečnost.
5. **Kontrola** – validátor.
6. **Test** – spouštění a práce se skillem vs. bez.
7. **Vylepšení** – podle výsledků testů.
8. **Instalace a sdílení.**

## Co je uvnitř

```
skills/skill-master/
├── SKILL.md                      hlavní návod (8 kroků)
├── references/
│   ├── popis-a-spousteni.md      jak napsat popis, který se spouští
│   ├── stavba-skillu.md          všechna pole frontmatteru, struktura, vzory
│   ├── testovani.md              test spouštění i práce
│   ├── bezpecnost.md             klíče, nevratné akce, cizí obsah
│   ├── instalace-a-sdileni.md    Claude Code, Claude.ai, Codex, GitHub
│   └── caste-chyby.md            chyby z praxe a jejich opravy
├── scripts/
│   ├── novy_skill.py             kostra nového skillu
│   ├── validuj.py                kontrola skillu
│   ├── test_spousteni.py         test spouštění (Claude Code)
│   ├── zabal.py                  ZIP pro Claude.ai
│   └── nainstaluj.py             instalace se zálohou
└── assets/SKILL-sablona.md       šablona
priklady/                         dva hotové ukázkové skilly
testy/                            testovací věty pro test spouštění
```

Skripty potřebují jen **Python 3.8+** (standardní knihovnu, nic dalšího neinstaluješ). Test spouštění navíc potřebuje přihlášený **Claude Code**.

## Ukázkové skilly

- [`priklady/popis-videa`](priklady/popis-videa/SKILL.md) – popisek k YouTube videu s kapitolami z přepisu. Ukázka znalostního skillu se šablonou výstupu.
- [`priklady/uklid-slozky`](priklady/uklid-slozky/SKILL.md) – bezpečný úklid složky: inventura → schválení → přesun → možnost vrátit zpět. Ukázka skillu se skripty a bezpečným postupem u věcí, které mění soubory.

## Ověřeno

Při vydání verze 1.0.0 (30. 10. 2026) jsme udělali tyto testy:

- **Test spouštění:** 16 vět (8 má spustit, 8 záludných nemá) na modelu Sonnet v Claude Code 2.1, každá věta 2× → **32/32 běhů správně** (v čisté dočasné složce bez uživatelského nastavení, pluginů a MCP). Věty jsou v [`testy/dotazy-skill-master.json`](testy/dotazy-skill-master.json).
- **Test práce:** Claude se Skill Masterem v čisté složce bez dalšího kontextu postavil skill „zápis z porady“, který prošel validátorem. Tento test odhalil, že validátor pouštěl nevyplněnou šablonu, a opravili jsme to.
- **Plné prostředí s 300+ skilly:** sám se nespustil (0 ze 3 vět). Ruční `/skill-master:skill-master` fungoval a Claude postupoval přesně podle skillu.
- `validuj.py --prisne` projde na Skill Masteru i obou ukázkách. Plugin prošel `claude plugin validate`.

Na Macu a Linuxu skripty běží na standardním Pythonu, ale otestované jsou na Windows 11.

## Bezpečnost

Skilly od cizích lidí (i tenhle) si před instalací **přečti**, včetně skriptů. Skill Master nic neposílá na internet a nic nemaže. `test_spousteni.py` spouští Claude Code na tvém předplatném (čerpá limit) v dočasné složce a nemá povolené úpravy souborů ani příkazy.

## Komunita

- YouTube: [@VojtaCode](https://www.youtube.com/@VojtaCode)
- Skool komunita: [VojtaCode AI komunita](https://www.skool.com/vojtacode-ai-komunita-6194/about)

Našel jsi chybu nebo máš nápad? Založ [issue](https://github.com/hustlerv369/skill-master/issues) nebo pošli pull request.

## Licence

[MIT](LICENSE). Inspirováno oficiálním skillem [skill-creator](https://github.com/anthropics/skills) od Anthropicu (Apache 2.0). Text i kód Skill Masteru jsou napsané znovu česky a s vlastními nástroji. „Claude“ je ochranná známka společnosti Anthropic; tento projekt s ní není oficiálně spojený.
