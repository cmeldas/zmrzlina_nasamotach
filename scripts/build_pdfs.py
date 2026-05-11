"""Generování A4 PDF receptů zmrzliny pro offline tisk.

Načte všechny recepty ze `src/content/recepty/*.md`, vyparsuje YAML frontmatter
a vyrenderuje každý jako jednu A4 PDF do `public/pdfs/recept-NN-slug.pdf`.
S autofitem velikosti písma — pokud se obsah nevejde, font se postupně zmenšuje.

Použití:
    python scripts/build_pdfs.py                     # všechny recepty
    python scripts/build_pdfs.py --recipe 5          # jen jeden
    python scripts/build_pdfs.py --font-size 9.5     # ladění typografie
    python scripts/build_pdfs.py --columns 2

Závislosti:
    pip install playwright markdown-it-py pyyaml
    playwright install chromium

DŮLEŽITÉ — NIKDY nepřidávat Stop-Process / taskkill na chrome.exe apod.
Pokud je výstupní PDF zamčené (otevřené v prohlížeči), skript jen vypíše
hlášku a vyzve uživatele, aby soubor zavřel a spustil znovu.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml
from markdown_it import MarkdownIt
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "content" / "recepty"
OUT = ROOT / "public" / "pdfs"

BROWN = "#3d2e1e"
GOLD = "#e8a723"
GOLD_DARK = "#c47a15"
CREAM = "#faf6ee"
LINE = "#d8c89a"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm = yaml.safe_load(parts[1]) or {}
    body = parts[2].lstrip("\n")
    return fm, body


def strip_markdown_links(md_body: str) -> str:
    """V PDF nedávají smysl (nefungují) — zachová jen text odkazu.

    [text](url) → text   |  [text][ref] → text   |  ![alt](url) zůstává.
    """
    # inline link [text](url)
    md_body = re.sub(r"(?<!\!)\[([^\]]+)\]\([^)]*\)", r"\1", md_body)
    # reference link [text][ref] nebo [text][]
    md_body = re.sub(r"(?<!\!)\[([^\]]+)\]\[[^\]]*\]", r"\1", md_body)
    return md_body


def render_markdown(md_body: str) -> str:
    md_body = strip_markdown_links(md_body)
    md = MarkdownIt("commonmark", {"html": False, "linkify": False, "typographer": True})
    md.enable("table")
    md.enable("strikethrough")
    return md.render(md_body)


CSS_TEMPLATE = """
@import url("https://fonts.googleapis.com/css2?family=Sriracha&family=Rubik:wght@300;400;500;600;700&display=swap");

@page {{ size: A4 portrait; margin: 11mm 12mm 16mm 12mm; }}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

html, body {{
    font-family: "Rubik", Arial, sans-serif;
    color: {BROWN};
    background: #fff;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}}

.page {{
    --body-font: {FS}pt;
    --body-h3: {H3}pt;
    --body-table: {TB}pt;
}}

.header {{
    border-bottom: 0.6mm solid {GOLD};
    padding-bottom: 3mm; margin-bottom: 4mm;
    display: flex; align-items: flex-end; justify-content: space-between;
    gap: 6mm;
    break-inside: avoid; break-after: avoid;
}}
.header .header-left {{ flex: 1; min-width: 0; }}
.header .header-right {{
    text-align: right; flex-shrink: 0;
    max-width: 70mm;
}}
.header .brand {{
    font-size: 7pt; color: {GOLD_DARK};
    text-transform: uppercase; letter-spacing: 1pt;
    margin-bottom: 1.5mm;
}}
.header .brand strong {{
    display: block; font-family: "Sriracha", cursive;
    font-size: 11pt; color: {BROWN}; text-transform: none; letter-spacing: 0;
}}
.header .license-tag {{
    font-size: 6.5pt; color: {BROWN}; line-height: 1.25;
    background: {CREAM}; border-left: 0.5mm solid {GOLD};
    padding: 0.8mm 1.5mm;
}}
.header .license-tag strong {{ color: {GOLD_DARK}; font-weight: 700; }}

.recipe-num .stav-pill {{
    display: inline-block;
    padding: 0.1mm 1.5mm;
    border-radius: 2mm;
    font-family: "Rubik", sans-serif;
    font-size: 7pt;
    font-weight: 600;
    letter-spacing: 0.2pt;
    vertical-align: 0.5mm;
}}
.recipe-num .stav-pill.stav-navrh {{ background: #fef3e8; color: #8a4a08; border: 0.1mm solid #f0c177; }}
.recipe-num .stav-pill.stav-testovany {{ background: #fff7d6; color: #6b4d05; border: 0.1mm solid #e8c34a; }}
.recipe-num .stav-pill.stav-odladeny {{ background: #e8f4e0; color: #2d5016; border: 0.1mm solid #8ac070; }}

.recipe-num {{
    font-family: "Sriracha", cursive;
    font-size: 11pt; color: {GOLD_DARK};
}}
.recipe-title {{
    font-family: "Sriracha", cursive;
    font-size: 22pt; color: {BROWN}; line-height: 1.05;
}}

.meta-pills {{
    display: flex; gap: 4mm; flex-wrap: wrap;
    font-size: 8pt; color: {GOLD_DARK};
    margin-bottom: 3mm;
    break-inside: avoid; break-after: avoid;
}}
.meta-pills span {{ padding: 0.5mm 2mm; background: {CREAM}; border-radius: 1mm; }}
.meta-pills strong {{ color: {BROWN}; }}

.body {{
    font-size: var(--body-font); line-height: 1.32;
    column-count: {COLS}; column-gap: 6mm;
    column-rule: 0.15mm solid {LINE}; column-fill: auto;
}}

.body p, .body ul, .body ol, .body table, .body blockquote, .body h3, .body h4 {{
    margin-bottom: 1.6mm; break-inside: avoid;
}}
.body h3 {{
    font-family: "Rubik", sans-serif;
    font-size: var(--body-h3); font-weight: 700; color: {GOLD_DARK};
    margin-top: 2.5mm; margin-bottom: 1.2mm;
    padding-bottom: 0.5mm; border-bottom: 0.15mm dotted {GOLD};
    break-after: avoid;
}}
.body h3:first-child {{ margin-top: 0; }}
.body h4 {{ font-size: var(--body-font); font-weight: 700; color: {BROWN}; margin-top: 1.8mm; break-after: avoid; }}
.body strong {{ color: {BROWN}; font-weight: 600; }}
.body em {{ color: #6b5536; }}
.body ul, .body ol {{ padding-left: 4mm; }}
.body li {{ margin-bottom: 0.4mm; }}
.body blockquote {{
    border-left: 0.6mm solid {GOLD};
    padding: 0.8mm 0 0.8mm 2mm; background: {CREAM};
    color: #5a4528; font-style: italic;
}}
.body table {{
    width: 100%; border-collapse: collapse;
    font-size: var(--body-table); line-height: 1.2;
}}
.body th, .body td {{
    border: 0.1mm solid {LINE}; padding: 0.6mm 1.2mm;
    text-align: left; vertical-align: top;
}}
.body th {{ background: {CREAM}; color: {BROWN}; font-weight: 600; }}
.body tbody tr:nth-child(even) td {{ background: rgba(232,167,35,0.05); }}
.body td:not(:first-child), .body th:not(:first-child) {{ text-align: right; }}
"""


# Opakovaná patička na každé stránce — vykreslí Chromium do bottom margin oblasti.
# Pozor: musíme používat inline styly (Chrome ignoruje externí CSS v templates) a
# explicitní velikost písma; defaultní je 0pt.
FOOTER_TEMPLATE = """
<div style="font-family: 'Helvetica', 'Arial', sans-serif; font-size: 8pt;
            color: #c47a15; width: 100%; padding: 0 12mm 4mm 12mm;
            display: flex; justify-content: space-between; align-items: center;
            border-top: 0.3mm solid #d8c89a; padding-top: 2mm;
            -webkit-print-color-adjust: exact;">
  <span style="color:#c47a15;">zmrzlina.nasamotach.cz</span>
  <span style="color:#3d2e1e;">{AUTOR}</span>
  <span style="color:#c47a15;">{GENERATED} &nbsp;·&nbsp; str. <span class="pageNumber"></span>/<span class="totalPages"></span></span>
</div>
"""


HTML_TEMPLATE = """<!doctype html>
<html lang="cs"><head><meta charset="UTF-8"><title>Recept {NUM}: {TITLE}</title>
<style>{CSS}</style></head><body>
<div class="page">
  <header class="header">
    <div class="header-left">
      <div class="recipe-num">Recept č.&nbsp;{NUM} &nbsp;·&nbsp; <span class="stav-pill stav-{STAV}">{STAV_LABEL}</span></div>
      <h1 class="recipe-title">{TITLE}</h1>
    </div>
    <div class="header-right">
      <div class="brand">
        <strong>Zmrzlina&nbsp;Na&nbsp;Samotách</strong>
        Otevřená receptura
      </div>
      <div class="license-tag">
        <strong>CC&nbsp;BY-SA&nbsp;4.0</strong> · Sdílej a uprav. Uveď zdroj, zachovej licenci.
      </div>
    </div>
  </header>
  <div class="meta-pills">
    <span><strong>Typ:</strong> {TYP}</span>
    <span><strong>Tuk:</strong> {TUK}</span>
    <span><strong>PAC:</strong> {PAC}</span>
    <span><strong>Servírování:</strong> {SERV}</span>
    <span><strong>Várka:</strong> {VARKA} kg</span>
  </div>
  <main class="body">{CONTENT}</main>
</div></body></html>
"""


def build_html(num: int, fm: dict, body_md: str, *, fs: float, cols: int) -> str:
    css = CSS_TEMPLATE.format(
        BROWN=BROWN, GOLD=GOLD, GOLD_DARK=GOLD_DARK, CREAM=CREAM, LINE=LINE,
        FS=fs, H3=fs + 1, TB=max(fs - 1.0, 7.0), COLS=cols,
    )
    return HTML_TEMPLATE.format(
        NUM=num,
        TITLE=fm.get("title", "Recept"),
        CSS=css,
        CONTENT=render_markdown(body_md),
        GENERATED=datetime.now().strftime("%d.\u00a0%m.\u00a0%Y"),
        TYP=fm.get("typ", "—"),
        TUK=f"{fm.get('tuk_pct', '—')} %" if fm.get("tuk_pct") is not None else "—",
        PAC=fm.get("pac", "—"),
        SERV=fm.get("serv_teplota", "—"),
        VARKA=fm.get("varka_kg", 10),
        STAV=fm.get("stav", "navrh"),
        STAV_LABEL={"navrh": "Návrh", "testovany": "Testovaný", "odladeny": "Odladěný"}.get(fm.get("stav", "navrh"), "Návrh"),
        AUTOR=fm.get("autor", "Ranč Na Samotách"),
    )


def render_pdf(html_path: Path, pdf_path: Path, *, fs: float, min_fs: float = 7.5, step: float = 0.25,
               footer_autor: str = "Ranč Na Samotách", footer_date: str = "") -> tuple[float, int]:
    """Renderuje HTML do PDF. Pokouší se zmenšit font tak, aby vše bylo na 1 stránce.
    Pokud se to nedaří ani při `min_fs`, povolí přirozené stránkování na více A4.
    Vrací (použitý font, počet stránek).
    """
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    used = fs
    pages = 1
    # Printable area uvnitř @page { margin: 11mm 12mm 16mm 12mm }: 270mm na výšku.
    # CSS px: 1mm = 3.7795275. Toleranci dáváme 2mm.
    max_height_px = 270 * 3.7795275 - 4

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 794, "height": 1123})  # A4 v CSS px
        page.emulate_media(media="print")
        page.goto(html_path.as_uri())
        page.wait_for_load_state("networkidle")
        # iterativní zmenšování fontu, dokud .page.scrollHeight ≤ max_height_px
        while used >= min_fs:
            page.evaluate(
                """([fs, h3, tb]) => {
                    const r = document.querySelector('.page');
                    if (!r) return;
                    r.style.setProperty('--body-font', fs + 'pt');
                    r.style.setProperty('--body-h3', h3 + 'pt');
                    r.style.setProperty('--body-table', tb + 'pt');
                }""",
                [used, used + 1, max(used - 1.0, 7.0)],
            )
            height = page.evaluate(
                """() => {
                    const p = document.querySelector('.page');
                    return p ? p.scrollHeight : document.body.scrollHeight;
                }"""
            )
            if height <= max_height_px:
                break
            used -= step
        else:
            # vyšli jsme z while bez break → ani při min_fs se nevejde
            # zvedneme font zpět na komfortní hodnotu a necháme přetéct na další A4
            used = max(fs - 1.0, min_fs + 0.5)
            page.evaluate(
                """([fs, h3, tb]) => {
                    const r = document.querySelector('.page');
                    if (!r) return;
                    r.style.setProperty('--body-font', fs + 'pt');
                    r.style.setProperty('--body-h3', h3 + 'pt');
                    r.style.setProperty('--body-table', tb + 'pt');
                }""",
                [used, used + 1, max(used - 1.0, 7.0)],
            )
            final_height = page.evaluate("() => document.querySelector('.page').scrollHeight")
            pages = max(1, int(final_height / max_height_px) + (1 if final_height % max_height_px > 4 else 0))
        try:
            page.pdf(
                path=str(pdf_path),
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
                display_header_footer=True,
                header_template="<div></div>",
                footer_template=FOOTER_TEMPLATE.format(AUTOR=footer_autor, GENERATED=footer_date),
            )
        except (PermissionError, OSError) as exc:
            browser.close()
            raise PermissionError(
                f"Nelze zapsat PDF: {pdf_path}\n"
                f"   Soubor je pravděpodobně otevřený v prohlížeči (Acrobat, Edge, Chrome…).\n"
                f"   Zavřete ho a spusťte skript znovu."
            ) from exc
        browser.close()
    return used, pages


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--recipe", type=int, default=None, help="Jen recept s daným číslem (cislo: ve frontmatter)")
    parser.add_argument("--font-size", type=float, default=9.5)
    parser.add_argument("--min-font-size", type=float, default=7.5)
    parser.add_argument("--columns", type=int, default=2, choices=[1, 2, 3])
    parser.add_argument("--keep-html", action="store_true")
    parser.add_argument(
        "--include-unpublished", action="store_true",
        help="Generuj PDF i pro recepty s `publikovat: false` (defaultně se přeskakují).",
    )
    args = parser.parse_args()

    if not SRC.exists():
        print(f"✗ Zdroj neexistuje: {SRC}", file=sys.stderr)
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    files = sorted(SRC.glob("*.md"))
    print(f"Zdroj:  {SRC}")
    print(f"Výstup: {OUT}")
    print(f"Souborů: {len(files)}\n")

    for f in files:
        fm, body = parse_frontmatter(f.read_text(encoding="utf-8"))
        num = int(fm.get("cislo", 0))
        if args.recipe is not None and num != args.recipe:
            continue
        if fm.get("publikovat") is False and not args.include_unpublished:
            print(f"⊘ {num}. {fm.get('title')} — přeskočeno (publikovat: false)")
            continue
        slug = f.stem
        out_html = OUT / f"recept-{num:02d}-{slug}.html"
        out_pdf = OUT / f"recept-{num:02d}-{slug}.pdf"
        html = build_html(num, fm, body, fs=args.font_size, cols=args.columns)
        out_html.write_text(html, encoding="utf-8")
        print(f"▸ {num}. {fm.get('title')}")
        used, pages = render_pdf(
            out_html, out_pdf,
            fs=args.font_size, min_fs=args.min_font_size,
            footer_autor=str(fm.get("autor", "Ranč Na Samotách")),
            footer_date=datetime.now().strftime("%d.\u00a0%m.\u00a0%Y"),
        )
        size_kb = out_pdf.stat().st_size / 1024
        page_info = f"{pages} str." if pages > 1 else "1 str."
        print(f"  → {out_pdf.name} ({size_kb:.0f} KB, font {used:.2f}pt, {page_info})")
        if not args.keep_html:
            out_html.unlink(missing_ok=True)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except PermissionError as exc:
        print(f"✗ {exc}", file=sys.stderr)
        sys.exit(2)
