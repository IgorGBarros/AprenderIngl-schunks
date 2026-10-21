"""Motor da biblioteca: transforma cada chunk em uma função Python.

Um chunk é definido por um *template* em inglês:

    "[[Could I get]] {item}[[, please]]?"

- ``[[...]]`` marca a parte FIXA do chunk (o que você precisa memorizar).
- ``{nome}`` marca uma VARIÁVEL (o argumento da função).

Chamar o chunk devolve uma ``Phrase``: uma string em inglês que também
carrega a tradução (``.pt``) e o card do Anki pronto (``.cloze``).
"""

from __future__ import annotations

import inspect
import re
import string
from dataclasses import dataclass, field

_FIXED = re.compile(r"\[\[(.+?)\]\]")
_START, _END = "\x02", "\x03"
_REGISTRY: dict[str, "Chunk"] = {}


class Phrase(str):
    """Uma frase em inglês gerada por um chunk.

    Funciona como uma ``str`` normal (print, f-string, comparação), com
    atributos extras:

    - ``.en``     frase em inglês
    - ``.pt``     tradução/significado em português
    - ``.cloze``  frase no formato Cloze do Anki (parte fixa escondida)
    - ``.chunk``  o ``Chunk`` que gerou a frase
    """

    en: str
    pt: str
    cloze: str
    chunk: "Chunk"

    def __new__(cls, en: str, pt: str, cloze: str, chunk: "Chunk") -> "Phrase":
        obj = super().__new__(cls, en)
        obj.en, obj.pt, obj.cloze, obj.chunk = en, pt, cloze, chunk
        return obj

    def explain(self) -> str:
        """Texto completo: inglês, português, chunk fixo e card do Anki."""
        return (
            f"EN    : {self.en}\n"
            f"PT    : {self.pt}\n"
            f"CHUNK : {self.chunk.core}\n"
            f"ANKI  : {self.cloze}"
        )


@dataclass
class Chunk:
    """Um chunk reutilizável. É chamável como uma função."""

    name: str
    template: str
    pt: str
    category: str
    example: dict[str, str] = field(default_factory=dict)
    defaults: dict[str, str] = field(default_factory=dict)
    note: str = ""

    def __post_init__(self) -> None:
        self.slots = [
            f for _, f, _, _ in string.Formatter().parse(_FIXED.sub(r"\1", self.template)) if f
        ]
        params = [
            inspect.Parameter(
                s,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                default=self.defaults.get(s, inspect.Parameter.empty),
            )
            for s in self.slots
        ]
        self.__signature__ = inspect.Signature(params)
        self.__name__ = self.name
        self.__doc__ = self._build_doc()

    # ------------------------------------------------------------------ API
    def __call__(self, *args, **kwargs) -> Phrase:
        bound = self.__signature__.bind(*args, **kwargs)
        bound.apply_defaults()
        en_vals, pt_vals = {}, {}
        for slot, value in bound.arguments.items():
            en_vals[slot], pt_vals[slot] = _split_value(value)

        # Marca a parte fixa com sentinelas antes do format(), para que as
        # chaves do Cloze ({{c1::...}}) não sejam interpretadas pelo format.
        marked = _FIXED.sub(_mark, self.template).format(**en_vals).replace(_END + _START, "")
        en = marked.replace(_START, "").replace(_END, "")
        cloze = marked.replace(_START, "{{c1::").replace(_END, "}}")
        pt = self.pt.format(**pt_vals)
        return Phrase(_tidy(en), _tidy(pt), _tidy(cloze), self)

    def demo(self) -> Phrase:
        """Executa o chunk com as variáveis de exemplo."""
        return self(**self.example)

    @property
    def core(self) -> str:
        """Só a parte fixa do chunk, com as variáveis como ``...``."""
        return _FIXED.sub(r"\1", self.template).format(**{s: "..." for s in self.slots})

    @property
    def pattern(self) -> str:
        """Assinatura legível, ex.: ``could_i_get(item)``."""
        return f"{self.name}({', '.join(self.slots)})"

    # ------------------------------------------------------------ internals
    def _build_doc(self) -> str:
        lines = [self.core, "", f"PT: {self.pt}"]
        if self.note:
            lines += ["", self.note]
        if self.example:
            lines += ["", f"Exemplo: {self.pattern} -> {self.demo().en}"]
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"<chunk {self.pattern}: {self.core!r}>"


def chunk(
    name: str,
    template: str,
    pt: str,
    *,
    category: str,
    example: dict[str, str] | None = None,
    defaults: dict[str, str] | None = None,
    note: str = "",
) -> Chunk:
    """Cria e registra um chunk. Use isso para adicionar os seus."""
    if name in _REGISTRY:
        raise ValueError(f"Chunk duplicado: {name}")
    c = Chunk(name, template, pt, category, example or {}, defaults or {}, note)
    _REGISTRY[name] = c
    return c


def registry() -> dict[str, Chunk]:
    """Todos os chunks registrados, por nome."""
    return dict(_REGISTRY)


def get(name: str) -> Chunk:
    try:
        return _REGISTRY[name]
    except KeyError:
        raise KeyError(f"Chunk não encontrado: {name!r}. Use search() para procurar.") from None


def categories() -> list[str]:
    return sorted({c.category for c in _REGISTRY.values()})


def search(term: str) -> list[Chunk]:
    """Procura chunks pelo nome, inglês, português ou exemplo."""
    t = term.lower()
    return [
        c
        for c in _REGISTRY.values()
        if any(t in text.lower() for text in (c.name, c.core, c.pt, c.demo().en))
    ]


# ---------------------------------------------------------------- helpers
def a(noun: str) -> str:
    """Coloca o artigo certo: ``a("apple")`` -> ``"an apple"``."""
    first = noun.strip().lower()
    vowel_sound = first[:1] in "aeiou" and not first.startswith(("uni", "use", "eu", "one"))
    vowel_sound = vowel_sound or first.startswith(("hour", "honest", "mvp", "api", "sql", "sdk"))
    return f"{'an' if vowel_sound else 'a'} {noun}"


def _mark(m: re.Match) -> str:
    """Envolve a parte fixa em sentinelas (pontuação solta não vira cloze)."""
    text = m.group(1)
    return text if not re.search(r"\w", text) else f"{_START}{text}{_END}"


def _split_value(value) -> tuple[str, str]:
    """Aceita ``"water"`` ou ``("water", "água")`` (inglês, português)."""
    if isinstance(value, tuple) and len(value) == 2:
        return str(value[0]), str(value[1])
    return str(value), str(value)


def _tidy(text: str) -> str:
    """Remove espaços sobrando (variáveis vazias) e põe a 1ª letra em maiúscula."""
    text = re.sub(r"\s+([.,?!;:])", r"\1", re.sub(r"\s{2,}", " ", text)).strip()
    return text[:1].upper() + text[1:] if text else text
