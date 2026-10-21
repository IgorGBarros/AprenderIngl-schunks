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

### O que você precisa

| Para usar | Precisa de | Como conferir |
|---|---|---|
| Biblioteca e terminal (`python -m chunks`) | Python 3.10 ou mais novo | `python --version` |
| App web (`web/`) | Node.js 20.19 ou mais novo | `node --version` |
| Gerar entrevistas de qualquer vaga | [Ollama](https://ollama.com/download) e um modelo | `ollama --version` |

O Python não precisa de nenhum pacote externo: tudo usa a biblioteca padrão.

### 1. Python

```bash
git clone https://github.com/IgorGBarros/AprenderIngl-schunks.git
cd AprenderIngl-schunks

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt  # instala o projeto e o comando `chunks`
chunks list                      # testa: lista os chunks
```

Sem instalar nada, `python -m chunks` funciona direto da pasta do projeto, e
faz o mesmo que o comando `chunks`.

No **Windows (PowerShell)**:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
chunks list
```

Se aparecer *"O termo 'chunks' não é reconhecido"*:

- Confira se você está na pasta do projeto, a que tem o `pyproject.toml` e o
  `requirements.txt` (`dir pyproject.toml`). Dentro da subpasta `chunks` a
  instalação não funciona, e o `python -m chunks` também não.
- Rode `python -m pip install -r requirements.txt` com o venv ativado: o
  comando `chunks` só existe depois disso.
- Se o PowerShell bloquear o `Activate.ps1`, rode uma vez
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

### 2. App web (opcional)

```bash
cd web
npm ci            # instala as dependências (versões exatas do package-lock.json)
npm run dev       # abre em http://localhost:5173
```

Se o `npm ci` falhar com `Cannot read properties of null (reading 'edgesOut')`,
é um bug do npm 10: atualize com `npm install -g npm@11` e rode de novo.

### 3. Ollama (opcional, para entrevistas de qualquer vaga)

1. Baixe e instale em https://ollama.com/download (Windows, macOS ou Linux).
2. Baixe um modelo (uns 4,7 GB; 8 GB de RAM ou mais):

   ```bash
   ollama pull qwen2.5:7b
   ```

   Com pouca memória, use `llama3.2:3b` (2 GB), que é mais rápido mas erra mais.
3. Confira: `ollama list` deve mostrar o modelo. O Ollama fica rodando em
   segundo plano depois de instalado (se não estiver, rode `ollama serve`).

Para rodar os testes: `python -m unittest` (Python) e `cd web && npm test` (app).

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

## Preparação para entrevista (qualquer vaga)

Cada sessão de entrevista tem as perguntas prováveis, divididas em etapas
(recrutador, experiência STAR, técnica, específicas da vaga, caso prático e
encerramento). Cada pergunta traz:

- o que o entrevistador quer descobrir (em português);
- uma resposta modelo em inglês com os chunks marcados;
- dicas e perguntas que podem vir em seguida.

Nas respostas, `((...))` marca o que **você precisa trocar por um fato real
seu** (números, empresa, datas). Nunca diga algo que não consegue sustentar
com um exemplo.

Sessões incluídas:

| Sessão | Para quê |
|---|---|
| `general` | Perguntas que caem em quase qualquer vaga. Não precisa de LLM. |
| `vendor_data_platform` | Exemplo completo, feito à mão, para uma vaga real de Senior Software Engineer. |
| as suas | Geradas para **qualquer vaga** com o Ollama (abaixo). |

```bash
python -m chunks entrevista                      # escolhe a sessão numa lista
python -m chunks entrevista general screen       # sessão e etapa direto
```

### Gerar a entrevista de qualquer vaga com o Ollama

O [Ollama](https://ollama.com) roda um modelo de linguagem no seu computador,
de graça e sem mandar seus dados para fora.

1. Instale o Ollama e baixe um modelo. O `qwen2.5:7b` funciona bem; modelos
   menores (`llama3.2:3b`) são mais rápidos mas erram mais o formato.

   ```bash
   ollama pull qwen2.5:7b
   ```

2. (Opcional, recomendado) Copie `perfil.exemplo.md` para `perfil.md` e
   preencha com fatos reais seus. Ele fica fora do git. Com o perfil, as
   respostas modelo já vêm com a sua história; sem ele, tudo sobre você
   vem como `((preencha))`.

3. Salve a descrição da vaga num arquivo de texto e gere:

   ```bash
   python -m chunks vaga vaga.txt
   python -m chunks vaga vaga.txt --modelo llama3.1:8b -n 7   # outro modelo, 7 perguntas por etapa
   python -m chunks vaga -     # cola a vaga no terminal e termina com Ctrl+D (Ctrl+Z e Enter no Windows)
   ```

A sessão é salva em `chunks/interviews/generated/` e aparece no
`python -m chunks entrevista`. Para levá-la ao app web, rode
`python -m chunks json` (ou importe o `.json` direto no app).

Para usar outro endereço ou modelo por padrão: variáveis `OLLAMA_HOST` e
`OLLAMA_MODEL`. Os prompts ficam em `chunks/interviews/prompts.py` e são os
mesmos no terminal e no app.

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
  ouvida, para treinar *shadowing*). Em **+ Nova vaga** você cola qualquer vaga
  e o app gera a entrevista com o seu Ollama, ou importa um `.json` gerado no
  terminal.
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

**Ollama no app:** com o app rodando em `localhost` (`npm run dev`), ele fala
com o Ollama sem configuração. Para gerar pelo celular, na mesma rede Wi-Fi,
inicie o Ollama aceitando conexões da rede e de outros endereços:

```bash
OLLAMA_HOST=0.0.0.0 OLLAMA_ORIGINS="*" ollama serve
```

e, no app, em *Configurar Ollama*, use `http://IP-DO-SEU-COMPUTADOR:11434`.

A biblioteca do app vem de `web/src/data/`, gerado a partir do Python. Depois de criar ou editar chunks em Python, rode:

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
