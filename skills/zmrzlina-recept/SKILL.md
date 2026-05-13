---
name: zmrzlina-recept
description: Návrh nového receptu zmrzliny pro Ranč na Samotách — od hlavní příchuti a základních ingrediencí přes výpočet bilance (tuk, MSNF, cukry, PAC, sušina) až po vygenerovaný `.md` v `src/content/recepty/` a A4 PDF v `public/pdfs/`. Použij, když uživatel chce vytvořit novou točenou zmrzlinu, sorbet, nanuk nebo custard a zadá hlavní chuť + suroviny.
---

# Skill: Návrh a výpočet nového receptu zmrzliny

Tento skill provede agenta od **vstupu uživatele** (hlavní příchuť + ingredience, které chce použít) k **hotovému receptu**:
1. Markdown soubor v `src/content/recepty/`
2. A4 PDF v `public/pdfs/`

Recepty cílí na **provozní várku 10 kg** točené zmrzliny servírované při **−10 až −12 °C** (výjimka: nanuk, sorbet, kopečkový gelato — viz typové cíle PAC).

---

## Když tento skill použít

Spouštěč: uživatel zadá zhruba „udělej recept na **X** zmrzlinu s **Y, Z**" — např.:

- „Udělej recept na pistáciovou zmrzlinu, chci tam smetanu 33 % a pistáciovou pastu."
- „Navrhni mangový sorbet, do toho limetka."
- „Karamelovo-arašídový nanuk z mléka a kondenzovaného mléka."

Pokud uživatel **NEzadal hlavní příchuť** nebo **nezadal základní suroviny**, **zeptej se** (jedna sada otázek):

1. Hlavní příchuť (jedna dominantní).
2. Typ: točená smetanová / sorbet / nanuk / custard / Philadelphia bez vajec.
3. Suroviny, které chce použít (mléčný základ, cukry, ovoce, speciality).
4. Cílový tuk (pokud netriviální) — jinak default 8–10 % točená, 12 % custard, 0 % sorbet.

---

## Klíčová reference v repu

**VŽDY** si tyto soubory přečti před návrhem nového receptu:

| Co | Cesta | Proč |
|---|---|---|
| Konvence + MEC3 | `src/content/knowledge/konvence-receptu.md` | Várka, PAC cíle, dávkování |
| Teorie cukrů | `src/content/knowledge/cukry-ve-zmrzline.md` | FPDF, PAC, POD |
| Teorie tuků | `src/content/knowledge/tuky-ve-zmrzline.md` | Cíle tuku, MFGM |
| Stabilizátory | `src/content/knowledge/stabilizatory-ve-zmrzline.md` | Dávkování, kombinace |
| Sušina | `src/content/knowledge/sucha-latka-total-solids.md` | Cíle TS |
| Existující recepty | `src/content/recepty/*.md` | Vzory frontmatter, struktury |
| Karty surovin | `src/content/ingredience/*.md` | `pac`, `sucha_latka_pct`, slug pro odkaz |

---

## Pracovní postup

### Krok 1 — Načti vstupy

Z požadavku uživatele vytáhni:

- `flavor` — hlavní příchuť (slug, např. „pistacie")
- `typ` — `tocena` | `sorbet` | `nanuk` | `custard` | `philadelphia`
- `pozadovane_ingredience` — výpis surovin uživatele
- (volitelně) cílový tuk, cílový PAC, obtížnost

Pokud uživatel zmíní surovinu, která **ještě nemá kartu** v `src/content/ingredience/`, navrhni založení nové karty surovinou (viz Krok 5).

### Krok 2 — Vyber cílový profil

| Typ | Tuk | PAC | Sušina | Servírování | Pozn. |
|---|---|---|---|---|---|
| Točená smetanová | 8–10 % | 28–30 | 38–42 % | −10 až −12 °C | Default |
| Custard (French) | 11–13 % | 28 | 42–44 % | −10 až −12 °C | Žloutky 5–8 % |
| Tvarohová | 6–8 % | 28–30 | 40–44 % | −10 až −12 °C | Tvaroh 15–25 % |
| Sorbet (točený) | 0 % | 28–32 | 30–34 % | −10 až −12 °C | Ovoce 30–50 % |
| Nanuk | 4–8 % | 22–26 | 36–40 % | −18 °C výdej | Vyšší pevnost |
| Kopečkový gelato | 6–9 % | 24–28 | 38–42 % | −13 °C výdej | Tvrdší |

Zdroj cílů: `src/content/knowledge/konvence-receptu.md` + `cukry-ve-zmrzline.md` (sekce 4).

### Krok 3 — Spočítej bilanci

Na 10 kg várku (10 000 g). Pro každou ingredienci načti `sucha_latka_pct` a `pac` z její karty v `src/content/ingredience/`.

**Vzorce (vždy na 100 g směsi):**

```
TUK %       = Σ (g_ingredience × tuk_pct_ingredience) / 100
MSNF %      = Σ (mléčné_složky × msnf_pct) / 100         # mléko ~9 %, smetana 33 % má (67 % vody, MSNF ~6 %)
SUSINA %    = Σ (g_ingredience × sucha_latka_pct) / 100
PAC         = Σ (g_cukru × FPDF_cukru) / 100             # nezapomeň laktóza z mléka/SOM (FPDF 1,0)
POD         = Σ (g_cukru × POD_cukru) / 100              # sladivost, cíl ~16–22 pro smetanovou
```

**FPDF přehled** (z `cukry-ve-zmrzline.md`):

| Cukr | FPDF | POD |
|---|---|---|
| Sacharóza | 1,0 | 1,0 |
| Dextróza / glukóza prášek | 1,9 | 0,75 |
| Fruktóza | 1,9 | 1,7 |
| Invertní cukr | 1,9 | 1,3 |
| Glukózový sirup 42 DE / GL01934 | 0,8 | 0,5 |
| Maltodextrin 18 DE | 0,34 | 0,1 |
| Laktóza (z mléka, SOM) | 1,0 | 0,16 |

**Provozní defaulty:**

- Stabilizátor: **MEC3 Natura 50** (mléčné) nebo **MEC3 Natura frutta 50** (sorbet) — **50 g / 10 kg = 0,5 %**.
- SOM (sušené odtučněné mléko): 2–4 % pro doplnění MSNF.
- Špetka soli: **1 g / 10 kg** (ne 10 g — historická chyba).
- Žloutek: pasterovaný 1:1, 5–8 % pro custard.
- Voda: dopočet do 10 000 g. **Pokud lze, nahraď vodu mlékem** (lepší MSNF, krémovost).
- Pro čokoládu: **NEpoužívat jedlou sodu**.
- Pro nanuk: glukózový sirup v prášku **GL01934**, ne tekutý.

**Postup výpočtu:**

1. Nastav základní mléčnou matrici (mléko, smetana) podle cílového tuku.
2. Přidej hlavní příchuť v typickém dávkování (ovocné pyré 30–50 % pro sorbet, čokoládová hmota 5–8 %, ovocná pasta 10–15 %).
3. Doplň SOM tak, aby MSNF ≥ 8 % (smetanové) nebo dle typu.
4. Spočítej PAC ze známých cukrů + laktózy → uprav poměr sacharóza/dextróza/glukóza prášek tak, abys trefil cílový PAC.
5. Přidej 50 g MEC3, 1 g soli.
6. Dopočítej vodu (nebo přidej mléko) do 10 000 g.
7. Ověř sušinu, tuk, MSNF, PAC, POD proti tabulce cílů. Iteruj.

### Krok 4 — Sepiš recept podle vzoru

Soubor: `src/content/recepty/{slug}.md`. Slug = příchuť-typ, např. `mangovy-sorbet.md`, `pistaciova-zmrzlina.md`.

**Frontmatter** (povinný — schema viz `src/content.config.ts`):

```yaml
---
title: "Mangový sorbet"
cislo: 9                              # další volné číslo
typ: "sorbet"                         # tocena | sorbet | nanuk | premium | custard
obtiznost: "zacatecnik"               # zacatecnik | stredni | pokrocily
tuk_pct: 0
pac: 30
serv_teplota: "−10 až −12 °C"
varka_kg: 10
tags:
  - sorbet
  - ovocna
  - mango
ingredience:
  - mangove-pyre                      # slug existující karty
  - sacharoza
  - dextroza
  - glukoza-suseny-sirup
  - mec3-natura-frutta-50
  - citronova-stava
description: "Krátký popis (1 věta) ovocného sorbetu z čerstvého mangového pyré."
pdf: "/pdfs/recept-09-mangovy-sorbet.pdf"
---
```

**Tělo** — drž se struktury existujících receptů (vzor: `cokoladova-zmrzlina.md`, `french-custard-vanilka.md`):

1. Hlavička: `**Typ:** ... | **Servírování:** ...`
2. `**Cíl:** ...` — 1–2 věty o senzorickém záměru
3. Případná teoretická sekce (`### Specifika …`, `### Proč kombinace …`) — když je co vysvětlit
4. `### Receptura` — markdown tabulka **seskupená nadpisy řádků**:
   - `**TEKUTÉ**` (mléko, smetana, pyré, voda)
   - `**ROZPUSTIT VE SMETANĚ PŘI 50–60 °C**` (kakaová hmota, čokoláda)
   - `**SYPKÉ**` (cukry, SOM, stabilizátor, sůl)
   - `**DO INFUZE S MLÉKEM**` (lusk, koření)
   - `**PO PASTERACI**` (čerstvá kůra, extrakty, citronová šťáva, čerstvé ovoce)
   - Celkem `**10 000**` / `**100 %**`
   - Každá ingredience odkaz: `[Název](/ingredience/{slug}/)` — slug **musí existovat** v `src/content/ingredience/`
5. `### Bilance` — tabulka tuk/MSNF/cukry/sušina s výpočtem
6. PAC tabulka s rozpisem cukrů
7. `### Logika návrhu` — bullety, proč ty poměry
8. `### Postup` — číslovaný, kroky včetně pasterace (63 °C / 30 min LTLT, 75 °C / 25 s HTST, nebo 82 °C nappe pro custard), aging 4–12 h. **Postup KONČÍ agingem** — šlehání ve výrobníku a servírování nežpisuj, je to točená zmrzlina a uživatel ví jak nalít směs do stroje.
9. `### Bezpečnost` — pokud vejce nebo riziková surovina
10. `### Tipy a varianty` — 3–5 bulletů
11. `### Co se stane když...` — tabulka problém / příčina / řešení

**Jazyk:** česky, tykání, neformální. Žádné superlativy.

### Krok 5 — Doplň chybějící karty surovin

Pokud recept odkazuje na slug, který **neexistuje** v `src/content/ingredience/`, založ kartu podle šablony (vzor: `sacharoza.md`):

```yaml
---
title: "Mangové pyré"
kategorie: ovoce                       # cukr | tuk-mlecny | protein | stabilizator | emulgator | ovoce | kakao | aroma | sul-mineral | vlaknina | alkohol | baze-komercni | voda
forma: kapalna                         # kapalna | sypka | pasta | polotuhe (volitelné)
sucha_latka_pct: 16
pac: 18                                # ovocný cukr ~ FPDF 1,9 × cca 10 %
typicke_davkovani: "30–50 % m/m"
nazev_alt: []
tags: [ovoce, sorbet, mango]
knowledge_refs: [cukry-ve-zmrzline]
eshopy: []
description: "Stručný 1–2 věty popis."
---

Tělo karty: 1–2 odstavce + sekce **Specifikace**, **Kde koupit**, **Související knowledge**.
```

### Krok 6 — Vygeneruj PDF

```powershell
cd c:\git_my\zmrzlina_nasamotach
python scripts/build_pdfs.py --recipe {cislo}
```

Pro `--recipe` použij `cislo` z frontmatter. Bez parametru se přegenerují všechny.

**Důležité:**
- Skript NIKDY nevolá `Stop-Process` na chrome — pokud je PDF zamčené (otevřené v prohlížeči/Acrobatu), skript vypíše hlášku a uživatel ho má sám zavřít.
- Auto-fit: pokud obsah přetéká A4, font se zmenšuje z 9,5pt po 0,25pt až na 7,0pt. Když ani 7,0pt nestačí, zkrať text v receptu (typicky méně bulletů v sekci „Tipy" nebo „Co se stane když...").
- Po úspěšném vygenerování ověř, že `public/pdfs/recept-{NN}-{slug}.pdf` existuje.

Pokud uživatel chce i sloučený `recepty-vse.pdf`, spusť skript bez `--recipe`.

### Krok 7 — Spusť autolink

Po přidání receptu pusť ještě:

```powershell
python scripts/autolink_ingredience.py
```

Skript projde nové recepty a doplní odkazy na karty surovin, pokud něco chybí.

### Krok 8 — Reportuj výsledek

Krátké shrnutí uživateli:

- Cesta k MD: `src/content/recepty/{slug}.md`
- Cesta k PDF: `public/pdfs/recept-{NN}-{slug}.pdf`
- Klíčové bilance: tuk %, PAC, sušina
- Nově založené karty surovin (pokud nějaké)
- Co případně iterovat (typicky: ověřit chuť, doladit PAC po první várce)

---

## Sanity-checky před odevzdáním

- [ ] Součet ingrediencí = **přesně 10 000 g** a 100,00 %
- [ ] PAC v cílovém rozsahu (viz tabulka v Kroku 2)
- [ ] Tuk v cílovém rozsahu
- [ ] MSNF ≥ 8 % pro smetanové, ≥ 6 % pro custard (žloutek to dorovnává)
- [ ] Sušina v cílovém rozsahu (sorbet 30–34, smetanová 38–42, custard 42–44)
- [ ] Sůl **1 g**, ne víc
- [ ] Stabilizátor 50 g (0,5 %)
- [ ] Čerstvé ovoce/kůra/extrakty v sekci **PO PASTERACI**
- [ ] Všechny slug-y ingrediencí existují (nebo jsou založeny)
- [ ] Frontmatter validní YAML, schema dle `src/content.config.ts`
- [ ] `cislo` ve frontmatter je další volné (zkontroluj existující recepty)
- [ ] PDF se vygenerovalo bez overflow varování

---

## Pasterační postup (standard pro všechny recepty s ohřevem)

**Sypké NIKDY nepřidávat do studeného mixu před ohřevem** — cukry a SOM se rády připálí na dně hrnce. Standardní pořadí:

1. **Předmíchat sypké za sucha** (sacharóza + dextróza + glukóza prášek + SOM + MEC3 + případně sůl). Připravit stranou.
2. **Pasterovat jen tekuté složky** — mléko + smetana + případně pyré / pasty / invertní cukr. Zahřát za stálého míchání na cílovou teplotu (63 °C pro LTLT, 75–80 °C pro HTST, 82–84 °C pro custard „nappe").
3. **Při dosažení teploty vsypat sypké** a okamžitě **rozmixovat tyčovým mixérem** do hladka (1–2 min) bez hrudek.
4. **Držet pasterační teplotu po požadovanou dobu** (63 °C / 30 min, 75 °C / 25 s, atd.).
5. Rychlé zchlazení, aging. (Šlehání ve výrobníku již v postupu neuvádíme — všechno je to točená zmrzlina.)

**Výjimky:**
- **Custard / žloutky:** žloutky se temperují s mlékem v separátní fázi (viz `french-custard-vanilka.md`).
- **Tvaroh:** **vždy** až do vychlazené směsi (≤ 30 °C), nikdy před pasterací. Tvaroh je už pasterizovaný od výrobce, při ohřevu by koaguloval.
- **Čerstvé ovoce, kůra citrusů, extrakty, fleur de sel, citronová šťáva:** **vždy po pasteraci** (sekce `**PO PASTERACI**` v tabulce ingrediencí).

---

## Sorbety a sherbety — BEZ pasterace

**Sorbety** (bez mléčné složky) a **sherbety** (s tvarohem nebo lehkou mléčnou složkou) **se NEpasterují**. Chtěli bychom zachovat:

- **Vitamíny** (zvláště C-vitamín z ovoce a citronu) — nad 60 °C rychle degraduje.
- **Syrovou ovocnou chuť** — ohřevem se chuť posune do „kompotu“.
- **Živé antokyany** (červené/fialové ovoce) — ohřevem blednou.

**Hygiena je zajištěna:**
- Nízkým pH (~3,5–4) z citronu a kyselin v ovoci.
- Vysokou koncentrací cuků (snížená aktivita vody).
- Tvaroh je výrobcem pasterizovaný.
- Krátká shelf life ve vitríně (24–48 h).

**Postup sorbet/sherbet:**

1. Předmíchat sypké za sucha (cukry + MEC3 + sůl).
2. Rozmixovat ovoce na pyré.
3. Smíchat pyré + sypké → rozmixovat tyčovým mixérem 2–3 min.
4. (sherbet) Vmíchat prošlehaný tvaroh.
5. Citronka.
6. Aging 4–8 h při 4 °C.

**Tvaroh pro sherbet:** pokud je příliš tuhý (hodně odkapaný, „selský“), nahradit **část tvarohu vodou v poměru 1:1** (např. 500 g tvarohu → 250 g tvarohu + 250 g vody). Jinak by se ve studeném pyré špatně rozmíchal a vznikla by zrnitá textura.

**Sekce v tabulce ingrediencí:** použít `**MÍCHÁNÍ ZA STUDENA**` místo `**PO PASTERACI**`.

**Výjimka pro rizikové skupiny** (děti, senioři, těhotné): ovocné pyré lze krátce pasterovat 63 °C / 30 min před smícháním s tvarohem — ale ztratí se vitamíny a svěžest.

---

## Časté chyby (z předchozích iterací)

| Chyba | Náprava |
|---|---|
| Čokoláda nedrží tvar | Více smetany, méně vody (nebo žádná), `MEC3 Natura 50`, PAC ≤ 28 |
| Banán/ovoce moc sladké | Odebrat invertní cukr, držet PAC kolem 25 |
| Sůl 10 g | **Vždy 1 g** — historická chyba v původních receptech |
| Tekutý glukózový sirup | Pro nanuk používat **GL01934 prášek** |
| Voda místo mléka | Pokud lze, mléko → lepší MSNF a krémovost |
| Jedlá soda v čokoládě | **Nepoužívat** — narušuje texturu |
| Žloutky 200 g surové | Použít **pasterované žloutky 1:1**, dávkování 5–8 % pro custard |
| Stabilizátor 2 g + MEC3 | Buď jedno, nebo druhé — ne oba dohromady |
| Sypké do studeného mixu | **Pasterovat jen tekuté**, sypké vsypat až při dosažení teploty (riziko připálení) |
| Tvaroh pasterovat ve směsi | **Vždy do vychlazené směsi** (≤ 30 °C), kasein koaguluje |
| Pasterace sorbetu / sherbetu | **NEpasterovat** — zničí C-vitamín, vybledne barva, kompotová chuť |
| Tuhý „selský“ tvaroh v sherbetu | Část tvarohu nahradit vodou 1:1 — jinak se ve studeném pyré nerozmíchá |

---

## Licence vygenerovaných materiálů

Všechny recepty (.md i PDF) jsou pod **CC BY-SA 4.0** — info je už v patičce PDF a v `CONTENT-LICENSE.md`. Nemusíš nic přidávat.
