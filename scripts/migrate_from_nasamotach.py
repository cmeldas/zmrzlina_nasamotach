"""Jednorázová migrace knowledge a receptů z nasamotach do tohoto repa.

Spustit z kořene zmrzlina_nasamotach repa:
    python scripts/migrate_from_nasamotach.py

Po úspěšné migraci lze (manuálně) smazat zdrojové soubory v nasamotach repu.
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_KNOWLEDGE = Path(r"c:/git_my/nasamotach/knowledge/zmrzlina")
SRC_RECEPTY = SRC_KNOWLEDGE / "recepty.md"

DST_KNOWLEDGE = ROOT / "src" / "content" / "knowledge"
DST_RECEPTY = ROOT / "src" / "content" / "recepty"

# Tagy odvozené z názvu / obsahu
KNOWLEDGE_META = {
    "tuky-ve-zmrzline": ("Tuky ve zmrzlině", "slozky", ["tuk", "mlecny-tuk", "emulze", "struktura"], 10),
    "proteiny-ve-zmrzline": ("Proteiny ve zmrzlině", "slozky", ["protein", "kasein", "msnf"], 11),
    "cukry-ve-zmrzline": ("Cukry ve zmrzlině", "slozky", ["cukry", "pac", "fpd", "sladkost"], 12),
    "vlaknina-ve-zmrzline": ("Vláknina ve zmrzlině", "slozky", ["vlaknina", "inulin", "polydextroza"], 13),
    "stabilizatory-ve-zmrzline": ("Stabilizátory ve zmrzlině", "slozky", ["stabilizator", "guar", "lbg", "karagenan"], 14),
    "emulgatory-ve-zmrzline": ("Emulgátory ve zmrzlině", "slozky", ["emulgator", "lecitin", "mono-diglyceridy"], 15),
    "sucha-latka-total-solids": ("Sušina (total solids)", "slozky", ["sucha-latka", "ts", "mass-balance"], 16),
    "vzduch-overrun": ("Vzduch a overrun", "slozky", ["overrun", "vzduch", "pena"], 17),
    "voda-a-led": ("Voda a led", "slozky", ["voda", "led", "krystaly", "tg"], 18),
    "chutove-slozky": ("Chuťové složky", "chemie", ["chut", "vanilka", "kakao", "ovoce"], 20),
    "kyseliny-a-ph": ("Kyseliny a pH", "chemie", ["ph", "kyseliny", "sorbet"], 21),
    "soli-a-mineraly": ("Soli a minerály", "chemie", ["sul", "mineraly", "vapnik"], 22),
    "alkohol-ve-zmrzline": ("Alkohol ve zmrzlině", "chemie", ["alkohol", "fpd"], 23),
    "barviva-a-antioxidanty": ("Barviva a antioxidanty", "chemie", ["barvivo", "antioxidant"], 24),
    "procesni-parametry": ("Procesní parametry", "procesy", ["pasterizace", "homogenizace", "aging", "freezing"], 30),
    "slovnik-zkratek": ("Slovník zkratek a pojmů", "reference", ["slovnik", "zkratky", "pojmy"], 90),
}


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text


def fix_internal_links(body: str, kind: str) -> str:
    """Přepíše [neco.md](neco.md) na [neco](/knowledge/neco/) apod."""

    def repl_knowledge(m: re.Match[str]) -> str:
        text = m.group(1)
        target = m.group(2)
        slug = target.replace(".md", "")
        if slug == "recepty":
            return f"[{text}](/recepty/)"
        return f"[{text}](/knowledge/{slug}/)"

    body = re.sub(r"\[([^\]]+)\]\(([a-z0-9\-]+\.md)\)", repl_knowledge, body)
    return body


def write_with_frontmatter(dst: Path, fm: dict, body: str) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            if not v:
                lines.append(f"{k}: []")
            else:
                lines.append(f"{k}:")
                for item in v:
                    lines.append(f"  - {item}")
        elif isinstance(v, (int, float)):
            lines.append(f"{k}: {v}")
        else:
            # quote strings to be safe
            sval = str(v).replace('"', '\\"')
            lines.append(f'{k}: "{sval}"')
    lines.append("---")
    lines.append("")
    lines.append(body.strip())
    lines.append("")
    dst.write_text("\n".join(lines), encoding="utf-8")
    print(f"  → {dst.relative_to(ROOT)}")


def migrate_knowledge() -> None:
    print("Migruji knowledge články...")
    for src in sorted(SRC_KNOWLEDGE.glob("*.md")):
        stem = src.stem
        if stem in ("README", "recepty"):
            continue
        meta = KNOWLEDGE_META.get(stem)
        if meta is None:
            print(f"  ! přeskakuji (žádná metadata): {stem}")
            continue
        title, sekce, tags, poradi = meta
        text = src.read_text(encoding="utf-8")
        # odstraň první H1 pokud je
        text = re.sub(r"^#\s+.+?\n+", "", text, count=1)
        # extract description z prvního >  blockquote nebo prvního odstavce
        desc_match = re.search(r"^>\s*(.+?)(?:\n\n|\n>)", text, re.DOTALL | re.MULTILINE)
        desc = ""
        if desc_match:
            desc = re.sub(r"\s+", " ", desc_match.group(1)).strip()[:200]
        body = fix_internal_links(text, "knowledge")
        fm = {
            "title": title,
            "sekce": sekce,
            "tags": tags,
            "poradi": poradi,
        }
        if desc:
            fm["description"] = desc
        write_with_frontmatter(DST_KNOWLEDGE / f"{stem}.md", fm, body)


# --- Recepty -------------------------------------------------------------

RECIPE_META = {
    1: {
        "slug": "jahodovy-sorbet",
        "typ": "sorbet",
        "tuk_pct": 0,
        "pac": 30,
        "serv_teplota": "−10 až −12 °C",
        "tags": ["sorbet", "ovoce", "jahody", "bez-mleka", "bez-vajec", "letni"],
        "ingredience": ["jahodove-pyre", "voda", "citronova-stava", "invertni-cukr", "sacharoza", "dextroza", "glukoza-suseny-sirup", "fruktoza", "mec3-natura-frutta-50"],
        "obtiznost": "zacatecnik",
        "description": "Sorbet s 45 % jahodového pyré, hladká krémová textura bez mléka i vajec.",
    },
    2: {
        "slug": "smetanovy-zaklad",
        "typ": "tocena",
        "tuk_pct": 8.9,
        "pac": 28,
        "serv_teplota": "−10 až −12 °C",
        "tags": ["smetanova", "univerzalni-zaklad", "vanilka", "klasika"],
        "ingredience": ["plnotucne-mleko", "smetana-33", "vajecny-zloutek", "invertni-cukr", "som", "sacharoza", "dextroza", "glukoza-suseny-sirup", "mec3-natura-50"],
        "obtiznost": "zacatecnik",
        "description": "Univerzální smetanový základ pro točenou zmrzlinu, ~9 % tuku.",
    },
    3: {
        "slug": "citronova-zmrzlina",
        "typ": "tocena",
        "tuk_pct": 8,
        "pac": 29,
        "serv_teplota": "−10 až −12 °C",
        "tags": ["smetanova", "ovoce", "citron", "svezi", "letni"],
        "ingredience": ["plnotucne-mleko", "smetana-33", "citronova-stava", "vajecny-zloutek", "som", "sacharoza", "dextroza", "glukoza-suseny-sirup", "mec3-natura-50"],
        "obtiznost": "zacatecnik",
        "description": "Svěží citronová zmrzlina na krémovém základě, ~8 % tuku.",
    },
    4: {
        "slug": "tvarohova-zmrzlina",
        "typ": "tocena",
        "tuk_pct": 7.8,
        "pac": 28,
        "serv_teplota": "−10 až −12 °C",
        "tags": ["smetanova", "tvaroh", "cheesecake"],
        "ingredience": ["tvaroh", "plnotucne-mleko", "smetana-33", "vajecny-zloutek", "citronova-stava", "som", "sacharoza", "dextroza", "glukoza-suseny-sirup", "mec3-natura-50"],
        "obtiznost": "stredne-pokrocily",
        "description": "Krémová tvarohová zmrzlina s cheesecake profilem, ~8 % tuku.",
    },
    5: {
        "slug": "bananova-zmrzlina",
        "typ": "tocena",
        "tuk_pct": 7.8,
        "pac": 25,
        "serv_teplota": "−10 až −12 °C",
        "tags": ["smetanova", "ovoce", "banan"],
        "ingredience": ["banan", "plnotucne-mleko", "smetana-33", "vajecny-zloutek", "citronova-stava", "som", "sacharoza", "dextroza", "mec3-natura-50"],
        "obtiznost": "stredne-pokrocily",
        "description": "Banánová zmrzlina ze zralých banánů, mléka a smetany, ~7,5 % tuku.",
    },
    6: {
        "slug": "jahodovo-tvarohovy-nanuk",
        "typ": "nanuk",
        "tuk_pct": 1.5,
        "pac": 28,
        "serv_teplota": "−18 °C",
        "tags": ["nanuk", "ovoce", "jahody", "tvaroh", "letni"],
        "ingredience": ["tvaroh", "jahodove-pyre", "citronova-stava", "invertni-cukr", "sacharoza", "dextroza", "glukoza-suseny-sirup", "mec3-natura-50", "pektin"],
        "obtiznost": "stredne-pokrocily",
        "description": "Nanuk s 50 % jahod a 22 % tvarohu, na špejli ve formičkách.",
    },
    7: {
        "slug": "french-custard-vanilka",
        "typ": "premium",
        "tuk_pct": 12.4,
        "pac": 28,
        "serv_teplota": "−10 až −12 °C",
        "tags": ["smetanova", "vanilka", "premium", "custard", "francouzska"],
        "ingredience": ["plnotucne-mleko", "smetana-33", "vajecny-zloutek", "invertni-cukr", "som", "sacharoza", "dextroza", "vanilkovy-lusk", "stabilizator-guar-lbg"],
        "obtiznost": "pokrocily",
        "description": "Klasická francouzská vanilková zmrzlina na bázi crème anglaise, vysoký podíl žloutků.",
    },
    8: {
        "slug": "cokoladova-zmrzlina",
        "typ": "tocena",
        "tuk_pct": 10.5,
        "pac": 28,
        "serv_teplota": "−10 až −12 °C",
        "tags": ["smetanova", "cokolada", "kakao", "premium"],
        "ingredience": ["plnotucne-mleko", "smetana-33", "invertni-cukr", "kakaova-hmota", "raw-kakao", "sacharoza", "dextroza", "glukoza-suseny-sirup", "som", "mec3-natura-50"],
        "obtiznost": "pokrocily",
        "description": "Plná čokoládová zmrzlina z přírodního raw kakaa a kakaové hmoty, ~10 % tuku.",
    },
}


def split_recipes() -> None:
    print("Rozděluji recepty.md na samostatné soubory...")
    text = SRC_RECEPTY.read_text(encoding="utf-8")
    pattern = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    if not matches:
        print("  ! žádné recepty nenalezeny")
        return

    # vyextrahuj společné Konvence + Provozní základy MEC3 jako úvodní článek do knowledge
    intro_end = matches[0].start()
    intro_body = text[: intro_end].strip()
    # odstraň první H1
    intro_body = re.sub(r"^#\s+.+?\n+", "", intro_body, count=1)
    intro_body = fix_internal_links(intro_body, "knowledge")
    write_with_frontmatter(
        DST_KNOWLEDGE / "konvence-receptu.md",
        {
            "title": "Konvence receptů a provozní základy MEC3",
            "sekce": "reference",
            "tags": ["konvence", "mec3", "stabilizator", "varka", "pac"],
            "poradi": 5,
            "description": "Společné konvence pro všechny recepty, dávkování provozní velikosti 10 kg a použití komerčních základů MEC3 Natura 50 a Natura frutta 50.",
        },
        intro_body,
    )

    for i, m in enumerate(matches):
        num = int(m.group(1))
        title = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n+---\s*$", "", body)
        body = fix_internal_links(body, "recepty")

        meta = RECIPE_META.get(num, {})
        slug = meta.get("slug", slugify(title))
        fm = {
            "title": title,
            "cislo": num,
            "typ": meta.get("typ", "tocena"),
            "obtiznost": meta.get("obtiznost", "stredne-pokrocily"),
            "tuk_pct": meta.get("tuk_pct"),
            "pac": meta.get("pac"),
            "serv_teplota": meta.get("serv_teplota"),
            "varka_kg": 10,
            "tags": meta.get("tags", []),
            "ingredience": meta.get("ingredience", []),
            "description": meta.get("description"),
            "pdf": f"/pdfs/recept-{num:02d}-{slug}.pdf",
        }
        # vyhoď None
        fm = {k: v for k, v in fm.items() if v is not None}
        write_with_frontmatter(DST_RECEPTY / f"{slug}.md", fm, body)


def main() -> None:
    if not SRC_KNOWLEDGE.exists():
        raise SystemExit(f"Zdroj neexistuje: {SRC_KNOWLEDGE}")
    DST_KNOWLEDGE.mkdir(parents=True, exist_ok=True)
    DST_RECEPTY.mkdir(parents=True, exist_ok=True)
    migrate_knowledge()
    split_recipes()
    print("Hotovo.")


if __name__ == "__main__":
    main()
