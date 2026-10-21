import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

/** Imita a Web Speech API: guarda a fila e deixa o teste "tocar" cada fala. */
class FakeUtterance {
  rate = 1;
  lang = "";
  voice: unknown = null;
  onstart: (() => void) | null = null;
  onend: (() => void) | null = null;
  onerror: (() => void) | null = null;
  constructor(public text: string) {}
}

let queue: FakeUtterance[] = [];

beforeEach(() => {
  queue = [];
  vi.resetModules();
  vi.stubGlobal("SpeechSynthesisUtterance", FakeUtterance);
  vi.stubGlobal("speechSynthesis", {
    speak: (u: FakeUtterance) => queue.push(u),
    cancel: () => (queue = []),
    getVoices: () => [],
  });
  vi.stubGlobal("window", { speechSynthesis: {} });
});

afterEach(() => vi.unstubAllGlobals());

describe("speech", () => {
  it("o destaque conta as palavras igual à voz, em todas as frases", async () => {
    const { tokenize, wordsOf } = await import("./speech");
    const { BUILTIN, demos } = await import("./chunks");
    for (const c of BUILTIN) {
      for (const p of demos(c)) {
        let n = 0;
        const highlighted: string[] = [];
        for (const part of p.parts) {
          for (const t of tokenize(part.text, n)) if (t.word !== null) highlighted.push(t.text);
          n = highlighted.length;
        }
        expect(highlighted.map((w) => w.replace(/^[^\w']+|[^\w'%]+$/g, ""))).toEqual(wordsOf(p.en));
      }
    }
  });

  it("lê na velocidade escolhida (0.75x por padrão)", async () => {
    const s = await import("./speech");
    s.speak("Could I get a coffee?");
    expect(queue[0].rate).toBe(0.75);
    s.setRate(0.5);
    s.speak("Hi");
    expect(queue[0].rate).toBe(0.5);
  });

  it("palavra por palavra: uma fala por palavra, sem pontuação", async () => {
    const s = await import("./speech");
    const seen: number[] = [];
    s.speakWords("Could I get a coffee, please?", (i) => seen.push(i));
    expect(queue.map((u) => u.text)).toEqual(["Could", "I", "get", "a", "coffee", "please"]);
    const words = [...queue];
    words.forEach((u) => u.onstart?.());
    words.at(-1)?.onend?.();
    expect(seen).toEqual([0, 1, 2, 3, 4, 5, -1]);
  });

  it("outra leitura avisa o botão anterior e ignora avisos atrasados", async () => {
    const s = await import("./speech");
    const first: number[] = [];
    s.speakWords("one two", (i) => first.push(i));
    const old = [...queue];
    old[0].onstart?.();
    s.speak("other"); // interrompe
    expect(first).toEqual([0, -1]);
    old[1].onstart?.(); // aviso atrasado da leitura cancelada
    old[1].onerror?.();
    expect(first).toEqual([0, -1]);
  });
});
