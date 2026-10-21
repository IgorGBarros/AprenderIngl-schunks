import { canSpeak, speak } from "../lib/speech";

export function SpeakButton({ text }: { text: string }) {
  if (!canSpeak) return null;
  return (
    <button className="icon-btn" onClick={() => speak(text)} aria-label="Ouvir pronúncia">
      <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden>
        <path
          fill="currentColor"
          d="M3 10v4h4l5 4V6L7 10H3zm13.5 2a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4zM14 3.2v2.1a7 7 0 0 1 0 13.4v2.1a9 9 0 0 0 0-17.6z"
        />
      </svg>
    </button>
  );
}
