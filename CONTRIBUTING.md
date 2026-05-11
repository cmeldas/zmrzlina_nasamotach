# Jak přispět

Děkujeme, že chceš pomoct! Tenhle projekt žije z toho, že se ostatní podělí o své zkušenosti.

Plná příručka je na webu: <https://zmrzlina.nasamotach.cz/prispivat/>.

## TL;DR

1. Forkni si repo, naklonuj lokálně, `npm install`.
2. Pro **nový recept** vytvoř `src/content/recepty/tvuj-recept.md`. Inspirace v `smetanovy-zaklad.md`.
3. Pro **eshop link** edituj odpovídající `src/content/ingredience/*.md` (frontmatter `eshopy:`).
4. Pro **knowledge článek** vytvoř `src/content/knowledge/*.md` se sekcí `slozky | chemie | procesy | reference`.
5. `npm run dev` — zkontroluj že to vypadá dobře.
6. `npm run build` — ověř, že schema validace projde.
7. Otevři PR.

## Co posíláme zpátky

Otevřením PR souhlasíš, že tvůj příspěvek bude uvolněn pod licencí
**CC BY-SA 4.0** (obsah) nebo **MIT** (kód). Tvoje autorství zůstává a
bude uvedeno v `autor:` frontmatter daného souboru.

## Pravidla pro recepty

- **Provozní velikost** 10 kg várka.
- **Bilance je nutná** — uveď tuk %, MSNF %, cukry %, PAC.
- **Vysvětli "proč"** — proč tento poměr cukrů, proč tato teplota, proč tento postup.
- **Reference** k použité literatuře, pokud čerpáš.
- **Bezpečnost** — u syrových složek (vejce) uveď pasterizační režim.

## Co nepřijímáme

- Receptury chráněné NDA / komerčním tajemstvím výrobců směsí.
- Marketingové texty bez technické hodnoty.
- Opisy z knih bez přepracování (autorská práva).

## Code of Conduct

Buďme k sobě slušní. Diskutujeme o zmrzlině, ne o lidech.
