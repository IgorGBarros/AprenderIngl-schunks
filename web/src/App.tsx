import { useEffect, useMemo, useState } from "react";
import { ChunkView } from "./components/ChunkView";
import { Interview } from "./components/Interview";
import { Library } from "./components/Library";
import { MyChunks } from "./components/MyChunks";
import { Quiz } from "./components/Quiz";
import { BUILTIN, type Chunk } from "./lib/chunks";
import type { Progress } from "./lib/srs";
import { load, save } from "./lib/storage";

type Tab = "library" | "quiz" | "interview" | "mine";

const TABS: { id: Tab; label: string; icon: string }[] = [
  { id: "library", label: "Biblioteca", icon: "{ }" },
  { id: "quiz", label: "Treinar", icon: "▶" },
  { id: "interview", label: "Entrevista", icon: "?" },
  { id: "mine", label: "Meus", icon: "+" },
];

/** Rotas por hash (#/quiz, #/c/could_i_get) para o botão "voltar" do celular funcionar. */
function useHashRoute(): [string[], (path: string) => void] {
  const read = () => window.location.hash.replace(/^#\/?/, "").split("/").filter(Boolean);
  const [route, setRoute] = useState(read);
  useEffect(() => {
    const onChange = () => setRoute(read());
    window.addEventListener("hashchange", onChange);
    return () => window.removeEventListener("hashchange", onChange);
  }, []);
  return [route, (path) => (window.location.hash = `/${path}`)];
}

export default function App() {
  const [route, go] = useHashRoute();
  const [mine, setMine] = useState<Chunk[]>(() => load("chunks.mine", []));
  const [progress, setProgress] = useState<Progress>(() => load("chunks.progress", {}));

  useEffect(() => save("chunks.mine", mine), [mine]);
  useEffect(() => save("chunks.progress", progress), [progress]);

  const all = useMemo(() => [...BUILTIN, ...mine], [mine]);
  const [section, param] = route;
  const tab: Tab =
    section === "quiz" || section === "mine" || section === "interview" ? section : "library";
  const opened = section === "c" ? all.find((c) => c.name === param) : undefined;

  return (
    <div className="app">
      <main className="screen">
        {opened ? (
          <ChunkView key={opened.name} chunk={opened} onBack={() => (window.history.length > 1 ? window.history.back() : go(""))} />
        ) : tab === "interview" ? (
          <Interview openId={param} onOpen={(id) => go(id ? `interview/${id}` : "interview")} />
        ) : tab === "quiz" ? (
          <Quiz chunks={all} progress={progress} onProgress={setProgress} />
        ) : tab === "mine" ? (
          <MyChunks
            all={all}
            mine={mine}
            onChange={setMine}
            onOpen={(c) => go(`c/${c.name}`)}
            onResetProgress={() => setProgress({})}
          />
        ) : (
          <Library chunks={all} onOpen={(c) => go(`c/${c.name}`)} />
        )}
      </main>

      <nav className="tabbar" aria-label="Seções">
        {TABS.map((t) => (
          <button
            key={t.id}
            className={!opened && tab === t.id ? "tab active" : "tab"}
            aria-current={!opened && tab === t.id ? "page" : undefined}
            onClick={() => go(t.id === "library" ? "" : t.id)}
          >
            <span className="tab-icon" aria-hidden>
              {t.icon}
            </span>
            {t.label}
          </button>
        ))}
      </nav>
    </div>
  );
}
