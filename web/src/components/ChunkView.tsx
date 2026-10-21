import { useState } from "react";
import { CATEGORY_LABELS, type Chunk, type SlotValue, exampleValues, render } from "../lib/chunks";
import { PhraseText } from "./PhraseText";
import { SpeakButton } from "./SpeakButton";

interface Props {
  chunk: Chunk;
  onBack: () => void;
}

/** "Executa" o chunk: o usuário preenche as variáveis e vê a frase pronta. */
export function ChunkView({ chunk, onBack }: Props) {
  const [values, setValues] = useState<Record<string, SlotValue>>(() => exampleValues(chunk));
  const [showPt, setShowPt] = useState(false);
  const [copied, setCopied] = useState(false);
  const phrase = render(chunk, values);

  const set = (slot: string, field: keyof SlotValue, text: string) =>
    setValues((v) => ({ ...v, [slot]: { ...v[slot], [field]: text } }));

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(phrase.cloze);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      // clipboard indisponível: o texto continua visível para copiar à mão
    }
  };

  return (
    <>
      <header className="header detail-header">
        <button className="back" onClick={onBack}>
          ‹ Voltar
        </button>
        <span className="badge">{CATEGORY_LABELS[chunk.category] ?? chunk.category}</span>
      </header>

      <code className="signature">
        <span className="kw">def</span> {chunk.name}(
        <span className="args">{chunk.slots.join(", ")}</span>)
      </code>

      <section className="card output" aria-live="polite">
        <div className="output-en">
          <p className="phrase">
            <PhraseText phrase={phrase} />
          </p>
          <SpeakButton text={phrase.en} />
        </div>
        <p className="pt">{phrase.pt}</p>
      </section>

      {chunk.slots.length > 0 && (
        <section className="slots">
          <div className="slots-head">
            <h2>Variáveis</h2>
            <button className="link" onClick={() => setShowPt((s) => !s)}>
              {showPt ? "Ocultar tradução" : "+ Traduzir variáveis"}
            </button>
          </div>
          {chunk.slots.map((slot) => (
            <div className="slot" key={slot}>
              <label htmlFor={`slot-${slot}`}>
                <code>{slot}</code>
                {slot in chunk.defaults && <span className="optional">opcional</span>}
              </label>
              <input
                id={`slot-${slot}`}
                value={values[slot]?.en ?? ""}
                onChange={(e) => set(slot, "en", e.target.value)}
                autoCapitalize="off"
                autoCorrect="off"
                spellCheck={false}
                enterKeyHint="done"
              />
              {showPt && (
                <input
                  className="pt-input"
                  placeholder="tradução (opcional)"
                  value={values[slot]?.pt ?? ""}
                  onChange={(e) => set(slot, "pt", e.target.value)}
                  aria-label={`Tradução de ${slot}`}
                />
              )}
            </div>
          ))}
          <button className="secondary" onClick={() => setValues(exampleValues(chunk))}>
            Voltar ao exemplo
          </button>
        </section>
      )}

      {chunk.note && <p className="note">💡 {chunk.note}</p>}

      <section className="card anki">
        <div className="anki-head">
          <h2>Card do Anki (Cloze)</h2>
          <button className="link" onClick={copy}>
            {copied ? "Copiado ✓" : "Copiar"}
          </button>
        </div>
        <code className="cloze">{phrase.cloze}</code>
      </section>
    </>
  );
}
