"""Vygeneruje stub markdown soubory pro databázi ingrediencí.

Každá ingredience má frontmatter (kategorie, dávkování, knowledge_refs, eshopy)
a krátký popis. Eshop linky jsou ponechané jako TODO a každý přispěvatel je
může doplnit přes PR.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DST = ROOT / "src" / "content" / "ingredience"


# (slug, title, kategorie, sucha_latka_pct, pac, davkovani, alt_nazvy, knowledge_refs, tags, popis)
INGREDIENCE: list[tuple] = [
    (
        "sacharoza",
        "Sacharóza (řepný cukr)",
        "cukr",
        99.9,
        1.0,
        "10–15 % m/m",
        ["cukr krystal", "řepný cukr", "sucrose"],
        ["cukry-ve-zmrzline"],
        ["cukr", "disacharid", "sladidlo"],
        "Disacharid glukózy a fruktózy. Základní sladidlo všech receptů. FPDF = 1,0 — drží PAC v rozumných mezích, takže lze dávkovat ve větších množstvích bez rizika příliš měkké zmrzliny.",
    ),
    (
        "dextroza",
        "Dextróza (glukóza monohydrát)",
        "cukr",
        91.0,
        1.9,
        "2–7 % m/m",
        ["glukóza monohydrát", "hroznový cukr"],
        ["cukry-ve-zmrzline"],
        ["cukr", "monosacharid", "sladidlo", "anti-krystalizace"],
        "Monosacharid s vysokým FPDF (1,9). Snižuje teplotu mrznutí dvojnásobně oproti sacharóze, dělá zmrzlinu měkčí a krémovější. Méně sladká než sacharóza (~70 %).",
    ),
    (
        "glukoza-suseny-sirup",
        "Glukóza – sušený sirup GL01934 (~38 DE)",
        "cukr",
        96.0,
        0.8,
        "2–7 % m/m",
        ["sušený glukózový sirup", "DE 38", "spray-dried glucose syrup"],
        ["cukry-ve-zmrzline"],
        ["cukr", "sirup", "anti-rekrystalizace", "sypka-forma"],
        "Sušená forma standardního glukózového sirupu (~38 DE). Skvělý pro brzdění rekrystalizace při skladování (zejména nanuky). Mírně sladký, dodává sušinu bez přesladění. **Skladujeme tuto formu místo tekutého sirupu.**",
    ),
    (
        "fruktoza",
        "Fruktóza (ovocný cukr)",
        "cukr",
        99.0,
        1.9,
        "0,5–3 % m/m",
        ["ovocný cukr", "fruit sugar"],
        ["cukry-ve-zmrzline", "chutove-slozky"],
        ["cukr", "monosacharid", "ovoce", "sladidlo"],
        "Nejsladší běžný cukr (~140 % sladkosti sacharózy). Rychlý profil sladkosti — zvýrazní ovocné chutě (jahody, broskve) a rychle odezní. Vysoký FPDF, používat střídmě.",
    ),
    (
        "invertni-cukr",
        "Invertní cukr",
        "cukr",
        75.0,
        1.9,
        "0,5–2 % m/m",
        ["invertovaný sirup", "trimoline", "invert syrup"],
        ["cukry-ve-zmrzline"],
        ["cukr", "sirup", "hygroskopicky", "anti-krystalizace"],
        "Směs glukózy a fruktózy z hydrolýzy sacharózy. Hygroskopický — drží vlhkost, brání oddělování vody na povrchu nanuků (ice burn). Mírně zvyšuje PAC.",
    ),
    (
        "som",
        "Sušené odtučněné mléko (SOM / SMP)",
        "protein",
        96.0,
        None,
        "2–6 % m/m",
        ["SMP", "skim milk powder", "sušené odstředěné mléko"],
        ["proteiny-ve-zmrzline", "sucha-latka-total-solids"],
        ["protein", "msnf", "mleko", "sucha-latka"],
        "Hlavní zdroj MSNF (mléčné sušiny bez tuku). Dodává proteinovou strukturu, váže vodu a podporuje šlehání pěny. Obsahuje ~50 % laktózy — pozor na pískovitost při >12 % MSNF.",
    ),
    (
        "plnotucne-mleko",
        "Plnotučné mléko 3,5 %",
        "tuk-mlecny",
        12.5,
        None,
        "30–55 % m/m",
        ["plnotučné kravské mléko", "whole milk"],
        ["tuky-ve-zmrzline", "proteiny-ve-zmrzline"],
        ["mleko", "tuk", "voda", "kasein"],
        "Základní tekutý nosič. ~3,5 % tuku, ~3,3 % proteinu, ~4,7 % laktózy, zbytek voda. Vlastní mléko z farmy je nejlepší — čerstvé, plné aroma.",
    ),
    (
        "smetana-33",
        "Smetana 33 % tuku",
        "tuk-mlecny",
        38.0,
        None,
        "10–30 % m/m",
        ["smetana ke šlehání", "heavy cream"],
        ["tuky-ve-zmrzline"],
        ["smetana", "tuk", "mlecny-tuk"],
        "Hlavní zdroj mléčného tuku. Nepoužívat smetanu s rostlinnými ztužovači — pravá smetana z živočišného tuku tvoří částečnou koalescenci globulí, která drží strukturu zmrzliny.",
    ),
    (
        "vajecny-zloutek",
        "Pasterovaný vaječný žloutek",
        "emulgator",
        50.0,
        None,
        "2,5–8 % m/m",
        ["pasterovaný žloutek", "egg yolk", "yolk"],
        ["emulgatory-ve-zmrzline", "tuky-ve-zmrzline"],
        ["vejce", "lecitin", "emulgator", "custard"],
        "Přírodní emulgátor díky lecitinu. Dodává krémovost, hloubku chuti a stabilitu pěny. **Pro provoz používáme pasterovaný žloutek 1:1** (Ovostar, Bohušovice). Sušené žloutky NE.",
    ),
    (
        "tvaroh",
        "Tvaroh polotučný (4 %)",
        "protein",
        25.0,
        None,
        "20–25 % m/m (tvarohové recepty)",
        ["tvaroh polotučný", "kvark"],
        ["proteiny-ve-zmrzline"],
        ["tvaroh", "kasein", "mlecny-vyrobek"],
        "Bohatý zdroj kaseinu — extra krémovost a stabilita. Pozor: kasein koaguluje při >80 °C, pasterizovat max. 78 °C. Vždy rozmixovat tyčovým mixérem do hladka.",
    ),
    (
        "jahodove-pyre",
        "Jahodové pyré",
        "ovoce",
        10.0,
        None,
        "30–50 % m/m (sorbety, ovocné)",
        ["jahody mražené", "jahodový mus", "strawberry purée"],
        ["chutove-slozky"],
        ["ovoce", "jahody", "pyre", "letni"],
        "Čerstvé nebo mražené jahody rozmixované do hladka, případně přepasírované přes síto. Obsahují ~7 % vlastních cukrů (mix sacharóza/glukóza/fruktóza), počítat do bilance.",
    ),
    (
        "banan",
        "Banán (zralý)",
        "ovoce",
        25.0,
        None,
        "25–35 % m/m",
        ["banánové pyré", "banana purée"],
        ["chutove-slozky"],
        ["ovoce", "banan"],
        'Velmi zralé banány („tygří“ se skvrnami) — nezralé jsou škrobnaté, přezralé příliš měkké. Obsahují polyfenoloxidázu — zpracovávat ihned s citronovou šťávou proti zhnědnutí.',
    ),
    (
        "citronova-stava",
        "Citronová šťáva (čerstvá)",
        "ovoce",
        9.0,
        None,
        "0,5–8 % m/m",
        ["citrón", "lemon juice"],
        ["chutove-slozky", "kyseliny-a-ph"],
        ["citrus", "kyselina", "antioxidant"],
        "Kyselina citronová (~5 %) + vitamin C. Vyvažuje sladkost, zvýrazňuje ovocné chutě, brání oxidaci (banány, jablka). Pozor na pH u mléčných základů.",
    ),
    (
        "vanilkovy-lusk",
        "Vanilkový lusk (Bourbon)",
        "aroma",
        85.0,
        None,
        "0,3–0,6 % m/m (~1–1,5 ks/litr)",
        ["vanilla bean", "vanilka madagaskarská"],
        ["chutove-slozky"],
        ["vanilka", "aroma", "premium"],
        "Pro autentickou vanilkovou chuť používat lusk, ne extrakt. Lusk podélně rozříznout, vyškrábnout semínka, oboje vyluhovat v horkém mléce 30 min.",
    ),
    (
        "raw-kakao",
        "Přírodní raw kakao (~11 % tuku)",
        "kakao",
        97.0,
        None,
        "3–4 % m/m",
        ["natural cocoa powder", "raw cocoa", "nealkalizované kakao"],
        ["chutove-slozky"],
        ["kakao", "cokolada", "raw"],
        "Nealkalizovaný (přírodní) kakaový prášek z nepražených bobů. pH 5,0–5,8 — kyselejší, ovocnější, světlejší barva výsledku. Vyžaduje delší aging (24 h) pro hloubku chuti.",
    ),
    (
        "kakaova-hmota",
        "Kakaová hmota (cocoa liquor)",
        "kakao",
        99.0,
        None,
        "5–10 % m/m",
        ["cocoa mass", "cocoa liquor", "kakaová pasta 100%"],
        ["chutove-slozky", "tuky-ve-zmrzline"],
        ["kakao", "cokolada", "kakaove-maslo"],
        "Čistá pasta z mletých kakaových bobů, ~55 % kakaového másla. Doplňuje raw kakao o krémovost, máslové aroma a hloubku. Rozpouštět v mléce/smetaně při 50–60 °C.",
    ),
    (
        "mec3-natura-50",
        "MEC3 Natura 50 (báze pro mléčné zmrzliny)",
        "baze-komercni",
        95.0,
        None,
        "0,5 % m/m (50 g/10 kg)",
        ["MEC3", "Natura 50", "komerční báze mléčná"],
        ["stabilizatory-ve-zmrzline", "proteiny-ve-zmrzline"],
        ["baze", "stabilizator", "komercni", "mec3"],
        "Hotová báze pro mléčné zmrzliny. Obsahuje SOM, mléčné bílkoviny, vlákna, gumu tara, gumu guar a dřeň baobabu. Nahrazuje samostatný stabilizátor a část SOM.",
    ),
    (
        "mec3-natura-frutta-50",
        "MEC3 Natura frutta 50 (báze pro sorbety)",
        "baze-komercni",
        95.0,
        None,
        "0,5 % m/m (50 g/10 kg)",
        ["MEC3", "Natura frutta 50", "báze sorbet"],
        ["stabilizatory-ve-zmrzline"],
        ["baze", "stabilizator", "komercni", "mec3", "sorbet"],
        "Hotová báze pro sorbety. Obsahuje rostlinná vlákna, glukózový sirup, maltodextrin, gumu tara, gumu guar a dřeň baobabu. Bez mléčné složky.",
    ),
    (
        "stabilizator-guar-lbg",
        "Stabilizátor guar + LBG",
        "stabilizator",
        92.0,
        None,
        "0,15–0,3 % m/m",
        ["guarová guma", "lokustová guma", "carob bean gum", "LBG"],
        ["stabilizatory-ve-zmrzline"],
        ["stabilizator", "hydrokoloid", "anti-krystalizace"],
        "Synergická směs guar + LBG (1:1) je klasická volba — guar pracuje za studena, LBG při vyšších teplotách. Aktivace při pasterizaci >65 °C.",
    ),
    (
        "pektin",
        "Pektin NH (jablečný)",
        "stabilizator",
        90.0,
        None,
        "0,05–0,15 % m/m",
        ["pectin NH", "jablečný pektin"],
        ["stabilizatory-ve-zmrzline"],
        ["stabilizator", "ovoce", "sorbet", "nanuk"],
        "Vhodný pro sorbety a nanuky s vysokým podílem ovoce. Zlepšuje držení tvaru, omezuje ledové krystaly. Aktivuje se zahřátím se sacharózou nad 65 °C.",
    ),
    (
        "voda",
        "Voda",
        "voda",
        0.0,
        None,
        "doplnění do 100 %",
        ["pitná voda", "filtered water"],
        ["voda-a-led"],
        ["voda", "rozpoustedlo"],
        "Pitná voda dobré kvality (filtrovaná, bez chloru). Tvoří ~60–75 % směsi. Její vázání na ostatní složky určuje texturu — viz článek o vodě a ledu.",
    ),
]


def write_ingredience(slug: str, title: str, kat: str, sucha: float | None, pac: float | None,
                       davk: str, alt: list[str], krefs: list[str], tags: list[str], popis: str) -> None:
    fm_lines = ["---", f'title: "{title}"', f"kategorie: {kat}"]
    if sucha is not None:
        fm_lines.append(f"sucha_latka_pct: {sucha}")
    if pac is not None:
        fm_lines.append(f"pac: {pac}")
    if davk:
        fm_lines.append(f'typicke_davkovani: "{davk}"')
    if alt:
        fm_lines.append("nazev_alt:")
        for a in alt:
            fm_lines.append(f'  - "{a}"')
    fm_lines.append("tags:")
    for t in tags:
        fm_lines.append(f"  - {t}")
    fm_lines.append("knowledge_refs:")
    for k in krefs:
        fm_lines.append(f"  - {k}")
    fm_lines.append("eshopy: []")
    fm_lines.append(f'description: "{popis[:160]}"')
    fm_lines.append("---")
    fm_lines.append("")
    fm_lines.append(popis)
    fm_lines.append("")
    fm_lines.append("## Specifikace")
    fm_lines.append("")
    if sucha is not None:
        fm_lines.append(f"- **Sušina:** ~{sucha} %")
    if pac is not None:
        fm_lines.append(f"- **PAC:** {pac}")
    if davk:
        fm_lines.append(f"- **Typické dávkování:** {davk}")
    fm_lines.append("")
    fm_lines.append("## Kde koupit")
    fm_lines.append("")
    fm_lines.append("> _Tato sekce je otevřená komunitě. Pošli PR s odkazy na ověřené eshopy v `eshopy:` frontmatter._")
    fm_lines.append("")
    if krefs:
        fm_lines.append("## Související knowledge")
        fm_lines.append("")
        for k in krefs:
            fm_lines.append(f"- [{k}](/knowledge/{k}/)")
        fm_lines.append("")
    DST.mkdir(parents=True, exist_ok=True)
    (DST / f"{slug}.md").write_text("\n".join(fm_lines), encoding="utf-8")
    print(f"  → src/content/ingredience/{slug}.md")


def main() -> None:
    print("Generuji databázi ingrediencí...")
    for row in INGREDIENCE:
        write_ingredience(*row)
    print(f"Hotovo, {len(INGREDIENCE)} ingrediencí.")


if __name__ == "__main__":
    main()
