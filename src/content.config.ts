import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const recepty = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/recepty" }),
  schema: z.object({
    title: z.string(),
    cislo: z.number().optional(),
    typ: z.enum(["tocena", "sorbet", "nanuk", "kopeckova", "premium"]),
    obtiznost: z.enum(["zacatecnik", "stredne-pokrocily", "pokrocily"]).default("stredne-pokrocily"),
    tuk_pct: z.number().optional(),
    pac: z.number().optional(),
    serv_teplota: z.string().optional(),
    overrun: z.string().optional(),
    varka_kg: z.number().default(10),
    tags: z.array(z.string()).default([]),
    ingredience: z.array(z.string()).default([]),
    souvisejici: z.array(z.string()).default([]),
    description: z.string().optional(),
    pdf: z.string().optional(),
    autor: z.string().default("Ranč Na Samotách"),
    licence: z.string().default("CC BY-SA 4.0"),
    aktualizovano: z.coerce.date().optional(),
    /** Stav vývoje receptu:
     *  - navrh:    teoretický návrh, nevyzkoušený
     *  - testovany: jednou vyrobený, ale ještě dolaďujeme
     *  - odladeny: ověřený, použitelný v provozu
     */
    stav: z.enum(["navrh", "testovany", "odladeny"]).default("navrh"),
    /** Pokud false, recept se nevygeneruje do Vercel buildu (zůstává v Gitu). */
    publikovat: z.boolean().default(true),
  }),
});

const ingredience = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/ingredience" }),
  schema: z.object({
    title: z.string(),
    kategorie: z.enum([
      "cukr",
      "tuk-mlecny",
      "protein",
      "stabilizator",
      "emulgator",
      "ovoce",
      "kakao",
      "aroma",
      "sul-mineral",
      "vlaknina",
      "alkohol",
      "baze-komercni",
      "voda",
    ]),
    nazev_alt: z.array(z.string()).default([]),
    forma: z.enum(["kapalna", "sypka", "pasta", "polotuhe"]).optional(),
    sucha_latka_pct: z.number().optional(),
    pac: z.number().optional(),
    pod: z.number().optional(),
    typicke_davkovani: z.string().optional(),
    eshopy: z
      .array(
        z.object({
          nazev: z.string(),
          url: z.string().url(),
          poznamka: z.string().optional(),
        })
      )
      .default([]),
    tags: z.array(z.string()).default([]),
    knowledge_refs: z.array(z.string()).default([]),
    description: z.string().optional(),
  }),
});

const knowledge = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/knowledge" }),
  schema: z.object({
    title: z.string(),
    sekce: z.enum(["slozky", "chemie", "procesy", "reference"]).default("slozky"),
    tags: z.array(z.string()).default([]),
    description: z.string().optional(),
    poradi: z.number().default(100),
  }),
});

export const collections = { recepty, ingredience, knowledge };
