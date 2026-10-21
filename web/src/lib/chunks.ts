// Mesmo motor da biblioteca Python (chunks/core.py), em TypeScript.
//
// Template:  "[[Could I get]] {item}[[, please]]?"
//   [[...]] = parte fixa (o que você memoriza)
//   {nome}  = variável (argumento da "função")

import library from "../data/chunks.json";

/** Valor de exemplo: só inglês, ou [inglês, português]. */
export type ExampleValue = string | [string, string];

export interface Chunk {
  name: string;
  template: string;
  pt: string;
  category: string;
  slots: string[];
  /** Exemplos prontos (o primeiro é o principal). */
  examples: Record<string, ExampleValue>[];
  /** Formato antigo (um exemplo só), ainda salvo nos "Meus chunks" de versões anteriores. */
  example?: Record<string, ExampleValue>;
  defaults: Record<string, string>;
  note: string;
  /** Saída gerada pelo Python para cada exemplo (usada nos testes). */
  demos?: { en: string; pt: string; cloze: string }[];
}

/** Variável preenchida pelo usuário; `pt` é opcional. */
export interface SlotValue {
  en: string;
  pt?: string;
}

export interface Phrase {
  en: string;
  pt: string;
  cloze: string;
  /** Pedaços da frase em inglês, marcando o que é fixo e o que é variável. */
  parts: { text: string; fixed: boolean }[];
}

export const BUILTIN = library as unknown as Chunk[];

export const CATEGORY_LABELS: Record<string, string> = {
  survival: "Sobrevivência",
  home: "Casa",
  meetings: "Reuniões",
  tech: "Tech",
  business: "Negócios",
  interview: "Entrevista",
  data: "Dados",
  mine: "Meus",
};

/** Categorias na ordem de exibição (as desconhecidas vão para o fim). */
export function categoriesOf(chunks: Chunk[]): string[] {
  const order = Object.keys(CATEGORY_LABELS);
  const rank = (c: string) => (order.includes(c) ? order.indexOf(c) : order.length);
  return [...new Set(chunks.map((c) => c.category))].sort((x, y) => rank(x) - rank(y));
}

const TOKEN = /\[\[(.+?)\]\]|\{(\w+)\}/g;

/** Nomes das variáveis na ordem em que aparecem no template. */
export function slotsOf(template: string): string[] {
  const out: string[] = [];
  for (const m of template.matchAll(TOKEN)) {
    if (m[2] && !out.includes(m[2])) out.push(m[2]);
  }
  return out;
}

export function examplesOf(c: Chunk): Record<string, ExampleValue>[] {
  return c.examples?.length ? c.examples : c.example ? [c.example] : [{}];
}

/** Valores do exemplo ``index`` (o primeiro, se não informado). */
export function exampleValues(c: Chunk, index = 0): Record<string, SlotValue> {
  const example = examplesOf(c)[index] ?? {};
  const values: Record<string, SlotValue> = {};
  for (const slot of c.slots) {
    const ex = example[slot] ?? c.defaults[slot] ?? "";
    values[slot] = Array.isArray(ex) ? { en: ex[0], pt: ex[1] } : { en: ex };
  }
  return values;
}

/** Todos os exemplos já montados. */
export function demos(c: Chunk): Phrase[] {
  return examplesOf(c).map((_, i) => render(c, exampleValues(c, i)));
}

/** Dica do quiz: cada letra da parte fixa vira "_" (mostra quantas palavras faltam). */
export function blanks(p: Phrase): string {
  return p.parts.map((x) => (x.fixed ? x.text.replace(/[A-Za-z0-9']/g, "_") : x.text)).join("");
}

export function render(c: Chunk, values: Record<string, SlotValue>): Phrase {
  const parts: Phrase["parts"] = [];
  let last = 0;
  const push = (text: string, fixed: boolean) => {
    if (!text) return;
    const prev = parts[parts.length - 1];
    if (prev && prev.fixed === fixed) prev.text += text;
    else parts.push({ text, fixed });
  };
  for (const m of c.template.matchAll(TOKEN)) {
    push(c.template.slice(last, m.index), false);
    if (m[1] !== undefined) {
      // Pontuação solta não conta como parte fixa (não vira cloze).
      push(m[1], /\w/.test(m[1]));
    } else {
      push(slotEn(c, values, m[2]), false);
    }
    last = m.index! + m[0].length;
  }
  push(c.template.slice(last), false);

  const clean = tidyParts(parts);
  const en = clean.map((p) => p.text).join("");
  const cloze = clean.map((p) => (p.fixed ? `{{c1::${p.text}}}` : p.text)).join("");
  const pt = tidy(
    c.pt.replace(/\{(\w+)\}/g, (_, slot: string) => {
      const v = values[slot];
      return v?.pt?.trim() || slotEn(c, values, slot);
    }),
  );
  return { en, pt, cloze, parts: clean };
}

/** Parte fixa com as variáveis como "...". */
export function core(c: Chunk): string {
  return c.template.replace(/\[\[(.+?)\]\]/g, "$1").replace(/\{\w+\}/g, "...");
}

export function pattern(c: Chunk): string {
  return `${c.name}(${c.slots.join(", ")})`;
}

export function search(chunks: Chunk[], term: string): Chunk[] {
  const t = normalizeSearch(term);
  if (!t) return chunks;
  return chunks.filter((c) =>
    [c.name.replace(/_/g, " "), core(c), c.pt, ...demos(c).flatMap((p) => [p.en, p.pt])].some((s) =>
      normalizeSearch(s).includes(t),
    ),
  );
}

/** Artigo certo: a("apple") -> "an apple". */
export function a(noun: string): string {
  const w = noun.trim().toLowerCase();
  let vowel = /^[aeiou]/.test(w) && !/^(uni|use|eu|one)/.test(w);
  vowel ||= /^(hour|honest|mvp|api|sql|sdk)/.test(w);
  return `${vowel ? "an" : "a"} ${noun}`;
}

/** Compara a resposta ignorando maiúsculas, pontuação e espaços. */
export function normalizeAnswer(text: string): string {
  return text
    .toLowerCase()
    .replace(/[’‘]/g, "'")
    .replace(/[^a-z0-9' ]+/g, " ")
    .split(/\s+/)
    .filter(Boolean)
    .join(" ");
}

/** Gera um nome de função a partir da parte fixa: "I'm blocked by" -> "im_blocked_by". */
export function nameFrom(template: string): string {
  const fixed = [...template.matchAll(/\[\[(.+?)\]\]/g)].map((m) => m[1]).join(" ");
  return (
    fixed
      .toLowerCase()
      .replace(/'/g, "")
      .replace(/[^a-z0-9]+/g, "_")
      .replace(/^_+|_+$/g, "")
      .slice(0, 50) || "my_chunk"
  );
}

function slotEn(c: Chunk, values: Record<string, SlotValue>, slot: string): string {
  const v = values[slot]?.en;
  return v !== undefined && v.trim() !== "" ? v : (c.defaults[slot] ?? "");
}

function tidy(text: string): string {
  const t = text.replace(/\s{2,}/g, " ").replace(/\s+([.,?!;:])/g, "$1").trim();
  return t.charAt(0).toUpperCase() + t.slice(1);
}

/** Mesma limpeza do tidy(), mas preservando o que é fixo e o que é variável. */
function tidyParts(parts: Phrase["parts"]): Phrase["parts"] {
  const chars = parts.flatMap((p) => [...p.text].map((ch) => ({ ch, fixed: p.fixed })));
  const kept: typeof chars = [];
  chars.forEach((c, i) => {
    const next = chars[i + 1]?.ch;
    const dropSpace =
      /\s/.test(c.ch) && (kept.length === 0 || next === undefined || /[\s.,?!;:]/.test(next));
    if (!dropSpace) kept.push(/\s/.test(c.ch) ? { ...c, ch: " " } : c);
  });
  if (kept[0]) kept[0] = { ...kept[0], ch: kept[0].ch.toUpperCase() };

  const out: Phrase["parts"] = [];
  for (const { ch, fixed } of kept) {
    const prev = out[out.length - 1];
    if (prev && prev.fixed === fixed) prev.text += ch;
    else out.push({ text: ch, fixed });
  }
  return out;
}

function normalizeSearch(s: string): string {
  return s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .trim();
}
