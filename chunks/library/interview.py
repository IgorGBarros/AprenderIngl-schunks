"""Entrevista de emprego tech (método STAR e small talk)."""

from chunks.core import chunk

C = "interview"

i_currently_work_as = chunk(
    "i_currently_work_as",
    "[[I currently work as]] {role} [[at]] {company}.",
    "Atualmente trabalho como {role} na {company}.",
    category=C,
    example={"role": "a Data Analyst", "company": "PGBA"},
)
ive_been_working_in = chunk(
    "ive_been_working_in",
    "[[I've been working in]] {field} [[for]] {years}.",
    "Trabalho com {field} há {years}.",
    category=C,
    example={"field": "data and software development", "years": "ten years"},
)
ive_been_using_extensively_for = chunk(
    "ive_been_using_extensively_for",
    "[[I've been using]] {tool} [[extensively for]] {purpose}.",
    "Tenho usado {tool} bastante para {purpose}.",
    category=C,
    example={"tool": "Python", "purpose": "data pipelines"},
)
im_particularly_comfortable_with = chunk(
    "im_particularly_comfortable_with",
    "[[I'm particularly comfortable with]] {skill}.",
    "Tenho bastante facilidade com {skill}.",
    category=C,
    example={"skill": "SQL and Django"},
)
im_now_looking_to = chunk(
    "im_now_looking_to",
    "[[I'm now looking to]] {goal}[[, and that's what brought me here today]].",
    "Agora estou buscando {goal}, e foi isso que me trouxe aqui hoje.",
    category=C,
    example={"goal": "take the next step in my career"},
)
what_really_drives_me_is = chunk(
    "what_really_drives_me_is",
    "[[What really drives me is]] {motivation}.",
    "O que realmente me motiva é {motivation}.",
    category=C,
    example={"motivation": "solving real business problems with data"},
)
im_a_big_believer_in = chunk(
    "im_a_big_believer_in",
    "[[I'm a big believer in]] {idea}.",
    "Eu acredito muito em {idea}.",
    category=C,
    example={"idea": "automated testing"},
)
the_situation_was = chunk(
    "the_situation_was",
    "[[The situation was that]] {context}.",
    "A situação era que {context}.",
    category=C,
    example={"context": "our reports took two days to generate"},
    note="STAR — S (Situation).",
)
my_task_was_to = chunk(
    "my_task_was_to",
    "[[My task was to]] {task}.",
    "Minha tarefa era {task}.",
    category=C,
    example={"task": "automate the whole pipeline"},
    note="STAR — T (Task).",
)
what_i_did_was = chunk(
    "what_i_did_was",
    "[[What I did was]] {action}.",
    "O que eu fiz foi {action}.",
    category=C,
    example={"action": "build an ETL with Airflow"},
    note="STAR — A (Action).",
)
as_a_result = chunk(
    "as_a_result",
    "[[As a result]], {result}.",
    "Como resultado, {result}.",
    category=C,
    example={"result": "we cut the processing time by 80%"},
    note="STAR — R (Result).",
)
can_you_tell_me_about_a_time_when = chunk(
    "can_you_tell_me_about_a_time_when",
    "[[Can you tell me about a time when]] {situation}[[?]]",
    "Pode me contar sobre uma vez em que {situation}?",
    category=C,
    example={"situation": "you had to deal with a difficult stakeholder"},
    note="Pergunta clássica do entrevistador — reconheça e responda com STAR.",
)
sure_let_me_think_of_a_good_example = chunk(
    "sure_let_me_think_of_a_good_example",
    "[[Sure, let me think of a good example.]]",
    "Claro, deixa eu pensar em um bom exemplo.",
    category=C,
    note="Ganha tempo sem parecer travado.",
)
whats_your_experience_with = chunk(
    "whats_your_experience_with",
    "[[What's your experience with]] {thing}[[?]]",
    "Qual é a sua experiência com {thing}?",
    category=C,
    example={"thing": "cloud platforms"},
)
how_do_you_stay_up_to_date_with = chunk(
    "how_do_you_stay_up_to_date_with",
    "[[How do you stay up to date with]] {topic}[[?]]",
    "Como você se mantém atualizado em {topic}?",
    category=C,
    example={"topic": "new AI tools"},
)
im_curious_to_know = chunk(
    "im_curious_to_know",
    "[[I'm curious to know]] {question}.",
    "Tenho curiosidade de saber {question}.",
    category=C,
    example={"question": "what success looks like in this role"},
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
    example={"what": ("the question", "a pergunta")},
    note="Muito melhor do que responder outra coisa. Ninguém perde pontos por isso.",
)
just_to_make_sure_i_understood = chunk(
    "just_to_make_sure_i_understood",
    "[[Just to make sure I understood, you're asking about]] {topic}[[?]]",
    "Só para ter certeza de que entendi, você está perguntando sobre {topic}?",
    category=C,
    example={"topic": "how we handle duplicate vendors"},
)
thats_a_great_question = chunk(
    "thats_a_great_question",
    "[[That's a great question. Let me think about]] {topic} [[for a second]].",
    "Ótima pergunta. Deixa eu pensar um segundo sobre {topic}.",
    category=C,
    example={"topic": "the trade-offs"},
    note="Ganha 3 segundos para organizar a resposta.",
)
i_havent_used_but = chunk(
    "i_havent_used_but",
    "[[I haven't used]] {tool} [[in production, but]] {bridge}.",
    "Não usei {tool} em produção, mas {bridge}.",
    category=C,
    example={
        "tool": "Azure",
        "bridge": ("I've used the equivalent services on AWS", "usei os serviços equivalentes na AWS"),
    },
    note="Honestidade + ponte para o que você sabe. Nunca finja.",
)
the_trade_off_is = chunk(
    "the_trade_off_is",
    "[[The trade-off is]] {a} [[versus]] {b}.",
    "O trade-off é {a} versus {b}.",
    category=C,
    example={"a": ("isolation", "isolamento"), "b": ("cost", "custo")},
)
before_i_start_can_i_ask = chunk(
    "before_i_start_can_i_ask",
    "[[Before I start, can I ask]] {question}[[?]]",
    "Antes de começar, posso perguntar {question}?",
    category=C,
    example={"question": "how many records we're talking about"},
    note="Em system design, sempre pergunte antes de desenhar.",
)
lets_start_with_the_big_picture = chunk(
    "lets_start_with_the_big_picture",
    "[[Let me start with the big picture, and then we can zoom in on]] {part}.",
    "Deixa eu começar pela visão geral, e depois a gente detalha {part}.",
    category=C,
    example={"part": "the matching step"},
)
