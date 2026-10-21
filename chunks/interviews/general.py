"""Entrevista geral: as perguntas que aparecem em quase qualquer vaga (sem LLM)."""

from chunks.interviews import Question, Session, Stage, register

Q = Question

STAGES = (
    Stage(
        "screen",
        "Recrutador",
        "Perguntas da primeira conversa, iguais em quase toda empresa.",
    ),
    Stage(
        "experience",
        "Experiência (STAR)",
        "Comportamentais. Tenha 4 ou 5 histórias reais prontas: elas servem para várias perguntas.",
    ),
    Stage(
        "technical",
        "Como você trabalha",
        "Perguntas sobre o seu jeito de trabalhar, aprender e lidar com problemas.",
    ),
    Stage(
        "closing",
        "Suas perguntas e encerramento",
        "Nunca termine sem perguntas. Feche com uma frase curta e positiva.",
    ),
)

QUESTIONS = (
    Q(
        "about_you",
        "screen",
        "Could you tell me a little bit about yourself?",
        "Seu pitch de 60 a 90 segundos: quem você é profissionalmente e por que faz sentido para a vaga.",
        "Sure! [[I've been working in]] ((your field)) [[for]] ((number of years)). "
        "[[I currently work as]] ((your role)) at ((company)), [[where I'm responsible for]] "
        "((two main responsibilities)). "
        "[[Prior to that]], ((previous experience in one sentence)). "
        "[[What really drives me is]] ((what motivates you)), "
        "[[and that's why I'm excited about this role]].",
        tips=(
            "Presente → passado → futuro → ligação com a vaga.",
            "Não conte a vida toda. É um trailer, não o filme.",
        ),
    ),
    Q(
        "why_company",
        "screen",
        "Why do you want to work with us?",
        "Se você pesquisou a empresa e se o interesse é real.",
        "[[I've been following]] ((something specific about the company: product, mission, news)), "
        "and [[what caught my attention]] was ((a concrete detail)). "
        "[[On top of that]], the role [[is a great match for]] my experience with ((your relevant skill)). "
        "[[I believe I can contribute]] from day one.",
        tips=("Cite algo específico da empresa. 'É uma ótima empresa' não conta.",),
    ),
    Q(
        "why_leave",
        "screen",
        "Why are you looking for a new opportunity?",
        "Se existe algum problema e se você vai ficar. Querem uma motivação positiva.",
        "[[To be honest]], I'm not running away from anything. I've learned a lot in my current role, "
        "but [[I'm looking to]] ((what you want: more ownership, an international team, a bigger "
        "product)). [[I believe]] this role is the right next step for that.",
        tips=("Nunca fale mal do emprego atual.",),
    ),
    Q(
        "strengths",
        "screen",
        "What would you say is your greatest strength?",
        "Autoconhecimento. Uma força, com prova.",
        "[[I'd say]] my biggest strength is ((one strength)). [[For instance]], ((a short real example "
        "that proves it)). [[That's why]] ((how it helps in this role)).",
        tips=("Uma força só, com um exemplo. Lista de adjetivos não convence.",),
    ),
    Q(
        "weakness",
        "screen",
        "What's your biggest weakness?",
        "Honestidade e maturidade: um ponto real que você já está melhorando.",
        "[[To be honest]], ((a real weakness that doesn't block the job)). "
        "[[I've been working on it by]] ((concrete action)), and [[I've already noticed]] "
        "((a real improvement)).",
        tips=(
            "Evite 'sou perfeccionista'. Todo recrutador já ouviu.",
            "Para quem está aprendendo inglês, falar do inglês com o plano de estudo é uma boa resposta.",
        ),
    ),
    Q(
        "salary",
        "screen",
        "What are your salary expectations?",
        "Se você cabe no orçamento.",
        "Based on my research for similar roles, [[I'm looking for something in the range of]] "
        "((your range, with the currency and period)). [[That said, I'm open to]] discussing the full "
        "package. [[Is that within the budget for this role?]]",
        tips=("Pesquise antes. O piso da faixa tem que ser um valor que você aceitaria.",),
    ),
    Q(
        "start_date",
        "screen",
        "When would you be available to start?",
        "Prazo de saída do emprego atual.",
        "I'd need ((notice period)) to hand over my current responsibilities properly, "
        "[[so I could start]] ((date)).",
    ),
    Q(
        "challenge",
        "experience",
        "Can you tell me about a challenging project you worked on?",
        "Como você resolve problemas difíceis. Use STAR.",
        "[[Sure, let me think of a good example.]] [[The situation was that]] ((context)). "
        "[[My task was to]] ((your responsibility)). [[What I did was]] ((your actions, in the first "
        "person)). [[As a result]], ((measurable result)).",
        tips=("Use 'I' para o que você fez. Termine com um número.",),
    ),
    Q(
        "failure",
        "experience",
        "Tell me about a time you failed or made a mistake.",
        "Se você assume erros e aprende com eles.",
        "((A real mistake)). [[To be honest]], it was my fault: ((what went wrong)). "
        "I fixed it by ((action)), and [[what I learned was]] ((the lesson and what you do differently "
        "now)).",
    ),
    Q(
        "conflict",
        "experience",
        "Tell me about a time you disagreed with a colleague or your manager.",
        "Se você discorda com respeito e com dados, e depois segue em frente.",
        "((Situation)). I disagreed because ((reason)). Instead of arguing, I ((how you handled it: "
        "data, a proof of concept, a one-on-one conversation)). ((Outcome)). "
        "[[Even when the decision doesn't go my way]], once we decide, I fully support it.",
    ),
    Q(
        "pressure",
        "experience",
        "How do you handle pressure and tight deadlines?",
        "Organização e comunicação.",
        "I [[break the problem down into]] smaller pieces and agree on priorities early. "
        "[[I keep people in the loop]]: if something will slip, they hear it from me first. "
        "[[For instance]], ((a short real example)).",
    ),
    Q(
        "learning",
        "technical",
        "How do you keep your skills up to date?",
        "Curiosidade e autonomia.",
        "[[I'm a big believer in]] learning by doing. [[I usually]] ((how you learn: documentation, "
        "courses, newsletters)), but [[what really sticks is]] building things. [[For instance]], "
        "((something you learned recently by building it)).",
    ),
    Q(
        "unknown_answer",
        "technical",
        "What do you do when you don't know how to solve a problem?",
        "Autonomia sem orgulho: você tenta, pesquisa e pede ajuda na hora certa.",
        "First, I make sure I understand the problem and try to [[narrow it down]]. Then I look at "
        "the documentation, the logs and similar issues. [[If I'm still stuck after]] ((a time box, "
        "for example an hour)), I ask for help, with what I already tried. "
        "[[That way]], nobody wastes time and I still learn.",
    ),
    Q(
        "remote",
        "technical",
        "Have you worked remotely before? How do you stay productive?",
        "Para vagas remotas: disciplina e comunicação escrita.",
        "((Your remote experience)). [[What works for me is]] a fixed routine, clear goals for the day, "
        "and over-communicating in writing: short updates, documented decisions. "
        "[[I also make sure to]] be available during the team's core hours.",
    ),
    Q(
        "your_questions",
        "closing",
        "Do you have any questions for us?",
        "Nunca responda 'no'. Perguntas boas mostram interesse real.",
        "Yes, a few. [[I'm curious to know]] what the biggest challenge for this team is right now. "
        "[[What would success look like]] in the first ninety days? "
        "How is the team organized, and who would I work with most closely? "
        "And what are the next steps in the process?",
    ),
    Q(
        "closing",
        "closing",
        "Great, that's all from our side. Anything else you'd like to add?",
        "Última impressão: curta, positiva, reforçando o encaixe.",
        "Just that I'm really excited about this opportunity. ((One sentence connecting your "
        "experience to the role)). [[Thank you for the opportunity]], [[it was great chatting with "
        "you]], and [[I look forward to hearing from you]].",
    ),
)

SESSION = register(
    Session(
        id="general",
        title="Entrevista geral",
        company="Qualquer vaga",
        summary="As perguntas que aparecem em quase todo processo seletivo: apresentação, motivação, "
        "forças e fraquezas, histórias STAR, salário e encerramento.",
        stages=STAGES,
        questions=QUESTIONS,
    )
)
