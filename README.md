# AprenderIngl-schunks

**Aprenda inglês como você aprende programação.** Na Abordagem Lexical, você
não monta frases palavra por palavra: você usa *chunks*, blocos prontos de
palavras. Aqui cada chunk é uma **função Python**. Você passa as variáveis e
ela devolve a frase pronta, com a tradução e o card do Anki.

```python
>>> from chunks import *

>>> could_i_get("a glass of water")
'Could I get a glass of water, please?'

>>> could_i_get("a cup of coffee")
'Could I get a cup of coffee, please?'

>>> let_me_loop_in("John", "the backend issue")
'Let me loop in John to help us with the backend issue.'

>>> p = lets_touch_base(("tomorrow", "amanhã"), ("review the PR", "revisar o PR"))
>>> print(p.explain())
EN    : Let's touch base tomorrow to review the PR.
PT    : Vamos conversar rapidinho amanhã para revisar o PR.
CHUNK : Let's touch base ... to ....
ANKI  : {{c1::Let's touch base}} tomorrow{{c1:: to}} review the PR.
```

A analogia:

| Programação         | Inglês                                       |
|---------------------|----------------------------------------------|
| função              | chunk (`could_i_get`)                        |
| argumento/variável  | o que muda (`"a glass of water"`)            |
| corpo da função     | a parte fixa que você memoriza (`Could I get ..., please?`) |
| `help(funcao)`      | tradução, nota de uso e exemplo              |
| `import`            | `from chunks import *`                       |

## Instalação

Só precisa de Python 3.10+, sem nenhuma dependência.

```bash
git clone <este repositório>
cd AprenderIngl-schunks
pip install -e .        # opcional: habilita o comando `chunks`
```

Sem instalar, use `python -m chunks` no lugar de `chunks`.

## Usando no Python (REPL / Jupyter)

```python
from chunks import *

# Toda chamada devolve uma Phrase, que é uma str com atributos extras
p = i_have_a_blocker("the API credentials")
p.en      # 'I'm blocked by the API credentials.'
p.pt      # 'Estou travado por causa de the API credentials.'
p.cloze   # '{{c1::I'm blocked by}} the API credentials.'

# Variável traduzida: passe uma tupla (inglês, português)
could_i_get(("a coffee", "um café")).pt   # 'Pode me ver um café, por favor?'

# Argumentos nomeados também funcionam
a_ticket_to(kind="a round-trip", place="Chicago")

# Documentação do chunk
help(walk_me_through)

# Helper de artigo
could_i_get(a("apple"))     # 'Could I get an apple, please?'

# Explorar a biblioteca
categories()                # ['business', 'home', 'interview', 'meetings', 'mine', 'survival', 'tech']
search("deploy")            # procura em inglês, português, nome e exemplos
```

## Usando no terminal

```bash
chunks list                      # todas as funções, por categoria
chunks list meetings             # só uma categoria
chunks show walk_me_through      # documentação
chunks run could_i_get "a cup of coffee"
chunks run could_i_get "a cup of coffee|uma xícara de café"   # inglês|português
chunks play let_me_loop_in       # pergunta cada variável
chunks search bandwidth
chunks quiz                      # treino do dia (repetição espaçada)
chunks quiz interview -n 5
chunks anki cards.txt            # exporta tudo para o Anki
chunks anki home.txt home        # exporta só uma categoria
```

### Quiz com repetição espaçada

O `quiz` mostra a frase em português e as variáveis, e você digita a frase em
inglês. Maiúsculas e pontuação não contam. Ele usa o sistema de Leitner:

- acertou: o chunk sobe de caixa e volta em 2, 4, 8 e depois 16 dias;
- errou: o chunk volta para a caixa 1 e reaparece amanhã.

O progresso fica salvo em `~/.chunks_progress.json`.

### Anki

`chunks anki cards.txt` gera um arquivo pronto para o tipo de nota **Cloze**.
A parte fixa do chunk fica escondida e a variável continua visível, que é
exatamente o que você precisa memorizar. No Anki: *Arquivo > Importar*. As
tags (`chunks::meetings` etc.) já vêm no arquivo.

## Categorias incluídas (121 chunks)

| Categoria   | Conteúdo                                                        |
|-------------|-----------------------------------------------------------------|
| `survival`  | restaurante, transporte, compras, farmácia, hotel               |
| `home`      | rotina de casa, refeições, filho, hora de dormir                |
| `meetings`  | reuniões, apresentações, e-mail e Slack                         |
| `tech`      | dev, dados, IA, troubleshooting                                 |
| `business`  | negócios, SaaS, networking                                      |
| `interview` | entrevista tech, STAR e frases para ganhar tempo ou pedir para repetir |
| `data`      | matching, deduplicação, reconciliação, multi-tenant, eventos    |
| `mine`      | os seus chunks                                                  |

## Preparação para entrevista

Uma sessão completa para a vaga **Senior Software Engineer, Vendor Data
Platform** (DistantJob): 38 perguntas prováveis, em 6 etapas (recrutador,
experiência STAR, técnica, dados de fornecedores, system design e
encerramento). Cada pergunta tem:

- o que o entrevistador quer descobrir (em português);
- uma resposta modelo em inglês com os chunks marcados;
- dicas e perguntas que podem vir em seguida.

Nas respostas, `((...))` marca o que **você precisa trocar por um fato real
seu** (números, empresa, datas). Nunca diga algo que não consegue sustentar
com um exemplo.

```bash
python -m chunks entrevista                              # sessão completa
python -m chunks entrevista vendor_data_platform domain  # só uma etapa
```

Etapas: `screen`, `experience`, `technical`, `domain`, `design`, `closing`.
As perguntas ficam em `chunks/interviews/vendor_data_platform.py`. Para
preparar outra vaga, crie um arquivo parecido na mesma pasta.

## App web para o celular (`web/`)

Um app em React + TypeScript + Vite com a mesma biblioteca e o mesmo motor:

- **Biblioteca:** busca (com ou sem acento), filtro por categoria e a parte
  fixa de cada chunk destacada.
- **Chunk:** você digita as variáveis e vê a frase montada na hora, com
  tradução, pronúncia (🔊, voz do próprio celular) e o card do Anki para copiar.
- **Treinar:** o mesmo quiz com repetição espaçada. O progresso fica salvo no
  celular.
- **Entrevista:** simulação da entrevista. O app lê a pergunta em voz alta, você
  responde falando e depois compara com a resposta modelo (que também pode ser
  ouvida, para treinar *shadowing*).
- **Meus:** crie chunks pelo celular (`[[fixo]] {variável}`) e baixe o
  arquivo do Anki.
- Funciona offline e pode ser instalado na tela inicial ("Adicionar à tela de
  início" no Safari ou Chrome).

```bash
cd web
npm ci
npm run dev        # abre em http://localhost:5173 (e na rede local, para testar no celular)
npm test           # testes (inclui conferir que o TS gera o mesmo que o Python)
npm run build      # gera web/dist
```

A biblioteca do app vem de `web/src/data/chunks.json`, gerado a partir do
Python. Depois de criar ou editar chunks em Python, rode:

```bash
python -m chunks json
```

(Os testes do Python falham se você esquecer.)

**Publicar no GitHub Pages:** o workflow `.github/workflows/web.yml` testa e
publica o app a cada push na branch `main`. Antes, ative em *Settings › Pages ›
Source: GitHub Actions*. O endereço fica
`https://<seu-usuário>.github.io/AprenderIngl-schunks/`.

## Criando os seus chunks

Encontrou uma frase boa num vídeo, numa reunião ou numa documentação? Crie a
função em `chunks/library/my_chunks.py`:

```python
we_should_consider = chunk(
    "we_should_consider",                       # nome da função
    "[[I think we should consider]] {option}.", # [[fixo]] e {variável}
    "Acho que devíamos considerar {option}.",   # tradução com as mesmas variáveis
    category="mine",
    example={"option": "using a cache"},
    note="Jeito educado de sugerir algo numa reunião.",  # opcional
)
```

- `[[...]]` marca a parte fixa: é o que o Anki esconde e o que o quiz cobra.
- `{nome}` vira um parâmetro da função.
- `defaults={"when": "later"}` torna uma variável opcional.

Rode os testes depois de adicionar chunks. Eles conferem se a tradução usa as
mesmas variáveis do inglês:

```bash
python -m unittest discover -s tests
```

## Rotina sugerida (15 min/dia)

1. **Manhã:** `chunks quiz -n 10`.
2. **Durante o dia:** use 3 chunks de verdade (reunião, Slack, com seu filho).
   Use `chunks run` para montar a frase antes.
3. **Noite:** adicione em `my_chunks.py` 1 chunk novo que você ouviu ou leu.
