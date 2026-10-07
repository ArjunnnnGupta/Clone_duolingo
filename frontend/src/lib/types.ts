export interface HealthResponse {
  status: "ok";
}

export interface ApiErrorBody {
  error: {
    code: string;
    message: string;
  };
}

export type NodeState = "locked" | "active" | "completed";

export interface PathSkill {
  id: number;
  title: string;
  icon: string;
  state: NodeState;
  lessons_completed: number;
  lesson_count: number;
}

export interface PathUnit {
  id: number;
  position: number;
  title: string;
  description: string;
  // Tailwind token name (e.g. "green"), resolved to classes in lib/unitColors.ts.
  color: string;
  state: NodeState;
  skills: PathSkill[];
}

export interface PathResponse {
  course: { id: number; code: string; title: string };
  units: PathUnit[];
}

export interface MeStats {
  total_xp: number;
  gems: number;
  hearts: number;
  max_hearts: number;
  next_heart_at: string | null;
  current_streak: number;
  longest_streak: number;
  streak_active_today: boolean;
}

export interface MeResponse {
  user: {
    id: number;
    username: string;
    display_name: string;
    avatar_color: string;
    daily_goal_xp: number;
  };
  stats: MeStats;
  daily: { goal_xp: number; today_xp: number };
}

// Phase 6 extends this with the exercises; the path only needs the id and hearts.
export interface AttemptResponse {
  attempt_id: number;
  hearts: number;
}
