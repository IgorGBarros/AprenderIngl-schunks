import { describe, expect, it } from "vitest";
import { ankiText } from "./anki";
import {
  BUILTIN,
  type Chunk,
  a,
  blanks,
  demos,
  core,
  nameFrom,
  normalizeAnswer,
  render,
  search,
  slotsOf,
} from "./chunks";
import { dueChunks, record } from "./srs";

const byName = (name: string) => BUILTIN.find((c) => c.name === name)!;

describe("render", () => {
  it.each(BUILTIN.map((c) => [c.name, c] as const))("%s gera o mesmo que o Python", (_, c) => {
    const phrases = demos(c);
    expect(phrases.map((p) => ({ en: p.en, pt: p.pt, cloze: p.cloze }))).toEqual(c.demos);
    for (const p of phrases) expect(p.parts.map((x) => x.text).join("")).toBe(p.en);
  });

  it("aceita chunks salvos no formato antigo (example)", () => {
    const old = { ...byName("could_i_get"), examples: undefined, example: { item: "tea" } } as unknown as Chunk;
    expect(demos(old).map((p) => p.en)).toEqual(["Could I get tea, please?"]);
  });

  it("dica mostra só o tamanho da parte fixa", () => {
    expect(blanks(render(byName("could_i_get"), { item: { en: "a glass of water" } }))).toBe(
      "_____ _ ___ a glass of water, ______?",
    );
  });

  it("usa as variáveis do usuário", () => {
    expect(render(byName("could_i_get"), { item: { en: "a cup of coffee" } }).en).toBe(
      "Could I get a cup of coffee, please?",
    );
  });

  it("traduz a variável quando há pt", () => {
    const p = render(byName("could_i_get"), { item: { en: "a coffee", pt: "um café" } });
    expect(p.pt).toBe("Pode me trazer um café, por favor?");
  });

  it("variável vazia usa o default sem deixar espaço sobrando", () => {
    const p = render(byName("keep_me_in_the_loop"), { about: { en: "" } });
    expect(p.en).toBe("Please keep me in the loop.");
    expect(p.parts).toEqual([
      { text: "Please keep me in the loop", fixed: true },
      { text: ".", fixed: false },
    ]);
  });

  it("separa parte fixa e variável", () => {
    expect(render(byName("could_i_get"), { item: { en: "water" } }).parts).toEqual([
      { text: "Could I get", fixed: true },
      { text: " water", fixed: false },
      { text: ", please", fixed: true },
      { text: "?", fixed: false },
    ]);
  });
});

describe("helpers", () => {
  it("core e slots", () => {
    expect(core(byName("let_me_loop_in"))).toBe("Let me loop in ... to help us with ....");
    expect(slotsOf("[[Let's sync up on]] {topic} {when} {topic}.")).toEqual(["topic", "when"]);
  });

  it("artigo", () => {
    expect([a("apple"), a("hour"), a("university"), a("car")]).toEqual([
      "an apple",
      "an hour",
      "a university",
      "a car",
    ]);
  });

  it("busca ignora acentos e acha pelo exemplo", () => {
    expect(search(BUILTIN, "glass of water").map((c) => c.name)).toContain("could_i_get");
    expect(search(BUILTIN, "alergia").map((c) => c.name)).toContain("im_allergic_to");
    expect(search(BUILTIN, "cardapio").map((c) => c.name)).toContain("could_i_get");
  });

  it("corrige ignorando maiúsculas e pontuação", () => {
    expect(normalizeAnswer("could i get a glass of water please")).toBe(
      normalizeAnswer("Could I get a glass of water, please?"),
    );
    expect(normalizeAnswer("I’m in")).toBe("i'm in");
  });

  it("gera nome de função", () => {
    expect(nameFrom("[[I'm blocked by]] {x}.")).toBe("im_blocked_by");
    expect(nameFrom("{x}")).toBe("my_chunk");
  });
});

describe("srs", () => {
  it("sobe e desce de caixa", () => {
    let p = record({}, "time_to", true, "2026-01-01");
    expect(p.time_to).toEqual({ box: 2, due: "2026-01-03" });
    p = record(p, "time_to", false, "2026-01-03");
    expect(p.time_to).toEqual({ box: 1, due: "2026-01-04" });
  });

  it("não traz o que vence no futuro", () => {
    const chunks: Chunk[] = [byName("time_to"), byName("time_for")];
    const due = dueChunks(chunks, { time_to: { box: 3, due: "2099-01-01" } }, "2026-01-01");
    expect(due.map((c) => c.name)).toEqual(["time_for"]);
  });
});

describe("anki", () => {
  it("gera arquivo Cloze", () => {
    const lines = ankiText([byName("could_i_get")]).trim().split("\n");
    expect(lines[2]).toBe("#notetype:Cloze");
    expect(lines[4]).toBe(
      "{{c1::Could I get}} a glass of water{{c1::, please}}?\tPode me trazer um copo de água, por favor? | could_i_get(item)\tchunks::survival",
    );
  });
});
