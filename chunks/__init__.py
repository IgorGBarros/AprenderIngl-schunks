"""chunks — aprenda inglês como você aprende programação.

Cada chunk (bloco de palavras) é uma FUNÇÃO. Você passa as variáveis e
recebe a frase pronta:

    >>> from chunks import *
    >>> could_i_get("a glass of water")
    'Could I get a glass of water, please?'
    >>> could_i_get(("a coffee", "um café")).pt
    'Pode me ver um café, por favor?'
    >>> print(lets_touch_base("tomorrow", "review the PR").explain())
"""

from chunks.core import Chunk, Phrase, a, categories, chunk, get, registry, search
from chunks.library.business import *  # noqa: F401,F403
from chunks.library.home import *  # noqa: F401,F403
from chunks.library.interview import *  # noqa: F401,F403
from chunks.library.meetings import *  # noqa: F401,F403
from chunks.library.my_chunks import *  # noqa: F401,F403
from chunks.library.survival import *  # noqa: F401,F403
from chunks.library.tech import *  # noqa: F401,F403

__all__ = ["Chunk", "Phrase", "a", "categories", "chunk", "get", "registry", "search", *registry()]
