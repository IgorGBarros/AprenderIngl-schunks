// Gera uma sessão de entrevista para qualquer vaga (mesma lógica de
// chunks/interviews/generate.py, com os prompts exportados do Python).

import prompts from "../data/interview_prompts.json";
import type { Question, Session } from "./interviews";
import { type OllamaConfig, OllamaError, chatJson } from "./ollama";

const COUNT_OVERRIDE: Record<string, number> = { closing: 2 };

interface RawQuestions {
  questions?: unknown;
}

interface RawMeta {
  title?: unknown;
  company?: unknown;
  summary?: unknown;
}

export async function generateSession(
  job: string,
  profile: string,
  config: OllamaConfig,
  options: { perStage?: number; onProgress?: (msg: string) => void; signal?: AbortSignal; takenIds?: string[] } = {},
): Promise<Session> {
  const { perStage = 5, onProgress = () => {}, signal, takenIds = [] } = options;
  job = job.trim();
  if (job.length < 80) throw new OllamaError("Cole a descrição completa da vaga (o texto está curto demais).");
  const profileText = profile.trim() || prompts.no_profile;

  onProgress("Lendo a vaga…");
  const meta = await chatJson<RawMeta>(
    config,
    "You extract information from job descriptions. Answer only with JSON.",
    fill(prompts.meta_prompt, { job }),
    prompts.meta_schema,
    0.1,
    signal,
  );

  const questions: Question[] = [];
  for (const stage of prompts.stages) {
    onProgress(`Gerando: ${stage.title}…`);
    const count = COUNT_OVERRIDE[stage.id] ?? perStage;
    const prompt = fill(prompts.stage_prompt, {
      job,
      profile: profileText,
      stage_title: stage.title,
      count: String(count),
      stage_focus: (prompts.stage_focus as Record<string, string>)[stage.id],
      already: questions.map((q) => `- ${q.en}`).join("\n") || "(none yet)",
    });
    const raw = await chatJson<RawQuestions>(config, prompts.system, prompt, prompts.questions_schema, 0.4, signal);
    const found = normalizeQuestions(raw, stage.id, questions.length).slice(0, count);
    if (found.length === 0) {
      throw new OllamaError(
        `O modelo ${config.model} não gerou perguntas para a etapa "${stage.title}". Tente de novo ou use um modelo maior.`,
      );
    }
    questions.push(...found);
  }

  const title = text(meta.title) || "Entrevista";
  const company = text(meta.company);
  return {
    id: uniqueId(slugify(`${company} ${title}`), takenIds),
    title,
    company,
    summary: text(meta.summary),
    stages: prompts.stages,
    questions,
  };
}

export function normalizeQuestions(raw: RawQuestions, stage: string, start = 0): Question[] {
  const items = Array.isArray(raw?.questions) ? raw.questions : [];
  const out: Question[] = [];
  for (const item of items) {
    if (!item || typeof item !== "object") continue;
    const r = item as Record<string, unknown>;
    const en = text(r.question);
    const answer = fixMarkup(text(r.answer));
    if (!en || !answer) continue;
    out.push({
      id: `${stage}_${start + out.length + 1}`,
      stage,
      en,
      goal: text(r.goal),
      answer,
      tips: texts(r.tips).slice(0, 3),
      follow_ups: texts(r.follow_ups).slice(0, 2),
    });
  }
  return out;
}

/** Remove marcadores [[ ]] / (( )) quando o modelo os deixou desbalanceados. */
export function fixMarkup(s: string): string {
  for (const [open, close] of [
    ["[[", "]]"],
    ["((", "))"],
  ]) {
    const pair = new RegExp(`${escape(open)}.+?${escape(close)}`, "g");
    const leftover = s.replace(pair, "");
    if (leftover.includes(open) || leftover.includes(close)) s = s.split(open).join("").split(close).join("");
  }
  return s;
}

export function slugify(s: string): string {
  return (
    s
      .normalize("NFKD")
      .replace(/[̀-ͯ]/g, "")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "_")
      .replace(/^_+|_+$/g, "")
      .slice(0, 60) || "vaga"
  );
}

/** Valida um JSON de sessão (ex.: gerado pelo `python -m chunks vaga`) antes de importar. */
export function parseSession(json: string): Session {
  const data = JSON.parse(json) as Partial<Session>;
  if (!data || typeof data.id !== "string" || !Array.isArray(data.stages) || !Array.isArray(data.questions)) {
    throw new Error("Este arquivo não parece uma sessão de entrevista.");
  }
  const stages = new Set(data.stages.map((s) => s.id));
  if (data.questions.some((q) => !q || typeof q.en !== "string" || !stages.has(q.stage))) {
    throw new Error("A sessão tem perguntas inválidas.");
  }
  return data as Session;
}

function uniqueId(base: string, taken: string[]): string {
  let name = base;
  for (let i = 2; taken.includes(name); i++) name = `${base}_${i}`;
  return name;
}

function fill(template: string, values: Record<string, string>): string {
  return template.replace(/\{(\w+)\}/g, (m, key: string) => values[key] ?? m);
}

function text(v: unknown): string {
  return typeof v === "string" ? v.split(/\s+/).filter(Boolean).join(" ") : "";
}

function texts(v: unknown): string[] {
  return Array.isArray(v) ? v.map(text).filter(Boolean) : [];
}

function escape(s: string): string {
  return s.replace(/[[\]()]/g, "\\$&");
}
