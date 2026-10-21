// Repetição espaçada (sistema de Leitner), igual ao chunks/study.py:
// acertou -> sobe de caixa (revisa mais tarde); errou -> volta para a caixa 1.

import type { Chunk } from "./chunks";

export const BOX_INTERVAL_DAYS: Record<number, number> = { 1: 1, 2: 2, 3: 4, 4: 8, 5: 16 };

export interface Card {
  box: number;
  /** Data ISO (yyyy-mm-dd) da próxima revisão. */
  due: string;
}

export type Progress = Record<string, Card>;

export function today(): string {
  return toIso(new Date());
}

export function record(progress: Progress, name: string, correct: boolean, on = today()): Progress {
  const box = correct ? Math.min((progress[name]?.box ?? 1) + 1, 5) : 1;
  const due = new Date(`${on}T12:00:00`);
  due.setDate(due.getDate() + BOX_INTERVAL_DAYS[box]);
  return { ...progress, [name]: { box, due: toIso(due) } };
}

/** Chunks que vencem hoje (ou nunca estudados), os mais difíceis primeiro. */
export function dueChunks(chunks: Chunk[], progress: Progress, on = today()): Chunk[] {
  const due = chunks.filter((c) => (progress[c.name]?.due ?? on) <= on);
  return shuffle(due).sort((x, y) => (progress[x.name]?.box ?? 0) - (progress[y.name]?.box ?? 0));
}

export function stats(chunks: Chunk[], progress: Progress, on = today()) {
  let learned = 0;
  let due = 0;
  for (const c of chunks) {
    const card = progress[c.name];
    if (card && card.box >= 3) learned++;
    if ((card?.due ?? on) <= on) due++;
  }
  return { learned, due, total: chunks.length };
}

function toIso(d: Date): string {
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

function shuffle<T>(items: T[]): T[] {
  const out = [...items];
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}
