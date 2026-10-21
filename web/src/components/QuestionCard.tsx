import { useRef, useState } from "react";
import { type Chunk, type Phrase, blanks, core, normalizeAnswer } from "../lib/chunks";
import { PhraseText } from "./PhraseText";
import { SpeakButton } from "./SpeakButton";

interface Props {
  chunk: Chunk;
  phrase: Phrase;
  onAnswer: (correct: boolean) => void;
  nextLabel?: string;
}

/** Uma pergunta: mostra o português, o usuário escreve em inglês e confere. */
export function QuestionCard({ chunk, phrase, onAnswer, nextLabel = "Próximo" }: Props) {
  const [answer, setAnswer] = useState("");
  const [checked, setChecked] = useState<boolean | null>(null);
  const [hint, setHint] = useState(false);
  const nextRef = useRef<HTMLButtonElement>(null);

  const check = () => {
    setChecked(normalizeAnswer(answer) === normalizeAnswer(phrase.en));
    setTimeout(() => nextRef.current?.focus(), 0);
  };

  return (
    <>
      <section className="card question">
        <p className="label">Como se diz em inglês?</p>
        <p className="phrase">{phrase.pt}</p>
        {hint && checked === null && (
          <p className="hint-line" aria-live="polite">
            <code>{blanks(phrase)}</code>
          </p>
        )}
      </section>

      <form
        className="form"
        onSubmit={(e) => {
          e.preventDefault();
          if (checked === null) check();
        }}
      >
        <textarea
          rows={3}
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Escreva a frase em inglês…"
          readOnly={checked !== null}
          autoCapitalize="sentences"
          autoCorrect="off"
          spellCheck={false}
          autoFocus
          aria-label="Sua resposta"
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              if (checked === null) check();
            }
          }}
        />
        {checked === null && (
          <>
            <div className="row">
              <button type="button" className="secondary" onClick={() => setChecked(false)}>
                Não sei
              </button>
              <button type="submit" className="primary" disabled={!answer.trim()}>
                Verificar
              </button>
            </div>
            {!hint && (
              <button type="button" className="link" onClick={() => setHint(true)}>
                Mostrar dica
              </button>
            )}
          </>
        )}
      </form>

      {checked !== null && (
        <section className={checked ? "card feedback ok" : "card feedback wrong"} aria-live="polite">
          <p className="verdict">{checked ? "✔ Correto!" : "✘ Resposta:"}</p>
          <div className="output-en">
            <p className="phrase">
              <PhraseText phrase={phrase} />
            </p>
            <SpeakButton text={phrase.en} />
          </div>
          <p className="pt">
            Chunk: <strong>{core(chunk)}</strong>
          </p>
          <div className="row">
            {!checked && answer.trim() && (
              <button className="secondary" onClick={() => onAnswer(true)}>
                Eu acertei
              </button>
            )}
            <button ref={nextRef} className="primary" onClick={() => onAnswer(checked)}>
              {nextLabel}
            </button>
          </div>
        </section>
      )}
    </>
  );
}
