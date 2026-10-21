"""Desenvolvimento, dados, IA e troubleshooting."""

from chunks.core import chunk

C = "tech"

fetch_the_data_from = chunk(
    "fetch_the_data_from",
    "[[We need to fetch the data from]] {source}.",
    "Precisamos buscar os dados {source}.",
    category=C,
    examples=[
        {"source": ("the SAP database", "do banco do SAP")},
        {"source": ("the client's API", "da API do cliente")},
        {"source": ("these spreadsheets", "destas planilhas")},
    ],
)
clean_up_the_dataset = chunk(
    "clean_up_the_dataset",
    "[[I spent]] {time} [[cleaning up the dataset]].",
    "Passei {time} limpando o dataset.",
    category=C,
    examples=[
        {"time": ("the whole morning", "a manhã inteira")},
        {"time": ("two days", "dois dias")},
        {"time": ("an hour", "uma hora")},
    ],
)
fine_tune_the_model = chunk(
    "fine_tune_the_model",
    "[[We need]] {resource} [[to fine-tune the model]].",
    "Precisamos de {resource} para fazer o ajuste fino do modelo.",
    category=C,
    examples=[
        {"resource": ("more data", "mais dados")},
        {"resource": ("labeled examples", "exemplos rotulados")},
        {"resource": ("a bigger GPU", "uma GPU maior")},
    ],
)
push_the_changes = chunk(
    "push_the_changes",
    "[[I'll push the changes to]] {branch}.",
    "Vou subir as alterações {branch}.",
    category=C,
    examples=[
        {"branch": ("the dev branch", "para a branch de dev")},
        {"branch": ("main", "para a main")},
        {"branch": ("my fork", "para o meu fork")},
    ],
)
refactor = chunk(
    "refactor",
    "[[We need to refactor]] {code} [[to make it]] {quality}.",
    "Precisamos refatorar {code} para deixar {quality}.",
    category=C,
    examples=[
        {"code": ("the auth module", "o módulo de autenticação"), "quality": ("more maintainable", "mais fácil de manter")},
        {"code": ("this function", "esta função"), "quality": ("easier to test", "mais fácil de testar")},
        {"code": ("the API layer", "a camada da API"), "quality": ("faster", "mais rápida")},
    ],
)
avoid_hardcoding = chunk(
    "avoid_hardcoding",
    "[[Avoid hardcoding]] {thing}[[; use]] {alternative} [[instead]].",
    "Evite colocar {thing} direto no código; use {alternative}.",
    category=C,
    examples=[
        {"thing": ("the API keys", "as chaves da API"), "alternative": ("environment variables", "variáveis de ambiente")},
        {"thing": ("the URL", "a URL"), "alternative": ("a config file", "um arquivo de configuração")},
        {"thing": ("the tax rate", "a alíquota"), "alternative": ("a database table", "uma tabela no banco")},
    ],
)
did_you_test_the_edge_case = chunk(
    "did_you_test_the_edge_case",
    "[[Did you test for the edge case where]] {situation}[[?]]",
    "Você testou o caso extremo em que {situation}?",
    category=C,
    examples=[
        {"situation": ("the user has no internet", "o usuário está sem internet")},
        {"situation": ("the list is empty", "a lista está vazia")},
        {"situation": ("two requests arrive at the same time", "chegam duas requisições ao mesmo tempo")},
    ],
)
pay_off_tech_debt = chunk(
    "pay_off_tech_debt",
    "[[We need to allocate time]] {when} [[to pay off some tech debt]].",
    "Precisamos reservar tempo {when} para pagar parte da dívida técnica.",
    category=C,
    examples=[
        {"when": ("next sprint", "na próxima sprint")},
        {"when": ("every Friday", "toda sexta")},
        {"when": ("this quarter", "neste trimestre")},
    ],
)
we_found_the_root_cause = chunk(
    "we_found_the_root_cause",
    "[[We found the root cause of]] {problem}.",
    "Encontramos a causa raiz {problem}.",
    category=C,
    examples=[
        {"problem": ("the memory leak", "do vazamento de memória")},
        {"problem": ("the outage", "da queda do sistema")},
        {"problem": ("the duplicate records", "dos registros duplicados")},
    ],
)
theres_a_workaround = chunk(
    "theres_a_workaround",
    "[[We don't have a fix yet, but there's a workaround for]] {problem}.",
    "Ainda não temos a correção, mas há uma solução provisória para {problem}.",
    category=C,
    examples=[
        {"problem": ("the timeout issue", "o problema de timeout")},
        {"problem": ("the login error", "o erro no login")},
        {"problem": ("the slow report", "o relatório lento")},
    ],
)
i_cant_reproduce_the_bug = chunk(
    "i_cant_reproduce_the_bug",
    "[[I can't reproduce the bug on]] {env}.",
    "Não consigo reproduzir o bug {env}.",
    category=C,
    examples=[
        {"env": ("my local machine", "na minha máquina")},
        {"env": ("staging", "em homologação")},
        {"env": ("Chrome", "no Chrome")},
    ],
)
lets_roll_back_to = chunk(
    "lets_roll_back_to",
    "[[Let's roll back to]] {version}.",
    "Vamos voltar para {version}.",
    category=C,
    examples=[
        {"version": ("v1.2", "a v1.2")},
        {"version": ("the previous version", "a versão anterior")},
        {"version": ("yesterday's release", "a release de ontem")},
    ],
)
we_deployed_a_hotfix = chunk(
    "we_deployed_a_hotfix",
    "[[We deployed a hotfix to address]] {problem}.",
    "Subimos uma correção urgente para resolver {problem}.",
    category=C,
    examples=[
        {"problem": ("the payment issue", "o problema no pagamento")},
        {"problem": ("the broken login", "o login quebrado")},
        {"problem": ("the security vulnerability", "a falha de segurança")},
    ],
)
it_turned_out_to_be = chunk(
    "it_turned_out_to_be",
    "[[It turned out to be]] {cause}.",
    "No fim, era {cause}.",
    category=C,
    examples=[
        {"cause": ("a missing index", "um índice faltando")},
        {"cause": ("a typo in the config", "um erro de digitação na configuração")},
        {"cause": ("an expired certificate", "um certificado vencido")},
    ],
)
we_ran_into = chunk(
    "we_ran_into",
    "[[We ran into]] {problem} [[while]] {action}.",
    "Demos de cara com {problem} enquanto {action}.",
    category=C,
    examples=[
        {"problem": ("a major issue", "um problema sério"), "action": ("migrating the database", "migrávamos o banco")},
        {"problem": ("a memory leak", "um vazamento de memória"), "action": ("load testing", "fazíamos o teste de carga")},
        {"problem": ("some duplicates", "algumas duplicatas"), "action": ("importing the data", "importávamos os dados")},
    ],
)
can_you_take_a_look_at = chunk(
    "can_you_take_a_look_at",
    "[[Can you take a look at]] {thing} [[when you get a chance]]?",
    "Você pode dar uma olhada {thing} quando puder?",
    category=C,
    examples=[
        {"thing": ("my PR", "no meu PR")},
        {"thing": ("this error", "neste erro")},
        {"thing": ("the new design", "no novo layout")},
    ],
)
its_integrated_with = chunk(
    "its_integrated_with",
    "{system} [[is integrated with]] {other}.",
    "{system} está integrado com {other}.",
    category=C,
    examples=[
        {"system": ("The dashboard", "O dashboard"), "other": ("the SAP API", "a API do SAP")},
        {"system": ("Our app", "O nosso app"), "other": ("Stripe", "o Stripe")},
        {"system": ("The CRM", "O CRM"), "other": ("our email tool", "a nossa ferramenta de e-mail")},
    ],
)
