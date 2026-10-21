"""Survival chunks: restaurante, transporte, compras, farmácia, hotel."""

from chunks.core import chunk

C = "survival"

# --- Restaurante e cafés -------------------------------------------------
could_i_get = chunk(
    "could_i_get",
    "[[Could I get]] {item}[[, please]]?",
    "Pode me ver {item}, por favor?",
    category=C,
    example={"item": "a glass of water"},
    note="Mais educado que 'I want'. Serve para qualquer pedido.",
)
can_i_have = chunk(
    "can_i_have",
    "[[Can I have]] {item}[[, please]]?",
    "Posso pedir {item}, por favor?",
    category=C,
    example={"item": "the menu"},
)
ill_have = chunk(
    "ill_have",
    "[[I'll have]] {item}[[, please]].",
    "Vou querer {item}, por favor.",
    category=C,
    example={"item": "the chicken salad"},
    note="Usado na hora de fazer o pedido ao garçom.",
)
could_i_get_extra = chunk(
    "could_i_get_extra",
    "[[Could I get an extra]] {item}[[?]]",
    "Pode me trazer mais um(a) {item}?",
    category=C,
    example={"item": "napkin"},
)
on_the_side = chunk(
    "on_the_side",
    "[[Could I get]] {item} [[on the side]]?",
    "Pode trazer {item} à parte?",
    category=C,
    example={"item": "the dressing"},
)
im_allergic_to = chunk(
    "im_allergic_to",
    "[[I'm allergic to]] {thing}.",
    "Eu sou alérgico a {thing}.",
    category=C,
    example={"thing": "peanuts"},
)
could_we_get_the_check = chunk(
    "could_we_get_the_check",
    "[[Could we get the check, please?]]",
    "Pode trazer a conta, por favor?",
    category=C,
)

# --- Transporte e direções -----------------------------------------------
how_do_i_get_to = chunk(
    "how_do_i_get_to",
    "[[Excuse me, how do I get to]] {place}[[?]]",
    "Com licença, como eu chego em {place}?",
    category=C,
    example={"place": "the train station"},
)
which_train_goes_to = chunk(
    "which_train_goes_to",
    "[[Which train goes to]] {place}[[?]]",
    "Qual trem vai para {place}?",
    category=C,
    example={"place": "Manhattan"},
)
a_ticket_to = chunk(
    "a_ticket_to",
    "[[I'd like]] {kind} [[ticket to]] {place}[[, please]].",
    "Eu gostaria de uma passagem {kind} para {place}, por favor.",
    category=C,
    example={"kind": "a one-way", "place": "Boston"},
    note="kind: 'a', 'a one-way' (só ida), 'a round-trip' (ida e volta).",
)
how_long_does_it_take = chunk(
    "how_long_does_it_take",
    "[[How long does it take to]] {action}[[?]]",
    "Quanto tempo leva para {action}?",
    category=C,
    example={"action": "get to the airport"},
)
heading_to = chunk(
    "heading_to",
    "[[I'm heading to]] {place}.",
    "Estou indo para {place}.",
    category=C,
    example={"place": "the airport"},
)
is_this_the_right_way_to = chunk(
    "is_this_the_right_way_to",
    "[[Is this the right way to]] {place}[[?]]",
    "Esse é o caminho certo para {place}?",
    category=C,
    example={"place": "downtown"},
)

# --- Compras ---------------------------------------------------------------
do_you_have_this_in = chunk(
    "do_you_have_this_in",
    "[[Do you have this in]] {variant}[[?]]",
    "Vocês têm isso em {variant}?",
    category=C,
    example={"variant": "a medium"},
)
how_much_is = chunk(
    "how_much_is",
    "[[How much is]] {item}[[?]]",
    "Quanto custa {item}?",
    category=C,
    example={"item": "this jacket"},
)
im_just_looking = chunk(
    "im_just_looking",
    "[[I'm just looking, thanks.]]",
    "Só estou olhando, obrigado.",
    category=C,
)
can_i_pay_with = chunk(
    "can_i_pay_with",
    "[[Can I pay with]] {method}[[?]]",
    "Posso pagar com {method}?",
    category=C,
    example={"method": "a credit card"},
)

# --- Farmácia --------------------------------------------------------------
do_you_have_something_for = chunk(
    "do_you_have_something_for",
    "[[Do you have something for]] {problem}[[?]]",
    "Você tem alguma coisa para {problem}?",
    category=C,
    example={"problem": "a headache"},
)
how_often_should_i = chunk(
    "how_often_should_i",
    "[[How often should I]] {action}[[?]]",
    "Com que frequência eu devo {action}?",
    category=C,
    example={"action": "take this medicine"},
)

# --- Hotel -----------------------------------------------------------------
i_have_a_reservation_under = chunk(
    "i_have_a_reservation_under",
    "[[I have a reservation under]] {name}.",
    "Tenho uma reserva no nome de {name}.",
    category=C,
    example={"name": "Barros"},
)
what_time_is = chunk(
    "what_time_is",
    "[[What time is]] {event}[[?]]",
    "Que horas é {event}?",
    category=C,
    example={"event": "check-out"},
)
