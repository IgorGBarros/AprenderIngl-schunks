"""Reuniões, apresentações e comunicação assíncrona (e-mail / Slack)."""

from chunks.core import chunk

C = "meetings"

lets_dive_into = chunk(
    "lets_dive_into",
    "[[Let's dive into]] {topic}.",
    "Vamos entrar direto {topic}.",
    category=C,
    examples=[
        {"topic": ("the Q3 numbers", "nos números do terceiro trimestre")},
        {"topic": ("the demo", "na demonstração")},
        {"topic": ("today's agenda", "na pauta de hoje")},
    ],
)
just_to_give_you_a_quick_overview_of = chunk(
    "just_to_give_you_a_quick_overview_of",
    "[[Just to give you a quick overview of]] {topic}...",
    "Só para dar uma visão geral rápida {topic}...",
    category=C,
    examples=[
        {"topic": ("the architecture", "da arquitetura")},
        {"topic": ("where we are", "de onde estamos")},
        {"topic": ("the project", "do projeto")},
    ],
)
walk_me_through = chunk(
    "walk_me_through",
    "[[Could you walk me through]] {thing}[[?]]",
    "Você pode me explicar {thing} passo a passo?",
    category=C,
    examples=[
        {"thing": ("the deployment process", "o processo de deploy")},
        {"thing": ("your background", "a sua trajetória")},
        {"thing": ("the numbers", "os números")},
    ],
)
thanks_for_walking_me_through = chunk(
    "thanks_for_walking_me_through",
    "[[Thanks for walking me through]] {thing}.",
    "Obrigado por me explicar {thing}.",
    category=C,
    examples=[
        {"thing": ("that", "isso")},
        {"thing": ("the codebase", "o código")},
        {"thing": ("the new process", "o novo processo")},
    ],
)
lets_touch_base = chunk(
    "lets_touch_base",
    "[[Let's touch base]] {when}[[ to]] {goal}.",
    "Vamos conversar rapidinho {when} para {goal}.",
    category=C,
    examples=[
        {"when": ("next Monday", "na segunda que vem"), "goal": ("review the sprint", "revisar a sprint")},
        {"when": ("tomorrow", "amanhã"), "goal": ("check the results", "ver os resultados")},
        {"when": ("after lunch", "depois do almoço"), "goal": ("decide the next steps", "decidir os próximos passos")},
    ],
)
lets_sync_up_on = chunk(
    "lets_sync_up_on",
    "[[Let's sync up on]] {topic} {when}.",
    "Vamos nos alinhar sobre {topic} {when}.",
    category=C,
    examples=[
        {"topic": ("the roadmap", "o roadmap"), "when": ("tomorrow", "amanhã")},
        {"topic": ("the migration", "a migração"), "when": ("on Friday", "na sexta")},
        {"topic": ("this", "isso"), "when": ("later", "mais tarde")},
    ],
    defaults={"when": "later"},
)
ill_get_back_to_you_on = chunk(
    "ill_get_back_to_you_on",
    "[[I'll get back to you on]] {topic} {deadline}.",
    "Eu te dou um retorno sobre {topic} {deadline}.",
    category=C,
    examples=[
        {"topic": ("this", "isso"), "deadline": ("by end of day", "até o fim do dia")},
        {"topic": ("the budget", "o orçamento"), "deadline": ("tomorrow", "amanhã")},
        {"topic": ("your question", "a sua pergunta"), "deadline": ("this week", "esta semana")},
    ],
    defaults={"deadline": "soon"},
)
just_following_up_on = chunk(
    "just_following_up_on",
    "[[Just following up on]] {thing}.",
    "Só passando para retomar {thing}.",
    category=C,
    examples=[
        {"thing": ("the proposal I sent last Tuesday", "a proposta que enviei na terça passada")},
        {"thing": ("my previous email", "o meu e-mail anterior")},
        {"thing": ("our conversation", "a nossa conversa")},
    ],
    note="Jeito educado de cobrar uma resposta.",
)
keep_me_in_the_loop = chunk(
    "keep_me_in_the_loop",
    "[[Please keep me in the loop]] {about}.",
    "Por favor, me mantenha informado {about}.",
    category=C,
    examples=[
        {"about": ("about the migration", "sobre a migração")},
        {"about": ("on any changes", "sobre qualquer mudança")},
        {"about": ("", "")},
    ],
    defaults={"about": ""},
)
let_me_loop_in = chunk(
    "let_me_loop_in",
    "[[Let me loop in]] {person} [[to help us with]] {topic}.",
    "Deixa eu incluir {person} para nos ajudar com {topic}.",
    category=C,
    examples=[
        {"person": ("John", "o John"), "topic": ("the backend issue", "o problema do backend")},
        {"person": ("our designer", "a nossa designer"), "topic": ("the layout", "o layout")},
        {"person": ("Maria from finance", "a Maria do financeiro"), "topic": ("the invoices", "as notas fiscais")},
    ],
)
i_have_a_blocker = chunk(
    "i_have_a_blocker",
    "[[I'm blocked by]] {blocker}.",
    "Estou travado por causa {blocker}.",
    category=C,
    examples=[
        {"blocker": ("the API credentials", "das credenciais da API")},
        {"blocker": ("a failing test", "de um teste quebrando")},
        {"blocker": ("missing data", "de dados faltando")},
    ],
)
ill_pick_this_up = chunk(
    "ill_pick_this_up",
    "[[I'll pick up]] {task}.",
    "Eu assumo {task}.",
    category=C,
    examples=[
        {"task": ("the login bug", "o bug do login")},
        {"task": ("this ticket", "este ticket")},
        {"task": ("the code review", "o code review")},
    ],
)
can_you_hear_me = chunk(
    "can_you_hear_me",
    "[[Can you hear me okay?]]",
    "Vocês estão me ouvindo bem?",
    category=C,
)
let_me_share_my_screen = chunk(
    "let_me_share_my_screen",
    "[[Let me share my screen]][[ and show you]] {thing}.",
    "Deixa eu compartilhar a tela e te mostrar {thing}.",
    category=C,
    examples=[
        {"thing": ("the dashboard", "o dashboard")},
        {"thing": ("what I mean", "o que eu quero dizer")},
        {"thing": ("the error", "o erro")},
    ],
)
sounds_like_a_plan = chunk(
    "sounds_like_a_plan",
    "{plan}. [[Sounds like a plan?]]",
    "{plan}. Combinado?",
    category=C,
    examples=[
        {"plan": ("We ship on Friday", "A gente lança na sexta")},
        {"plan": ("I'll write the docs and you review them", "Eu escrevo a documentação e você revisa")},
        {"plan": ("Let's meet again next week", "Vamos nos reunir de novo semana que vem")},
    ],
)
the_action_items_are = chunk(
    "the_action_items_are",
    "[[So the action items are]]: {items}.",
    "Então os próximos passos são: {items}.",
    category=C,
    examples=[
        {"items": ("fix the bug, update the docs and schedule the demo", "corrigir o bug, atualizar a documentação e marcar a demo")},
        {"items": ("send the proposal and wait for feedback", "enviar a proposta e esperar o retorno")},
        {"items": ("test the new version on Monday", "testar a nova versão na segunda")},
    ],
)
im_not_sure_i_follow = chunk(
    "im_not_sure_i_follow",
    "[[Sorry, I'm not sure I follow. Could you elaborate on]] {thing}[[?]]",
    "Desculpe, não sei se entendi. Você pode explicar melhor {thing}?",
    category=C,
    examples=[
        {"thing": ("the second point", "o segundo ponto")},
        {"thing": ("that last part", "essa última parte")},
        {"thing": ("what you mean by 'scalable'", "o que você quer dizer com 'escalável'")},
    ],
    note="Salva vidas quando você não entendeu algo na reunião.",
)
lets_take_this_offline = chunk(
    "lets_take_this_offline",
    "[[Let's take]] {topic} [[offline]].",
    "Vamos conversar sobre {topic} fora da reunião.",
    category=C,
    examples=[
        {"topic": ("the pricing discussion", "o preço")},
        {"topic": ("this", "isso")},
        {"topic": ("the technical details", "os detalhes técnicos")},
    ],
)
i_look_forward_to = chunk(
    "i_look_forward_to",
    "[[I look forward to]] {thing}.",
    "Estou ansioso {thing}.",
    category=C,
    examples=[
        {"thing": ("hearing from you", "pelo seu retorno")},
        {"thing": ("working with you", "para trabalhar com você")},
        {"thing": ("our meeting", "pela nossa reunião")},
    ],
    note="Depois de 'to' vem verbo com -ing: 'hearing', 'working', 'meeting'.",
)
