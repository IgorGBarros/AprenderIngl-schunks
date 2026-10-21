import { useMemo, useState } from "react";
import { type Question, type Session, SESSIONS, parseAnswer, speakable } from "../lib/interviews";
import { canSpeak, speak } from "../lib/speech";
import { load, save } from "../lib/storage";
import { NewJob } from "./NewJob";
import { SpeakButton } from "./SpeakButton";

type Practiced = Record<string, number>;

interface Props {
  /** Rota dentro da aba: [] lista, ["new"] nova vaga, [sessão, pergunta] prática. */
  path: string[];
  go: (path: string) => void;
}

/** Simulação de entrevista: pergunta → resposta em voz alta → resposta modelo. */
export function Interview({ path, go }: Props) {
  const [local, setLocal] = useState<Session[]>(() => load("chunks.sessions", []));
  const [selected, setSelected] = useState<string>(() => load("chunks.session", SESSIONS[0].id));
  const [stage, setStage] = useState<string>("all");
  const [practiced, setPracticed] = useState<Practiced>(() => load("chunks.interview", {}));
  const [confirmDelete, setConfirmDelete] = useState(false);

  const all = useMemo(() => [...SESSIONS, ...local], [local]);
  const [first, second] = path;
  const session = all.find((s) => s.id === (second ? first : selected)) ?? all[0];
  const isLocal = local.some((s) => s.id === session.id);

  const visible = useMemo(
    () => session.questions.filter((q) => stage === "all" || q.stage === stage),
    [session, stage],
  );
  const key = (q: Question) => `${session.id}/${q.id}`;
  const done = session.questions.filter((q) => practiced[key(q)]).length;

  const pick = (id: string) => {
    setSelected(id);
    save("chunks.session", id);
    setStage("all");
    setConfirmDelete(false);
  };

  const addSession = (s: Session) => {
    const next = [...local.filter((x) => x.id !== s.id), s];
    setLocal(next);
    save("chunks.sessions", next);
    pick(s.id);
    go("interview");
  };

  const removeSession = () => {
    const next = local.filter((s) => s.id !== session.id);
    setLocal(next);
    save("chunks.sessions", next);
    pick(SESSIONS[0].id);
  };

  if (first === "new") {
    return <NewJob takenIds={all.map((s) => s.id)} onCreated={addSession} onCancel={() => go("interview")} />;
  }

  const open = second ? session.questions.find((q) => q.id === second) : undefined;
  if (open) {
    // Navega dentro do filtro atual; se a pergunta não está nele, usa a sessão toda.
    const list = visible.includes(open) ? visible : session.questions;
    const i = list.indexOf(open);
    const openQ = (q: Question) => go(`interview/${session.id}/${q.id}`);
    return (
      <Practice
        key={key(open)}
        question={open}
        stageTitle={session.stages.find((s) => s.id === open.stage)?.title ?? ""}
        position={`${i + 1}/${list.length}`}
        onReveal={() => {
          const next = { ...practiced, [key(open)]: (practiced[key(open)] ?? 0) + 1 };
          setPracticed(next);
          save("chunks.interview", next);
        }}
        onPrev={i > 0 ? () => openQ(list[i - 1]) : undefined}
        onNext={i < list.length - 1 ? () => openQ(list[i + 1]) : undefined}
        onClose={() => go("interview")}
      />
    );
  }

  return (
    <>
      <header className="header">
        <h1>Entrevista</h1>
        <p className="subtitle">Responda em voz alta, depois compare com a resposta modelo.</p>
      </header>

      <div className="session-bar">
        <label htmlFor="session" className="visually-hidden">
          Sessão de entrevista
        </label>
        <select id="session" value={session.id} onChange={(e) => pick(e.target.value)}>
          {all.map((s) => (
            <option key={s.id} value={s.id}>
              {s.title}
              {s.company ? ` — ${s.company}` : ""}
            </option>
          ))}
        </select>
        <button className="secondary" onClick={() => go("interview/new")}>
          + Nova vaga
        </button>
      </div>

      <section className="card job">
        <p className="job-company">{session.company}</p>
        <h2 className="job-title">{session.title}</h2>
        <p className="pt">{session.summary}</p>
        <div className="meter" aria-label={`${done} de ${session.questions.length} praticadas`}>
          <div className="meter-fill" style={{ width: `${(done / session.questions.length) * 100}%` }} />
        </div>
        <p className="meter-label">
          {done} de {session.questions.length} perguntas praticadas
        </p>
        <button
          className="primary"
          onClick={() => visible[0] && go(`interview/${session.id}/${visible[0].id}`)}
        >
          {stage === "all" ? "Simular entrevista completa" : "Simular esta etapa"}
        </button>
        {isLocal && (
          <button
            className={confirmDelete ? "link danger armed" : "link danger"}
            onClick={() => (confirmDelete ? removeSession() : setConfirmDelete(true))}
          >
            {confirmDelete ? "Toque de novo para apagar esta sessão" : "Apagar esta sessão"}
          </button>
        )}
      </section>

      <div className="chips" role="tablist" aria-label="Etapas">
        {[{ id: "all", title: "Todas" }, ...session.stages].map((s) => (
          <button
            key={s.id}
            role="tab"
            aria-selected={stage === s.id}
            className={stage === s.id ? "chip active" : "chip"}
            onClick={() => setStage(s.id)}
          >
            {s.title}
          </button>
        ))}
      </div>

      {stage !== "all" && (
        <p className="stage-description">{session.stages.find((s) => s.id === stage)?.description}</p>
      )}

      <ul className="list question-list">
        {visible.map((q) => (
          <li key={q.id}>
            <button className="card question-row" onClick={() => go(`interview/${session.id}/${q.id}`)}>
              <span className={practiced[key(q)] ? "check done" : "check"} aria-hidden>
                {practiced[key(q)] ? "✓" : ""}
              </span>
              <span className="question-text">
                <span className="en">{q.en}</span>
                <span className="pt">{q.goal}</span>
              </span>
            </button>
          </li>
        ))}
      </ul>

      <section className="card help legend">
        <p>
          <mark className="fixed">Amarelo</mark> = chunk para memorizar.{" "}
          <span className="fill">Tracejado</span> = troque pelo seu fato real. Nunca diga algo que
          você não consegue sustentar com um exemplo.
        </p>
      </section>
    </>
  );
}

interface PracticeProps {
  question: Question;
  stageTitle: string;
  position: string;
  onReveal: () => void;
  onPrev?: () => void;
  onNext?: () => void;
  onClose: () => void;
}

function Practice({ question: q, stageTitle, position, onReveal, onPrev, onNext, onClose }: PracticeProps) {
  const [revealed, setRevealed] = useState(false);

  return (
    <>
      <header className="header detail-header">
        <button className="back" onClick={onClose}>
          ‹ Perguntas
        </button>
        <span className="badge">
          {stageTitle} · {position}
        </span>
      </header>

      <section className="card interviewer">
        <p className="label">O entrevistador pergunta</p>
        <div className="output-en">
          <p className="phrase">{q.en}</p>
          <SpeakButton text={q.en} />
        </div>
      </section>

      {!revealed ? (
        <section className="form">
          <p className="hint">
            Responda em voz alta, como se fosse a entrevista. Use a estrutura que você lembrar e só
            depois veja a resposta modelo.
          </p>
          <button
            className="primary"
            onClick={() => {
              setRevealed(true);
              onReveal();
            }}
          >
            Ver resposta modelo
          </button>
        </section>
      ) : (
        <>
          {q.goal && (
            <section className="goal">
              <h2>O que eles querem saber</h2>
              <p>{q.goal}</p>
            </section>
          )}

          <section className="card answer" aria-live="polite">
            <div className="answer-head">
              <h2>Resposta modelo</h2>
              {canSpeak && (
                <button className="link" onClick={() => speak(speakable(q.answer), 0.85)}>
                  🔊 Ouvir (shadowing)
                </button>
              )}
            </div>
            <p className="answer-text">
              {parseAnswer(q.answer).map((p, i) =>
                p.kind === "chunk" ? (
                  <mark key={i} className="fixed">
                    {p.text}
                  </mark>
                ) : p.kind === "fill" ? (
                  <span key={i} className="fill" title="Troque pelo seu fato real">
                    {p.text}
                  </span>
                ) : (
                  <span key={i}>{p.text}</span>
                ),
              )}
            </p>
          </section>

          {q.tips.length > 0 && (
            <section className="note tips">
              <h2>Dicas</h2>
              <ul>
                {q.tips.map((t) => (
                  <li key={t}>{t}</li>
                ))}
              </ul>
            </section>
          )}

          {q.follow_ups.length > 0 && (
            <section className="follow-ups">
              <h2>Pode vir em seguida</h2>
              <ul className="list">
                {q.follow_ups.map((f) => (
                  <li key={f} className="card follow-up">
                    <span>{f}</span>
                    <SpeakButton text={f} />
                  </li>
                ))}
              </ul>
            </section>
          )}
        </>
      )}

      <nav className="row pager" aria-label="Navegar entre perguntas">
        <button className="secondary" disabled={!onPrev} onClick={onPrev}>
          ‹ Anterior
        </button>
        <button className={revealed ? "primary" : "secondary"} disabled={!onNext} onClick={onNext}>
          Próxima ›
        </button>
      </nav>
    </>
  );
}
