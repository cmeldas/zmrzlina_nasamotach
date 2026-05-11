"""Autolinkuje ingredience v markdown receptech.

Pro každý recept v `src/content/recepty/*.md`:
1. Načte slug ingredience ze frontmatter `ingredience: [...]`.
2. Načte title + nazev_alt z `src/content/ingredience/<slug>.md`.
3. V tabulkách (řádky začínající `|`) najde první sloupec obsahující název
   ingredience a obalí ho do markdown odkazu `[text](/ingredience/<slug>/)`.

Spuštění:
    python scripts/autolink_ingredience.py            # všechny recepty
    python scripts/autolink_ingredience.py --dry-run  # jen ukáže změny
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
RECEPTY = ROOT / "src" / "content" / "recepty"
INGREDIENCE = ROOT / "src" / "content" / "ingredience"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    return yaml.safe_load(parts[1]) or {}, parts[2]


def norm(s: str) -> str:
    """Bezdiakritiku, lowercase, jen alfanum + mezery."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    return re.sub(r"[^a-z0-9 ]+", " ", s).strip()


def first_significant_word(s: str) -> str:
    """První slovo s alespoň 4 znaky (přeskakuje krátká slova jako 'a', 'z')."""
    for w in norm(s).split():
        if len(w) >= 4:
            return w
    return norm(s).split()[0] if norm(s) else ""


def load_ingredience_map() -> dict[str, dict]:
    """Map slug -> {title, search_terms: [norm strings]}."""
    out: dict[str, dict] = {}
    for f in INGREDIENCE.glob("*.md"):
        fm, _ = parse_frontmatter(f.read_text(encoding="utf-8"))
        title = fm.get("title", "").strip()
        aliases = fm.get("nazev_alt") or []
        terms = []
        # primární klíč: první významné slovo z titulku (bez diakritiky)
        terms.append(first_significant_word(title))
        # plný normalizovaný titulek
        terms.append(norm(title))
        for a in aliases:
            terms.append(norm(a))
            terms.append(first_significant_word(a))
        terms = [t for t in terms if t and len(t) >= 4]
        out[f.stem] = {"title": title, "terms": list(dict.fromkeys(terms))}
    return out


def strip_markdown(s: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\*(.+?)\*", r"\1", s)
    s = re.sub(r"`(.+?)`", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return s.strip()


def cell_already_linked(cell: str) -> bool:
    return "](/ingredience/" in cell


def find_matching_slug(cell_text: str, recipe_slugs: list[str], ing_map: dict) -> str | None:
    """Vrátí slug ingredience, jejíž název je v textu buňky."""
    cell_norm = " " + norm(cell_text) + " "
    best: tuple[int, str] | None = None  # (skóre, slug)
    for slug in recipe_slugs:
        info = ing_map.get(slug)
        if not info:
            continue
        for term in info["terms"]:
            t = " " + term + " "
            if t in cell_norm:
                score = len(term)
                if best is None or score > best[0]:
                    best = (score, slug)
    return best[1] if best else None


def process_recipe(path: Path, ing_map: dict, dry_run: bool = False) -> int:
    raw = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(raw)
    recipe_slugs: list[str] = fm.get("ingredience") or []
    if not recipe_slugs:
        return 0

    lines = body.split("\n")
    replacements = 0
    used_slugs: set[str] = set()

    for i, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            continue
        # Rozdělit na buňky
        parts = line.split("|")
        if len(parts) < 3:
            continue
        # první "užitečná" buňka (parts[0] je obvykle prázdná před prvním |)
        first_idx = 1
        first_cell = parts[first_idx]
        stripped = strip_markdown(first_cell)
        if not stripped:
            continue
        if cell_already_linked(first_cell):
            continue
        # přeskočit separátorové řádky (---|---)
        if re.fullmatch(r"[\s\-:]+", stripped):
            continue
        # přeskočit záhlaví tabulky (obsahuje slovo "Ingredience"/"Složka"/"Cukr"/"Aspekt"/"Produkt" → poznáme až podle textu)
        # Použijeme jen find_matching_slug — pokud nic nematchne, řádek zůstane.
        slug = find_matching_slug(stripped, recipe_slugs, ing_map)
        if not slug:
            continue
        if slug in used_slugs:
            continue  # každou ingredienci linkovat jen jednou
        # zachovat původní padding a markdown bold/italic uvnitř
        leading = re.match(r"^(\s*)", first_cell).group(1)
        trailing = re.match(r"^.*?(\s*)$", first_cell, re.DOTALL).group(1)
        inner = first_cell.strip()
        new_inner = f"[{inner}](/ingredience/{slug}/)"
        parts[first_idx] = f"{leading}{new_inner}{trailing}"
        lines[i] = "|".join(parts)
        replacements += 1
        used_slugs.add(slug)

    if replacements == 0:
        return 0

    new_body = "\n".join(lines)
    new_raw = raw.replace(body, new_body, 1)

    if dry_run:
        print(f"  [dry-run] by upravil {replacements} buněk")
    else:
        path.write_text(new_raw, encoding="utf-8")
    return replacements


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--recipe", help="jen jeden recept podle slugu")
    args = parser.parse_args()

    ing_map = load_ingredience_map()
    print(f"Ingredience: {len(ing_map)}")

    total = 0
    for f in sorted(RECEPTY.glob("*.md")):
        if args.recipe and f.stem != args.recipe:
            continue
        print(f"▸ {f.name}")
        n = process_recipe(f, ing_map, dry_run=args.dry_run)
        total += n
        print(f"  ↳ {n} odkazů")
    print(f"\nCelkem: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
