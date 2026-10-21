"""DistantJob — Senior Software Engineer, Vendor Data Platform (cliente nos EUA).

Vaga: plataforma que limpa, cruza (matching) e unifica dados de fornecedores
(vendors) de várias empresas clientes (multi-tenant) e entrega esses dados
para produtos de pagamento via API. Stack: Python, TypeScript (Angular ou
React), SQL, Azure ou AWS, REST, arquitetura orientada a eventos.

Processo típico da DistantJob: (1) conversa com o recrutador, (2) entrevistas
técnicas com o cliente (tech lead / time), às vezes um exercício prático.
"""

from chunks.interviews import Question, Session, Stage, register

Q = Question

STAGES = (
    Stage(
        "screen",
        "Recrutador",
        "Primeira conversa com a DistantJob: trajetória, motivação, inglês, horário, "
        "salário e disponibilidade. Eles filtram encaixe e comunicação, não código.",
    ),
    Stage(
        "experience",
        "Experiência (STAR)",
        "Perguntas comportamentais. Responda sempre com uma história real: "
        "Situation, Task, Action, Result.",
    ),
    Stage(
        "technical",
        "Técnica",
        "Python, APIs, SQL, multi-tenant, eventos, nuvem, frontend e testes.",
    ),
    Stage(
        "domain",
        "Dados de fornecedores",
        "O coração da vaga: matching, deduplicação, reconciliação e qualidade de dados "
        "num contexto de pagamentos.",
    ),
    Stage(
        "design",
        "System design",
        "Desenhar a plataforma no quadro: ingestão, processamento, armazenamento, API e escala.",
    ),
    Stage(
        "closing",
        "Suas perguntas e encerramento",
        "Perguntar bem mostra senioridade. Tenha 3 ou 4 perguntas prontas.",
    ),
)

QUESTIONS = (
    # ------------------------------------------------------------ recrutador
    Q(
        "about_you",
        "screen",
        "So, Igor, could you walk me through your background?",
        "Seu pitch de 90 segundos. Querem ver se você se comunica bem em inglês e se a sua "
        "história leva naturalmente até esta vaga.",
        "Sure! [[I've been working in]] tech and data [[for]] ((about six years)). "
        "[[I currently work as]] a Data Analyst ((at an oil refinery in Brazil)), "
        "[[where I'm responsible for]] building data pipelines and dashboards with Python. "
        "In parallel, I founded PGBA Solutions, [[where I've been hands-on with]] the whole stack: "
        "Python backends with Django and FastAPI, React and TypeScript frontends, PostgreSQL, "
        "and integrations with third-party APIs. "
        "A lot of my work is exactly what this role describes: taking data from different sources, "
        "cleaning it, matching records and exposing them through APIs. "
        "[[I'm now looking to]] focus that experience on one product with a strong engineering team, "
        "[[and that's what brought me here today]].",
        tips=(
            "Estrutura: presente → passado → futuro → ligação com a vaga. No máximo 90 segundos.",
            "Ensaie em voz alta até sair sem ler. Grave no celular e ouça.",
            "Termine falando da vaga, assim a próxima pergunta vem para o seu terreno.",
        ),
        follow_ups=(
            "How many years have you worked professionally with Python?",
            "What does PGBA do, exactly?",
        ),
    ),
    Q(
        "why_role",
        "screen",
        "What caught your attention about this role?",
        "Se você leu a descrição e se o seu interesse é real (não só 'qualquer vaga remota').",
        "Two things. First, the problem itself. [[Turning messy data into]] clean, trustworthy records "
        "is the kind of work I enjoy most, and I deal with it every day ((with SAP and spreadsheet "
        "data at the refinery)). "
        "Second, the ownership. The description says this is not a 'pick up tickets' role, "
        "[[and that's exactly what I'm looking for]]: being involved from the first scoping "
        "conversation all the way to production.",
        tips=(
            "Cite algo específico da descrição: 'garbage in, garbage out', ownership, matching.",
        ),
    ),
    Q(
        "why_leave",
        "screen",
        "Why are you looking for a new opportunity right now?",
        "Se há algum problema (conflito, demissão) e se você vai ficar. Querem uma motivação positiva.",
        "[[To be honest]], I'm not running away from anything. I've learned a lot in my current role, "
        "but [[I'm looking to]] work on a software product at scale, with a strong engineering team "
        "and in an international environment. [[I believe]] this role is the right next step for that.",
        tips=(
            "Nunca fale mal do emprego atual.",
            "Fale do que você busca, não do que você quer evitar.",
        ),
    ),
    Q(
        "pgba_conflict",
        "screen",
        "You run your own company. How would that work with a full-time position?",
        "PERGUNTA QUASE CERTA. A DistantJob contrata em tempo integral e exclusivo (8h/dia). "
        "Querem ter certeza de que a PGBA não vai competir com o trabalho.",
        "[[That's a fair question.]] ((Decida antes e diga a verdade: por exemplo, 'PGBA would be "
        "on hold' / 'my partner would run the day-to-day' / 'I'd only keep it outside working "
        "hours, with no conflict of interest')). "
        "[[To be clear]], this position would be my main focus: full-time, eight hours a day, "
        "aligned with US business hours.",
        tips=(
            "Decida a resposta real ANTES da entrevista. Hesitar aqui pesa muito.",
            "Transforme a PGBA em ponto forte: é onde você teve ownership de ponta a ponta.",
        ),
    ),
    Q(
        "us_hours",
        "screen",
        "This role requires overlap with US business hours. Does that work for you?",
        "Confirmação prática de disponibilidade.",
        "Yes, [[I'm fully comfortable with that]]. Brazil is usually one or two hours ahead of "
        "US Eastern time, depending on daylight saving, [[so I could easily work]] "
        "((from 10 AM to 7 PM Brasília time)). If the team is on the West Coast, "
        "I can shift my day later.",
        tips=(
            "Brasília (UTC-3) fica 2h à frente de Nova York no inverno de lá e 1h no verão de lá.",
            "Pergunte de volta: 'Which time zone is the team in?'",
        ),
    ),
    Q(
        "start_date",
        "screen",
        "When would you be available to start?",
        "Prazo de aviso prévio e quando você realmente pode começar.",
        "I'd need ((two weeks / thirty days)) to hand over my current responsibilities properly, "
        "[[so I could start]] ((around date)).",
        tips=("Sair do jeito certo do emprego atual é bem visto. Não prometa 'amanhã'.",),
    ),
    Q(
        "salary",
        "screen",
        "What are your salary expectations?",
        "Se você cabe no orçamento. A DistantJob costuma pagar em dólar, por mês, como contractor.",
        "Based on my research for senior remote roles with this scope, "
        "[[I'm looking for something in the range of]] ((X to Y US dollars per month)). "
        "[[That said, I'm open to]] discussing the full package. "
        "[[Is that within the budget for this role?]]",
        tips=(
            "Responda em dólares por MÊS (é como a DistantJob costuma falar).",
            "Pesquise antes. O piso da faixa tem que ser um valor que você aceitaria.",
            "Contractor não tem 13º, férias pagas nem FGTS: considere isso no valor.",
        ),
    ),
    Q(
        "contractor",
        "screen",
        "The position is as an independent contractor. Are you comfortable with that?",
        "Se você sabe emitir nota/fatura para o exterior e receber em dólar.",
        "Yes. ((I already have a company / CNPJ)), so invoicing an international client and "
        "receiving in US dollars [[won't be a problem]].",
        tips=("Confirme com seu contador como faturar exportação de serviços antes da conversa.",),
    ),
    Q(
        "english",
        "screen",
        "How comfortable are you working in English day to day?",
        "Se você vai conseguir participar de reuniões, code reviews e Slack com o time americano.",
        "I read and write in English every day: documentation, code, technical discussions. "
        "Speaking is the skill [[I've been actively improving]], ((with daily practice)). "
        "In technical conversations I'm comfortable, and [[if I don't understand something, "
        "I ask]] instead of assuming. I think that matters more than a perfect accent.",
        tips=(
            "Seja honesto. A própria entrevista já é o teste.",
            "Se não entender uma pergunta: 'Sorry, could you rephrase that?'",
        ),
    ),
    Q(
        "other_processes",
        "screen",
        "Are you interviewing with other companies at the moment?",
        "Urgência e concorrência. Não precisa dar nomes.",
        "((Answer honestly: 'I'm in early conversations with a couple of companies' or 'Not "
        "actively')), but this role is [[at the top of my list]] because it matches what I do best.",
    ),
    # --------------------------------------------------------- experiência
    Q(
        "proud_project",
        "experience",
        "Tell me about a project you owned from design to production.",
        "Ownership real. Querem ouvir decisões que VOCÊ tomou, não só tarefas que executou.",
        "[[Sure, let me think of a good example.]] At PGBA, ((we built a SaaS for ...)). "
        "[[The situation was that]] ((the client had ... problem)). "
        "[[My task was to]] design and build it end to end. "
        "[[What I did was]] ((define the data model in PostgreSQL, build the API with Django/FastAPI, "
        "the React frontend, set up deploy and monitoring)). "
        "[[As a result]], ((numbers: users, time saved, revenue)). "
        "[[What I learned was]] ((one real lesson)).",
        tips=(
            "Use 'I' para o que você fez. 'We' só para o contexto do time.",
            "Tenha números: usuários, tempo, custo, erros. Sem números a história perde força.",
        ),
        follow_ups=(
            "What would you do differently today?",
            "What was the hardest technical decision?",
        ),
    ),
    Q(
        "messy_data",
        "experience",
        "Tell me about a time you had to deal with messy data from multiple sources.",
        "Experiência direta com o problema da vaga.",
        "[[The situation was that]] ((we were pulling data from SAP and spreadsheets)), and the "
        "same entity appeared with different names, formats and duplicates. "
        "[[My task was to]] build one reliable dataset for ((reporting)). "
        "[[What I did was]] create a Python pipeline that first standardized the fields, "
        "then deduplicated using ((the key you used)), and added validation checks that flagged "
        "bad records instead of silently fixing them. "
        "[[As a result]], ((the report went from X days to Y hours / errors dropped by Z%)).",
        tips=(
            "Esta é a sua melhor história para esta vaga: prepare-a com detalhes reais.",
            "Na mensagem ao recrutador você disse que lida com matching e deduplicação multi-tenant. "
            "Tenha um exemplo concreto que sustente isso.",
        ),
    ),
    Q(
        "incident",
        "experience",
        "Tell me about a production issue you were responsible for. What happened?",
        "Como você age sob pressão e se aprende com o erro (postmortem).",
        "[[We ran into]] a major performance issue ((at PGBA)): ((some pages took over ten seconds)). "
        "[[What I did was]] [[dive deep into]] the PostgreSQL logs and query plans. "
        "[[It turned out to be]] missing indexes and N+1 queries in the Django ORM. "
        "I added the indexes, fixed the queries with select_related and prefetch_related, "
        "and added a test that fails if the number of queries grows. "
        "[[As a result]], ((response time dropped from X to Y)). "
        "After that, [[I made sure to]] monitor slow queries in production.",
        tips=("Confirme os números reais. Termine sempre com o que mudou para não repetir.",),
    ),
    Q(
        "disagreement",
        "experience",
        "Tell me about a time you disagreed with a technical decision.",
        "Se você sabe discordar com respeito e com dados, e depois seguir em frente.",
        "((Situation)). I disagreed because ((reason)). Instead of arguing in the meeting, "
        "I wrote down the trade-offs and built a small proof of concept to compare both options. "
        "((Outcome: we went with X)). Even when the decision doesn't go my way, "
        "[[I'm a big believer in]] 'disagree and commit': once we decide, I fully support it.",
        tips=("Nunca conte uma história em que o outro era 'burro'. Mostre respeito.",),
    ),
    Q(
        "mistake",
        "experience",
        "Tell me about a mistake you made and what you learned from it.",
        "Autocrítica e maturidade. Fugir da pergunta é a pior resposta.",
        "((A real mistake: e.g. I ran a database migration that locked a large table in production)). "
        "[[To be honest]], it was my fault: ((what went wrong)). I fixed it by ((action)) and "
        "communicated clearly with ((the client / team)). "
        "[[What I learned was]] ((to test migrations with production-sized data and keep them "
        "backwards compatible)).",
        tips=("Escolha um erro real, já resolvido, e foque no aprendizado.",),
    ),
    Q(
        "unclear_requirements",
        "experience",
        "How do you work with product when the requirements are unclear?",
        "A vaga diz 'partner closely with product'. Querem autonomia sem sair construindo a coisa errada.",
        "First, I ask questions to understand the problem behind the request: who is the user and "
        "[[what does success look like]]. Then I write down my assumptions and "
        "[[align on the requirements]] before coding. "
        "If there's still uncertainty, I [[build a quick proof of concept]] or a small slice and "
        "demo it early. It's much cheaper to change direction after two days than after two months.",
    ),
    Q(
        "priorities",
        "experience",
        "How do you handle several urgent priorities at the same time?",
        "Organização e comunicação num ambiente rápido.",
        "I make the trade-offs visible. I list what's on my plate, estimate the impact of each item, "
        "and [[sync up with]] the tech lead or product to agree on the order. "
        "Production issues affecting clients come first. "
        "And [[I keep people in the loop]]: if something will slip, they hear it from me early.",
    ),
    Q(
        "code_review",
        "experience",
        "What do you look for when you review someone's code?",
        "Qualidade e colaboração: a vaga cita code review e testes.",
        "First, correctness: does it solve the problem, and what about the edge cases? "
        "Then tests, readability and naming, and any security or data-isolation risk, which is "
        "critical in a multi-tenant system. "
        "I try to keep comments about the code, not the person, and I separate blocking issues "
        "from suggestions. And I prefer small pull requests: they get better reviews.",
    ),
    # ------------------------------------------------------------- técnica
    Q(
        "api_design",
        "technical",
        "How do you design a REST API that other systems depend on?",
        "Os produtos de pagamento dependem da API. Querem ver cuidado com contrato e compatibilidade.",
        "I treat the API as a contract. I model it around resources, version it from day one, "
        "and never break existing clients: new fields are additive. "
        "I use consistent error formats, cursor-based pagination for large lists, and "
        "idempotency keys on POST requests, so a retry never creates a duplicate. "
        "With FastAPI, the OpenAPI documentation comes for free. "
        "And authentication defines the tenant, so every request is scoped to one client.",
        follow_ups=(
            "How would you version the API?",
            "What is idempotency and why does it matter here?",
        ),
    ),
    Q(
        "django_fastapi",
        "technical",
        "When would you choose FastAPI over Django?",
        "Se você conhece os trade-offs, não só a sintaxe.",
        "Django is great when I need a full product quickly: ORM, migrations, admin and auth out of "
        "the box. The admin is perfect for internal operator screens. "
        "FastAPI shines for API-first services: it's async, very fast, and the type hints give me "
        "validation and documentation automatically. "
        "[[As a rule of thumb]], Django for the core product with many models, "
        "FastAPI for focused, high-throughput services.",
    ),
    Q(
        "sql_duplicates",
        "technical",
        "How would you find duplicate vendors using SQL?",
        "SQL sólido: normalização, window functions, índices e similaridade.",
        "First I'd normalize the key fields, for example upper case, trimmed names without "
        "punctuation, and tax IDs with digits only. "
        "For exact duplicates, I'd use a window function: ROW_NUMBER() OVER (PARTITION BY tenant_id, "
        "normalized_tax_id ORDER BY updated_at DESC), and everything with row number greater than one "
        "is a duplicate candidate. "
        "For fuzzy duplicates in PostgreSQL, I'd use the pg_trgm extension with a trigram index "
        "to compare name similarity, but only inside smaller blocks, like the same ZIP code, "
        "to avoid comparing every record with every other one.",
        tips=("Se pedirem para escrever a query, fale enquanto escreve: 'I'm partitioning by...'",),
    ),
    Q(
        "slow_endpoint",
        "technical",
        "An endpoint suddenly became slow in production. How do you investigate?",
        "Método de investigação, não chute.",
        "First I measure instead of guessing: logs, APM traces and which tenant or input is slow. "
        "[[Nine times out of ten]], it's the database, so I look at the slow queries and run "
        "EXPLAIN ANALYZE. Typical causes are a missing index, an N+1 query, or a query without "
        "pagination that grew with the data. "
        "I fix the root cause, add a test or an alert so it doesn't come back, "
        "and only then think about caching.",
    ),
    Q(
        "multi_tenant",
        "technical",
        "How would you design a multi-tenant system? How do you guarantee one client never sees "
        "another client's data?",
        "Requisito explícito da vaga e risco grave em pagamentos.",
        "There are three common models: a shared schema with a tenant_id column, a schema per "
        "tenant, or a database per tenant. [[The trade-off is]] isolation versus cost and "
        "operational complexity. For many clients, I'd usually start with a shared schema and "
        "tenant_id on every table. "
        "Then I'd enforce isolation in layers: the tenant comes from the authentication token, "
        "never from the request body; all queries go through a base repository that filters by "
        "tenant; PostgreSQL row-level security as a safety net; and automated tests that try to "
        "read another tenant's data and must fail. "
        "I'd also watch for noisy neighbors: one big client shouldn't slow down everyone else.",
    ),
    Q(
        "event_driven",
        "technical",
        "Have you worked with event-driven or message-based architectures? How do you handle "
        "failures?",
        "Experiência com filas e, principalmente, se você entende entrega 'at-least-once'.",
        "Yes, ((describe what you used: for example Celery with Redis or RabbitMQ, SQS...)). "
        "The key thing is that most queues deliver messages at least once, so consumers must be "
        "idempotent: processing the same message twice can't create a duplicate. "
        "I use retries with exponential backoff and a dead-letter queue for messages that keep "
        "failing, so they can be inspected and replayed. "
        "To avoid saving to the database and failing to publish the event, I use the outbox "
        "pattern. And I monitor queue depth and age, because a growing queue is an early warning.",
        tips=(
            "Se a sua experiência for só com Celery, diga isso. Os conceitos são os mesmos.",
        ),
    ),
    Q(
        "big_file",
        "technical",
        "A client uploads a file with two million vendor records. How do you process it?",
        "Processamento assíncrono e robusto, um cenário real da vaga.",
        "Not inside the HTTP request. The API stores the file in blob storage, like S3 or Azure "
        "Blob, and returns 202 Accepted with a job ID. "
        "A worker splits the file into batches and publishes them to a queue, so several workers "
        "can process in parallel. Each record is validated: good records continue, bad records go "
        "to a report with the reason, so one bad line doesn't fail the whole file. "
        "The client can follow the progress through the job status endpoint, and the processing is "
        "idempotent, so if a worker crashes we can safely resume.",
    ),
    Q(
        "testing",
        "technical",
        "What's your testing strategy?",
        "Disciplina de qualidade.",
        "Mostly fast unit tests with pytest, some integration tests against a real PostgreSQL, "
        "and a few end-to-end tests for the critical flows. "
        "For matching logic specifically, I'd keep a labeled set of tricky real-world examples, "
        "like 'ACME Inc.' versus 'Acme Incorporated', and run it in CI, so any change to the rules "
        "shows exactly which matches improved or broke. "
        "And contract tests for the API, because other systems depend on it.",
    ),
    Q(
        "cloud",
        "technical",
        "What's your experience with Azure or AWS?",
        "Requisito da vaga. Honestidade aqui vale mais do que fingir.",
        "((List what you really used, e.g. 'On AWS, I've used EC2, S3 and RDS for PGBA's "
        "products')). "
        "[[I haven't used]] ((Azure)) [[in production yet, but]] the concepts map directly: "
        "Blob Storage is like S3, Service Bus is like SQS and SNS, Azure Functions are like Lambda. "
        "[[I'm confident I can ramp up quickly]].",
        tips=("Nunca diga que usou algo que não usou: a próxima pergunta vai expor isso.",),
    ),
    Q(
        "frontend",
        "technical",
        "Tell me about your frontend experience. Have you worked with Angular?",
        "A vaga é full-stack: telas para operadores.",
        "My frontend experience is mostly React with TypeScript. ((For example, I recently built "
        "a mobile web app with React, TypeScript and Vite.)) "
        "[[I haven't used]] Angular [[professionally, but]] it's also TypeScript and components, "
        "and I'm familiar with the ideas behind it, like services and dependency injection. "
        "For this platform, I imagine screens like a review queue, where operators confirm or "
        "reject suggested matches. I'd focus on making that fast with keyboard shortcuts and "
        "showing why the system suggested each match.",
    ),
    # ------------------------------------------------- dados de fornecedores
    Q(
        "dedup_vendors",
        "domain",
        "How would you deduplicate vendors coming from different clients and systems?",
        "A pergunta central da vaga. Querem um processo, não uma biblioteca mágica.",
        "I'd build it as a pipeline. "
        "First, standardize: names in the same case, without punctuation and legal suffixes like "
        "Inc or LLC, addresses in a standard format, tax IDs with digits only. "
        "Second, use strong identifiers first: if the tax ID or bank account matches, that's "
        "a very strong signal. "
        "Third, blocking: only compare records that share something, like the ZIP code or the "
        "first letters of the name, to avoid comparing millions of pairs. "
        "Fourth, score the candidates with fuzzy similarity on name and address, and use two "
        "thresholds: high scores are matched automatically, the gray zone goes to human review, "
        "low scores are different vendors. "
        "Finally, survivorship rules build the golden record, and I never delete the source "
        "records, so every decision is traceable and reversible. "
        "And I'd measure precision and recall on a labeled set before changing any threshold.",
        follow_ups=(
            "What similarity algorithms would you use?",
            "How do you choose the thresholds?",
        ),
        tips=(
            "Palavras-chave que eles esperam: standardization, blocking, scoring, thresholds, "
            "human review, golden record, survivorship, lineage, precision/recall.",
        ),
    ),
    Q(
        "false_match",
        "domain",
        "What's worse in this domain: a false match or a missed match?",
        "Pergunta de senioridade: entender o impacto de negócio do erro.",
        "In payments, a false match is usually worse. If we merge two different vendors, "
        "money can go to the wrong company or the wrong bank account, and that's very hard to undo. "
        "A missed match creates a duplicate vendor, which is bad, but we can detect and merge it "
        "later. "
        "So I'd set a high threshold for automatic merges and send the uncertain cases to review. "
        "[[That said]], duplicates also cause real problems, like paying the same invoice twice, "
        "so I'd monitor both rates per client.",
    ),
    Q(
        "data_quality",
        "domain",
        "What data-quality checks would you put in place?",
        "'Clean, trustworthy records' é o produto. Como você garante isso?",
        "On ingestion: schema validation, required fields and format checks, for example tax ID "
        "length and checksum or bank routing numbers. "
        "Records that fail go to quarantine with a clear reason, instead of being silently fixed "
        "or dropped. "
        "Then checks on the dataset: volume anomalies, like a client file with half the usual "
        "rows, duplicate rate per tenant, and freshness. "
        "All of that goes to dashboards and alerts, so we find problems before the payment "
        "products do.",
    ),
    Q(
        "reconciliation",
        "domain",
        "How would you reconcile vendor records between our platform and a client's ERP?",
        "Reconciliação entre fontes, citada como bônus na vaga.",
        "I'd keep a crosswalk table that maps each source system and source ID to our master "
        "vendor ID. "
        "Then I'd compare snapshots and classify every record: matched, matched with different "
        "fields, only in the ERP, or only in our platform. "
        "Each category has an action: some are fixed automatically, others go to a report or a "
        "review queue. "
        "It runs on a schedule, it's idempotent, and it keeps history, so we can show the client "
        "what changed and when.",
    ),
    Q(
        "ai_matching",
        "domain",
        "How would you use AI or LLMs to help with matching?",
        "Bônus da vaga: AI-assisted matching. Querem uso sensato, não hype.",
        "I'd use AI where the rules struggle, not everywhere. "
        "Embeddings can help find candidate pairs that string similarity misses, like abbreviations "
        "or translated names. "
        "An LLM can act as a tie-breaker for the gray zone, returning a decision and an explanation "
        "that the operator can see. "
        "But I'd keep a human in the loop for anything that affects payments, measure it against a "
        "labeled set, and watch cost, latency and data privacy. "
        "Day to day, I also use AI coding tools ((like ...)) to move faster, always reviewing what "
        "they produce.",
    ),
    Q(
        "bank_change",
        "domain",
        "A vendor's bank account changes in one of the sources. What should the platform do?",
        "Consciência de risco em pagamentos (fraude por troca de dados bancários é comum).",
        "I'd treat it as a high-risk change. A bank account change is a classic fraud pattern in "
        "accounts payable. "
        "So the platform shouldn't propagate it automatically: flag it, keep the previous value "
        "active, require verification, and record everything in an audit log. "
        "I'd also notify the client and alert if the same account suddenly appears on several "
        "unrelated vendors.",
    ),
    # ------------------------------------------------------- system design
    Q(
        "system_design",
        "design",
        "Design a platform that ingests vendor data from many client firms, cleans and unifies it, "
        "and serves it to payment products through an API.",
        "Visão de arquitetura de ponta a ponta. Comece perguntando, depois desenhe por camadas.",
        "[[Before I start, can I ask a few questions?]] How many clients and records, how often "
        "the data changes, and how fresh it needs to be for the payment products. "
        "Then I'd split it into layers. "
        "Ingestion: clients send data by API or file upload; raw data goes to blob storage "
        "untouched, and an event starts processing. "
        "Processing: event-driven workers validate, standardize, match and merge, each step "
        "idempotent, with a dead-letter queue. "
        "Storage: PostgreSQL with tenants, source records, master vendors, match links and an "
        "audit log. "
        "Review: an operator screen for the uncertain matches. "
        "Serving: a versioned REST API for the golden records, plus events or webhooks when a "
        "vendor changes. "
        "Across everything: tenant isolation, monitoring and data-quality alerts. "
        "[[I'd start simple]] and only split into more services when the volume requires it.",
        tips=(
            "Fale enquanto desenha. Pergunte antes de desenhar.",
            "Use: 'Let me start with the big picture, and then we can zoom in.'",
        ),
        follow_ups=(
            "How would you scale it when the volume grows ten times?",
            "Where would you put the matching logic?",
        ),
    ),
    Q(
        "scale_10x",
        "design",
        "How would you scale it if the volume grew ten times?",
        "Gargalos reais e não reescrever tudo.",
        "First I'd find the real bottleneck with metrics. Usually it's matching, because it grows "
        "faster than the data. "
        "So I'd make matching incremental, comparing only new or changed records, with good "
        "blocking keys and indexes. "
        "Workers scale horizontally from the queue depth, and large clients can be processed in "
        "separate partitions so they don't affect smaller ones. "
        "On the read side, read replicas and caching for the API.",
    ),
    # ------------------------------------------------------------ fechamento
    Q(
        "your_questions",
        "closing",
        "Do you have any questions for us?",
        "Nunca responda 'no'. Perguntas boas mostram que você já se imagina no time.",
        "Yes, a few. "
        "[[I'm curious to know]] what the platform looks like today and what the biggest pain "
        "point is. "
        "How is matching done right now: rules, machine learning, or mostly manual review? "
        "Are you on Azure or AWS, and Angular or React? "
        "[[What would success look like]] for this role in the first ninety days? "
        "And what are the next steps in the process?",
        tips=("Escolha 3 ou 4. Anote as respostas: elas ajudam na próxima entrevista.",),
    ),
    Q(
        "closing",
        "closing",
        "Great, that's all from our side. Anything else you'd like to add?",
        "Última impressão. Curto, positivo, e reforce o encaixe.",
        "Just that I'm really excited about this opportunity. The problem you're solving is "
        "exactly the kind of work I enjoy, and I'd love to take ownership of it. "
        "[[Thank you for the opportunity]], [[it was great chatting with you]], and "
        "[[I look forward to hearing from you]].",
    ),
)

SESSION = register(
    Session(
        id="vendor_data_platform",
        title="Senior Software Engineer, Vendor Data Platform",
        company="DistantJob (cliente nos EUA)",
        summary="Plataforma que limpa, cruza e unifica dados de fornecedores de vários clientes "
        "e entrega para produtos de pagamento via API. Python, TypeScript, SQL, Azure/AWS, eventos.",
        stages=STAGES,
        questions=QUESTIONS,
    )
)
