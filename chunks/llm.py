"""Cliente mínimo do Ollama (https://ollama.com), só com a biblioteca padrão.

Configuração por variável de ambiente:
    OLLAMA_HOST   endereço do servidor (padrão http://localhost:11434)
    OLLAMA_MODEL  modelo padrão (padrão qwen2.5:7b)
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5:7b"


class OllamaError(RuntimeError):
    """Erro com mensagem pronta para mostrar ao usuário."""


class Ollama:
    def __init__(self, host: str | None = None, model: str | None = None, timeout: float = 600):
        host = host or os.environ.get("OLLAMA_HOST") or DEFAULT_HOST
        if not host.startswith(("http://", "https://")):
            host = f"http://{host}"  # o próprio Ollama aceita OLLAMA_HOST sem esquema
        self.host = host.rstrip("/")
        self.model = model or os.environ.get("OLLAMA_MODEL") or DEFAULT_MODEL
        self.timeout = timeout

    def models(self) -> list[str]:
        """Modelos já baixados (``ollama list``)."""
        data = self._request("GET", "/api/tags")
        return [m["name"] for m in data.get("models", [])]

    def chat_json(self, system: str, user: str, schema: dict, temperature: float = 0.4) -> dict:
        """Conversa pedindo resposta em JSON no formato de ``schema`` (structured outputs)."""
        payload = {
            "model": self.model,
            "stream": False,
            "format": schema,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "options": {"temperature": temperature, "num_ctx": 8192},
        }
        data = self._request("POST", "/api/chat", payload)
        content = data.get("message", {}).get("content", "")
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            raise OllamaError(
                f"O modelo {self.model} não devolveu um JSON válido. "
                "Tente de novo ou use um modelo maior (ex.: qwen2.5:7b, llama3.1:8b)."
            ) from None

    # ------------------------------------------------------------ internals
    def _request(self, method: str, path: str, payload: dict | None = None) -> dict:
        body = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(
            self.host + path,
            data=body,
            method=method,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            detail = _error_detail(e)
            if e.code == 404 and "not found" in detail:
                raise OllamaError(
                    f"O modelo {self.model!r} não está instalado. Rode: ollama pull {self.model}"
                ) from None
            raise OllamaError(f"O Ollama respondeu com erro {e.code}: {detail}") from None
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            raise OllamaError(
                f"Não consegui falar com o Ollama em {self.host} ({_reason(e)}). "
                "Ele está rodando? Abra o app do Ollama ou rode: ollama serve"
            ) from None


def _error_detail(e: urllib.error.HTTPError) -> str:
    try:
        return json.loads(e.read().decode()).get("error", "")
    except (ValueError, OSError):
        return e.reason or ""


def _reason(e: Exception) -> str:
    return str(getattr(e, "reason", e))
