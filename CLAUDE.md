# zmrzlina_nasamotach — zmrzlina.nasamotach.cz

Astro 5 + MDX web s otevřenou knowledge base o točené zmrzlině. Veřejný repozitář, přijímá PR.

## Nový nebo upravený recept → jeď podle skillu

**[skills/zmrzlina-recept/SKILL.md](skills/zmrzlina-recept/SKILL.md)** je závazný devítikrokový
postup: cílové profily (tuk / PAC / sušina podle typu), vzorce bilance, FPDF a POD tabulka cukrů,
struktura MD, generování PDF, autolink, changelog a závěrečný sanity-check.

Nevymýšlej recept od oka — skill obsahuje i seznam chyb z reálných várek (sůl 1 g ne 10 g, sorbety
a sherbety se nepasterují, tvaroh až do vychlazené směsi ≤ 30 °C, žádná jedlá soda do čokolády,
sypké nikdy do studeného mixu).

## Příkazy

```powershell
npm install
npm run dev        # http://localhost:4321
npm run build      # astro build + pagefind index → dist/  (ověří i Zod schémata)
npm run pdfs       # python scripts/build_pdfs.py — všechna PDF
python scripts/build_pdfs.py --recipe <cislo>    # jen jeden recept
python scripts/autolink_ingredience.py           # doplní odkazy na karty surovin
```

`npm run build` je zároveň validace obsahu — pokud frontmatter nesedí se schématem, build spadne.

## Obsah

Tři kolekce, schémata v [src/content.config.ts](src/content.config.ts) — enumy jsou úzké, drž se jich:

| Kolekce | Kde | Klíčová pole |
|---|---|---|
| `recepty` | `src/content/recepty/` | `typ` (`tocena\|sorbet\|nanuk\|kopeckova\|premium`), `obtiznost`, `stav` (`navrh\|testovany\|odladeny`), `pac`, `tuk_pct`, `publikovat` |
| `ingredience` | `src/content/ingredience/` | `kategorie`, `sucha_latka_pct`, `pac`, `pod`, `eshopy` |
| `knowledge` | `src/content/knowledge/` | `sekce` (`slozky\|chemie\|procesy\|reference`), `poradi` |

- Nový recept má vždy `stav: navrh`, dokud ho někdo skutečně nevyrobí.
- `publikovat: false` nechá recept v gitu, ale vynechá ho z buildu.
- Odkaz na surovinu `[Název](/ingredience/{slug}/)` — slug **musí** existovat, jinak je odkaz mrtvý.

## Changelog je povinný

Při přidání i změně receptu přidej záznam **na začátek** [src/data/novinky.json](src/data/novinky.json)
(`datum`, `typ` = `nove`/`zmena`, `popis` jednou větou, volitelně `odkaz`). Zobrazuje se na úvodní
stránce a na `/novinky/`. Na tohle se nejčastěji zapomíná.

## Jazyk a licence

Česky, tykání, neformálně, žádné superlativy — viz `../nasamotach/.github/copilot-instructions.md`
a [CONTRIBUTING.md](CONTRIBUTING.md). Kód MIT, obsah CC BY-SA 4.0 (v patičce PDF už je, nic
nepřidávej).

## Deploy

GitHub Actions → Vercel, automaticky z `master`. Matematika se sází přes KaTeX
(`remark-math` + `rehype-katex`), fulltext staví Pagefind při buildu.
