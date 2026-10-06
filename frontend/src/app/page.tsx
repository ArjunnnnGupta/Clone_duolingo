"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { HealthResponse } from "@/lib/types";

// Temporary Phase 1 page: proves the frontend can reach the backend. Replaced by real pages later.
export default function HomePage() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    api
      .getHealth()
      .then(setHealth)
      .catch((error: Error) => setErrorMessage(error.message));
  }, []);

  return (
    <main className="mx-auto mt-24 w-full max-w-xl rounded-2xl border-2 border-b-4 border-border p-6">
      <h1 className="text-2xl font-extrabold text-green">API health</h1>
      <pre className="mt-4 text-text-muted">
        {errorMessage
          ? `Error: ${errorMessage}`
          : health
            ? JSON.stringify(health)
            : "Loading..."}
      </pre>
    </main>
  );
}
