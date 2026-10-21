// Cliente do Ollama para o navegador (mesmo comportamento de chunks/llm.py).

export const DEFAULT_HOST = "http://localhost:11434";
export const DEFAULT_MODEL = "qwen2.5:7b";

export class OllamaError extends Error {}

export interface OllamaConfig {
  host: string;
  model: string;
}

export function normalizeHost(host: string): string {
  const h = host.trim() || DEFAULT_HOST;
  return (/^https?:\/\//.test(h) ? h : `http://${h}`).replace(/\/+$/, "");
}

export async function listModels(host: string, signal?: AbortSignal): Promise<string[]> {
  const data = await request<{ models?: { name: string }[] }>(normalizeHost(host), "/api/tags", undefined, signal);
  return (data.models ?? []).map((m) => m.name);
}

export async function chatJson<T>(
  config: OllamaConfig,
  system: string,
  user: string,
  schema: object,
  temperature = 0.4,
  signal?: AbortSignal,
): Promise<T> {
  const data = await request<{ message?: { content?: string } }>(
    normalizeHost(config.host),
    "/api/chat",
    {
      model: config.model,
      stream: false,
      format: schema,
      messages: [
        { role: "system", content: system },
        { role: "user", content: user },
      ],
      options: { temperature, num_ctx: 8192 },
    },
    signal,
    config.model,
  );
  try {
    return JSON.parse(data.message?.content ?? "") as T;
  } catch {
    throw new OllamaError(
      `O modelo ${config.model} não devolveu um JSON válido. Tente de novo ou use um modelo maior (ex.: qwen2.5:7b, llama3.1:8b).`,
    );
  }
}

async function request<T>(host: string, path: string, body?: object, signal?: AbortSignal, model?: string): Promise<T> {
  let resp: Response;
  try {
    resp = await fetch(host + path, {
      method: body ? "POST" : "GET",
      headers: body ? { "Content-Type": "application/json" } : undefined,
      body: body ? JSON.stringify(body) : undefined,
      signal,
    });
  } catch (e) {
    if ((e as Error).name === "AbortError") throw e;
    throw new OllamaError(
      `Não consegui falar com o Ollama em ${host}. Ele está rodando? Se o app não está em localhost, ` +
        `inicie o Ollama com OLLAMA_ORIGINS="*" (e OLLAMA_HOST=0.0.0.0 para acessar pelo celular).`,
    );
  }
  if (!resp.ok) {
    let detail = resp.statusText;
    try {
      detail = ((await resp.json()) as { error?: string }).error ?? detail;
    } catch {
      // corpo sem JSON
    }
    if (resp.status === 404 && model && /not found/i.test(detail)) {
      throw new OllamaError(`O modelo "${model}" não está instalado. Rode: ollama pull ${model}`);
    }
    throw new OllamaError(`O Ollama respondeu com erro ${resp.status}: ${detail}`);
  }
  return (await resp.json()) as T;
}
