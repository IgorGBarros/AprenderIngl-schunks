// Reconhecimento de voz do navegador (Web Speech API) para responder falando.
// Funciona no Chrome, Edge e Safari (iOS 14.5+); precisa de HTTPS ou localhost.

import { VOICE_LOCALE, type VoiceLang } from "./speech";

interface RecognitionEvent {
  resultIndex: number;
  results: ArrayLike<{ isFinal: boolean; 0: { transcript: string } }>;
}

interface Recognition {
  lang: string;
  interimResults: boolean;
  continuous: boolean;
  maxAlternatives: number;
  onresult: ((e: RecognitionEvent) => void) | null;
  onerror: ((e: { error: string }) => void) | null;
  onend: (() => void) | null;
  start(): void;
  stop(): void;
  abort(): void;
}

type RecognitionCtor = new () => Recognition;

function ctor(): RecognitionCtor | undefined {
  if (typeof window === "undefined") return undefined;
  const w = window as unknown as { SpeechRecognition?: RecognitionCtor; webkitSpeechRecognition?: RecognitionCtor };
  return w.SpeechRecognition ?? w.webkitSpeechRecognition;
}

/** O navegador tem reconhecimento de voz (e a página está em HTTPS ou localhost). */
export const canListen = !!ctor() && typeof window !== "undefined" && window.isSecureContext;

/** Mensagens em português para os erros do reconhecimento. */
export function listenErrorMessage(error: string): string {
  switch (error) {
    case "not-allowed":
    case "service-not-allowed":
      return "O microfone foi bloqueado. Permita o acesso ao microfone nas configurações do navegador.";
    case "no-speech":
      return "Não ouvi nada. Toque no microfone e fale perto do celular.";
    case "audio-capture":
      return "Nenhum microfone encontrado.";
    case "network":
      return "O reconhecimento de voz precisa de internet.";
    case "language-not-supported":
      return "Este navegador não reconhece fala neste idioma.";
    default:
      return "Não consegui reconhecer a fala. Tente de novo.";
  }
}

interface Handlers {
  /** Texto reconhecido até agora (atualiza enquanto você fala). */
  onText: (text: string) => void;
  onError: (message: string) => void;
  onEnd: () => void;
}

/** Começa a ouvir no idioma pedido; devolve uma função para parar. */
export function listen(lang: VoiceLang, { onText, onError, onEnd }: Handlers): () => void {
  const Ctor = ctor();
  if (!Ctor) {
    onError("Este navegador não tem reconhecimento de voz. Use o Chrome, o Edge ou o Safari.");
    onEnd();
    return () => {};
  }
  const rec = new Ctor();
  rec.lang = VOICE_LOCALE[lang];
  rec.interimResults = true;
  rec.continuous = false;
  rec.maxAlternatives = 1;
  let finalText = "";
  rec.onresult = (e) => {
    let interim = "";
    for (let i = e.resultIndex; i < e.results.length; i++) {
      const r = e.results[i];
      if (r.isFinal) finalText += r[0].transcript;
      else interim += r[0].transcript;
    }
    onText((finalText + interim).trim());
  };
  rec.onerror = (e) => {
    if (e.error !== "aborted") onError(listenErrorMessage(e.error));
  };
  rec.onend = onEnd;
  try {
    rec.start();
  } catch {
    onError("Não consegui ligar o microfone. Tente de novo.");
    onEnd();
  }
  return () => rec.stop();
}
