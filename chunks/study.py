"""Ferramentas de estudo: quiz com repetição espaçada e exportação para o Anki."""

from __future__ import annotations

import json
import random
import re
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


# ---------------------------------------------------------------- correção
def normalize(text: str) -> str:
    text = text.lower().replace("’", "'")
    return " ".join(re.sub(r"[^a-z0-9' ]+", " ", text).split())


def check(answer: str, expected: Phrase) -> bool:
    """Compara ignorando maiúsculas, pontuação e espaços extras."""
    return normalize(answer) == normalize(expected.en)


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
            "example": {k: list(v) if isinstance(v, tuple) else v for k, v in c.example.items()},
            "defaults": c.defaults,
            "note": c.note,
            # Saída esperada: o app web testa se o motor em TS gera o mesmo.
            "demo": {"en": (d := c.demo()).en, "pt": d.pt, "cloze": d.cloze},
        }
        for c in registry().values()
    ]
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def interviews_json() -> str:
    """Sessões de entrevista para o app web (``web/src/data/interviews.json``)."""
    from chunks import interviews

    data = [interviews.to_dict(s) for s in interviews.sessions().values()]
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


# ------------------------------------------------------------------- Anki
def anki_export(path: Path, category: str | None = None) -> int:
    """Gera um arquivo .txt para importar no Anki (tipo de nota *Cloze*).

    Campos: Text (frase com a parte fixa escondida) e Back Extra
    (tradução + padrão da função).
    """
    rows = ["#separator:tab", "#html:false", "#notetype:Cloze", "#tags column:3"]
    for c in registry().values():
        if category not in (None, c.category):
            continue
        p = c.demo()
        extra = f"{p.pt} | {c.pattern}"
        rows.append(f"{p.cloze}\t{extra}\tchunks::{c.category}")
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return len(rows) - 4
