import type { ImageMetadata } from "astro";

/** Eager import všech fotek receptů. Klíč = absolutní cesta, hodnota = ImageMetadata. */
const images = import.meta.glob<{ default: ImageMetadata }>(
  "../content/recepty/pics/*.{jpg,jpeg,png,webp,JPG,JPEG,PNG,WEBP}",
  { eager: true }
);

const byFilename = new Map<string, ImageMetadata>();
for (const path in images) {
  const filename = path.split("/").pop();
  if (filename) byFilename.set(filename, images[path].default);
}

export interface Foto {
  src: ImageMetadata;
  caption: string;
  filename: string;
  /** Odkazy na recepty, ke kterým fotka patří (pro carousel na úvodní stránce). */
  recipes?: { title: string; href: string }[];
}

/**
 * Popisek z názvu souboru:
 *  - odebere příponu,
 *  - odebere koncové číslo (`_1`, `_2`, …),
 *  - podtržítka nahradí mezerami.
 * Např. `horka_cokolada_1.jpg` → `horka cokolada`.
 */
export function captionFromFilename(filename: string): string {
  return filename
    .replace(/\.[^.]+$/, "")
    .replace(/_\d+$/, "")
    .replace(/_/g, " ")
    .trim();
}

/** Přeloží názvy souborů z frontmatteru na Foto objekty (zachová pořadí, vynechá nenalezené). */
export function resolveFotky(filenames: string[]): Foto[] {
  return filenames
    .map((f) => {
      const src = byFilename.get(f);
      if (!src) return null;
      return { src, caption: captionFromFilename(f), filename: f } satisfies Foto;
    })
    .filter((x): x is Foto => x !== null);
}

/** Fisher–Yates zamíchání (vrací novou kopii). */
export function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
