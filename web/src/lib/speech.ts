// Pronúncia com a voz do próprio celular (Web Speech API, funciona offline).

import { useSyncExternalStore } from "react";
import { load, save } from "./storage";

export const canSpeak = typeof window !== "undefined" && "speechSynthesis" in window;

export const RATES = [1, 0.75, 0.5] as const;
const DEFAULT_RATE = 0.75;

// Velocidade escolhida pelo usuário, compartilhada por todos os botões de áudio.
let rate: number = load("chunks.speech.rate", DEFAULT_RATE);
const listeners = new Set<() => void>();

export function getRate(): number {
  return rate;
}

export function setRate(next: number): void {
  rate = next;
  save("chunks.speech.rate", next);
  listeners.forEach((l) => l());
}

export function useRate(): number {
  return useSyncExternalStore(
    (l) => {
      listeners.add(l);
      return () => listeners.delete(l);
    },
    getRate,
  );
}

function utterance(text: string): SpeechSynthesisUtterance {
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "en-US";
  u.rate = rate;
  const voice = speechSynthesis.getVoices().find((v) => v.lang.startsWith("en-US"));
  if (voice) u.voice = voice;
  return u;
}

// Leitura palavra por palavra em andamento: avisamos o botão dela quando outra
// leitura começa, porque o cancel() nem sempre dispara onend/onerror.
let activeWords: ((index: number) => void) | null = null;

let runId = 0;

function interrupt(): void {
  // Primeiro avisa o botão da leitura atual (ainda com o número dela), depois invalida.
  const previous = activeWords;
  activeWords = null;
  previous?.(-1);
  runId++;
  speechSynthesis.cancel();
}

/** Lê a frase inteira na velocidade escolhida. */
export function speak(text: string, onEnd?: () => void): void {
  if (!canSpeak) return;
  interrupt();
  const u = utterance(text);
  u.onend = u.onerror = () => onEnd?.();
  speechSynthesis.speak(u);
}

const strip = (token: string) => token.replace(/^[^\w']+|[^\w'%]+$/g, "");

/** Palavras da frase, sem a pontuação colada (o que a voz vai ler uma a uma). */
export function wordsOf(text: string): string[] {
  return text.split(/\s+/).map(strip).filter(Boolean);
}

/**
 * Divide um texto em pedaços para destacar a palavra que está tocando.
 * ``word`` é o índice da palavra (mesma contagem de ``wordsOf``), ou ``null``
 * para espaços e pontuação solta. ``start`` continua a contagem de um pedaço anterior.
 */
export function tokenize(text: string, start = 0): { text: string; word: number | null }[] {
  let n = start;
  return text
    .split(/(\s+)/)
    .filter((t) => t !== "")
    .map((t) => ({ text: t, word: /\S/.test(t) && strip(t) ? n++ : null }));
}

/**
 * Lê palavra por palavra, com uma pausa entre elas.
 * ``onWord(i)`` avisa qual palavra está tocando; ``-1`` quando termina.
 */
export function speakWords(text: string, onWord: (index: number) => void): void {
  if (!canSpeak) return;
  interrupt();
  // Avisos atrasados de uma leitura cancelada não podem mexer na leitura nova.
  const run = ++runId;
  const report = (i: number) => {
    if (run === runId) onWord(i);
  };
  activeWords = report;
  const words = wordsOf(text);
  words.forEach((word, i) => {
    const u = utterance(word);
    u.onstart = () => report(i);
    if (i === words.length - 1) {
      u.onend = u.onerror = () => {
        if (activeWords === report) activeWords = null;
        report(-1);
      };
    }
    speechSynthesis.speak(u);
  });
}

export function stopSpeaking(): void {
  if (canSpeak) interrupt();
}
