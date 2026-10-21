"""Sessões de entrevista: perguntas prováveis + respostas modelo.

Marcação usada nas respostas modelo (``answer``):

- ``[[...]]``  chunk (bloco pronto para memorizar), destacado no app.
- ``((...))``  PREENCHA com um fato seu (número, empresa, data). Nunca diga
  na entrevista algo que você não consegue sustentar com um exemplo real.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

_CHUNK = re.compile(r"\[\[(.+?)\]\]")
_FILL = re.compile(r"\(\((.+?)\)\)")


@dataclass(frozen=True)
class Question:
    id: str
    stage: str
    en: str
    """A pergunta, como o entrevistador falaria."""
    goal: str
    """Em português: o que eles realmente querem descobrir."""
    answer: str
    """Resposta modelo em inglês, com [[chunks]] e ((preencha))."""
    tips: tuple[str, ...] = ()
    follow_ups: tuple[str, ...] = ()


@dataclass(frozen=True)
class Stage:
    id: str
    title: str
    description: str


@dataclass(frozen=True)
class Session:
    id: str
    title: str
    company: str
    summary: str
    stages: tuple[Stage, ...]
    questions: tuple[Question, ...] = field(default_factory=tuple)

    def by_stage(self, stage: str) -> list[Question]:
        return [q for q in self.questions if q.stage == stage]


_SESSIONS: dict[str, Session] = {}


def register(session: Session) -> Session:
    stage_ids = {s.id for s in session.stages}
    seen: set[str] = set()
    for q in session.questions:
        if q.stage not in stage_ids:
            raise ValueError(f"{session.id}/{q.id}: etapa desconhecida {q.stage!r}")
        if q.id in seen:
            raise ValueError(f"{session.id}: pergunta duplicada {q.id!r}")
        seen.add(q.id)
    _SESSIONS[session.id] = session
    return session


def sessions() -> dict[str, Session]:
    return dict(_SESSIONS)


def plain(text: str) -> str:
    """Resposta sem marcação; ``((x))`` vira ``[x]`` para você lembrar de trocar."""
    return _FILL.sub(r"[\1]", _CHUNK.sub(r"\1", text))


def chunks_in(text: str) -> list[str]:
    return _CHUNK.findall(text)


def to_dict(session: Session) -> dict:
    return asdict(session)


from chunks.interviews import vendor_data_platform  # noqa: E402,F401  (registra a sessão)
