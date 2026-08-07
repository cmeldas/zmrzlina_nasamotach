---
title: "Smetana"
kategorie: tuk-mlecny
forma: kapalna
sucha_latka_pct: 39.0
pac: 0
typicke_davkovani: "10–30 % m/m"
nazev_alt:
  - "smetana ke šlehání"
  - "smetana 33 %"
  - "smetana 35 %"
  - "heavy cream"
  - "whipping cream"
tags:
  - smetana
  - tuk
  - mlecny-tuk
knowledge_refs:
  - tuky-ve-zmrzline
eshopy:
  - nazev: "Almeco"
    url: "https://www.almeco.cz/"
    poznamka: "Gastro smetana ke šlehání 33 % i 35 % tuku, bez rostlinných ztužovačů. Alternativně běžná smetana ke šlehání ze supermarketu — vždy zkontrolovat, že je z pravého mléčného tuku."
description: "Hlavní zdroj mléčného tuku. Jedna karta pro všechny tučnosti (30–40 %) — v tabulce najdeš sušinu, MSNF a laktózu pro každou z nich."
---

Hlavní zdroj mléčného tuku ve smetanových zmrzlinách. **Nepoužívat smetanu s rostlinnými ztužovači** — pravá smetana z živočišného tuku tvoří při šlehání částečnou koalescenci tukových globulí, a právě to ve zmrzlině drží strukturu a dělá suchou texturu, která na kornoutu nesteče.

V maloobchodu i v gastro se u nás potkáš hlavně s **33 %** a **35 %**. Recepty v tomto repu píšou v tabulce ingrediencí konkrétní tučnost, kterou byly počítané (např. „Smetana 33 %"), ale odkazují sem — tučnost si přepočítej podle toho, co máš zrovna ve chladu.

## Specifikace podle tučnosti

Smetana je emulze mléčného tuku ve zbytku, který se chová jako odtučněné mléko (~9 % sušiny). Z toho se dá všechno dopočítat:

| Tuk  | MSNF   | Sušina celkem | Laktóza |
| ---- | ------ | ------------- | ------- |
| 30 % | 6,30 % | 36,3 %        | 3,40 %  |
| 33 % | 6,03 % | **39,0 %**    | 3,26 %  |
| 35 % | 5,85 % | 40,9 %        | 3,16 %  |
| 38 % | 5,58 % | 43,6 %        | 3,01 %  |
| 40 % | 5,40 % | 45,4 %        | 2,92 %  |

Hodnota `sucha_latka_pct` ve frontmatteru je **39,0 (pro 33 %)** — nejčastější tučnost v receptech. Pro jinou tučnost použij tabulku.

**Vzorce, kdyby ti tučnost v tabulce chyběla** (F = % tuku):

```
MSNF   = (100 − F) × 0,09
Sušina = F + MSNF
Laktóza = MSNF × 0,54
```

- **PAC 0** — smetana sama nesladí; laktóza, kterou nese, se do PAC počítá zvlášť v součtu laktózy (FPDF 1,0) společně s mlékem a SOM.
- **Typické dávkování:** 10–30 % m/m

## Přepočet receptu na jinou tučnost

Na stejný cílový tuk vynásob množství smetany poměrem tučností a rozdíl doplň mlékem:

```
nová_smetana = původní_smetana × (původní_tuk % / nová_tuk %)
```

Například 1 500 g smetany 33 % → `1500 × 33/35 = 1 420 g` smetany 35 %, a uvolněných 80 g dej do [mléka](/ingredience/plnotucne-mleko/).

Tučnější smetana je pro recept mírně výhodnější: na stejný tuk jí potřebuješ méně a uvolněnou hmotnost můžeš dát do mléka, které nese na svou hmotnost víc mléčné sušiny než smetana. MSNF tím trochu vzroste a zmrzlina je krémovější. Rozdíl mezi 33 a 35 % je malý, ale u receptů s tučnou oříškovou pastou — kde je na mléčný tuk málo místa — se to hodí (viz [pistáciová zmrzlina](/recepty/pistaciova-zmrzlina/)).

## Související knowledge

- [tuky-ve-zmrzline](/knowledge/tuky-ve-zmrzline/)
