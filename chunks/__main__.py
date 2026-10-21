"""Linha de comando: ``python -m chunks <comando>``.

Comandos:
    list   [categoria]           lista os chunks (funções) disponíveis
    show   <chunk>               mostra a "documentação" do chunk, com os exemplos
    estudar <chunk>              exemplos do chunk e, no final, um quiz com eles
    run    <chunk> [valores...]  executa o chunk com as suas variáveis
    play   <chunk>               pergunta cada variável e executa
    search <termo>               procura por inglês, português ou nome
    quiz   [categoria] [-n N]    treino com repetição espaçada
    anki   <arquivo.txt> [cat]   exporta cards Cloze para o Anki
    json   [pasta]               exporta biblioteca e entrevistas para o app web
    entrevista [sessão] [etapa]  simulação de entrevista (perguntas + respostas modelo)
    vaga   <vaga.txt|-> [opções] gera uma entrevista para QUALQUER vaga com o Ollama
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

import chunks
from chunks import study

WEB_DATA = Path(__file__).resolve().parent.parent / "web" / "src" / "data"
DEFAULT_PROFILE = "perfil.md"


def cmd_list(args) -> None:
    for cat in chunks.categories():
        if args.category not in (None, cat):
            continue
        print(f"\n## {cat}")
        for c in chunks.registry().values():
            if c.category == cat:
                print(f"  {c.pattern:<55} {c.core}")


def cmd_show(args) -> None:
    c = chunks.get(args.chunk)
    print(c.pattern)
    print("-" * len(c.pattern))
    print(c.__doc__)


def cmd_run(args) -> None:
    c = chunks.get(args.chunk)
    values = [_parse_value(v) for v in args.values]
    try:
        print(c(*values).explain())
    except TypeError:
        sys.exit(f"Uso: {c.pattern}  (ex.: {c.demo().en})")


def cmd_play(args) -> None:
    c = chunks.get(args.chunk)
    print(f"{c.pattern} -> {c.core}\n(dica: 'inglês|português' traduz a variável)\n")
    values = {}
    for slot in c.slots:
        hint = c.example.get(slot) or c.defaults.get(slot, "")
        hint = hint[0] if isinstance(hint, tuple) else hint
        raw = input(f"{slot} [{hint}]: ").strip()
        values[slot] = _parse_value(raw) if raw else c.example.get(slot, hint)
    print()
    print(c(**values).explain())


def cmd_search(args) -> None:
    found = chunks.search(args.term)
    for c in found:
        print(f"{c.pattern:<55} {c.core}")
    if not found:
        print("Nada encontrado.")


def cmd_quiz(args) -> None:
    progress = study.load_progress()
    queue = study.due_chunks(progress, args.category)[: args.n]
    if not queue:
        print("Nada para revisar hoje. Volte amanhã!")
        return
    print(f"{len(queue)} chunks para hoje. Escreva a frase em inglês (? mostra uma dica). Ctrl+C sai.\n")
    score = 0
    try:
        for i, c in enumerate(queue, 1):
            ok = _ask(study.random_phrase(c), f"[{i}/{len(queue)}]")
            score += ok
            study.record(progress, c.name, ok)
    except (KeyboardInterrupt, EOFError):
        print()
    study.save_progress(progress)
    print(f"Placar: {score}/{len(queue)}. Progresso salvo em {study.PROGRESS_FILE}")


def cmd_study(args) -> None:
    c = chunks.get(args.chunk)
    print(f"{c.pattern}\n{c.core}\n")
    if c.note:
        print(f"💡 {c.note}\n")
    phrases = c.demos()
    print("Exemplos (leia em voz alta):")
    for p in phrases:
        print(f"  • {p.en}\n    {p.pt}")
    input("\nEnter para começar o quiz deste chunk… ")
    print("\nEscreva em inglês. Digite ? para ver uma dica.\n")
    quiz = random.sample(phrases, len(phrases))
    score = 0
    try:
        for i, p in enumerate(quiz, 1):
            score += _ask(p, f"[{i}/{len(quiz)}]")
    except (KeyboardInterrupt, EOFError):
        print()
        return
    print(f"Placar: {score}/{len(quiz)}." + (" Perfeito! 🎉" if score == len(quiz) else " Repita amanhã."))
    if score == len(quiz):
        progress = study.load_progress()
        study.record(progress, c.name, True)
        study.save_progress(progress)


def _ask(p, label: str) -> bool:
    """Mostra o português, lê a resposta (``?`` mostra a dica) e corrige."""
    print(f"{label} {p.pt}")
    answer = input("  > ")
    if answer.strip() == "?":
        print(f"  dica: {p.blanks}")
        answer = input("  > ")
    ok = study.check(answer, p)
    print("  ✔ Correto!\n" if ok else f"  ✘ {p.en}\n    chunk: {p.chunk.core}\n")
    return ok


def cmd_anki(args) -> None:
    n = study.anki_export(Path(args.file), args.category)
    print(f"{n} cards exportados para {args.file}.")
    print("No Anki: Arquivo > Importar > escolha o arquivo (tipo de nota: Cloze).")


def cmd_json(args) -> None:
    folder = Path(args.folder)
    (folder / "chunks.json").write_text(study.to_json(), encoding="utf-8")
    (folder / "interviews.json").write_text(study.interviews_json(), encoding="utf-8")
    (folder / "interview_prompts.json").write_text(study.prompts_json(), encoding="utf-8")
    print(f"{len(chunks.registry())} chunks e as entrevistas exportados para {folder}.")


def cmd_interview(args) -> None:
    from chunks import interviews

    all_sessions = interviews.sessions()
    if args.session is None:
        args.session = _pick_session(all_sessions)
    if args.session not in all_sessions:
        sys.exit("Sessões: " + ", ".join(all_sessions))
    session = all_sessions[args.session]
    stages = [s for s in session.stages if args.stage in (None, s.id)]
    if not stages:
        sys.exit("Etapas: " + ", ".join(s.id for s in session.stages))

    print(f"{session.title} — {session.company}\n{session.summary}\n")
    print("Leia a pergunta, responda EM VOZ ALTA e depois aperte Enter para ver a resposta modelo.")
    print("[entre colchetes] = troque pelo seu fato real. Ctrl+C para sair.\n")
    try:
        for stage in stages:
            print(f"=== {stage.title} ===\n{stage.description}\n")
            for q in session.by_stage(stage.id):
                input(f"🎤 {q.en}\n   (Enter para ver a resposta) ")
                print(f"\n   O que querem saber: {q.goal}\n")
                print(f"   {interviews.plain(q.answer)}\n")
                found = interviews.chunks_in(q.answer)
                if found:
                    print("   Chunks: " + " · ".join(found))
                for tip in q.tips:
                    print(f"   Dica: {tip}")
                for f in q.follow_ups:
                    print(f"   Pode vir em seguida: {f}")
                print()
    except (KeyboardInterrupt, EOFError):
        print()


def _pick_session(all_sessions: dict) -> str:
    items = list(all_sessions.values())
    print("Sessões de entrevista:\n")
    for i, sess in enumerate(items, 1):
        print(f"  {i}. {sess.title} — {sess.company} ({len(sess.questions)} perguntas)  [{sess.id}]")
    print("\nNova vaga? python -m chunks vaga descricao_da_vaga.txt\n")
    choice = input("Número ou id da sessão: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(items):
        return items[int(choice) - 1].id
    return choice


def cmd_job(args) -> None:
    from chunks.interviews import generate
    from chunks.llm import Ollama, OllamaError

    job = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
    profile = ""
    if args.profile:
        profile = Path(args.profile).read_text(encoding="utf-8")
    elif Path(DEFAULT_PROFILE).exists():
        profile = Path(DEFAULT_PROFILE).read_text(encoding="utf-8")
        print(f"Usando seu perfil de {DEFAULT_PROFILE}.")
    else:
        print(f"Sem perfil: os fatos sobre você virão como ((preencha)). Veja {DEFAULT_PROFILE.replace('.md', '.exemplo.md')}.")

    client = Ollama(host=args.host, model=args.model)
    print(f"Ollama: {client.host} · modelo {client.model}. Isso pode levar alguns minutos.\n")
    try:
        session = generate.generate_session(
            job, profile, client, per_stage=args.n, on_progress=lambda msg: print(f"  {msg}")
        )
    except (OllamaError, ValueError) as e:
        sys.exit(f"\n{e}")
    path = generate.save(session)
    print(f"\n{len(session.questions)} perguntas para {session.title!r} salvas em {path}.")
    print(f"Pratique: python -m chunks entrevista {session.id}")
    print("App web: rode `python -m chunks json` para incluir a sessão no app.")


def _parse_value(raw: str):
    """``'a coffee|um café'`` vira ``('a coffee', 'um café')``."""
    if "|" in raw:
        en, pt = raw.split("|", 1)
        return en.strip(), pt.strip()
    return raw


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="chunks", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list"); p.add_argument("category", nargs="?"); p.set_defaults(fn=cmd_list)
    p = sub.add_parser("show"); p.add_argument("chunk"); p.set_defaults(fn=cmd_show)
    p = sub.add_parser("estudar"); p.add_argument("chunk"); p.set_defaults(fn=cmd_study)
    p = sub.add_parser("run"); p.add_argument("chunk"); p.add_argument("values", nargs="*")
    p.set_defaults(fn=cmd_run)
    p = sub.add_parser("play"); p.add_argument("chunk"); p.set_defaults(fn=cmd_play)
    p = sub.add_parser("search"); p.add_argument("term"); p.set_defaults(fn=cmd_search)
    p = sub.add_parser("quiz"); p.add_argument("category", nargs="?")
    p.add_argument("-n", type=int, default=10); p.set_defaults(fn=cmd_quiz)
    p = sub.add_parser("anki"); p.add_argument("file"); p.add_argument("category", nargs="?")
    p.set_defaults(fn=cmd_anki)
    p = sub.add_parser("json"); p.add_argument("folder", nargs="?", default=str(WEB_DATA))
    p.set_defaults(fn=cmd_json)
    p = sub.add_parser("vaga", help="gera uma entrevista para qualquer vaga com o Ollama")
    p.add_argument("file", help="arquivo .txt com a descrição da vaga, ou - para colar no terminal")
    p.add_argument("--perfil", dest="profile", help=f"seu perfil/currículo (padrão: {DEFAULT_PROFILE})")
    p.add_argument("--modelo", dest="model", help="modelo do Ollama (padrão: $OLLAMA_MODEL ou qwen2.5:7b)")
    p.add_argument("--host", help="endereço do Ollama (padrão: $OLLAMA_HOST ou http://localhost:11434)")
    p.add_argument("-n", type=int, default=5, help="perguntas por etapa (padrão: 5)")
    p.set_defaults(fn=cmd_job)
    p = sub.add_parser("entrevista"); p.add_argument("session", nargs="?")
    p.add_argument("stage", nargs="?"); p.set_defaults(fn=cmd_interview)

    args = parser.parse_args(argv)
    # Terminais sem UTF-8 (ex.: Windows antigo) não quebram com acentos ou emojis.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    try:
        args.fn(args)
    except KeyError as e:
        sys.exit(e.args[0])
    except BrokenPipeError:
        # Saída cortada (ex.: `chunks list | head`): sai em silêncio.
        sys.stderr.close()


if __name__ == "__main__":
    main()
