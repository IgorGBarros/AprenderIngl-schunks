import { useState } from "react";
import {
  CATEGORY_LABELS,
  type Chunk,
  LANG_NAMES,
  type Lang,
  type SlotValue,
  demos,
  examplesOf,
  exampleValues,
  hasLang,
  langText,
  render,
} from "../lib/chunks";
import { useLangs } from "../lib/langs";
import { ChunkQuiz } from "./ChunkQuiz";
import { LangControl, SpeedControl, SpokenPhrase } from "./SpeakButton";

interface Props {
  chunk: Chunk;
  onBack: () => void;
  /** Chamado no fim do quiz do chunk: perfeito = acertou todas. */
  onQuizDone: (perfect: boolean) => void;
}

/** Página do chunk: exemplos prontos, montar a sua frase e, no final, o quiz. */
export function ChunkView({ chunk, onBack, onQuizDone }: Props) {
  const [values, setValues] = useState<Record<string, SlotValue>>(() => exampleValues(chunk));
  const [showPt, setShowPt] = useState(false);
  const [copied, setCopied] = useState<string | null>(null);
  const selected = useLangs();
  const available = selected.filter((l) => hasLang(chunk, l));
  const langs: Lang[] = available.length ? available : ["en"];
  const missingDe = selected.includes("de") && !hasLang(chunk, "de");
  const many = langs.length > 1;
  const phrase = render(chunk, values);
  const examples = demos(chunk);

  const set = (slot: string, field: keyof SlotValue, text: string) =>
    setValues((v) => ({ ...v, [slot]: { ...v[slot], [field]: text } }));

  const copy = async (lang: string, text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(lang);
      setTimeout(() => setCopied(null), 1500);
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

      <div className="controls">
        <LangControl />
        <SpeedControl />
      </div>
      {missingDe && <p className="hint">Este chunk ainda não tem versão em alemão.</p>}

      <section className="examples" aria-labelledby="examples-title">
        <h2 id="examples-title">
          {examples.length > 1 ? `${examples.length} exemplos` : "Exemplo"}
        </h2>
        <ul className="list">
          {examples.map((p, i) => (
            <li key={p.en} className="card example">
              {langs.map((lang) => (
                <SpokenPhrase key={lang} phrase={p} lang={lang} label={many} />
              ))}
              <p className="pt">{p.pt}</p>
              {chunk.slots.length > 0 && examplesOf(chunk).length > 1 && (
                <button
                  className="link small"
                  onClick={() => {
                    setValues(exampleValues(chunk, i));
                    document.getElementById("build-title")?.scrollIntoView({ behavior: "smooth" });
                  }}
                >
                  Editar este exemplo
                </button>
              )}
            </li>
          ))}
        </ul>
      </section>

      {chunk.note && <p className="note">💡 {chunk.note}</p>}

      {chunk.slots.length > 0 && (
        <section className="slots" aria-labelledby="build-title">
          <div className="slots-head">
            <h2 id="build-title">Monte a sua</h2>
            <button className="link" onClick={() => setShowPt((s) => !s)}>
              {showPt ? "Ocultar tradução" : "+ Traduzir variáveis"}
            </button>
          </div>

          <div className="card output" aria-live="polite">
            {langs.map((lang) => (
              <SpokenPhrase key={lang} phrase={phrase} lang={lang} label={many} />
            ))}
            <p className="pt">{phrase.pt}</p>
          </div>

          {chunk.slots.map((slot) => (
            <div className="slot" key={slot}>
              <label htmlFor={`slot-${slot}`}>
                <code>{slot}</code>
                {slot in chunk.defaults && <span className="optional">opcional</span>}
              </label>
              {langs.includes("en") && (
                <input
                  id={`slot-${slot}`}
                  value={values[slot]?.en ?? ""}
                  onChange={(e) => set(slot, "en", e.target.value)}
                  placeholder="em inglês"
                  aria-label={`${slot} em inglês`}
                  autoCapitalize="off"
                  autoCorrect="off"
                  spellCheck={false}
                  enterKeyHint="done"
                />
              )}
              {langs.includes("de") && (
                <input
                  id={langs.includes("en") ? `slot-${slot}-de` : `slot-${slot}`}
                  value={values[slot]?.de ?? values[slot]?.en ?? ""}
                  onChange={(e) => set(slot, "de", e.target.value)}
                  placeholder="em alemão (com artigo: den, die, das…)"
                  aria-label={`${slot} em alemão`}
                  autoCapitalize="off"
                  autoCorrect="off"
                  spellCheck={false}
                  enterKeyHint="done"
                  lang="de"
                />
              )}
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

          {langs.map((lang) => {
            const cloze = langText(phrase, lang)!.cloze;
            return (
              <div className="anki" key={lang}>
                <div className="anki-head">
                  <h3>
                    Card do Anki{many ? ` (${LANG_NAMES[lang]})` : ""}
                  </h3>
                  <button className="link" onClick={() => copy(lang, cloze)}>
                    {copied === lang ? "Copiado ✓" : "Copiar"}
                  </button>
                </div>
                <code className="cloze">{cloze}</code>
              </div>
            );
          })}
        </section>
      )}

      <ChunkQuiz chunk={chunk} phrases={examples} onDone={onQuizDone} />
    </>
  );
}
