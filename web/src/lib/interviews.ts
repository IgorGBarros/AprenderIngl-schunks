// Sessões de entrevista exportadas de chunks/interviews (python -m chunks json).

import data from "../data/interviews.json";

export interface Question {
  id: string;
  stage: string;
  en: string;
  goal: string;
  answer: string;
  tips: string[];
  follow_ups: string[];
}

export interface Stage {
  id: string;
  title: string;
  description: string;
}

export interface Session {
  id: string;
  title: string;
  company: string;
  summary: string;
  stages: Stage[];
  questions: Question[];
}

export const SESSIONS = data as unknown as Session[];

/** Pedaço da resposta: texto normal, chunk ([[...]]) ou algo para preencher (((...))). */
export interface AnswerPart {
  text: string;
  kind: "text" | "chunk" | "fill";
}

export function parseAnswer(answer: string): AnswerPart[] {
  const parts: AnswerPart[] = [];
  let last = 0;
  for (const m of answer.matchAll(/\[\[(.+?)\]\]|\(\((.+?)\)\)/g)) {
    if (m.index! > last) parts.push({ text: answer.slice(last, m.index), kind: "text" });
    parts.push(m[1] !== undefined ? { text: m[1], kind: "chunk" } : { text: m[2], kind: "fill" });
    last = m.index! + m[0].length;
  }
  if (last < answer.length) parts.push({ text: answer.slice(last), kind: "text" });
  return parts;
}

/** Texto para ler em voz alta: sem marcação e sem os trechos a preencher. */
export function speakable(answer: string): string {
  return parseAnswer(answer)
    .filter((p) => p.kind !== "fill")
    .map((p) => p.text)
    .join("")
    .replace(/\s{2,}/g, " ")
    .replace(/\s+([.,?!;:])/g, "$1");
}

export function chunksIn(answer: string): string[] {
  return parseAnswer(answer)
    .filter((p) => p.kind === "chunk")
    .map((p) => p.text);
}
