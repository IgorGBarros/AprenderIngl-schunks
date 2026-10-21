import { describe, expect, it } from "vitest";
import { SESSIONS, chunksIn, parseAnswer, speakable } from "./interviews";

describe("interviews", () => {
  it("separa chunks e trechos para preencher", () => {
    expect(parseAnswer("[[I currently work as]] a Data Analyst ((at X)).")).toEqual([
      { text: "I currently work as", kind: "chunk" },
      { text: " a Data Analyst ", kind: "text" },
      { text: "at X", kind: "fill" },
      { text: ".", kind: "text" },
    ]);
  });

  it("texto falado ignora o que falta preencher", () => {
    expect(speakable("[[So I could start]] ((date)).")).toBe("So I could start.");
    expect(chunksIn("[[A]] b [[C]]")).toEqual(["A", "C"]);
  });

  it("toda pergunta pertence a uma etapa da sessão", () => {
    for (const s of SESSIONS) {
      const stages = new Set(s.stages.map((x) => x.id));
      for (const q of s.questions) expect(stages.has(q.stage)).toBe(true);
    }
  });
});
