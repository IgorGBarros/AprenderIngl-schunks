import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

/** Reconhecimento de voz falso: o teste dispara os eventos à mão. */
class FakeRecognition {
  static last: FakeRecognition;
  lang = "";
  interimResults = false;
  continuous = true;
  maxAlternatives = 0;
  onresult: ((e: unknown) => void) | null = null;
  onerror: ((e: { error: string }) => void) | null = null;
  onend: (() => void) | null = null;
  started = false;
  constructor() {
    FakeRecognition.last = this;
  }
  start() {
    this.started = true;
  }
  stop() {
    this.onend?.();
  }
  abort() {}
  say(...chunks: [string, boolean][]) {
    this.onresult?.({ resultIndex: 0, results: chunks.map(([t, isFinal]) => ({ isFinal, 0: { transcript: t } })) });
  }
}

beforeEach(() => {
  vi.resetModules();
  vi.stubGlobal("window", { webkitSpeechRecognition: FakeRecognition, isSecureContext: true });
});
afterEach(() => vi.unstubAllGlobals());

describe("listen", () => {
  it("ouve no idioma pedido e devolve o texto enquanto você fala", async () => {
    const { listen, canListen } = await import("./listen");
    expect(canListen).toBe(true);
    const texts: string[] = [];
    let ended = false;
    const stop = listen("de", { onText: (t) => texts.push(t), onError: () => {}, onEnd: () => (ended = true) });
    const rec = FakeRecognition.last;
    expect(rec.lang).toBe("de-DE");
    expect(rec.interimResults).toBe(true);
    expect(rec.started).toBe(true);
    rec.say(["Könnte ich", false]);
    rec.say(["Könnte ich bitte", true], [" ein Glas", false]);
    expect(texts).toEqual(["Könnte ich", "Könnte ich bitte ein Glas"]);
    stop();
    expect(ended).toBe(true);
  });

  it("explica os erros em português e ignora o 'aborted'", async () => {
    const { listen } = await import("./listen");
    const errors: string[] = [];
    listen("en", { onText: () => {}, onError: (m) => errors.push(m), onEnd: () => {} });
    FakeRecognition.last.onerror?.({ error: "not-allowed" });
    FakeRecognition.last.onerror?.({ error: "aborted" });
    FakeRecognition.last.onerror?.({ error: "no-speech" });
    expect(errors).toEqual([
      "O microfone foi bloqueado. Permita o acesso ao microfone nas configurações do navegador.",
      "Não ouvi nada. Toque no microfone e fale perto do celular.",
    ]);
  });

  it("sem HTTPS (ou sem suporte) o microfone fica escondido", async () => {
    vi.stubGlobal("window", { webkitSpeechRecognition: FakeRecognition, isSecureContext: false });
    const { canListen } = await import("./listen");
    expect(canListen).toBe(false);
  });
});
