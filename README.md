# Zmrzlina Na Samotách

> Otevřená knowledge base a receptury na točenou zmrzlinu.
> Web běží na [zmrzlina.nasamotach.cz](https://zmrzlina.nasamotach.cz).

Sourozenec hlavního webu [nasamotach.cz](https://nasamotach.cz) — všechno o jedné konkrétní věci, do které jsme se na ranči zamilovali: o zmrzlině.

## Proč to existuje

V češtině neexistuje použitelná, otevřená a do hloubky jdoucí knowledge base o točené zmrzlině. Posbíral jsem to z desítek zdrojů, knih, vlastních pokusů a omylů. Sdílím dál, ať to ostatní mají snadnější.

## Stack

- **[Astro 5](https://astro.build/)** s Content Collections (typed přes Zod)
- **[MDX](https://mdxjs.com/)** pro recepty + knowledge články
- **[Pagefind](https://pagefind.app/)** pro fulltextové hledání (build-time, klientský)
- **CSS** — vlastní brand styly (žádný framework)
- **Vercel** pro deploy přes GitHub Actions

## Lokální vývoj

```bash
npm install
npm run dev          # http://localhost:4321
npm run build        # produkce do dist/
npm run preview      # náhled buildu
```

Pro generování PDF receptů (volitelné, v CI běží zvlášť):

```bash
pip install playwright markdown-it-py
playwright install chromium
npm run pdfs         # vygeneruje public/pdfs/recept-NN-slug.pdf
```

## Struktura

```
src/
├── content/
│   ├── content.config.ts   # Zod schémata
│   ├── recepty/            # 1 markdown = 1 recept
│   ├── ingredience/        # databáze surovin
│   └── knowledge/          # teoretické články
├── layouts/
├── components/
├── pages/                  # routing
└── styles/

scripts/
├── migrate_from_nasamotach.py   # jednorázová migrace (hotovo)
├── seed_ingredience.py          # generátor stub ingrediencí
└── build_pdfs.py                # PDF export receptů (Playwright)

public/
├── favicon.svg
└── pdfs/                        # pre-built recepty A4 PDF

.github/workflows/
└── deploy.yml                   # build + deploy na Vercel
```

## Licence

- **Kód** — [MIT](LICENSE)
- **Obsah** (recepty, knowledge, ingredience) — [CC BY-SA 4.0](CONTENT-LICENSE.md)

Komerční použití je vítané. Stačí uvést zdroj a remixy zachovat pod stejnou licencí.

## Přispívání

Vítáme pull requesty s novými recepty, lepšími variantami, eshop linky k ingrediencím a opravami. Viz [CONTRIBUTING.md](CONTRIBUTING.md) nebo stránku [Přispět](https://zmrzlina.nasamotach.cz/prispivat/) na webu.

## Deploy

Web se automaticky deployuje na Vercel přes GitHub Action při pushi do `main`. Tajemství (`VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`) jsou v repo Settings → Secrets.
