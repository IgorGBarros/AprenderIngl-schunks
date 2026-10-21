import { useEffect, useState } from "react";
import { ankiText, downloadText } from "../lib/anki";
import {
  type Chunk,
  type ExampleValue,
  demos,
  exampleValues,
  langText,
  nameFrom,
  render,
  slotsOf,
} from "../lib/chunks";
import { useLangs } from "../lib/langs";
import { PhraseText } from "./PhraseText";

interface Props {
  all: Chunk[];
  mine: Chunk[];
  onChange: (mine: Chunk[]) => void;
  onOpen: (c: Chunk) => void;
  onResetProgress: () => void;
}

type DraftExample = Record<string, { en: string; pt: string; de: string }>;

const MAX_EXAMPLES = 10;
const EMPTY = { template: "", pt: "", de: "", examples: [{}] as DraftExample[], note: "" };

/** Criar os próprios chunks (como em chunks/library/my_chunks.py). */
export function MyChunks({ all, mine, onChange, onOpen, onResetProgress }: Props) {
  const [draft, setDraft] = useState(EMPTY);
  const [copied, setCopied] = useState(false);
  const langs = useLangs();
  const slots = slotsOf(draft.template);
  const ptSlots = slotsOf(draft.pt);
  const deSlots = slotsOf(draft.de);
  const withDe = draft.de.trim() !== "";

  const candidate: Chunk = {
    name: uniqueName(nameFrom(draft.template), all),
    template: draft.template,
    pt: draft.pt,
    category: "mine",
    slots,
    // Exemplos completos viram ["inglês", "português", "alemão"]; o que faltar repete o inglês.
    examples: draft.examples
      .filter((ex) => slots.every((s) => ex[s]?.en.trim()))
      .map((ex) =>
        Object.fromEntries(
          slots.map((s): [string, ExampleValue] => {
            const en = ex[s].en.trim();
            const pt = ex[s].pt.trim() || en;
            const de = ex[s].de.trim();
            return [s, withDe && de ? [en, pt, de] : pt !== en ? [en, pt] : en];
          }),
        ),
      ),
    defaults: {},
    note: draft.note.trim(),
    de: withDe ? draft.de.trim() : undefined,
  };

  const errors: string[] = [];
  if (!/\[\[.+?\]\]/.test(draft.template)) errors.push("Marque a parte fixa com [[ ]].");
  if (!draft.pt.trim()) errors.push("Escreva a tradução.");
  const missing = slots.filter((s) => !ptSlots.includes(s));
  if (draft.pt.trim() && missing.length) errors.push(`Use na tradução: ${missing.map((s) => `{${s}}`).join(", ")}`);
  const extra = ptSlots.filter((s) => !slots.includes(s));
  if (extra.length) errors.push(`A tradução usa variáveis que não existem: ${extra.join(", ")}`);
  if (withDe && !/\[\[.+?\]\]/.test(draft.de)) errors.push("Marque a parte fixa do alemão com [[ ]].");
  if (withDe && (deSlots.length !== slots.length || deSlots.some((s) => !slots.includes(s)))) {
    errors.push(`O alemão precisa das mesmas variáveis do inglês: ${slots.map((s) => `{${s}}`).join(", ")}`);
  }
  if (slots.length && candidate.examples.length === 0) errors.push("Preencha pelo menos um exemplo completo.");
  const partial = draft.examples.some(
    (ex) => slots.some((s) => ex[s]?.en.trim()) && !slots.every((s) => ex[s]?.en.trim()),
  );
  if (partial) errors.push("Complete (ou apague) os exemplos pela metade.");

  const setSlot = (i: number, slot: string, field: "en" | "pt" | "de", value: string) =>
    setDraft({
      ...draft,
      examples: draft.examples.map((ex, j) =>
        j === i ? { ...ex, [slot]: { ...(ex[slot] ?? { en: "", pt: "", de: "" }), [field]: value } } : ex,
      ),
    });

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

        <label htmlFor="de">
          Frase em alemão <span className="optional">opcional</span>
        </label>
        <input
          id="de"
          value={draft.de}
          onChange={(e) => setDraft({ ...draft, de: e.target.value })}
          placeholder="[[Ich finde, wir sollten]] {option} [[in Betracht ziehen]]."
          autoCapitalize="off"
          autoCorrect="off"
          spellCheck={false}
          lang="de"
        />

        {slots.length > 0 &&
          draft.examples.map((ex, i) => (
            <fieldset key={i} className="example-set">
              <legend>Exemplo {i + 1}</legend>
              {slots.map((slot) => (
                <div key={slot} className="example-slot">
                  <label htmlFor={`ex-${i}-${slot}`}>
                    <code>{slot}</code>
                  </label>
                  <input
                    id={`ex-${i}-${slot}`}
                    value={ex[slot]?.en ?? ""}
                    onChange={(e) => setSlot(i, slot, "en", e.target.value)}
                    placeholder={i === 0 ? "using a cache" : "em inglês"}
                    autoCapitalize="off"
                  />
                  <input
                    id={`ex-${i}-${slot}-pt`}
                    className="pt-input"
                    value={ex[slot]?.pt ?? ""}
                    onChange={(e) => setSlot(i, slot, "pt", e.target.value)}
                    placeholder={i === 0 ? "usar um cache" : "tradução, com artigo (o, a, do…)"}
                    aria-label={`Tradução de ${slot}, exemplo ${i + 1}`}
                  />
                  {withDe && (
                    <input
                      id={`ex-${i}-${slot}-de`}
                      className="pt-input"
                      value={ex[slot]?.de ?? ""}
                      onChange={(e) => setSlot(i, slot, "de", e.target.value)}
                      placeholder={i === 0 ? "den Einsatz eines Caches" : "em alemão, com artigo (den, die, das…)"}
                      aria-label={`Alemão de ${slot}, exemplo ${i + 1}`}
                      lang="de"
                    />
                  )}
                </div>
              ))}
            </fieldset>
          ))}
        {slots.length > 0 && draft.examples.length < MAX_EXAMPLES && (
          <button
            type="button"
            className="link"
            onClick={() => setDraft({ ...draft, examples: [...draft.examples, {}] })}
          >
            + Outro exemplo
          </button>
        )}

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
            {(candidate.examples.length ? demos(candidate) : [preview]).map((p) => (
              <div key={p.en} className="preview-item">
                <p className="phrase">
                  <PhraseText text={p} />
                </p>
                {p.de && (
                  <p className="phrase" lang="de">
                    <PhraseText text={p.de} />
                  </p>
                )}
                <p className="pt">{p.pt}</p>
              </div>
            ))}
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
                    <PhraseText text={langText(render(c, exampleValues(c)), "en")!} />
                  </span>
                </button>
                <ConfirmButton
                  className="confirm-btn danger"
                  label="Apagar"
                  confirmLabel="Apagar?"
                  ariaLabel={`Apagar ${c.name}`}
                  onConfirm={() => onChange(mine.filter((m) => m !== c))}
                />
              </li>
            ))}
          </ul>
        </section>
      )}

      <section className="form">
        <h2 className="section-title">Exportar para o Anki</h2>
        <p className="hint">Arquivo para o tipo de nota Cloze. No Anki: Arquivo › Importar.</p>
        <div className="row">
          <button className="secondary" onClick={() => downloadText("chunks-anki.txt", ankiText(all, langs))}>
            Baixar ({all.length})
          </button>
          <button className="secondary" onClick={() => copyText(ankiText(all, langs), setCopied)}>
            {copied ? "Copiado ✓" : "Copiar"}
          </button>
        </div>
        {mine.length > 0 && (
          <button className="secondary" onClick={() => downloadText("meus-chunks-anki.txt", ankiText(mine, langs))}>
            Baixar só os meus ({mine.length})
          </button>
        )}
        <ConfirmButton
          className="link danger"
          label="Zerar progresso do treino"
          confirmLabel="Toque de novo para zerar o progresso"
          onConfirm={onResetProgress}
        />
      </section>
    </>
  );
}

/** Ação destrutiva em dois toques (confirm() não funciona em todo navegador embutido). */
function ConfirmButton(props: {
  className: string;
  label: string;
  confirmLabel: string;
  ariaLabel?: string;
  onConfirm: () => void;
}) {
  const [armed, setArmed] = useState(false);
  useEffect(() => {
    if (!armed) return;
    const t = setTimeout(() => setArmed(false), 3000);
    return () => clearTimeout(t);
  }, [armed]);
  return (
    <button
      className={armed ? `${props.className} armed` : props.className}
      aria-label={props.ariaLabel}
      onClick={() => {
        if (armed) props.onConfirm();
        setArmed(!armed);
      }}
    >
      {armed ? props.confirmLabel : props.label}
    </button>
  );
}

async function copyText(text: string, setCopied: (v: boolean) => void) {
  try {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  } catch {
    // sem acesso à área de transferência: o botão "Baixar" continua disponível
  }
}

function uniqueName(base: string, all: Chunk[]): string {
  const taken = new Set(all.map((c) => c.name));
  let name = base;
  for (let i = 2; taken.has(name); i++) name = `${base}_${i}`;
  return name;
}
