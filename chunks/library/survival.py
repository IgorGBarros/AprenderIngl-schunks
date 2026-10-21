"""Survival chunks: restaurante, transporte, compras, farmácia, hotel."""

from chunks.core import chunk

C = "survival"

# --- Restaurante e cafés -------------------------------------------------
could_i_get = chunk(
    "could_i_get",
    "[[Could I get]] {item}[[, please]]?",
    "Pode me trazer {item}, por favor?",
    category=C,
    examples=[
        {"item": ("a glass of water", "um copo de água")},
        {"item": ("a cup of coffee", "uma xícara de café")},
        {"item": ("the menu", "o cardápio")},
    ],
    note="Mais educado que 'I want'. Serve para qualquer pedido.",
)
can_i_have = chunk(
    "can_i_have",
    "[[Can I have]] {item}[[, please]]?",
    "Pode me dar {item}, por favor?",
    category=C,
    examples=[
        {"item": ("the menu", "o cardápio")},
        {"item": ("some more bread", "mais um pouco de pão")},
        {"item": ("a receipt", "o recibo")},
    ],
)
ill_have = chunk(
    "ill_have",
    "[[I'll have]] {item}[[, please]].",
    "Vou querer {item}, por favor.",
    category=C,
    examples=[
        {"item": ("the chicken salad", "a salada de frango")},
        {"item": ("a large latte", "um latte grande")},
        {"item": ("the same", "o mesmo")},
    ],
    note="Usado na hora de fazer o pedido ao garçom.",
)
could_i_get_extra = chunk(
    "could_i_get_extra",
    "[[Could I get an extra]] {item}[[?]]",
    "Pode me trazer mais {item}?",
    category=C,
    examples=[
        {"item": ("napkin", "um guardanapo")},
        {"item": ("plate", "um prato")},
        {"item": ("spoon", "uma colher")},
    ],
)
on_the_side = chunk(
    "on_the_side",
    "[[Could I get]] {item} [[on the side]]?",
    "Pode trazer {item} à parte?",
    category=C,
    examples=[
        {"item": ("the dressing", "o molho da salada")},
        {"item": ("the sauce", "o molho")},
        {"item": ("the fries", "a batata frita")},
    ],
)
im_allergic_to = chunk(
    "im_allergic_to",
    "[[I'm allergic to]] {thing}.",
    "Tenho alergia a {thing}.",
    category=C,
    examples=[
        {"thing": ("peanuts", "amendoim")},
        {"thing": ("shellfish", "frutos do mar")},
        {"thing": ("penicillin", "penicilina")},
    ],
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
    "Com licença, como eu chego {place}?",
    category=C,
    examples=[
        {"place": ("the train station", "à estação de trem")},
        {"place": ("the city center", "ao centro")},
        {"place": ("Gate 12", "ao portão 12")},
    ],
)
which_train_goes_to = chunk(
    "which_train_goes_to",
    "[[Which train goes to]] {place}[[?]]",
    "Qual trem vai {place}?",
    category=C,
    examples=[
        {"place": ("Manhattan", "para Manhattan")},
        {"place": ("the airport", "para o aeroporto")},
        {"place": ("downtown", "para o centro")},
    ],
)
a_ticket_to = chunk(
    "a_ticket_to",
    "[[I'd like]] {kind} [[ticket to]] {place}[[, please]].",
    "Eu queria {kind} para {place}, por favor.",
    category=C,
    examples=[
        {"kind": ("a one-way", "uma passagem só de ida"), "place": ("Boston", "Boston")},
        {"kind": ("a round-trip", "uma passagem de ida e volta"), "place": ("Chicago", "Chicago")},
        {"kind": ("a", "uma passagem"), "place": ("the airport", "o aeroporto")},
    ],
    note="kind: 'a', 'a one-way' (só ida), 'a round-trip' (ida e volta).",
)
how_long_does_it_take = chunk(
    "how_long_does_it_take",
    "[[How long does it take to]] {action}[[?]]",
    "Quanto tempo leva para {action}?",
    category=C,
    examples=[
        {"action": ("get to the airport", "chegar ao aeroporto")},
        {"action": ("walk there", "ir a pé até lá")},
        {"action": ("get my order", "o meu pedido ficar pronto")},
    ],
)
heading_to = chunk(
    "heading_to",
    "[[I'm heading to]] {place}.",
    "Estou indo {place}.",
    category=C,
    examples=[
        {"place": ("the airport", "para o aeroporto")},
        {"place": ("the hotel", "para o hotel")},
        {"place": ("a meeting", "para uma reunião")},
    ],
)
is_this_the_right_way_to = chunk(
    "is_this_the_right_way_to",
    "[[Is this the right way to]] {place}[[?]]",
    "Este é o caminho certo {place}?",
    category=C,
    examples=[
        {"place": ("downtown", "para o centro")},
        {"place": ("the museum", "para o museu")},
        {"place": ("the subway", "para o metrô")},
    ],
)

# --- Compras ---------------------------------------------------------------
do_you_have_this_in = chunk(
    "do_you_have_this_in",
    "[[Do you have this in]] {variant}[[?]]",
    "Tem esse {variant}?",
    category=C,
    examples=[
        {"variant": ("a medium", "no tamanho M")},
        {"variant": ("black", "em preto")},
        {"variant": ("a bigger size", "num tamanho maior")},
    ],
)
how_much_is = chunk(
    "how_much_is",
    "[[How much is]] {item}[[?]]",
    "Quanto custa {item}?",
    category=C,
    examples=[
        {"item": ("this jacket", "esta jaqueta")},
        {"item": ("a ticket", "uma passagem")},
        {"item": ("the room per night", "a diária do quarto")},
    ],
)
im_just_looking = chunk(
    "im_just_looking",
    "[[I'm just looking, thanks.]]",
    "Só estou dando uma olhada, obrigado.",
    category=C,
)
can_i_pay_with = chunk(
    "can_i_pay_with",
    "[[Can I pay with]] {method}[[?]]",
    "Posso pagar com {method}?",
    category=C,
    examples=[
        {"method": ("a credit card", "cartão de crédito")},
        {"method": ("cash", "dinheiro")},
        {"method": ("my phone", "o celular")},
    ],
)

# --- Farmácia --------------------------------------------------------------
do_you_have_something_for = chunk(
    "do_you_have_something_for",
    "[[Do you have something for]] {problem}[[?]]",
    "Você tem alguma coisa para {problem}?",
    category=C,
    examples=[
        {"problem": ("a headache", "dor de cabeça")},
        {"problem": ("a sore throat", "dor de garganta")},
        {"problem": ("a fever", "febre")},
    ],
)
how_often_should_i = chunk(
    "how_often_should_i",
    "[[How often should I]] {action}[[?]]",
    "De quanto em quanto tempo eu devo {action}?",
    category=C,
    examples=[
        {"action": ("take this medicine", "tomar este remédio")},
        {"action": ("give it to him", "dar para ele")},
        {"action": ("change the bandage", "trocar o curativo")},
    ],
)

# --- Hotel -----------------------------------------------------------------
i_have_a_reservation_under = chunk(
    "i_have_a_reservation_under",
    "[[I have a reservation under]] {name}.",
    "Tenho uma reserva no nome de {name}.",
    category=C,
    examples=[
        {"name": ("Barros", "Barros")},
        {"name": ("Igor Barros", "Igor Barros")},
        {"name": ("PGBA Solutions", "PGBA Solutions")},
    ],
)
what_time_is = chunk(
    "what_time_is",
    "[[What time is]] {event}[[?]]",
    "A que horas é {event}?",
    category=C,
    examples=[
        {"event": ("check-out", "o check-out")},
        {"event": ("breakfast", "o café da manhã")},
        {"event": ("the last train", "o último trem")},
    ],
)
