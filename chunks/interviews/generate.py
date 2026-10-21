"""Gera uma sessão de entrevista para qualquer vaga usando o Ollama."""

from __future__ import annotations

import json
import re
import unicodedata
from collections.abc import Callable
from pathlib import Path

from chunks.interviews import Question, Session, from_dict, to_dict
from chunks.interviews import prompts as P
from chunks.llm import Ollama, OllamaError

GENERATED_DIR = Path(__file__).resolve().parent / "generated"

# A etapa de encerramento precisa de menos perguntas.
COUNT_OVERRIDE = {"closing": 2}


def generate_session(
    job: str,
    profile: str = "",
    client: Ollama | None = None,
    per_stage: int = 5,
    on_progress: Callable[[str], None] = lambda _msg: None,
) -> Session:
    job = job.strip()
    if len(job) < 80:
        raise ValueError("Cole a descrição completa da vaga (o texto está curto demais).")
    client = client or Ollama()
    profile = profile.strip() or P.NO_PROFILE

    on_progress("Lendo a vaga…")
    meta = client.chat_json(
        "You extract information from job descriptions. Answer only with JSON.",
        P.META_PROMPT.format(job=job),
        P.META_SCHEMA,
        temperature=0.1,
    )

    questions: list[Question] = []
    for stage in P.STAGES:
        on_progress(f"Gerando: {stage.title}…")
        count = COUNT_OVERRIDE.get(stage.id, per_stage)
        prompt = P.STAGE_PROMPT.format(
            job=job,
            profile=profile,
            stage_title=stage.title,
            count=count,
            stage_focus=P.STAGE_FOCUS[stage.id],
            already="\n".join(f"- {q.en}" for q in questions) or "(none yet)",
        )
        raw = client.chat_json(P.SYSTEM, prompt, P.QUESTIONS_SCHEMA)
        found = normalize_questions(raw, stage.id, start=len(questions))[:count]
        if not found:
            raise OllamaError(
                f"O modelo {client.model} não gerou perguntas para a etapa {stage.title!r}. "
                "Tente de novo ou use um modelo maior."
            )
        questions.extend(found)

    title = _text(meta.get("title")) or "Entrevista"
    company = _text(meta.get("company"))
    return Session(
        id=unique_id(slugify(f"{company} {title}")),
        title=title,
        company=company,
        summary=_text(meta.get("summary")),
        stages=P.STAGES,
        questions=tuple(questions),
    )


def normalize_questions(raw: dict, stage: str, start: int = 0) -> list[Question]:
    """Limpa a saída do modelo: campos faltando, listas, marcação desbalanceada."""
    items = raw.get("questions") if isinstance(raw, dict) else None
    out: list[Question] = []
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict):
            continue
        en, answer = _text(item.get("question")), fix_markup(_text(item.get("answer")))
        if not en or not answer:
            continue
        out.append(
            Question(
                id=f"{stage}_{start + len(out) + 1}",
                stage=stage,
                en=en,
                goal=_text(item.get("goal")),
                answer=answer,
                tips=_texts(item.get("tips"))[:3],
                follow_ups=_texts(item.get("follow_ups"))[:2],
            )
        )
    return out


def fix_markup(text: str) -> str:
    """Remove marcadores [[ ]] / (( )) quando o modelo os deixou desbalanceados."""
    for open_, close in (("[[", "]]"), ("((", "))")):
        pattern = re.escape(open_) + r".+?" + re.escape(close)
        leftover = re.sub(pattern, "", text)
        if open_ in leftover or close in leftover:
            text = text.replace(open_, "").replace(close, "")
    return text


def save(session: Session, folder: Path = GENERATED_DIR) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{session.id}.json"
    path.write_text(json.dumps(to_dict(session), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def load_all(folder: Path = GENERATED_DIR) -> list[Session]:
    return [from_dict(json.loads(p.read_text(encoding="utf-8"))) for p in sorted(folder.glob("*.json"))]


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")[:60] or "vaga"


def unique_id(base: str, folder: Path = GENERATED_DIR) -> str:
    from chunks.interviews import sessions

    taken = set(sessions()) | {p.stem for p in folder.glob("*.json")}
    name = base
    for i in range(2, 1000):
        if name not in taken:
            break
        name = f"{base}_{i}"
    return name


def _text(value) -> str:
    return " ".join(value.split()) if isinstance(value, str) else ""


def _texts(value) -> tuple[str, ...]:
    return tuple(t for t in (_text(v) for v in value) if t) if isinstance(value, list) else ()
