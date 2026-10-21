"""Reuniões, apresentações e comunicação assíncrona (e-mail / Slack)."""

from chunks.core import chunk

C = "meetings"

lets_dive_into = chunk(
    "lets_dive_into",
    "[[Let's dive into]] {topic}.",
    "Vamos mergulhar em {topic}.",
    category=C,
    example={"topic": "the Q3 numbers"},
)
just_to_give_you_a_quick_overview_of = chunk(
    "just_to_give_you_a_quick_overview_of",
    "[[Just to give you a quick overview of]] {topic}...",
    "Só para dar uma visão geral rápida de {topic}...",
    category=C,
    example={"topic": "the architecture"},
)
walk_me_through = chunk(
    "walk_me_through",
    "[[Could you walk me through]] {thing}[[?]]",
    "Você pode me explicar {thing} passo a passo?",
    category=C,
    example={"thing": "the deployment process"},
)
thanks_for_walking_me_through = chunk(
    "thanks_for_walking_me_through",
    "[[Thanks for walking me through]] {thing}.",
    "Obrigado por me explicar {thing}.",
    category=C,
    example={"thing": "that"},
)
lets_touch_base = chunk(
    "lets_touch_base",
    "[[Let's touch base]] {when}[[ to]] {goal}.",
    "Vamos conversar rapidinho {when} para {goal}.",
    category=C,
    example={"when": ("next Monday", "segunda que vem"), "goal": ("review the sprint", "revisar a sprint")},
)
lets_sync_up_on = chunk(
    "lets_sync_up_on",
    "[[Let's sync up on]] {topic} {when}.",
    "Vamos nos alinhar sobre {topic} {when}.",
    category=C,
    example={"topic": "the roadmap", "when": "tomorrow"},
    defaults={"when": "later"},
)
ill_get_back_to_you_on = chunk(
    "ill_get_back_to_you_on",
    "[[I'll get back to you on]] {topic} {deadline}.",
    "Eu te retorno sobre {topic} {deadline}.",
    category=C,
    example={"topic": "this", "deadline": "by end of day"},
    defaults={"deadline": "soon"},
)
just_following_up_on = chunk(
    "just_following_up_on",
    "[[Just following up on]] {thing}.",
    "Só acompanhando/cobrando {thing}.",
    category=C,
    example={"thing": "the proposal I sent last Tuesday"},
)
keep_me_in_the_loop = chunk(
    "keep_me_in_the_loop",
    "[[Please keep me in the loop]] {about}.",
    "Por favor, me mantenha informado {about}.",
    category=C,
    example={"about": "about the migration"},
    defaults={"about": ""},
)
let_me_loop_in = chunk(
    "let_me_loop_in",
    "[[Let me loop in]] {person} [[to help us with]] {topic}.",
    "Deixa eu incluir {person} para nos ajudar com {topic}.",
    category=C,
    example={"person": "John", "topic": "the backend issue"},
)
i_have_a_blocker = chunk(
    "i_have_a_blocker",
    "[[I'm blocked by]] {blocker}.",
    "Estou travado por causa de {blocker}.",
    category=C,
    example={"blocker": "the API credentials"},
)
ill_pick_this_up = chunk(
    "ill_pick_this_up",
    "[[I'll pick up]] {task}.",
    "Eu pego {task}.",
    category=C,
    example={"task": "the login bug"},
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
    example={"thing": "the dashboard"},
)
sounds_like_a_plan = chunk(
    "sounds_like_a_plan",
    "{plan}. [[Sounds like a plan?]]",
    "{plan}. Fechado?",
    category=C,
    example={"plan": ("We ship on Friday", "Lançamos na sexta")},
)
the_action_items_are = chunk(
    "the_action_items_are",
    "[[So the action items are]]: {items}.",
    "Então os próximos passos são: {items}.",
    category=C,
    example={"items": "fix the bug, update the docs and schedule the demo"},
)
im_not_sure_i_follow = chunk(
    "im_not_sure_i_follow",
    "[[Sorry, I'm not sure I follow. Could you elaborate on]] {thing}[[?]]",
    "Desculpe, não sei se entendi. Você pode detalhar {thing}?",
    category=C,
    example={"thing": "the second point"},
    note="Salva vidas quando você não entendeu algo na reunião.",
)
lets_take_this_offline = chunk(
    "lets_take_this_offline",
    "[[Let's take]] {topic} [[offline]].",
    "Vamos discutir {topic} fora da reunião.",
    category=C,
    example={"topic": "the pricing discussion"},
)
i_look_forward_to = chunk(
    "i_look_forward_to",
    "[[I look forward to]] {thing}.",
    "Fico no aguardo de {thing}.",
    category=C,
    example={"thing": "hearing from you"},
    note="Depois de 'to' vem verbo com -ing: 'hearing', 'working', 'meeting'.",
)
