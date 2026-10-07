import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { api } from "./api";
import type { ExerciseAnswer, MeResponse } from "./types";

export const queryKeys = {
  me: ["me"],
  path: ["path"],
  attempt: (attemptId: number) => ["attempt", attemptId],
} as const;

export function useMe() {
  return useQuery({ queryKey: queryKeys.me, queryFn: api.getMe });
}

export function usePath() {
  return useQuery({ queryKey: queryKeys.path, queryFn: api.getPath });
}

// Every heart/settings/dev action answers with the whole /me view, so the response replaces the cache.
function useMeMutation(mutationFn: () => Promise<MeResponse>, shouldRefreshPath = false) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn,
    onSuccess: (me) => {
      queryClient.setQueryData<MeResponse>(queryKeys.me, me);
      if (shouldRefreshPath) {
        queryClient.invalidateQueries({ queryKey: queryKeys.path });
      }
    },
  });
}

export const useRefillHearts = () => useMeMutation(api.refillHearts);
export const usePracticeForHeart = () => useMeMutation(api.practiceForHeart);
export const useAdvanceDay = () => useMeMutation(api.advanceDay, true);
export const useResetDemo = () => useMeMutation(api.resetDemo, true);

export function useUpdateSettings() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.updateSettings,
    onSuccess: (me) => queryClient.setQueryData<MeResponse>(queryKeys.me, me),
  });
}

export function useRefreshMe() {
  const queryClient = useQueryClient();
  return () => queryClient.invalidateQueries({ queryKey: queryKeys.me });
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
      // Replace, as in plan section 6: the lesson takes the path page's place in history.
      router.replace(`/lesson/${attempt.attempt_id}`);
    },
  });
}

export function useAttempt(attemptId: number) {
  return useQuery({
    queryKey: queryKeys.attempt(attemptId),
    queryFn: () => api.getAttempt(attemptId),
    // The lesson reducer is built from this once; a refetch must never reshuffle a lesson in progress.
    refetchOnWindowFocus: false,
    gcTime: 0,
  });
}

export function useSubmitAnswer(attemptId: number) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (submission: { exerciseId: number; answer: ExerciseAnswer }) =>
      api.submitAnswer(attemptId, submission.exerciseId, submission.answer),
    onSuccess: (response) => {
      queryClient.setQueryData<MeResponse>(queryKeys.me, (current) =>
        current && { ...current, stats: { ...current.stats, hearts: response.hearts } },
      );
      if (response.result) {
        // The finalize ran in this same request: XP, streak and skill progress all changed.
        queryClient.invalidateQueries({ queryKey: queryKeys.me });
        queryClient.invalidateQueries({ queryKey: queryKeys.path });
      }
    },
  });
}

export function useQuitAttempt(attemptId: number) {
  const router = useRouter();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => api.quitAttempt(attemptId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.path });
      router.push("/learn");
    },
  });
}
