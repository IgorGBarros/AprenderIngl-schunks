"""Entrevista de emprego tech (método STAR e small talk)."""

from chunks.core import chunk

C = "interview"

i_currently_work_as = chunk(
    "i_currently_work_as",
    "[[I currently work as]] {role} [[at]] {company}.",
    "Atualmente trabalho como {role} {company}.",
    category=C,
    examples=[
        {"role": ("a Data Analyst", "analista de dados"), "company": ("PGBA", "na PGBA")},
        {"role": ("a backend developer", "desenvolvedor backend"), "company": ("a fintech", "numa fintech")},
        {"role": ("a team lead", "líder de equipe"), "company": ("an oil company", "numa petroleira")},
    ],
)
ive_been_working_in = chunk(
    "ive_been_working_in",
    "[[I've been working in]] {field} [[for]] {years}.",
    "Trabalho com {field} há {years}.",
    category=C,
    examples=[
        {"field": ("data and software development", "dados e desenvolvimento de software"), "years": ("ten years", "dez anos")},
        {"field": ("tech", "tecnologia"), "years": ("about six years", "uns seis anos")},
        {"field": ("finance", "finanças"), "years": ("a long time", "bastante tempo")},
    ],
)
ive_been_using_extensively_for = chunk(
    "ive_been_using_extensively_for",
    "[[I've been using]] {tool} [[extensively for]] {purpose}.",
    "Tenho usado {tool} bastante para {purpose}.",
    category=C,
    examples=[
        {"tool": ("Python", "Python"), "purpose": ("data pipelines", "pipelines de dados")},
        {"tool": ("Django", "Django"), "purpose": ("web applications", "aplicações web")},
        {"tool": ("Power BI", "Power BI"), "purpose": ("dashboards", "dashboards")},
    ],
)
im_particularly_comfortable_with = chunk(
    "im_particularly_comfortable_with",
    "[[I'm particularly comfortable with]] {skill}.",
    "Tenho bastante facilidade {skill}.",
    category=C,
    examples=[
        {"skill": ("SQL and Django", "com SQL e Django")},
        {"skill": ("data modeling", "com modelagem de dados")},
        {"skill": ("talking to clients", "para conversar com clientes")},
    ],
)
im_now_looking_to = chunk(
    "im_now_looking_to",
    "[[I'm now looking to]] {goal}[[, and that's what brought me here today]].",
    "Agora quero {goal}, e foi isso que me trouxe aqui hoje.",
    category=C,
    examples=[
        {"goal": ("take the next step in my career", "dar o próximo passo na carreira")},
        {"goal": ("work with an international team", "trabalhar com um time internacional")},
        {"goal": ("focus on one product", "me dedicar a um produto")},
    ],
)
what_really_drives_me_is = chunk(
    "what_really_drives_me_is",
    "[[What really drives me is]] {motivation}.",
    "O que realmente me motiva é {motivation}.",
    category=C,
    examples=[
        {"motivation": ("solving real business problems with data", "resolver problemas reais de negócio com dados")},
        {"motivation": ("building products from scratch", "criar produtos do zero")},
        {"motivation": ("seeing people use what I built", "ver as pessoas usando o que eu construí")},
    ],
)
im_a_big_believer_in = chunk(
    "im_a_big_believer_in",
    "[[I'm a big believer in]] {idea}.",
    "Eu acredito muito {idea}.",
    category=C,
    examples=[
        {"idea": ("automated testing", "em testes automatizados")},
        {"idea": ("learning by doing", "em aprender fazendo")},
        {"idea": ("small, frequent releases", "em entregas pequenas e frequentes")},
    ],
)
the_situation_was = chunk(
    "the_situation_was",
    "[[The situation was that]] {context}.",
    "A situação era a seguinte: {context}.",
    category=C,
    examples=[
        {"context": ("our reports took two days to generate", "os nossos relatórios levavam dois dias para sair")},
        {"context": ("the client was about to cancel", "o cliente estava prestes a cancelar")},
        {"context": ("we had no tests at all", "não tínhamos nenhum teste")},
    ],
    note="STAR — S (Situation).",
)
my_task_was_to = chunk(
    "my_task_was_to",
    "[[My task was to]] {task}.",
    "A minha tarefa era {task}.",
    category=C,
    examples=[
        {"task": ("automate the whole pipeline", "automatizar o pipeline inteiro")},
        {"task": ("find the bottleneck", "encontrar o gargalo")},
        {"task": ("migrate the data without downtime", "migrar os dados sem deixar o sistema fora do ar")},
    ],
    note="STAR — T (Task).",
)
what_i_did_was = chunk(
    "what_i_did_was",
    "[[What I did was]] {action}.",
    "O que eu fiz foi {action}.",
    category=C,
    examples=[
        {"action": ("build an ETL with Airflow", "montar um ETL com Airflow")},
        {"action": ("talk to each user first", "conversar com cada usuário antes")},
        {"action": ("split the problem into smaller parts", "dividir o problema em partes menores")},
    ],
    note="STAR — A (Action).",
)
as_a_result = chunk(
    "as_a_result",
    "[[As a result]], {result}.",
    "Como resultado, {result}.",
    category=C,
    examples=[
        {"result": ("we cut the processing time by 80%", "reduzimos o tempo de processamento em 80%")},
        {"result": ("the client renewed the contract", "o cliente renovou o contrato")},
        {"result": ("errors dropped to almost zero", "os erros caíram quase a zero")},
    ],
    note="STAR — R (Result).",
)
can_you_tell_me_about_a_time_when = chunk(
    "can_you_tell_me_about_a_time_when",
    "[[Can you tell me about a time when]] {situation}[[?]]",
    "Você pode me contar de uma vez em que {situation}?",
    category=C,
    examples=[
        {"situation": ("you had to deal with a difficult stakeholder", "teve que lidar com um stakeholder difícil")},
        {"situation": ("you made a mistake", "cometeu um erro")},
        {"situation": ("you had to learn something quickly", "precisou aprender algo rápido")},
    ],
    note="Pergunta clássica do entrevistador. Reconheça e responda com STAR.",
)
sure_let_me_think_of_a_good_example = chunk(
    "sure_let_me_think_of_a_good_example",
    "[[Sure, let me think of a good example.]]",
    "Claro, deixa eu pensar num bom exemplo.",
    category=C,
    note="Ganha tempo sem parecer travado.",
)
whats_your_experience_with = chunk(
    "whats_your_experience_with",
    "[[What's your experience with]] {thing}[[?]]",
    "Qual é a sua experiência com {thing}?",
    category=C,
    examples=[
        {"thing": ("cloud platforms", "plataformas de nuvem")},
        {"thing": ("React", "React")},
        {"thing": ("remote work", "trabalho remoto")},
    ],
)
how_do_you_stay_up_to_date_with = chunk(
    "how_do_you_stay_up_to_date_with",
    "[[How do you stay up to date with]] {topic}[[?]]",
    "Como você se mantém atualizado {topic}?",
    category=C,
    examples=[
        {"topic": ("new AI tools", "sobre as novas ferramentas de IA")},
        {"topic": ("the industry", "no mercado")},
        {"topic": ("Python", "em Python")},
    ],
)
im_curious_to_know = chunk(
    "im_curious_to_know",
    "[[I'm curious to know]] {question}.",
    "Tenho curiosidade de saber {question}.",
    category=C,
    examples=[
        {"question": ("what success looks like in this role", "o que seria sucesso nesta função")},
        {"question": ("how the team is organized", "como o time é organizado")},
        {"question": ("what the biggest challenge is right now", "qual é o maior desafio agora")},
    ],
)
thank_you_for_the_opportunity = chunk(
    "thank_you_for_the_opportunity",
    "[[Thank you for the opportunity]][[. It was great chatting with you]].",
    "Obrigado pela oportunidade. Foi ótimo conversar com você.",
    category=C,
)

# --- Sobrevivência: ganhar tempo, pedir para repetir, ser honesto -----------
could_you_rephrase = chunk(
    "could_you_rephrase",
    "[[Sorry, could you rephrase]] {what}[[?]]",
    "Desculpe, você pode reformular {what}?",
    category=C,
    examples=[
        {"what": ("the question", "a pergunta")},
        {"what": ("that", "isso")},
        {"what": ("the last part", "a última parte")},
    ],
    note="Muito melhor do que responder outra coisa. Ninguém perde pontos por isso.",
)
just_to_make_sure_i_understood = chunk(
    "just_to_make_sure_i_understood",
    "[[Just to make sure I understood, you're asking about]] {topic}[[?]]",
    "Só para ter certeza de que entendi, você está perguntando sobre {topic}?",
    category=C,
    examples=[
        {"topic": ("how we handle duplicate vendors", "como tratamos fornecedores duplicados")},
        {"topic": ("my last project", "o meu último projeto")},
        {"topic": ("the database design", "a modelagem do banco")},
    ],
)
thats_a_great_question = chunk(
    "thats_a_great_question",
    "[[That's a great question. Let me think about]] {topic} [[for a second]].",
    "Ótima pergunta. Deixa eu pensar um segundo {topic}.",
    category=C,
    examples=[
        {"topic": ("the trade-offs", "nos prós e contras")},
        {"topic": ("it", "nisso")},
        {"topic": ("the best example", "no melhor exemplo")},
    ],
    note="Ganha três segundos para organizar a resposta.",
)
i_havent_used_but = chunk(
    "i_havent_used_but",
    "[[I haven't used]] {tool} [[in production, but]] {bridge}.",
    "Não usei {tool} em produção, mas {bridge}.",
    category=C,
    examples=[
        {"tool": ("Azure", "Azure"), "bridge": ("I've used the equivalent services on AWS", "já usei os serviços equivalentes na AWS")},
        {"tool": ("Angular", "Angular"), "bridge": ("I work with React and TypeScript every day", "trabalho com React e TypeScript todo dia")},
        {"tool": ("Kafka", "Kafka"), "bridge": ("I've built queues with RabbitMQ", "já montei filas com RabbitMQ")},
    ],
    note="Honestidade + ponte para o que você sabe. Nunca finja.",
)
the_trade_off_is = chunk(
    "the_trade_off_is",
    "[[The trade-off is]] {a} [[versus]] {b}.",
    "O dilema é {a} versus {b}.",
    category=C,
    examples=[
        {"a": ("isolation", "isolamento"), "b": ("cost", "custo")},
        {"a": ("speed", "velocidade"), "b": ("accuracy", "precisão")},
        {"a": ("flexibility", "flexibilidade"), "b": ("simplicity", "simplicidade")},
    ],
)
before_i_start_can_i_ask = chunk(
    "before_i_start_can_i_ask",
    "[[Before I start, can I ask]] {question}[[?]]",
    "Antes de começar, posso perguntar {question}?",
    category=C,
    examples=[
        {"question": ("how many records we're talking about", "de quantos registros estamos falando")},
        {"question": ("who the users are", "quem são os usuários")},
        {"question": ("what the budget is", "qual é o orçamento")},
    ],
    note="Em system design, sempre pergunte antes de desenhar.",
)
lets_start_with_the_big_picture = chunk(
    "lets_start_with_the_big_picture",
    "[[Let me start with the big picture, and then we can zoom in on]] {part}.",
    "Deixa eu começar pela visão geral, e depois a gente detalha {part}.",
    category=C,
    examples=[
        {"part": ("the matching step", "a etapa de matching")},
        {"part": ("the database", "o banco de dados")},
        {"part": ("whatever you prefer", "o que você preferir")},
    ],
)
