// Pronúncia com a voz do próprio celular (Web Speech API, funciona offline).

export const canSpeak = typeof window !== "undefined" && "speechSynthesis" in window;

export function speak(text: string, rate = 0.9): void {
  if (!canSpeak) return;
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "en-US";
  u.rate = rate;
  const voice = speechSynthesis.getVoices().find((v) => v.lang.startsWith("en-US"));
  if (voice) u.voice = voice;
  speechSynthesis.speak(u);
}
