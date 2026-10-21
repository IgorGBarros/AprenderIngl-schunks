import { useMemo, useRef, useState } from "react";
import {
  CATEGORY_LABELS,
  type Chunk,
  categoriesOf,
  core,
  exampleValues,
  normalizeAnswer,
  render,
} from "../lib/chunks";
import { type Progress, dueChunks, record, stats } from "../lib/srs";
import { PhraseText } from "./PhraseText";
import { SpeakButton } from "./SpeakButton";

interface Props {
  chunks: Chunk[];
  progress: Progress;
  onProgress: (p: Progress) => void;
}

type Session = { queue: Chunk[]; index: number; score: number };

/** Treino do dia: mostra o português, o usuário escreve em inglês. */
export function Quiz({ chunks, progress, onProgress }: Props) {
  const [category, setCategory] = useState("all");
  const [size, setSize] = useState(10);
  const [session, setSession] = useState<Session | null>(null);

  const pool = useMemo(
    () => chunks.filter((c) => category === "all" || c.category === category),
    [chunks, category],
  );
  const s = stats(pool, progress);
  const categories = categoriesOf(chunks);

  if (session && session.index < session.queue.length) {
    return (
      <Question
        key={session.index}
        chunk={session.queue[session.index]}
        position={`${session.index + 1}/${session.queue.length}`}
        onAnswer={(correct) => {
          onProgress(record(progress, session.queue[session.index].name, correct));
          setSession({ ...session, index: session.index + 1, score: session.score + +correct });
        }}
        onQuit={() => setSession({ ...session, index: session.queue.length })}
      />
    );
  }

  return (
    <>
      <header className="header">
        <h1>Treinar</h1>
        <p className="subtitle">Repetição espaçada: o que você erra volta amanhã.</p>
      </header>

      {session && (
        <section className="card result">
          <p className="big">
            {session.score}/{session.index}
          </p>
          <p>{session.score === session.index ? "Perfeito! 🎉" : "Os que você errou voltam amanhã."}</p>
        </section>
      )}

      <section className="stats">
        <div className="stat">
          <span className="stat-value">{s.due}</span>
          <span className="stat-label">para hoje</span>
        </div>
        <div className="stat">
          <span className="stat-value">{s.learned}</span>
          <span className="stat-label">aprendidos</span>
        </div>
        <div className="stat">
          <span className="stat-value">{s.total}</span>
          <span className="stat-label">no total</span>
        </div>
      </section>

      <section className="form">
        <label htmlFor="quiz-cat">Categoria</label>
        <select id="quiz-cat" value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="all">Todas</option>
          {categories.map((c) => (
            <option key={c} value={c}>
              {CATEGORY_LABELS[c] ?? c}
            </option>
          ))}
        </select>

        <label htmlFor="quiz-size">Quantidade</label>
        <select id="quiz-size" value={size} onChange={(e) => setSize(Number(e.target.value))}>
          {[5, 10, 20].map((n) => (
            <option key={n} value={n}>
              {n} chunks
            </option>
          ))}
        </select>

        <button
          className="primary"
          disabled={s.due === 0}
          onClick={() =>
            setSession({ queue: dueChunks(pool, progress).slice(0, size), index: 0, score: 0 })
          }
        >
          {s.due === 0 ? "Nada para hoje ✓" : session ? "Treinar de novo" : "Começar"}
        </button>
      </section>
    </>
  );
}

interface QuestionProps {
  chunk: Chunk;
  position: string;
  onAnswer: (correct: boolean) => void;
  onQuit: () => void;
}

function Question({ chunk, position, onAnswer, onQuit }: QuestionProps) {
  const values = exampleValues(chunk);
  const phrase = render(chunk, values);
  const [answer, setAnswer] = useState("");
  const [checked, setChecked] = useState<boolean | null>(null);
  const nextRef = useRef<HTMLButtonElement>(null);

  const check = () => {
    setChecked(normalizeAnswer(answer) === normalizeAnswer(phrase.en));
    setTimeout(() => nextRef.current?.focus(), 0);
  };

  return (
    <>
      <header className="header detail-header">
        <button className="back" onClick={onQuit}>
          ✕ Sair
        </button>
        <span className="badge">{position}</span>
      </header>

      <section className="card question">
        <p className="label">Como se diz em inglês?</p>
        <p className="phrase">{phrase.pt}</p>
        {chunk.slots.length > 0 && (
          <ul className="hints">
            {chunk.slots.map((slot) => (
              <li key={slot}>
                <code>{slot}</code> = “{values[slot].en}”
              </li>
            ))}
          </ul>
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
          <div className="row">
            <button type="button" className="secondary" onClick={() => setChecked(false)}>
              Não sei
            </button>
            <button type="submit" className="primary" disabled={!answer.trim()}>
              Verificar
            </button>
          </div>
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
              Próximo
            </button>
          </div>
        </section>
      )}
    </>
  );
}
