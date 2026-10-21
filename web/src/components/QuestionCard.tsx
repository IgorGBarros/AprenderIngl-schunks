import { useEffect, useRef, useState } from "react";
import {
  type Chunk,
  LANG_NAMES,
  type Lang,
  type Phrase,
  blanks,
  core,
  hasLang,
  langText,
  normalizeAnswer,
} from "../lib/chunks";
import { useLangs } from "../lib/langs";
import { canListen, listen } from "../lib/listen";
import { SpokenPhrase } from "./SpeakButton";

interface Props {
  chunk: Chunk;
  phrase: Phrase;
  onAnswer: (correct: boolean) => void;
  nextLabel?: string;
}

type PerLang<T> = Partial<Record<Lang, T>>;

/**
 * Uma pergunta: mostra o português e pede a frase em cada idioma escolhido
 * (digitando ou falando no microfone). Só conta como acerto se acertar todos.
 */
export function QuestionCard({ chunk, phrase, onAnswer, nextLabel = "Próximo" }: Props) {
  const selected = useLangs();
  const available = selected.filter((l) => hasLang(chunk, l));
  const [langs] = useState<Lang[]>(available.length ? available : ["en"]);
  const [answers, setAnswers] = useState<PerLang<string>>({});
  const [result, setResult] = useState<PerLang<boolean> | null>(null);
  const [hint, setHint] = useState(false);
  const [listening, setListening] = useState<Lang | null>(null);
  const [micError, setMicError] = useState("");
  const stopRef = useRef<(() => void) | null>(null);
  const nextRef = useRef<HTMLButtonElement>(null);
  const many = langs.length > 1;

  // Desliga o microfone se a pergunta sair da tela.
  useEffect(() => {
    return () => stopRef.current?.();
  }, []);

  const expected = (lang: Lang) => langText(phrase, lang)?.text ?? "";
  const filled = langs.every((l) => answers[l]?.trim());
  const allOk = result !== null && langs.every((l) => result[l]);

  const check = () => {
    stopRef.current?.();
    setResult(
      Object.fromEntries(
        langs.map((l) => [l, normalizeAnswer(answers[l] ?? "") === normalizeAnswer(expected(l))]),
      ),
    );
    setTimeout(() => nextRef.current?.focus(), 0);
  };

  const toggleMic = (lang: Lang) => {
    setMicError("");
    if (listening) {
      stopRef.current?.();
      if (listening === lang) return;
    }
    setListening(lang);
    stopRef.current = listen(lang, {
      onText: (text) => setAnswers((a) => ({ ...a, [lang]: text })),
      onError: setMicError,
      onEnd: () => {
        setListening((l) => (l === lang ? null : l));
        stopRef.current = null;
      },
    });
  };

  const prompt = langs.map((l) => LANG_NAMES[l].toLowerCase()).join(" e ");

  return (
    <>
      <section className="card question">
        <p className="label">Como se diz em {prompt}?</p>
        <p className="phrase">{phrase.pt}</p>
      </section>

      <form
        className="form"
        onSubmit={(e) => {
          e.preventDefault();
          if (result === null && filled) check();
        }}
      >
        {langs.map((lang, i) => (
          <div className="answer-field" key={lang}>
            {many && (
              <label className="answer-label" htmlFor={`answer-${lang}`}>
                {LANG_NAMES[lang]}
              </label>
            )}
            {hint && result === null && (
              <p className="hint-line" aria-live="polite">
                <code>{blanks(phrase, lang)}</code>
              </p>
            )}
            <div className="answer-row">
              <textarea
                id={`answer-${lang}`}
                rows={many ? 2 : 3}
                lang={lang}
                value={answers[lang] ?? ""}
                onChange={(e) => setAnswers((a) => ({ ...a, [lang]: e.target.value }))}
                placeholder={
                  listening === lang ? "Ouvindo… fale agora" : `Escreva ou fale em ${LANG_NAMES[lang].toLowerCase()}…`
                }
                readOnly={result !== null}
                autoCapitalize="sentences"
                autoCorrect="off"
                spellCheck={false}
                autoFocus={i === 0}
                aria-label={`Sua resposta em ${LANG_NAMES[lang].toLowerCase()}`}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    if (i < langs.length - 1) document.getElementById(`answer-${langs[i + 1]}`)?.focus();
                    else if (result === null && filled) check();
                  }
                }}
              />
              {canListen && result === null && (
                <button
                  type="button"
                  className={listening === lang ? "icon-btn mic listening" : "icon-btn mic"}
                  onClick={() => toggleMic(lang)}
                  aria-label={
                    listening === lang ? "Parar de ouvir" : `Responder falando em ${LANG_NAMES[lang].toLowerCase()}`
                  }
                  aria-pressed={listening === lang}
                >
                  <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden>
                    <path
                      fill="currentColor"
                      d="M12 14a3 3 0 0 0 3-3V5a3 3 0 0 0-6 0v6a3 3 0 0 0 3 3zm5-3a5 5 0 0 1-10 0H5a7 7 0 0 0 6 6.92V21h2v-3.08A7 7 0 0 0 19 11h-2z"
                    />
                  </svg>
                </button>
              )}
            </div>
          </div>
        ))}

        {micError && (
          <p className="error-box" role="alert">
            {micError}
          </p>
        )}
        {!canListen && result === null && (
          <p className="hint">
            Para responder falando, abra o app no Chrome, Edge ou Safari, em HTTPS ou localhost.
          </p>
        )}

        {result === null && (
          <>
            <div className="row">
              <button
                type="button"
                className="secondary"
                onClick={() => {
                  stopRef.current?.();
                  setResult(Object.fromEntries(langs.map((l) => [l, false])));
                }}
              >
                Não sei
              </button>
              <button type="submit" className="primary" disabled={!filled}>
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

      {result !== null && (
        <section className={allOk ? "card feedback ok" : "card feedback wrong"} aria-live="polite">
          {langs.map((lang) => (
            <div className="feedback-lang" key={lang}>
              <p className="verdict">
                {result[lang] ? "✔ Correto" : "✘ Resposta"}
                {many ? ` (${LANG_NAMES[lang].toLowerCase()})` : ""}
                {result[lang] ? "!" : ":"}
              </p>
              <SpokenPhrase phrase={phrase} lang={lang} />
              <p className="pt">
                Chunk: <strong>{core(chunk, lang)}</strong>
              </p>
            </div>
          ))}
          <div className="row">
            {!allOk && langs.some((l) => answers[l]?.trim()) && (
              <button className="secondary" onClick={() => onAnswer(true)}>
                Eu acertei
              </button>
            )}
            <button ref={nextRef} className="primary" onClick={() => onAnswer(allOk)}>
              {nextLabel}
            </button>
          </div>
        </section>
      )}
    </>
  );
}
