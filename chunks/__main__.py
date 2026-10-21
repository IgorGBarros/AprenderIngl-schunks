"""Linha de comando: ``python -m chunks <comando>``.

Comandos:
    list   [categoria]           lista os chunks (funções) disponíveis
    show   <chunk>               mostra a "documentação" do chunk
    run    <chunk> [valores...]  executa o chunk com as suas variáveis
    play   <chunk>               pergunta cada variável e executa
    search <termo>               procura por inglês, português ou nome
    quiz   [categoria] [-n N]    treino com repetição espaçada
    anki   <arquivo.txt> [cat]   exporta cards Cloze para o Anki
    json   [pasta]               exporta biblioteca e entrevistas para o app web
    entrevista [sessão] [etapa]  simulação de entrevista (perguntas + respostas modelo)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import chunks
from chunks import study

WEB_DATA = Path(__file__).resolve().parent.parent / "web" / "src" / "data"


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
    print(f"{len(queue)} chunks para hoje. Escreva a frase em inglês. (Ctrl+C para sair)\n")
    score = 0
    try:
        for i, c in enumerate(queue, 1):
            p = c.demo()
            print(f"[{i}/{len(queue)}] {p.pt}")
            if c.example:
                hints = ", ".join(
                    f"{k}={(v[0] if isinstance(v, tuple) else v)!r}" for k, v in c.example.items()
                )
                print(f"        variáveis: {hints}")
            answer = input("  > ")
            ok = study.check(answer, p)
            score += ok
            study.record(progress, c.name, ok)
            print("  ✔ Correto!\n" if ok else f"  ✘ {p.en}\n    chunk: {c.core}\n")
    except (KeyboardInterrupt, EOFError):
        print()
    study.save_progress(progress)
    print(f"Placar: {score}/{len(queue)}. Progresso salvo em {study.PROGRESS_FILE}")


def cmd_anki(args) -> None:
    n = study.anki_export(Path(args.file), args.category)
    print(f"{n} cards exportados para {args.file}.")
    print("No Anki: Arquivo > Importar > escolha o arquivo (tipo de nota: Cloze).")


def cmd_json(args) -> None:
    folder = Path(args.folder)
    (folder / "chunks.json").write_text(study.to_json(), encoding="utf-8")
    (folder / "interviews.json").write_text(study.interviews_json(), encoding="utf-8")
    print(f"{len(chunks.registry())} chunks e as entrevistas exportados para {folder}.")


def cmd_interview(args) -> None:
    from chunks import interviews

    all_sessions = interviews.sessions()
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
    p = sub.add_parser("entrevista"); p.add_argument("session", nargs="?", default="vendor_data_platform")
    p.add_argument("stage", nargs="?"); p.set_defaults(fn=cmd_interview)

    args = parser.parse_args(argv)
    try:
        args.fn(args)
    except KeyError as e:
        sys.exit(e.args[0])


if __name__ == "__main__":
    main()
