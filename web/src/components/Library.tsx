import { useMemo, useState } from "react";
import {
  CATEGORY_LABELS,
  type Chunk,
  categoriesOf,
  exampleValues,
  hasLang,
  langText,
  render,
  search,
} from "../lib/chunks";
import { useLangs } from "../lib/langs";
import { load, save } from "../lib/storage";
import { PhraseText } from "./PhraseText";
import { LangControl } from "./SpeakButton";

interface Props {
  chunks: Chunk[];
  onOpen: (c: Chunk) => void;
}

export function Library({ chunks, onOpen }: Props) {
  const [term, setTerm] = useState("");
  const [category, setCategory] = useState<string>(() => load("chunks.category", "all"));
  const langs = useLangs();

  const categories = useMemo(() => categoriesOf(chunks), [chunks]);
  const visible = useMemo(
    () => search(chunks, term).filter((c) => category === "all" || c.category === category),
    [chunks, term, category],
  );

  const pick = (cat: string) => {
    setCategory(cat);
    save("chunks.category", cat);
  };

  return (
    <>
      <header className="header">
        <h1>Chunks</h1>
        <p className="subtitle">Cada frase é uma função. Passe as variáveis.</p>
        <LangControl />
        <input
          className="search"
          type="search"
          placeholder="Procurar em inglês ou português…"
          value={term}
          onChange={(e) => setTerm(e.target.value)}
          aria-label="Procurar chunks"
        />
        <div className="chips" role="tablist" aria-label="Categorias">
          {["all", ...categories].map((cat) => (
            <button
              key={cat}
              role="tab"
              aria-selected={category === cat}
              className={category === cat ? "chip active" : "chip"}
              onClick={() => pick(cat)}
            >
              {cat === "all" ? "Todos" : (CATEGORY_LABELS[cat] ?? cat)}
            </button>
          ))}
        </div>
      </header>

      <p className="count">
        {visible.length} {visible.length === 1 ? "chunk" : "chunks"}
      </p>

      <ul className="list">
        {visible.map((c) => {
          const p = render(c, exampleValues(c));
          return (
            <li key={c.name}>
              <button className="card chunk-row" onClick={() => onOpen(c)}>
                <code className="fn">
                  {c.name}
                  <span className="args">({c.slots.join(", ")})</span>
                </code>
                {langs
                  .filter((lang) => hasLang(c, lang))
                  .map((lang) => (
                    <span key={lang} className="en" lang={lang}>
                      {langs.length > 1 && <span className="lang-tag">{lang.toUpperCase()}</span>}
                      <PhraseText text={langText(p, lang)!} />
                    </span>
                  ))}
                <span className="pt">{p.pt}</span>
              </button>
            </li>
          );
        })}
      </ul>
      {visible.length === 0 && <p className="empty">Nada encontrado para “{term}”.</p>}
    </>
  );
}
