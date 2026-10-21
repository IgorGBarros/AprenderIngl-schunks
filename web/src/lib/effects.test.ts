import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

/** Todos os .tsx de src/, recursivamente. */
function sources(dir: string): string[] {
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? sources(join(dir, e.name)) : e.name.endsWith(".tsx") ? [join(dir, e.name)] : [],
  );
}

describe("useEffect", () => {
  // `useEffect(() => algo())` devolve o resultado de algo(); se não for uma
  // função, o React quebra ("destroy is not a function"). Use corpo em bloco.
  it("sempre usa corpo em bloco", () => {
    const offenders = sources(join(__dirname, ".."))
      .flatMap((f) => readFileSync(f, "utf8").split("\n").map((line, i) => ({ f, i, line })))
      .filter(({ line }) => /useEffect\(\s*\(\)\s*=>\s*[^{\s]/.test(line))
      .map(({ f, i }) => `${f}:${i + 1}`);
    expect(offenders).toEqual([]);
  });
});
