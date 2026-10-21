import { useEffect, useRef, useState } from "react";
import { LANG_NAMES, type Lang, type Phrase, langText } from "../lib/chunks";
import { LANG_OPTIONS, setLangs, useLangs } from "../lib/langs";
import { RATES, canSpeak, setRate, speak, speakWords, stopSpeaking, tokenize, useRate } from "../lib/speech";
import { PhraseText } from "./PhraseText";

const SPEAKER =
  "M3 10v4h4l5 4V6L7 10H3zm13.5 2a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4zM14 3.2v2.1a7 7 0 0 1 0 13.4v2.1a9 9 0 0 0 0-17.6z";

interface SpeakButtonProps {
  text: string;
  /** Idioma da voz (inglês por padrão). */
  lang?: Lang;
  /** Recebe a palavra que está tocando (-1 quando para), para a tela destacá-la. */
  onWord?: (index: number) => void;
  /** false esconde o "palavra por palavra" (ex.: respostas longas). */
  words?: boolean;
}

/** Ouvir a frase inteira ou palavra por palavra, na velocidade escolhida. */
export function SpeakButton({ text, lang = "en", onWord, words = true }: SpeakButtonProps) {
  const [word, setWord] = useState(-1);
  const playing = useRef(false);
  playing.current = word >= 0;
  const rate = useRate();

  // Para o áudio se o componente sair da tela no meio da leitura.
  useEffect(() => {
    return () => {
      if (playing.current) stopSpeaking();
    };
  }, []);

  if (!canSpeak) return null;
  const report = (i: number) => {
    setWord(i);
    onWord?.(i);
  };

  return (
    <div className="speak">
      <button
        className="icon-btn"
        onClick={() => speak(text, lang)}
        aria-label={`Ouvir a frase em ${LANG_NAMES[lang].toLowerCase()} (${rate}x)`}
        title={`Ouvir (${rate}x)`}
      >
        <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden>
          <path fill="currentColor" d={SPEAKER} />
        </svg>
      </button>
      {words && (
        <button
          className={word >= 0 ? "icon-btn words active" : "icon-btn words"}
          onClick={() => (word >= 0 ? stopSpeaking() : speakWords(text, report, lang))}
          aria-label={word >= 0 ? "Parar" : "Ouvir palavra por palavra"}
          title="Palavra por palavra"
        >
          {word >= 0 ? "■" : "A·B"}
        </button>
      )}
    </div>
  );
}

interface SpokenPhraseProps {
  phrase: Phrase;
  lang?: Lang;
  /** Mostra "EN"/"DE" antes da frase (quando há mais de um idioma na tela). */
  label?: boolean;
}

/** Frase do chunk com os botões de áudio; a palavra que está tocando fica destacada. */
export function SpokenPhrase({ phrase, lang = "en", label = false }: SpokenPhraseProps) {
  const [word, setWord] = useState(-1);
  const t = langText(phrase, lang);
  if (!t) return null;
  return (
    <div className="output-en" lang={lang}>
      <p className="phrase">
        {label && <span className="lang-tag">{lang.toUpperCase()}</span>}
        <PhraseText text={t} activeWord={word} />
      </p>
      <SpeakButton text={t.text} lang={lang} onWord={setWord} />
    </div>
  );
}

/** Texto simples com os botões de áudio e o destaque da palavra que está tocando. */
export function SpokenText({ text, className = "phrase" }: { text: string; className?: string }) {
  const [word, setWord] = useState(-1);
  return (
    <div className="output-en">
      <p className={className}>
        {word < 0
          ? text
          : tokenize(text).map((t, i) =>
              t.word === word ? (
                <span key={i} className="speaking">
                  {t.text}
                </span>
              ) : (
                t.text
              ),
            )}
      </p>
      <SpeakButton text={text} onWord={setWord} />
    </div>
  );
}

/** Seletor de idioma: inglês, alemão ou os dois (vale para o app todo). */
export function LangControl() {
  const langs = useLangs();
  const id = langs.join("+");
  return (
    <div className="speed lang-control" role="radiogroup" aria-label="Idioma que você está estudando">
      {LANG_OPTIONS.map((o) => (
        <button
          key={o.id}
          role="radio"
          aria-checked={id === o.id}
          className={id === o.id ? "speed-btn active" : "speed-btn"}
          onClick={() => setLangs(o.id)}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}

/** Seletor de velocidade (vale para todos os áudios do app). */
export function SpeedControl() {
  const rate = useRate();
  if (!canSpeak) return null;
  return (
    <div className="speed" role="radiogroup" aria-label="Velocidade do áudio">
      <span className="speed-label" aria-hidden>
        Áudio
      </span>
      {RATES.map((r) => (
        <button
          key={r}
          role="radio"
          aria-checked={rate === r}
          className={rate === r ? "speed-btn active" : "speed-btn"}
          onClick={() => setRate(r)}
        >
          {r}x
        </button>
      ))}
    </div>
  );
}
