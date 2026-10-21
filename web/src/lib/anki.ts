// Exporta cards no formato Cloze do Anki (mesmo formato de `chunks anki`).

import { type Chunk, demos, pattern } from "./chunks";

export function ankiText(chunks: Chunk[]): string {
  const rows = ["#separator:tab", "#html:false", "#notetype:Cloze", "#tags column:3"];
  for (const c of chunks) {
    for (const p of demos(c)) rows.push(`${p.cloze}\t${p.pt} | ${pattern(c)}\tchunks::${c.category}`);
  }
  return rows.join("\n") + "\n";
}

export function downloadText(filename: string, text: string): void {
  const url = URL.createObjectURL(new Blob([text], { type: "text/plain;charset=utf-8" }));
  const link = Object.assign(document.createElement("a"), { href: url, download: filename });
  link.click();
  URL.revokeObjectURL(url);
}
