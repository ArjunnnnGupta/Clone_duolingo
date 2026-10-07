import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { api } from "./api";
import type { MeResponse } from "./types";

export const queryKeys = {
  me: ["me"],
  path: ["path"],
} as const;

export function useMe() {
  return useQuery({ queryKey: queryKeys.me, queryFn: api.getMe });
}

export function usePath() {
  return useQuery({ queryKey: queryKeys.path, queryFn: api.getPath });
}

export function useStartLesson() {
  const router = useRouter();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (skillId: number) => api.startLesson(skillId),
    onSuccess: (attempt) => {
      // Starting a lesson applies heart regeneration server-side; mirror that value, never compute it.
      queryClient.setQueryData<MeResponse>(queryKeys.me, (current) =>
        current && { ...current, stats: { ...current.stats, hearts: attempt.hearts } },
      );
      router.push(`/lesson/${attempt.attempt_id}`);
    },
  });
}
