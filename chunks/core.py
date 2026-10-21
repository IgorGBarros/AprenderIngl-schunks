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

    @property
    def blanks(self) -> str:
        """Dica do quiz: cada letra da parte fixa vira ``_`` (mostra quantas palavras faltam)."""
        return re.sub(
            r"\{\{c1::(.*?)\}\}", lambda m: re.sub(r"[A-Za-z0-9']", "_", m.group(1)), self.cloze
        )

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
    examples: list[dict] = field(default_factory=list)
    """Exemplos prontos: {variável: "inglês"} ou {variável: ("inglês", "português")}."""
    defaults: dict[str, str] = field(default_factory=dict)
    note: str = ""

    def __post_init__(self) -> None:
        self.slots = [
            f for _, f, _, _ in string.Formatter().parse(_FIXED.sub(r"\1", self.template)) if f
        ]
        required = set(self.slots) - set(self.defaults)
        for i, ex in enumerate(self.examples, 1):
            if not required <= set(ex) <= set(self.slots):
                raise ValueError(
                    f"{self.name}: o exemplo {i} precisa das variáveis {sorted(required)}, "
                    f"e só pode usar {self.slots} (recebeu {sorted(ex)})"
                )
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

    @property
    def example(self) -> dict:
        """O primeiro exemplo (o principal)."""
        return self.examples[0] if self.examples else {}

    def demo(self) -> Phrase:
        """Executa o chunk com as variáveis do primeiro exemplo."""
        return self(**self.example)

    def demos(self) -> list[Phrase]:
        """Todos os exemplos prontos, já montados."""
        return [self(**ex) for ex in self.examples] or [self()]

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
        if self.examples:
            lines += ["", "Exemplos:"]
            lines += [f"  {p.en}  —  {p.pt}" for p in self.demos()]
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"<chunk {self.pattern}: {self.core!r}>"


def chunk(
    name: str,
    template: str,
    pt: str,
    *,
    category: str,
    examples: list[dict] | None = None,
    example: dict | None = None,
    defaults: dict[str, str] | None = None,
    note: str = "",
) -> Chunk:
    """Cria e registra um chunk. Use isso para adicionar os seus.

    ``examples`` é uma lista de exemplos; ``example`` (um só) também é aceito.
    """
    if name in _REGISTRY:
        raise ValueError(f"Chunk duplicado: {name}")
    all_examples = list(examples or []) or ([example] if example else [])
    c = Chunk(name, template, pt, category, all_examples, defaults or {}, note)
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
    """Procura chunks pelo nome, inglês, português ou qualquer exemplo."""
    t = term.lower()
    return [
        c
        for c in _REGISTRY.values()
        if any(
            t in text.lower()
            for text in (c.name, c.core, c.pt, *(s for p in c.demos() for s in (p.en, p.pt)))
        )
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
