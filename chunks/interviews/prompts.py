"""Etapas genéricas e prompts para gerar entrevistas de QUALQUER vaga com um LLM.

Também é exportado para o app web (``web/src/data/interview_prompts.json``),
então Python e celular geram sessões com exatamente as mesmas instruções.
"""

from __future__ import annotations

from chunks.interviews import Stage

STAGES = (
    Stage(
        "screen",
        "Recrutador",
        "Primeira conversa: trajetória, motivação, disponibilidade, modelo de trabalho, salário e "
        "inglês. Eles filtram encaixe e comunicação.",
    ),
    Stage(
        "experience",
        "Experiência (STAR)",
        "Perguntas comportamentais. Responda sempre com uma história real: Situation, Task, "
        "Action, Result.",
    ),
    Stage(
        "technical",
        "Técnica",
        "As habilidades e ferramentas que a vaga pede.",
    ),
    Stage(
        "domain",
        "Específicas da vaga",
        "O problema, o setor e as responsabilidades desta vaga em particular.",
    ),
    Stage(
        "design",
        "Caso prático",
        "Um cenário para resolver na hora: system design, estudo de caso ou situação do dia a dia "
        "da função.",
    ),
    Stage(
        "closing",
        "Suas perguntas e encerramento",
        "Perguntar bem mostra senioridade. Tenha 3 ou 4 perguntas prontas.",
    ),
)

# O que cada etapa deve cobrir, em inglês para o modelo.
STAGE_FOCUS = {
    "screen": "the first call with a recruiter: background pitch, motivation for this role and company, "
    "why the candidate is looking, availability and start date, time zone or work model, salary "
    "expectations, English level, other processes.",
    "experience": "behavioral questions answered with the STAR method, tied to the responsibilities "
    "in the job description: ownership, a difficult problem, a failure, conflict or disagreement, "
    "teamwork, prioritization.",
    "technical": "the hard skills, tools and technologies explicitly required by the job description. "
    "Ask how the candidate uses them and about trade-offs, not trivia.",
    "domain": "the specific problem, industry and day-to-day responsibilities of this role, including "
    "the 'bonus' or 'nice to have' items of the description.",
    "design": "one or two practical scenarios typical of this role (for engineers: a system design "
    "question; for other roles: a case study or a realistic work situation), plus a follow-up about "
    "scaling or edge cases.",
    "closing": "the moment the interviewer asks 'Do you have any questions for us?' and the closing of "
    "the interview. The answers must be good questions the candidate can ask about this specific role, "
    "and a short, positive closing.",
}

SYSTEM = """\
You are a senior interviewer and interview coach. You help a Brazilian professional who is \
learning English prepare for a job interview that will be conducted in English.

You write likely interview questions for one stage of the interview, based on the job \
description and the candidate profile you receive.

Rules for every question:
- "question": what the interviewer would actually say, in natural spoken English.
- "goal": in Brazilian Portuguese, one or two sentences explaining what the interviewer really \
wants to find out with this question.
- "answer": a model answer in English, in the first person, as the candidate would say it out \
loud: clear, natural, B2-level English, 60 to 150 words. Use the STAR structure for behavioral \
questions.
- In "answer", wrap 2 to 4 reusable expressions (chunks the candidate should memorize, such as \
"I've been working in", "As a result", "The trade-off is") in double square brackets: \
[[As a result]].
- NEVER invent facts about the candidate. Any fact that is not written in the candidate profile \
(employers, years, numbers, results, tools used, dates, salary) must be a placeholder in double \
parentheses describing what to fill in, in English, for example: ((number of years)), \
((a project where you cleaned messy data)), ((your salary range in USD per month)).
- "tips": 1 to 3 short, practical tips in Brazilian Portuguese.
- "follow_ups": 0 to 2 follow-up questions the interviewer could ask next, in English.
- Questions must be specific to this job, not generic, and must not repeat questions already \
asked.
"""

STAGE_PROMPT = """\
JOB DESCRIPTION:
\"\"\"
{job}
\"\"\"

CANDIDATE PROFILE:
\"\"\"
{profile}
\"\"\"

STAGE: {stage_title}
Write {count} questions about {stage_focus}

Questions already written for other stages (do not repeat them):
{already}
"""

META_PROMPT = """\
JOB DESCRIPTION:
\"\"\"
{job}
\"\"\"

Extract:
- "title": the job title, in the original language of the description.
- "company": the company name (and the hiring agency, if there is one). Use "" if unknown.
- "summary": one or two sentences in Brazilian Portuguese explaining what the job is about and \
the main skills required.
"""

NO_PROFILE = "(No profile given. Use ((placeholders)) for every fact about the candidate.)"

QUESTIONS_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "goal": {"type": "string"},
                    "answer": {"type": "string"},
                    "tips": {"type": "array", "items": {"type": "string"}},
                    "follow_ups": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["question", "goal", "answer", "tips", "follow_ups"],
            },
        }
    },
    "required": ["questions"],
}

META_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "company": {"type": "string"},
        "summary": {"type": "string"},
    },
    "required": ["title", "company", "summary"],
}


def to_dict() -> dict:
    """Tudo o que o app web precisa para gerar sessões igual ao Python."""
    return {
        "stages": [{"id": s.id, "title": s.title, "description": s.description} for s in STAGES],
        "stage_focus": STAGE_FOCUS,
        "system": SYSTEM,
        "stage_prompt": STAGE_PROMPT,
        "meta_prompt": META_PROMPT,
        "no_profile": NO_PROFILE,
        "questions_schema": QUESTIONS_SCHEMA,
        "meta_schema": META_SCHEMA,
    }
