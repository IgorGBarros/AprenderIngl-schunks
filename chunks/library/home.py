"""Rotina de casa: manhã, refeições, filho, noite."""

from chunks.core import chunk

C = "home"

time_to = chunk(
    "time_to",
    "[[Time to]] {action}!",
    "Hora de {action}!",
    category=C,
    example={"action": "wake up"},
    note="Funciona para tudo: 'go', 'eat', 'take a bath', 'brush your teeth'.",
)
time_for = chunk(
    "time_for",
    "[[Time for]] {thing}!",
    "Hora do/da {thing}!",
    category=C,
    example={"thing": "bed"},
)
dont_forget_to = chunk(
    "dont_forget_to",
    "[[Don't forget to]] {action}.",
    "Não esqueça de {action}.",
    category=C,
    example={"action": "brush your teeth"},
)
dont_forget_your = chunk(
    "dont_forget_your",
    "[[Don't forget your]] {thing}!",
    "Não esqueça seu/sua {thing}!",
    category=C,
    example={"thing": "backpack"},
)
could_you_pass_me = chunk(
    "could_you_pass_me",
    "[[Could you pass me]] {thing}[[, please]]?",
    "Você pode me passar {thing}, por favor?",
    category=C,
    example={"thing": "the salt"},
)
could_you_help_me_with = chunk(
    "could_you_help_me_with",
    "[[Could you help me with]] {thing}[[?]]",
    "Você pode me ajudar com {thing}?",
    category=C,
    example={"thing": "the dishes"},
)
what_do_you_want_for = chunk(
    "what_do_you_want_for",
    "[[What do you want for]] {meal}[[?]]",
    "O que você quer de {meal}?",
    category=C,
    example={"meal": "dinner"},
)
lets_go_to = chunk(
    "lets_go_to",
    "[[Let's go to]] {place}!",
    "Vamos para {place}!",
    category=C,
    example={"place": "the park"},
)
ill_pick_you_up_at = chunk(
    "ill_pick_you_up_at",
    "[[I'll pick you up at]] {time}.",
    "Eu te pego às {time}.",
    category=C,
    example={"time": "five"},
)
im_running_late = chunk(
    "im_running_late",
    "[[I'm running late]][[, I'll be there in]] {time}.",
    "Estou atrasado, chego em {time}.",
    category=C,
    example={"time": "ten minutes"},
)
can_you_turn = chunk(
    "can_you_turn",
    "[[Can you turn]] {state} [[the]] {device}[[?]]",
    "Você pode {state} o/a {device}?",
    category=C,
    example={"state": ("off", "desligar"), "device": ("TV", "TV")},
    note="state: 'on' (ligar), 'off' (desligar), 'up' (aumentar), 'down' (abaixar).",
)
where_did_you_put = chunk(
    "where_did_you_put",
    "[[Where did you put]] {thing}[[?]]",
    "Onde você colocou {thing}?",
    category=C,
    example={"thing": "the keys"},
)
did_you = chunk(
    "did_you",
    "[[Did you]] {action}[[?]]",
    "Você {action}?",
    category=C,
    example={"action": ("sleep well", "dormiu bem")},
)
lets_read = chunk(
    "lets_read",
    "[[Let me read you]] {story}.",
    "Deixa eu ler {story} para você.",
    category=C,
    example={"story": "a story"},
)
