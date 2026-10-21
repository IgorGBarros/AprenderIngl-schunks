import { useState } from "react";
import { ankiText, downloadText } from "../lib/anki";
import { type Chunk, exampleValues, nameFrom, render, slotsOf } from "../lib/chunks";
import { PhraseText } from "./PhraseText";

interface Props {
  all: Chunk[];
  mine: Chunk[];
  onChange: (mine: Chunk[]) => void;
  onOpen: (c: Chunk) => void;
  onResetProgress: () => void;
}

const EMPTY = { template: "", pt: "", example: {} as Record<string, string>, note: "" };

/** Criar os próprios chunks (como em chunks/library/my_chunks.py). */
export function MyChunks({ all, mine, onChange, onOpen, onResetProgress }: Props) {
  const [draft, setDraft] = useState(EMPTY);
  const slots = slotsOf(draft.template);
  const ptSlots = slotsOf(draft.pt);

  const candidate: Chunk = {
    name: uniqueName(nameFrom(draft.template), all),
    template: draft.template,
    pt: draft.pt,
    category: "mine",
    slots,
    example: Object.fromEntries(slots.map((s) => [s, draft.example[s] ?? ""])),
    defaults: {},
    note: draft.note.trim(),
  };

  const errors: string[] = [];
  if (!/\[\[.+?\]\]/.test(draft.template)) errors.push("Marque a parte fixa com [[ ]].");
  if (!draft.pt.trim()) errors.push("Escreva a tradução.");
  const missing = slots.filter((s) => !ptSlots.includes(s));
  if (draft.pt.trim() && missing.length) errors.push(`Use na tradução: ${missing.map((s) => `{${s}}`).join(", ")}`);
  const extra = ptSlots.filter((s) => !slots.includes(s));
  if (extra.length) errors.push(`A tradução usa variáveis que não existem: ${extra.join(", ")}`);
  if (slots.some((s) => !draft.example[s]?.trim())) errors.push("Preencha um exemplo para cada variável.");

  const preview = draft.template ? render(candidate, exampleValues(candidate)) : null;

  return (
    <>
      <header className="header">
        <h1>Meus chunks</h1>
        <p className="subtitle">Ouviu uma frase boa? Transforme em função.</p>
      </header>

      <section className="card help">
        <p>
          <code>[[...]]</code> = parte fixa (o que você memoriza)
          <br />
          <code>{"{nome}"}</code> = variável (o argumento)
        </p>
        <p className="example-code">
          [[I think we should consider]] {"{option}"}.
        </p>
      </section>

      <form
        className="form"
        onSubmit={(e) => {
          e.preventDefault();
          if (errors.length) return;
          onChange([...mine, candidate]);
          setDraft(EMPTY);
        }}
      >
        <label htmlFor="tpl">Frase em inglês</label>
        <input
          id="tpl"
          value={draft.template}
          onChange={(e) => setDraft({ ...draft, template: e.target.value })}
          placeholder="[[I think we should consider]] {option}."
          autoCapitalize="off"
          autoCorrect="off"
          spellCheck={false}
        />

        <label htmlFor="pt">Tradução</label>
        <input
          id="pt"
          value={draft.pt}
          onChange={(e) => setDraft({ ...draft, pt: e.target.value })}
          placeholder="Acho que devíamos considerar {option}."
        />

        {slots.map((slot) => (
          <div key={slot}>
            <label htmlFor={`ex-${slot}`}>
              Exemplo de <code>{slot}</code>
            </label>
            <input
              id={`ex-${slot}`}
              value={draft.example[slot] ?? ""}
              onChange={(e) =>
                setDraft({ ...draft, example: { ...draft.example, [slot]: e.target.value } })
              }
              placeholder="using a cache"
              autoCapitalize="off"
            />
          </div>
        ))}

        <label htmlFor="note">Nota (opcional)</label>
        <input
          id="note"
          value={draft.note}
          onChange={(e) => setDraft({ ...draft, note: e.target.value })}
          placeholder="Quando usar essa frase"
        />

        {preview && (
          <div className="card preview">
            <code className="fn">{candidate.name}({slots.join(", ")})</code>
            <p className="phrase">
              <PhraseText phrase={preview} />
            </p>
            <p className="pt">{preview.pt}</p>
          </div>
        )}

        {draft.template && errors.length > 0 && (
          <ul className="errors">
            {errors.map((e) => (
              <li key={e}>{e}</li>
            ))}
          </ul>
        )}

        <button className="primary" type="submit" disabled={errors.length > 0}>
          Salvar chunk
        </button>
      </form>

      {mine.length > 0 && (
        <section>
          <h2 className="section-title">Salvos ({mine.length})</h2>
          <ul className="list">
            {mine.map((c) => (
              <li key={c.name} className="card mine-row">
                <button className="mine-open" onClick={() => onOpen(c)}>
                  <code className="fn">{c.name}</code>
                  <span className="en">
                    <PhraseText phrase={render(c, exampleValues(c))} />
                  </span>
                </button>
                <button
                  className="icon-btn danger"
                  aria-label={`Apagar ${c.name}`}
                  onClick={() => {
                    if (confirm(`Apagar "${c.name}"?`)) onChange(mine.filter((m) => m !== c));
                  }}
                >
                  ✕
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section className="form">
        <h2 className="section-title">Exportar para o Anki</h2>
        <p className="hint">Arquivo para o tipo de nota Cloze. No Anki: Arquivo › Importar.</p>
        <button className="secondary" onClick={() => downloadText("chunks-anki.txt", ankiText(all))}>
          Baixar todos ({all.length})
        </button>
        {mine.length > 0 && (
          <button className="secondary" onClick={() => downloadText("meus-chunks-anki.txt", ankiText(mine))}>
            Baixar só os meus ({mine.length})
          </button>
        )}
        <button
          className="link danger"
          onClick={() => {
            if (confirm("Zerar todo o progresso do treino?")) onResetProgress();
          }}
        >
          Zerar progresso do treino
        </button>
      </section>
    </>
  );
}

function uniqueName(base: string, all: Chunk[]): string {
  const taken = new Set(all.map((c) => c.name));
  let name = base;
  for (let i = 2; taken.has(name); i++) name = `${base}_${i}`;
  return name;
}
