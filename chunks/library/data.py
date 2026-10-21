"""Plataformas de dados: matching, deduplicação, reconciliação, multi-tenant, eventos."""

from chunks.core import chunk

C = "data"

deduplicate = chunk(
    "deduplicate",
    "[[We need to deduplicate]] {records} [[before]] {step}.",
    "Precisamos remover as duplicatas {records} antes {step}.",
    category=C,
    examples=[
        {"records": ("the vendor records", "dos registros de fornecedores"), "step": ("sending them to the API", "de enviar para a API")},
        {"records": ("the customer list", "da lista de clientes"), "step": ("the campaign", "da campanha")},
        {"records": ("the invoices", "das notas fiscais"), "step": ("paying them", "de pagar")},
    ],
)
match_against = chunk(
    "match_against",
    "[[Each new record is matched against]] {target}.",
    "Cada registro novo é comparado com {target}.",
    category=C,
    examples=[
        {"target": ("the existing master records", "os registros mestres que já existem")},
        {"target": ("the client's vendor list", "a lista de fornecedores do cliente")},
        {"target": ("the records from the last import", "os registros da última importação")},
    ],
)
reconcile_with = chunk(
    "reconcile_with",
    "[[We reconcile]] {source} [[with]] {other} [[every]] {period}.",
    "Conciliamos {source} com {other} {period}.",
    category=C,
    examples=[
        {"source": ("our vendor list", "a nossa lista de fornecedores"), "other": ("the client's ERP", "o ERP do cliente"), "period": ("night", "toda noite")},
        {"source": ("the payments", "os pagamentos"), "other": ("the bank statement", "o extrato bancário"), "period": ("day", "todo dia")},
        {"source": ("the stock", "o estoque"), "other": ("the sales system", "o sistema de vendas"), "period": ("week", "toda semana")},
    ],
)
golden_record = chunk(
    "golden_record",
    "[[The golden record is built from]] {sources}.",
    "O registro mestre é montado a partir {sources}.",
    category=C,
    examples=[
        {"sources": ("the most reliable source for each field", "da fonte mais confiável para cada campo")},
        {"sources": ("three different systems", "de três sistemas diferentes")},
        {"sources": ("the latest verified data", "dos dados verificados mais recentes")},
    ],
)
flag_for_review = chunk(
    "flag_for_review",
    "{items} [[are flagged for human review]].",
    "{items} vão para revisão humana.",
    category=C,
    examples=[
        {"items": ("Matches with a score between 0.7 and 0.9", "Os matches com pontuação entre 0,7 e 0,9")},
        {"items": ("Bank account changes", "As trocas de conta bancária")},
        {"items": ("Records with missing tax IDs", "Os registros sem CNPJ")},
    ],
)
is_idempotent = chunk(
    "is_idempotent",
    "{component} [[is idempotent, so processing the same]] {thing} [[twice is safe]].",
    "{component} é idempotente, então processar {thing} duas vezes não causa problema.",
    category=C,
    examples=[
        {"component": ("The consumer", "O consumidor"), "thing": ("message", "a mesma mensagem")},
        {"component": ("The import job", "A rotina de importação"), "thing": ("file", "o mesmo arquivo")},
        {"component": ("The payment API", "A API de pagamentos"), "thing": ("request", "a mesma requisição")},
    ],
)
scoped_to_the_tenant = chunk(
    "scoped_to_the_tenant",
    "[[Every]] {thing} [[is scoped to the tenant]].",
    "{thing} só enxerga os dados do próprio cliente (tenant).",
    category=C,
    examples=[
        {"thing": ("query", "Toda consulta")},
        {"thing": ("API key", "Toda chave de API")},
        {"thing": ("report", "Todo relatório")},
    ],
)
goes_to_the_dead_letter_queue = chunk(
    "goes_to_the_dead_letter_queue",
    "[[After]] {n} [[retries, the message goes to the dead-letter queue]].",
    "Depois de {n} tentativas, a mensagem vai para a fila de mensagens com falha (dead-letter queue).",
    category=C,
    examples=[
        {"n": ("five", "cinco")},
        {"n": ("three", "três")},
        {"n": ("ten", "dez")},
    ],
)
garbage_in_garbage_out = chunk(
    "garbage_in_garbage_out",
    "[[Garbage in, garbage out]]: {consequence}.",
    "Entra lixo, sai lixo: {consequence}.",
    category=C,
    examples=[
        {"consequence": ("if the input data is bad, the payments will be wrong", "se os dados de entrada forem ruins, os pagamentos vão sair errados")},
        {"consequence": ("the model is only as good as the data", "o modelo só é tão bom quanto os dados")},
        {"consequence": ("we have to validate everything first", "temos que validar tudo antes")},
    ],
)
