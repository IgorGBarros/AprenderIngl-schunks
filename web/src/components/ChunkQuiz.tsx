import { useState } from "react";
import type { Chunk, Phrase } from "../lib/chunks";
import { Modal } from "./Modal";
import { QuestionCard } from "./QuestionCard";

interface Props {
  chunk: Chunk;
  phrases: Phrase[];
  onDone: (perfect: boolean) => void;
}

type State = { order: Phrase[]; index: number; score: number } | null;

/** Quiz do chunk: abre num modal que cobre a página, para os exemplos não ficarem à vista. */
export function ChunkQuiz({ chunk, phrases, onDone }: Props) {
  const [state, setState] = useState<State>(null);

  const start = () =>
    setState({ order: [...phrases].sort(() => Math.random() - 0.5), index: 0, score: 0 });

  const finished = state && state.index >= state.order.length;

  return (
    <section className="chunk-quiz" aria-labelledby="quiz-title">
      <h2 id="quiz-title">Quiz deste chunk</h2>
      <div className="card quiz-intro">
        <p>
          Você vai ver {phrases.length === 1 ? "a frase" : `as ${phrases.length} frases`} em
          português e escrever em inglês. Os exemplos ficam escondidos durante o quiz: leia em voz
          alta antes de começar.
        </p>
        <button className="primary" onClick={start}>
          Começar quiz
        </button>
      </div>

      {state && (
        <Modal title="Quiz deste chunk" onClose={() => setState(null)}>
          {!finished ? (
            <>
              <p className="quiz-progress">
                Pergunta {state.index + 1} de {state.order.length}
              </p>
              <QuestionCard
                key={state.index}
                chunk={chunk}
                phrase={state.order[state.index]}
                nextLabel={state.index + 1 < state.order.length ? "Próxima" : "Ver resultado"}
                onAnswer={(correct) => {
                  const next = { ...state, index: state.index + 1, score: state.score + +correct };
                  setState(next);
                  if (next.index >= next.order.length) onDone(next.score === next.order.length);
                }}
              />
            </>
          ) : (
            <div className="card result">
              <p className="big">
                {state.score}/{state.order.length}
              </p>
              <p>
                {state.score === state.order.length
                  ? "Perfeito! Este chunk volta para revisão daqui a alguns dias. 🎉"
                  : "Releia os exemplos em voz alta e tente de novo."}
              </p>
              <div className="row">
                <button className="secondary" onClick={start}>
                  Refazer
                </button>
                <button className="primary" onClick={() => setState(null)}>
                  Ver os exemplos
                </button>
              </div>
            </div>
          )}
        </Modal>
      )}
    </section>
  );
}
