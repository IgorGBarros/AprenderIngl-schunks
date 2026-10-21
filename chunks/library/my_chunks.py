"""SEUS chunks. Adicione aqui as frases que você encontrar no dia a dia.

Receita (igual a criar uma função):

1. Escolha um nome em snake_case: ``we_should_consider``.
2. Escreva o template em inglês:
   - ``[[...]]`` = parte fixa (o que você quer memorizar)
   - ``{variavel}`` = o que muda a cada uso
3. Escreva a tradução em português com as mesmas variáveis. Deixe artigos e
   preposições ("o", "a", "do", "para a") dentro da tradução de cada variável:
   assim a frase fica natural em qualquer gênero.
4. (Opcional) A versão em alemão em ``de=``, com as mesmas variáveis.
5. Dê uns 10 exemplos com ``ex()``: uma linha por exemplo,
   ``"inglês | português | alemão"`` (``;;`` separa as variáveis).

Depois é só chamar: ``we_should_consider("using a cache")``.
"""

from chunks.core import chunk, ex

C = "mine"

we_should_consider = chunk(
    "we_should_consider",
    "[[I think we should consider]] {option}.",
    "Acho que devíamos considerar {option}.",
    de="[[Ich finde, wir sollten]] {option} [[in Betracht ziehen]].",
    category=C,
    examples=ex(
        "option",
        "using a cache | usar um cache | den Einsatz eines Caches",
        "a different approach | outra abordagem | einen anderen Ansatz",
        "hiring a contractor | contratar um freelancer | die Einstellung eines Freelancers",
        "a smaller scope | um escopo menor | einen kleineren Umfang",
        "moving to the cloud | migrar para a nuvem | den Umzug in die Cloud",
        "a monthly plan | um plano mensal | ein Monatsabo",
        "open-source tools | ferramentas open source | Open-Source-Tools",
        "a second opinion | uma segunda opinião | eine zweite Meinung",
        "delaying the launch | adiar o lançamento | eine Verschiebung des Launches",
        "a pilot project | um projeto piloto | ein Pilotprojekt",
    ),
)
