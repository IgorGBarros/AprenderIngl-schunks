"""SEUS chunks. Adicione aqui as frases que você encontrar no dia a dia.

Receita (igual a criar uma função):

1. Escolha um nome em snake_case: ``we_should_consider``.
2. Escreva o template em inglês:
   - ``[[...]]`` = parte fixa (o que você quer memorizar)
   - ``{variavel}`` = o que muda a cada uso
3. Escreva a tradução em português com as mesmas variáveis.
4. Dê um exemplo de uso.

Depois é só chamar: ``we_should_consider("using a cache")``.
"""

from chunks.core import chunk

C = "mine"

we_should_consider = chunk(
    "we_should_consider",
    "[[I think we should consider]] {option}.",
    "Acho que devíamos considerar {option}.",
    category=C,
    example={"option": "using a cache"},
)
