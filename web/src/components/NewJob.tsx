import { useRef, useState } from "react";
import { generateSession, parseSession } from "../lib/generate";
import type { Session } from "../lib/interviews";
import { DEFAULT_HOST, DEFAULT_MODEL, listModels } from "../lib/ollama";
import { load, save } from "../lib/storage";

interface Props {
  takenIds: string[];
  onCreated: (s: Session) => void;
  onCancel: () => void;
}

/** Cola a descrição de qualquer vaga e gera a entrevista com o Ollama. */
export function NewJob({ takenIds, onCreated, onCancel }: Props) {
  const [job, setJob] = useState(() => load("chunks.job.draft", ""));
  const [profile, setProfile] = useState(() => load("chunks.profile", ""));
  const [host, setHost] = useState(() => load("chunks.ollama.host", DEFAULT_HOST));
  const [model, setModel] = useState(() => load("chunks.ollama.model", DEFAULT_MODEL));
  const [perStage, setPerStage] = useState(5);
  const [models, setModels] = useState<string[] | null>(null);
  const [steps, setSteps] = useState<string[]>([]);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const abort = useRef<AbortController | null>(null);

  const remember = (key: string, value: string) => save(key, value);

  const connect = async () => {
    setError("");
    try {
      const found = await listModels(host);
      setModels(found);
      if (found.length && !found.includes(model)) setModel(found[0]);
      if (!found.length) setError("O Ollama está rodando, mas não tem modelos. Rode: ollama pull qwen2.5:7b");
    } catch (e) {
      setModels(null);
      setError((e as Error).message);
      setSettingsOpen(true);
    }
  };

  const generate = async () => {
    setError("");
    setSteps([]);
    setBusy(true);
    remember("chunks.ollama.host", host);
    remember("chunks.ollama.model", model);
    abort.current = new AbortController();
    try {
      const session = await generateSession(job, profile, { host, model }, {
        perStage,
        takenIds,
        signal: abort.current.signal,
        onProgress: (msg) => setSteps((s) => [...s, msg]),
      });
      save("chunks.job.draft", "");
      onCreated(session);
    } catch (e) {
      if ((e as Error).name !== "AbortError") {
        setError((e as Error).message);
        setSettingsOpen(true);
      }
    } finally {
      setBusy(false);
    }
  };

  const importFile = async (file: File) => {
    setError("");
    try {
      onCreated(parseSession(await file.text()));
    } catch (e) {
      setError((e as Error).message);
    }
  };

  return (
    <>
      <header className="header detail-header">
        <button className="back" onClick={onCancel} disabled={busy}>
          ‹ Entrevista
        </button>
        <span className="badge">Ollama</span>
      </header>

      <h1>Nova vaga</h1>
      <p className="subtitle">
        Cole a descrição de qualquer vaga. O seu modelo local cria as perguntas e as respostas modelo.
      </p>

      <form
        className="form"
        onSubmit={(e) => {
          e.preventDefault();
          if (!busy) generate();
        }}
      >
        <label htmlFor="job">Descrição da vaga</label>
        <textarea
          id="job"
          rows={8}
          value={job}
          onChange={(e) => {
            setJob(e.target.value);
            remember("chunks.job.draft", e.target.value);
          }}
          placeholder="Cole aqui o texto completo da vaga (título, responsabilidades, requisitos)…"
        />

        <label htmlFor="profile">
          Seu perfil <span className="optional">opcional, fica só neste aparelho</span>
        </label>
        <textarea
          id="profile"
          rows={5}
          value={profile}
          onChange={(e) => {
            setProfile(e.target.value);
            remember("chunks.profile", e.target.value);
          }}
          placeholder="Cargo atual, empresas, anos de experiência, projetos com números, tecnologias que você usou de verdade…"
        />
        <p className="hint">
          O modelo não inventa fatos: o que não estiver no perfil aparece tracejado para você preencher.
        </p>

        <details
          className="settings"
          open={settingsOpen}
          onToggle={(e) => setSettingsOpen((e.target as HTMLDetailsElement).open)}
        >
          <summary>Configurar Ollama</summary>
          <div className="form">
            <label htmlFor="host">Endereço</label>
            <input
              id="host"
              value={host}
              onChange={(e) => setHost(e.target.value)}
              autoCapitalize="off"
              autoCorrect="off"
              spellCheck={false}
              inputMode="url"
            />
            <label htmlFor="model">Modelo</label>
            {models && models.length > 0 ? (
              <select id="model" value={model} onChange={(e) => setModel(e.target.value)}>
                {models.map((m) => (
                  <option key={m} value={m}>
                    {m}
                  </option>
                ))}
              </select>
            ) : (
              <input
                id="model"
                value={model}
                onChange={(e) => setModel(e.target.value)}
                autoCapitalize="off"
                autoCorrect="off"
                spellCheck={false}
              />
            )}
            <button type="button" className="secondary" onClick={connect}>
              {models ? `Conectado ✓ (${models.length} modelos)` : "Testar conexão"}
            </button>

            <label htmlFor="per-stage">Perguntas por etapa</label>
            <select id="per-stage" value={perStage} onChange={(e) => setPerStage(Number(e.target.value))}>
              {[3, 5, 7].map((n) => (
                <option key={n} value={n}>
                  {n} (cerca de {n * 5 + 2} perguntas)
                </option>
              ))}
            </select>
          </div>
        </details>

        {error && (
          <p className="error-box" role="alert">
            {error}
          </p>
        )}

        {busy || steps.length > 0 ? (
          <ol className="steps" aria-live="polite">
            {steps.map((s, i) => (
              <li key={s} className={busy && i === steps.length - 1 ? "current" : "done"}>
                {s}
              </li>
            ))}
          </ol>
        ) : null}

        {busy ? (
          <button type="button" className="secondary" onClick={() => abort.current?.abort()}>
            Cancelar
          </button>
        ) : (
          <button className="primary" type="submit" disabled={job.trim().length < 80}>
            Gerar entrevista
          </button>
        )}
        {busy && <p className="hint">Modelos locais levam alguns minutos. Deixe esta tela aberta.</p>}
      </form>

      <section className="form import">
        <h2 className="section-title">Já gerou no computador?</h2>
        <p className="hint">
          Importe o arquivo criado pelo <code>python -m chunks vaga</code> (pasta{" "}
          <code>chunks/interviews/generated</code>).
        </p>
        <label className="secondary file-button">
          Importar sessão (.json)
          <input
            type="file"
            accept="application/json,.json"
            onChange={(e) => e.target.files?.[0] && importFile(e.target.files[0])}
          />
        </label>
      </section>
    </>
  );
}
