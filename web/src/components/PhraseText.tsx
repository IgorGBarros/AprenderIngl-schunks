import type { Phrase } from "../lib/chunks";
import { tokenize } from "../lib/speech";

interface Props {
  phrase: Phrase;
  /** Palavra que está tocando no "palavra por palavra" (índice), para destacar. */
  activeWord?: number;
}

/** Frase em inglês com a parte fixa do chunk destacada. */
export function PhraseText({ phrase, activeWord = -1 }: Props) {
  let count = 0;
  return (
    <>
      {phrase.parts.map((p, i) => {
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
