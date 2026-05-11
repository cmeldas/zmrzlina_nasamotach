export function slugifyTag(tag: string): string {
  return tag
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export function formatPct(v?: number): string {
  if (v === undefined || v === null) return "—";
  return `${v.toLocaleString("cs-CZ", { maximumFractionDigits: 1 })} %`;
}

export const TYP_LABEL: Record<string, string> = {
  tocena: "Točená",
  sorbet: "Sorbet",
  nanuk: "Nanuk",
  kopeckova: "Kopečková",
  premium: "Premium",
};

export const KATEGORIE_LABEL: Record<string, string> = {
  cukr: "Cukry",
  "tuk-mlecny": "Mléčné tuky",
  protein: "Proteiny",
  stabilizator: "Stabilizátory",
  emulgator: "Emulgátory",
  ovoce: "Ovoce",
  kakao: "Kakao a čokoláda",
  aroma: "Aromata",
  "sul-mineral": "Soli a minerály",
  vlaknina: "Vlákniny",
  alkohol: "Alkohol",
  "baze-komercni": "Komerční báze",
  voda: "Voda",
};

export const SEKCE_LABEL: Record<string, string> = {
  slozky: "Hlavní složky mixu",
  chemie: "Chemie a chuť",
  procesy: "Procesy",
  reference: "Reference a slovník",
};

export const OBTIZNOST_LABEL: Record<string, string> = {
  zacatecnik: "Začátečník",
  "stredne-pokrocily": "Středně pokročilý",
  pokrocily: "Pokročilý",
};
