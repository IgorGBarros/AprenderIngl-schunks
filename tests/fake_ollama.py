"""Servidor HTTP que imita a API do Ollama (/api/tags e /api/chat) para os testes."""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class FakeOllama:
    """Uso: ``with FakeOllama() as fake: Ollama(host=fake.url, model="fake")``."""

    def __init__(self, models=("fake:latest",), bad_json: bool = False, port: int = 0):
        self.models = list(models)
        self.bad_json = bad_json
        self.requests: list[dict] = []
        fake = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):  # silencia o log
                pass

            def _send(self, code: int, body):
                data = (body if isinstance(body, str) else json.dumps(body)).encode()
                self.send_response(code)
                self.send_header("Access-Control-Allow-Origin", "*")  # como o Ollama para localhost
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_OPTIONS(self):
                self.send_response(204)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.end_headers()

            def do_GET(self):
                if self.path == "/api/tags":
                    self._send(200, {"models": [{"name": m} for m in fake.models]})
                else:
                    self._send(404, {"error": "not found"})

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                fake.requests.append(body)
                if body["model"] not in fake.models:
                    self._send(404, {"error": f"model '{body['model']}' not found"})
                    return
                content = "not json" if fake.bad_json else json.dumps(fake.answer(body))
                self._send(200, {"model": body["model"], "message": {"role": "assistant", "content": content}})

        self.server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
        self.url = f"http://127.0.0.1:{self.server.server_port}"

    def answer(self, body: dict) -> dict:
        props = body["format"]["properties"]
        if "title" in props:
            return {
                "title": "Data Engineer",
                "company": "Acme Corp",
                "summary": "Vaga de engenharia de dados com Python e SQL.",
            }
        stage = body["messages"][1]["content"].split("STAGE: ")[1].split("\n")[0]
        return {
            "questions": [
                {
                    "question": f"{stage} question {i}?",
                    "goal": "O que querem saber.",
                    "answer": f"[[I've been working in]] data [[for]] ((number of years)). Answer {i}.",
                    "tips": ["Dica 1", "Dica 2", "Dica 3", "Dica extra"],
                    "follow_ups": ["Why?"],
                }
                for i in range(1, 7)
            ]
            # Uma pergunta quebrada que deve ser descartada:
            + [{"question": "", "goal": "", "answer": "", "tips": [], "follow_ups": []}]
        }

    def __enter__(self) -> "FakeOllama":
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        return self

    def __exit__(self, *exc) -> None:
        self.server.shutdown()
        self.server.server_close()
