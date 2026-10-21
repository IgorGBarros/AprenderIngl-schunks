import type { Phrase } from "../lib/chunks";

/** Frase em inglês com a parte fixa do chunk destacada. */
export function PhraseText({ phrase }: { phrase: Phrase }) {
  return (
    <>
      {phrase.parts.map((p, i) =>
        p.fixed ? (
          <mark key={i} className="fixed">
            {p.text}
          </mark>
        ) : (
          <span key={i}>{p.text}</span>
        ),
      )}
    </>
  );
}
