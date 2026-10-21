"""Negócios, empreendedorismo e networking."""

from chunks.core import chunk

C = "business"

wont_move_the_needle = chunk(
    "wont_move_the_needle",
    "{thing} [[won't move the needle on]] {metric}.",
    "{thing} não vai fazer diferença real em {metric}.",
    category=C,
    example={"thing": "That small feature", "metric": "our revenue"},
)
dont_have_the_bandwidth = chunk(
    "dont_have_the_bandwidth",
    "[[I'd love to help, but I don't have the bandwidth]] {when}.",
    "Adoraria ajudar, mas não tenho tempo/capacidade {when}.",
    category=C,
    example={"when": "this week"},
)
the_bottom_line_is = chunk(
    "the_bottom_line_is",
    "[[The bottom line is that]] {conclusion}.",
    "O que importa no fim é que {conclusion}.",
    category=C,
    example={"conclusion": "the server costs are too high"},
)
is_a_low_hanging_fruit = chunk(
    "is_a_low_hanging_fruit",
    "{thing} [[is a low-hanging fruit]].",
    "{thing} é uma vitória fácil.",
    category=C,
    example={"thing": "Optimizing the database queries"},
)
addresses_a_pain_point = chunk(
    "addresses_a_pain_point",
    "{product} [[addresses a major pain point for]] {audience}.",
    "{product} resolve uma dor importante de {audience}.",
    category=C,
    example={"product": "Our SaaS product", "audience": "small businesses"},
)
drive_user_adoption = chunk(
    "drive_user_adoption",
    "[[We need]] {strategy} [[to drive user adoption]].",
    "Precisamos de {strategy} para impulsionar a adoção pelos usuários.",
    category=C,
    example={"strategy": "a marketing strategy"},
)
reduce_time_to_market = chunk(
    "reduce_time_to_market",
    "{choice} [[will reduce our time to market]].",
    "{choice} vai reduzir nosso tempo de lançamento.",
    category=C,
    example={"choice": "Using an open-source framework"},
)
align_on_the_requirements = chunk(
    "align_on_the_requirements",
    "[[Before we]] {action}[[, let's align on the requirements with]] {who}.",
    "Antes de {action}, vamos alinhar os requisitos com {who}.",
    category=C,
    example={"action": "start coding", "who": "the stakeholder"},
)
build_a_proof_of_concept = chunk(
    "build_a_proof_of_concept",
    "[[Let's build a quick proof of concept to see if]] {hypothesis}.",
    "Vamos fazer uma prova de conceito rápida para ver se {hypothesis}.",
    category=C,
    example={"hypothesis": "the AI integration works"},
)
im_in = chunk(
    "im_in",
    "[[I'm in]] {field}.",
    "Eu trabalho com {field}.",
    category=C,
    example={"field": "the data analytics space"},
)
what_do_you_do_for_a_living = chunk(
    "what_do_you_do_for_a_living",
    "[[What do you do for a living?]]",
    "O que você faz da vida?",
    category=C,
)
lets_grab_a_coffee = chunk(
    "lets_grab_a_coffee",
    "[[Let's grab a coffee]] {when}.",
    "Vamos tomar um café {when}.",
    category=C,
    example={"when": "sometime"},
    defaults={"when": "sometime"},
)
i_heard_about = chunk(
    "i_heard_about",
    "[[I heard about]] {thing}[[ and I'd love to know more]].",
    "Ouvi falar de {thing} e adoraria saber mais.",
    category=C,
    example={"thing": "your company"},
)
set_up_a_quick_demo = chunk(
    "set_up_a_quick_demo",
    "[[Can we set up a quick demo]] {when}[[?]]",
    "Podemos marcar uma demo rápida {when}?",
    category=C,
    example={"when": "next week"},
)
as_a_rule_of_thumb = chunk(
    "as_a_rule_of_thumb",
    "[[As a rule of thumb]], {rule}.",
    "Como regra geral, {rule}.",
    category=C,
    example={"rule": "we never deploy on Fridays"},
)
at_the_end_of_the_day = chunk(
    "at_the_end_of_the_day",
    "[[At the end of the day]], {point}.",
    "No fim das contas, {point}.",
    category=C,
    example={"point": "the client just wants it to work"},
)
