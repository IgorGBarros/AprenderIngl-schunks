import type { LangText } from "../lib/chunks";
import { tokenize } from "../lib/speech";

interface Props {
  /** A frase num idioma (inglês ou alemão), com os pedaços fixos e variáveis. */
  text: Pick<LangText, "parts">;
  /** Palavra que está tocando no "palavra por palavra" (índice), para destacar. */
  activeWord?: number;
}

/** Frase com a parte fixa do chunk destacada. */
export function PhraseText({ text, activeWord = -1 }: Props) {
  let count = 0;
  return (
    <>
      {text.parts.map((p, i) => {
        const tokens = tokenize(p.text, count);
        count += tokens.filter((t) => t.word !== null).length;
        const content =
          activeWord < 0
            ? p.text
            : tokens.map((t, j) =>
                t.word === activeWord ? (
                  <span key={j} className="speaking">
                    {t.text}
                  </span>
                ) : (
                  t.text
                ),
              );
        return p.fixed ? (
          <mark key={i} className="fixed">
            {content}
          </mark>
        ) : (
          <span key={i}>{content}</span>
        );
      })}
    </>
  );
}
