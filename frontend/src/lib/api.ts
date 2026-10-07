import type {
  ApiErrorBody,
  AttemptResponse,
  HealthResponse,
  MeResponse,
  PathResponse,
} from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly status: number,
  ) {
    super(message);
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}/api${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });

  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as ApiErrorBody | null;
    throw new ApiError(
      body?.error.code ?? "unknown_error",
      body?.error.message ?? response.statusText,
      response.status,
    );
  }
  return (await response.json()) as T;
}

export const api = {
  getHealth: () => request<HealthResponse>("/health"),
  getMe: () => request<MeResponse>("/me"),
  getPath: () => request<PathResponse>("/path"),
  startLesson: (skillId: number) =>
    request<AttemptResponse>("/lessons/start", {
      method: "POST",
      body: JSON.stringify({ skill_id: skillId }),
    }),
};
