import { useMemo, useState } from "react";
import { CATEGORY_LABELS, type Chunk, categoriesOf, demos } from "../lib/chunks";
import { type Progress, dueChunks, record, stats } from "../lib/srs";
import { QuestionCard } from "./QuestionCard";

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
  // Cada revisão sorteia um dos exemplos do chunk.
  const [phrase] = useState(() => {
    const all = demos(chunk);
    return all[Math.floor(Math.random() * all.length)];
  });

  return (
    <>
      <header className="header detail-header">
        <button className="back" onClick={onQuit}>
          ✕ Sair
        </button>
        <span className="badge">{position}</span>
      </header>
      <QuestionCard chunk={chunk} phrase={phrase} onAnswer={onAnswer} />
    </>
  );
}
