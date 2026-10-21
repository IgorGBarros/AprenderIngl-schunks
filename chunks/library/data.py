"""Plataformas de dados: matching, deduplicação, reconciliação, multi-tenant, eventos."""

from chunks.core import chunk

C = "data"

deduplicate = chunk(
    "deduplicate",
    "[[We need to deduplicate]] {records} [[before]] {step}.",
    "Precisamos deduplicar {records} antes de {step}.",
    category=C,
    example={"records": "the vendor records", "step": ("sending them to the API", "enviar para a API")},
)
match_against = chunk(
    "match_against",
    "[[Each new record is matched against]] {target}.",
    "Cada registro novo é comparado com {target}.",
    category=C,
    example={"target": "the existing master records"},
)
reconcile_with = chunk(
    "reconcile_with",
    "[[We reconcile]] {source} [[with]] {other} [[every]] {period}.",
    "Reconciliamos {source} com {other} todo(a) {period}.",
    category=C,
    example={"source": "our vendor list", "other": "the client's ERP", "period": ("night", "noite")},
)
golden_record = chunk(
    "golden_record",
    "[[The golden record is built from]] {sources}.",
    "O registro mestre (golden record) é montado a partir de {sources}.",
    category=C,
    example={"sources": "the most reliable source for each field"},
)
flag_for_review = chunk(
    "flag_for_review",
    "{items} [[are flagged for human review]].",
    "{items} são marcados para revisão humana.",
    category=C,
    example={"items": "Matches with a score between 0.7 and 0.9"},
)
is_idempotent = chunk(
    "is_idempotent",
    "{component} [[is idempotent, so processing the same]] {thing} [[twice is safe]].",
    "{component} é idempotente, então processar o(a) mesmo(a) {thing} duas vezes é seguro.",
    category=C,
    example={"component": "The consumer", "thing": ("message", "mensagem")},
)
scoped_to_the_tenant = chunk(
    "scoped_to_the_tenant",
    "[[Every]] {thing} [[is scoped to the tenant]].",
    "Todo(a) {thing} é restrito(a) ao cliente (tenant).",
    category=C,
    example={"thing": ("query", "consulta")},
)
goes_to_the_dead_letter_queue = chunk(
    "goes_to_the_dead_letter_queue",
    "[[After]] {n} [[retries, the message goes to the dead-letter queue]].",
    "Depois de {n} tentativas, a mensagem vai para a dead-letter queue.",
    category=C,
    example={"n": "five"},
)
garbage_in_garbage_out = chunk(
    "garbage_in_garbage_out",
    "[[Garbage in, garbage out]]: {consequence}.",
    "Entra lixo, sai lixo: {consequence}.",
    category=C,
    example={"consequence": "if the input data is bad, the payments will be wrong"},
)
