"""Desenvolvimento, dados, IA e troubleshooting."""

from chunks.core import chunk

C = "tech"

fetch_the_data_from = chunk(
    "fetch_the_data_from",
    "[[We need to fetch the data from]] {source}.",
    "Precisamos buscar os dados de {source}.",
    category=C,
    example={"source": "the SAP database"},
)
clean_up_the_dataset = chunk(
    "clean_up_the_dataset",
    "[[I spent]] {time} [[cleaning up the dataset]].",
    "Passei {time} limpando o dataset.",
    category=C,
    example={"time": ("the whole morning", "a manhã toda")},
)
fine_tune_the_model = chunk(
    "fine_tune_the_model",
    "[[We need]] {resource} [[to fine-tune the model]].",
    "Precisamos de {resource} para ajustar o modelo.",
    category=C,
    example={"resource": "more data"},
)
push_the_changes = chunk(
    "push_the_changes",
    "[[I'll push the changes to]] {branch}.",
    "Vou subir as alterações para {branch}.",
    category=C,
    example={"branch": "the dev branch"},
)
refactor = chunk(
    "refactor",
    "[[We need to refactor]] {code} [[to make it]] {quality}.",
    "Precisamos refatorar {code} para deixá-lo {quality}.",
    category=C,
    example={"code": "the auth module", "quality": ("more maintainable", "mais fácil de manter")},
)
avoid_hardcoding = chunk(
    "avoid_hardcoding",
    "[[Avoid hardcoding]] {thing}[[; use]] {alternative} [[instead]].",
    "Evite deixar {thing} fixo no código; use {alternative}.",
    category=C,
    example={"thing": "the API keys", "alternative": "environment variables"},
)
did_you_test_the_edge_case = chunk(
    "did_you_test_the_edge_case",
    "[[Did you test for the edge case where]] {situation}[[?]]",
    "Você testou o caso extremo em que {situation}?",
    category=C,
    example={"situation": "the user has no internet"},
)
pay_off_tech_debt = chunk(
    "pay_off_tech_debt",
    "[[We need to allocate time]] {when} [[to pay off some tech debt]].",
    "Precisamos reservar tempo {when} para pagar dívida técnica.",
    category=C,
    example={"when": "next sprint"},
)
we_found_the_root_cause = chunk(
    "we_found_the_root_cause",
    "[[We found the root cause of]] {problem}.",
    "Encontramos a causa raiz de {problem}.",
    category=C,
    example={"problem": "the memory leak"},
)
theres_a_workaround = chunk(
    "theres_a_workaround",
    "[[We don't have a fix yet, but there's a workaround for]] {problem}.",
    "Ainda não temos correção, mas há uma solução paliativa para {problem}.",
    category=C,
    example={"problem": "the timeout issue"},
)
i_cant_reproduce_the_bug = chunk(
    "i_cant_reproduce_the_bug",
    "[[I can't reproduce the bug on]] {env}.",
    "Não consigo reproduzir o bug em {env}.",
    category=C,
    example={"env": "my local machine"},
)
lets_roll_back_to = chunk(
    "lets_roll_back_to",
    "[[Let's roll back to]] {version}.",
    "Vamos reverter para {version}.",
    category=C,
    example={"version": "v1.2"},
)
we_deployed_a_hotfix = chunk(
    "we_deployed_a_hotfix",
    "[[We deployed a hotfix to address]] {problem}.",
    "Fizemos o deploy de uma correção urgente para {problem}.",
    category=C,
    example={"problem": "the payment issue"},
)
it_turned_out_to_be = chunk(
    "it_turned_out_to_be",
    "[[It turned out to be]] {cause}.",
    "No fim das contas era {cause}.",
    category=C,
    example={"cause": "a missing index"},
)
we_ran_into = chunk(
    "we_ran_into",
    "[[We ran into]] {problem} [[while]] {action}.",
    "Esbarramos em {problem} enquanto {action}.",
    category=C,
    example={"problem": "a major issue", "action": "migrating the database"},
)
can_you_take_a_look_at = chunk(
    "can_you_take_a_look_at",
    "[[Can you take a look at]] {thing} [[when you get a chance]]?",
    "Você pode dar uma olhada em {thing} quando puder?",
    category=C,
    example={"thing": "my PR"},
)
its_integrated_with = chunk(
    "its_integrated_with",
    "{system} [[is integrated with]] {other}.",
    "{system} está integrado com {other}.",
    category=C,
    example={"system": "The dashboard", "other": "the SAP API"},
)
