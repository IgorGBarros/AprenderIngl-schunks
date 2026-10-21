"""Rotina de casa: manhã, refeições, filho, noite."""

from chunks.core import chunk

C = "home"

time_to = chunk(
    "time_to",
    "[[Time to]] {action}!",
    "Hora de {action}!",
    category=C,
    examples=[
        {"action": ("wake up", "acordar")},
        {"action": ("brush your teeth", "escovar os dentes")},
        {"action": ("go", "ir")},
    ],
    note="Funciona para tudo: 'go', 'eat', 'take a bath', 'brush your teeth'.",
)
time_for = chunk(
    "time_for",
    "[[Time for]] {thing}!",
    "Hora {thing}!",
    category=C,
    examples=[
        {"thing": ("bed", "de dormir")},
        {"thing": ("lunch", "do almoço")},
        {"thing": ("school", "da escola")},
    ],
)
dont_forget_to = chunk(
    "dont_forget_to",
    "[[Don't forget to]] {action}.",
    "Não esqueça de {action}.",
    category=C,
    examples=[
        {"action": ("brush your teeth", "escovar os dentes")},
        {"action": ("take out the trash", "levar o lixo para fora")},
        {"action": ("lock the door", "trancar a porta")},
    ],
)
dont_forget_your = chunk(
    "dont_forget_your",
    "[[Don't forget your]] {thing}!",
    "Não esqueça {thing}!",
    category=C,
    examples=[
        {"thing": ("backpack", "a sua mochila")},
        {"thing": ("jacket", "o seu casaco")},
        {"thing": ("keys", "as suas chaves")},
    ],
)
could_you_pass_me = chunk(
    "could_you_pass_me",
    "[[Could you pass me]] {thing}[[, please]]?",
    "Você pode me passar {thing}, por favor?",
    category=C,
    examples=[
        {"thing": ("the salt", "o sal")},
        {"thing": ("the remote", "o controle remoto")},
        {"thing": ("a towel", "uma toalha")},
    ],
)
could_you_help_me_with = chunk(
    "could_you_help_me_with",
    "[[Could you help me with]] {thing}[[?]]",
    "Você pode me ajudar com {thing}?",
    category=C,
    examples=[
        {"thing": ("the dishes", "a louça")},
        {"thing": ("these bags", "estas sacolas")},
        {"thing": ("my homework", "a minha lição de casa")},
    ],
)
what_do_you_want_for = chunk(
    "what_do_you_want_for",
    "[[What do you want for]] {meal}[[?]]",
    "O que você quer {meal}?",
    category=C,
    examples=[
        {"meal": ("dinner", "para o jantar")},
        {"meal": ("breakfast", "no café da manhã")},
        {"meal": ("your birthday", "de aniversário")},
    ],
)
lets_go_to = chunk(
    "lets_go_to",
    "[[Let's go to]] {place}!",
    "Vamos {place}!",
    category=C,
    examples=[
        {"place": ("the park", "ao parque")},
        {"place": ("the beach", "à praia")},
        {"place": ("Grandma's house", "para a casa da vovó")},
    ],
)
ill_pick_you_up_at = chunk(
    "ill_pick_you_up_at",
    "[[I'll pick you up at]] {time}.",
    "Eu te pego {time}.",
    category=C,
    examples=[
        {"time": ("five", "às cinco")},
        {"time": ("noon", "ao meio-dia")},
        {"time": ("the school gate", "no portão da escola")},
    ],
)
im_running_late = chunk(
    "im_running_late",
    "[[I'm running late]][[, I'll be there in]] {time}.",
    "Estou atrasado, chego em {time}.",
    category=C,
    examples=[
        {"time": ("ten minutes", "dez minutos")},
        {"time": ("half an hour", "meia hora")},
        {"time": ("five", "cinco minutos")},
    ],
)
can_you_turn = chunk(
    "can_you_turn",
    "[[Can you turn]] {state} [[the]] {device}[[?]]",
    "Você pode {state} {device}?",
    category=C,
    examples=[
        {"state": ("off", "desligar"), "device": ("TV", "a TV")},
        {"state": ("on", "ligar"), "device": ("lights", "a luz")},
        {"state": ("down", "abaixar"), "device": ("music", "a música")},
    ],
    note="state: 'on' (ligar), 'off' (desligar), 'up' (aumentar), 'down' (abaixar).",
)
where_did_you_put = chunk(
    "where_did_you_put",
    "[[Where did you put]] {thing}[[?]]",
    "Onde você colocou {thing}?",
    category=C,
    examples=[
        {"thing": ("the keys", "as chaves")},
        {"thing": ("my charger", "o meu carregador")},
        {"thing": ("the remote", "o controle remoto")},
    ],
)
did_you = chunk(
    "did_you",
    "[[Did you]] {action}[[?]]",
    "Você {action}?",
    category=C,
    examples=[
        {"action": ("sleep well", "dormiu bem")},
        {"action": ("eat already", "já comeu")},
        {"action": ("finish your homework", "terminou a lição de casa")},
    ],
)
lets_read = chunk(
    "lets_read",
    "[[Let me read you]] {story}.",
    "Deixa eu ler {story} para você.",
    category=C,
    examples=[
        {"story": ("a story", "uma história")},
        {"story": ("this book", "este livro")},
        {"story": ("one more page", "mais uma página")},
    ],
)
