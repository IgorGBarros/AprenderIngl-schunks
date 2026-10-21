"""Ferramentas de estudo: quiz com repetição espaçada e exportação para o Anki."""

from __future__ import annotations

import json
import random
import re
import unicodedata
from datetime import date, timedelta
from pathlib import Path

from chunks.core import Chunk, Phrase, registry

PROGRESS_FILE = Path.home() / ".chunks_progress.json"

# Sistema de Leitner: acertou -> sobe de caixa (revisa mais tarde);
# errou -> volta para a caixa 1 (revisa amanhã).
BOX_INTERVAL_DAYS = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16}


# ----------------------------------------------------------- progresso (SRS)
def load_progress(path: Path = PROGRESS_FILE) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_progress(progress: dict, path: Path = PROGRESS_FILE) -> None:
    path.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding="utf-8")


def record(progress: dict, name: str, correct: bool, today: date | None = None) -> None:
    today = today or date.today()
    box = progress.get(name, {}).get("box", 1)
    box = min(box + 1, 5) if correct else 1
    progress[name] = {
        "box": box,
        "due": (today + timedelta(days=BOX_INTERVAL_DAYS[box])).isoformat(),
    }


def due_chunks(
    progress: dict, category: str | None = None, today: date | None = None
) -> list[Chunk]:
    """Chunks que vencem hoje (ou nunca estudados), os mais difíceis primeiro."""
    today = (today or date.today()).isoformat()
    pool = [c for c in registry().values() if category in (None, c.category)]
    due = [c for c in pool if progress.get(c.name, {}).get("due", today) <= today]
    random.shuffle(due)
    return sorted(due, key=lambda c: progress.get(c.name, {}).get("box", 0))


def random_phrase(c: Chunk) -> Phrase:
    """Um dos exemplos do chunk, sorteado (cada revisão usa uma frase diferente)."""
    return random.choice(c.demos())


# ---------------------------------------------------------------- correção
LANGS = {"en": "inglês", "de": "alemão"}


def parse_langs(value: str) -> list[str]:
    """``"en"``, ``"de"`` ou ``"en+de"`` -> lista de idiomas."""
    langs = [v for v in value.replace(",", "+").split("+") if v]
    unknown = [v for v in langs if v not in LANGS]
    if unknown or not langs:
        raise ValueError(f"Idioma inválido: {value!r}. Use en, de ou en+de.")
    return langs


def normalize(text: str) -> str:
    """Minúsculas, sem pontuação, sem acento (ä -> a, ß -> ss): "konnen" vale "können"."""
    text = text.lower().replace("’", "'").replace("ß", "ss")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return " ".join(re.sub(r"[^a-z0-9' ]+", " ", text).split())


def check(answer: str, expected: Phrase, lang: str = "en") -> bool:
    """Compara ignorando maiúsculas, pontuação, acentos e espaços extras."""
    return normalize(answer) == normalize(expected.text(lang))


# ------------------------------------------------------------------- JSON
def to_json() -> str:
    """Serializa a biblioteca para o app web (``web/src/data/chunks.json``)."""
    data = [
        {
            "name": c.name,
            "template": c.template,
            "pt": c.pt,
            "category": c.category,
            "slots": c.slots,
            "examples": [
                {k: list(v) if isinstance(v, tuple) else v for k, v in ex.items()} for ex in c.examples
            ],
            "defaults": c.defaults,
            "note": c.note,
            "de": c.de,
            # Saída esperada: o app web testa se o motor em TS gera o mesmo.
            "demos": [
                {"en": d.en, "pt": d.pt, "cloze": d.cloze, "de": d.de, "de_cloze": d.de_cloze}
                for d in c.demos()
            ],
        }
        for c in registry().values()
    ]
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def interviews_json() -> str:
    """Sessões de entrevista para o app web (``web/src/data/interviews.json``)."""
    from chunks import interviews

    data = [interviews.to_dict(s) for s in interviews.sessions().values()]
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def prompts_json() -> str:
    """Prompts de geração de entrevistas, para o app web gerar igual ao Python."""
    from chunks.interviews import prompts

    return json.dumps(prompts.to_dict(), indent=2, ensure_ascii=False) + "\n"


# ------------------------------------------------------------------- Anki
def anki_export(path: Path, category: str | None = None, langs: list[str] | None = None) -> int:
    """Gera um arquivo .txt para importar no Anki (tipo de nota *Cloze*).

    Um card por exemplo e por idioma. Campos: Text (frase com a parte fixa
    escondida) e Back Extra (tradução + padrão da função).
    """
    rows = ["#separator:tab", "#html:false", "#notetype:Cloze", "#tags column:3"]
    for c in registry().values():
        if category not in (None, c.category):
            continue
        for lang in langs or ["en"]:
            for p in c.demos():
                if p.cloze_for(lang):
                    rows.append(f"{p.cloze_for(lang)}\t{p.pt} | {c.pattern}\tchunks::{c.category} chunks::{lang}")
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return len(rows) - 4
