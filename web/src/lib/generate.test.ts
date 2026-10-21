import { afterEach, describe, expect, it, vi } from "vitest";
import prompts from "../data/interview_prompts.json";
import { fixMarkup, generateSession, normalizeQuestions, parseSession, slugify } from "./generate";
import { OllamaError, listModels, normalizeHost } from "./ollama";

const JOB = "We are hiring a Data Engineer to build pipelines in Python and SQL. ".repeat(3);

/** Imita o /api/chat do Ollama (mesmas respostas do tests/fake_ollama.py). */
function fakeOllama() {
  const requests: { url: string; body: any }[] = [];
  const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
    const body = init?.body ? JSON.parse(init.body as string) : undefined;
    requests.push({ url, body });
    if (url.endsWith("/api/tags")) return Response.json({ models: [{ name: "fake:latest" }] });
    if (body.model !== "fake:latest") {
      return Response.json({ error: `model '${body.model}' not found` }, { status: 404 });
    }
    let content: object;
    if ("title" in body.format.properties) {
      content = { title: "Data Engineer", company: "Acme Corp", summary: "Vaga de dados." };
    } else {
      const stage = body.messages[1].content.split("STAGE: ")[1].split("\n")[0];
      content = {
        questions: [
          ...[1, 2, 3, 4, 5, 6].map((i) => ({
            question: `${stage} question ${i}?`,
            goal: "O que querem saber.",
            answer: `[[I've been working in]] data [[for]] ((number of years)). Answer ${i}.`,
            tips: ["Dica 1", "Dica 2", "Dica 3", "Dica extra"],
            follow_ups: ["Why?"],
          })),
          { question: "", goal: "", answer: "", tips: [], follow_ups: [] },
        ],
      };
    }
    return Response.json({ message: { role: "assistant", content: JSON.stringify(content) } });
  });
  vi.stubGlobal("fetch", fetchMock);
  return requests;
}

afterEach(() => vi.unstubAllGlobals());

describe("generateSession", () => {
  it("gera uma sessão completa igual ao Python", async () => {
    const requests = fakeOllama();
    const steps: string[] = [];
    const s = await generateSession(JOB, "", { host: "localhost:11434", model: "fake:latest" }, {
      perStage: 4,
      takenIds: ["acme_corp_data_engineer"],
      onProgress: (m) => steps.push(m),
    });
    expect(s.id).toBe("acme_corp_data_engineer_2");
    expect(s.title).toBe("Data Engineer");
    expect(s.stages.map((x) => x.id)).toEqual(prompts.stages.map((x) => x.id));
    expect(s.questions).toHaveLength(4 * 5 + 2);
    expect(new Set(s.questions.map((q) => q.id)).size).toBe(s.questions.length);
    expect(s.questions[0].tips).toEqual(["Dica 1", "Dica 2", "Dica 3"]);
    expect(steps).toHaveLength(1 + prompts.stages.length);

    expect(requests[0].url).toBe("http://localhost:11434/api/chat");
    expect(requests[1].body.format).toEqual(prompts.questions_schema);
    expect(requests[2].body.messages[1].content).toContain(prompts.no_profile);
    expect(requests[2].body.messages[1].content).toContain("Recrutador question 1?");
  });

  it("explica os erros", async () => {
    fakeOllama();
    await expect(generateSession(JOB, "", { host: DEFAULT, model: "llama3" })).rejects.toThrow(
      "ollama pull llama3",
    );
    await expect(generateSession("Dev", "", { host: DEFAULT, model: "x" })).rejects.toThrow("curto");
    expect(await listModels(DEFAULT)).toEqual(["fake:latest"]);

    vi.stubGlobal("fetch", vi.fn(async () => Promise.reject(new TypeError("Failed to fetch"))));
    await expect(listModels(DEFAULT)).rejects.toThrow(OllamaError);
    await expect(listModels(DEFAULT)).rejects.toThrow("OLLAMA_ORIGINS");
  });
});

const DEFAULT = "http://localhost:11434";

describe("helpers", () => {
  it("normaliza perguntas e marcação", () => {
    expect(normalizeQuestions({ questions: "nope" }, "screen")).toEqual([]);
    expect(fixMarkup("[[ok]] and ((fill))")).toBe("[[ok]] and ((fill))");
    expect(fixMarkup("[[broken and ((fill))")).toBe("broken and ((fill))");
    expect(slugify("Ação & Co — Sênior Dev")).toBe("acao_co_senior_dev");
    expect(normalizeHost("0.0.0.0:11434/")).toBe("http://0.0.0.0:11434");
  });

  it("valida o JSON importado", () => {
    expect(() => parseSession("{}")).toThrow("não parece");
    const ok = { id: "x", title: "X", company: "", summary: "", stages: [{ id: "a", title: "A", description: "" }], questions: [{ id: "q", stage: "a", en: "Q?", goal: "", answer: "A", tips: [], follow_ups: [] }] };
    expect(parseSession(JSON.stringify(ok)).id).toBe("x");
    expect(() => parseSession(JSON.stringify({ ...ok, questions: [{ ...ok.questions[0], stage: "b" }] }))).toThrow("inválidas");
  });
});
