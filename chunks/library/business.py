"""Negócios, empreendedorismo e networking."""

from chunks.core import chunk

C = "business"

wont_move_the_needle = chunk(
    "wont_move_the_needle",
    "{thing} [[won't move the needle on]] {metric}.",
    "{thing} não vai fazer diferença de verdade {metric}.",
    category=C,
    examples=[
        {"thing": ("That small feature", "Essa funcionalidade pequena"), "metric": ("our revenue", "no nosso faturamento")},
        {"thing": ("A new logo", "Um logo novo"), "metric": ("sales", "nas vendas")},
        {"thing": ("Another meeting", "Mais uma reunião"), "metric": ("this problem", "nesse problema")},
    ],
)
dont_have_the_bandwidth = chunk(
    "dont_have_the_bandwidth",
    "[[I'd love to help, but I don't have the bandwidth]] {when}.",
    "Eu adoraria ajudar, mas não tenho tempo {when}.",
    category=C,
    examples=[
        {"when": ("this week", "esta semana")},
        {"when": ("right now", "agora")},
        {"when": ("until the launch", "até o lançamento")},
    ],
    note="'Bandwidth' aqui é tempo ou capacidade, não internet.",
)
the_bottom_line_is = chunk(
    "the_bottom_line_is",
    "[[The bottom line is that]] {conclusion}.",
    "Resumindo, o que importa é que {conclusion}.",
    category=C,
    examples=[
        {"conclusion": ("the server costs are too high", "o custo dos servidores está alto demais")},
        {"conclusion": ("we need more clients", "precisamos de mais clientes")},
        {"conclusion": ("the product works", "o produto funciona")},
    ],
)
is_a_low_hanging_fruit = chunk(
    "is_a_low_hanging_fruit",
    "{thing} [[is a low-hanging fruit]].",
    "{thing} é uma vitória fácil.",
    category=C,
    examples=[
        {"thing": ("Optimizing the database queries", "Otimizar as consultas do banco")},
        {"thing": ("Fixing the signup form", "Arrumar o formulário de cadastro")},
        {"thing": ("Adding a cache", "Colocar um cache")},
    ],
)
addresses_a_pain_point = chunk(
    "addresses_a_pain_point",
    "{product} [[addresses a major pain point for]] {audience}.",
    "{product} resolve uma dor importante {audience}.",
    category=C,
    examples=[
        {"product": ("Our SaaS product", "O nosso SaaS"), "audience": ("small businesses", "das pequenas empresas")},
        {"product": ("This app", "Este app"), "audience": ("busy parents", "de pais sem tempo")},
        {"product": ("The new report", "O novo relatório"), "audience": ("the finance team", "do time financeiro")},
    ],
)
drive_user_adoption = chunk(
    "drive_user_adoption",
    "[[We need]] {strategy} [[to drive user adoption]].",
    "Precisamos de {strategy} para fazer os usuários adotarem o produto.",
    category=C,
    examples=[
        {"strategy": ("a marketing strategy", "uma estratégia de marketing")},
        {"strategy": ("better onboarding", "um onboarding melhor")},
        {"strategy": ("a free plan", "um plano gratuito")},
    ],
)
reduce_time_to_market = chunk(
    "reduce_time_to_market",
    "{choice} [[will reduce our time to market]].",
    "{choice} vai reduzir o nosso tempo até o lançamento.",
    category=C,
    examples=[
        {"choice": ("Using an open-source framework", "Usar um framework open source")},
        {"choice": ("Cutting this feature", "Cortar essa funcionalidade")},
        {"choice": ("Hiring a second developer", "Contratar mais um desenvolvedor")},
    ],
)
align_on_the_requirements = chunk(
    "align_on_the_requirements",
    "[[Before we]] {action}[[, let's align on the requirements with]] {who}.",
    "Antes de {action}, vamos alinhar os requisitos com {who}.",
    category=C,
    examples=[
        {"action": ("start coding", "começar a programar"), "who": ("the stakeholder", "o stakeholder")},
        {"action": ("sign the contract", "assinar o contrato"), "who": ("the client", "o cliente")},
        {"action": ("design the screens", "desenhar as telas"), "who": ("the product team", "o time de produto")},
    ],
)
build_a_proof_of_concept = chunk(
    "build_a_proof_of_concept",
    "[[Let's build a quick proof of concept to see if]] {hypothesis}.",
    "Vamos fazer uma prova de conceito rápida para ver se {hypothesis}.",
    category=C,
    examples=[
        {"hypothesis": ("the AI integration works", "a integração com IA funciona")},
        {"hypothesis": ("users actually want this", "os usuários querem mesmo isso")},
        {"hypothesis": ("the API is fast enough", "a API é rápida o suficiente")},
    ],
)
im_in = chunk(
    "im_in",
    "[[I'm in]] {field}.",
    "Eu trabalho com {field}.",
    category=C,
    examples=[
        {"field": ("the data analytics space", "análise de dados")},
        {"field": ("software development", "desenvolvimento de software")},
        {"field": ("fintech", "fintech")},
    ],
)
what_do_you_do_for_a_living = chunk(
    "what_do_you_do_for_a_living",
    "[[What do you do for a living?]]",
    "Com o que você trabalha?",
    category=C,
)
lets_grab_a_coffee = chunk(
    "lets_grab_a_coffee",
    "[[Let's grab a coffee]] {when}.",
    "Vamos tomar um café {when}.",
    category=C,
    examples=[
        {"when": ("sometime", "qualquer dia")},
        {"when": ("next week", "semana que vem")},
        {"when": ("after the event", "depois do evento")},
    ],
    defaults={"when": "sometime"},
)
i_heard_about = chunk(
    "i_heard_about",
    "[[I heard about]] {thing}[[ and I'd love to know more]].",
    "Ouvi falar {thing} e adoraria saber mais.",
    category=C,
    examples=[
        {"thing": ("your company", "da sua empresa")},
        {"thing": ("your new product", "do seu novo produto")},
        {"thing": ("your talk", "da sua palestra")},
    ],
)
set_up_a_quick_demo = chunk(
    "set_up_a_quick_demo",
    "[[Can we set up a quick demo]] {when}[[?]]",
    "Podemos marcar uma demonstração rápida {when}?",
    category=C,
    examples=[
        {"when": ("next week", "semana que vem")},
        {"when": ("on Thursday", "na quinta")},
        {"when": ("this afternoon", "hoje à tarde")},
    ],
)
as_a_rule_of_thumb = chunk(
    "as_a_rule_of_thumb",
    "[[As a rule of thumb]], {rule}.",
    "Como regra geral, {rule}.",
    category=C,
    examples=[
        {"rule": ("we never deploy on Fridays", "nunca fazemos deploy na sexta")},
        {"rule": ("a page should load in under two seconds", "uma página deve carregar em menos de dois segundos")},
        {"rule": ("reply to clients within a day", "responda aos clientes em até um dia")},
    ],
)
at_the_end_of_the_day = chunk(
    "at_the_end_of_the_day",
    "[[At the end of the day]], {point}.",
    "No fim das contas, {point}.",
    category=C,
    examples=[
        {"point": ("the client just wants it to work", "o cliente só quer que funcione")},
        {"point": ("it's your decision", "a decisão é sua")},
        {"point": ("results matter more than effort", "o resultado importa mais que o esforço")},
    ],
)
