// Exporta cards no formato Cloze do Anki (mesmo formato de `chunks anki`).

import { type Chunk, type Lang, demos, langText, pattern } from "./chunks";

/** Um card por exemplo e por idioma (mesmo formato de `chunks anki --idioma`). */
export function ankiText(chunks: Chunk[], langs: Lang[] = ["en"]): string {
  const rows = ["#separator:tab", "#html:false", "#notetype:Cloze", "#tags column:3"];
  for (const c of chunks) {
    for (const lang of langs) {
      for (const p of demos(c)) {
        const cloze = langText(p, lang)?.cloze;
        if (cloze) rows.push(`${cloze}\t${p.pt} | ${pattern(c)}\tchunks::${c.category} chunks::${lang}`);
      }
    }
  }
  return rows.join("\n") + "\n";
}

export function downloadText(filename: string, text: string): void {
  const url = URL.createObjectURL(new Blob([text], { type: "text/plain;charset=utf-8" }));
  const link = Object.assign(document.createElement("a"), { href: url, download: filename });
  link.click();
  URL.revokeObjectURL(url);
}
