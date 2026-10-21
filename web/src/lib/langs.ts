// Idiomas escolhidos pelo usuário (inglês, alemão ou os dois), salvos no aparelho.

import { useSyncExternalStore } from "react";
import type { Lang } from "./chunks";
import { load, save } from "./storage";

export const LANG_OPTIONS: { id: string; label: string; langs: Lang[] }[] = [
  { id: "en", label: "Inglês", langs: ["en"] },
  { id: "de", label: "Alemão", langs: ["de"] },
  { id: "en+de", label: "Os dois", langs: ["en", "de"] },
];

const VALID = new Set(LANG_OPTIONS.map((o) => o.id));
let current: string = load("chunks.langs", "en");
if (!VALID.has(current)) current = "en";
const listeners = new Set<() => void>();

export function getLangsId(): string {
  return current;
}

export function setLangs(id: string): void {
  if (!VALID.has(id)) return;
  current = id;
  save("chunks.langs", id);
  listeners.forEach((l) => l());
}

/** Idiomas ativos, na ordem de exibição (inglês primeiro). */
export function useLangs(): Lang[] {
  const id = useSyncExternalStore(
    (l) => {
      listeners.add(l);
      return () => listeners.delete(l);
    },
    getLangsId,
  );
  return LANG_OPTIONS.find((o) => o.id === id)!.langs;
}
