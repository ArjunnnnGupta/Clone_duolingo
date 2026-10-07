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

export type ExerciseType =
  | "multiple_choice"
  | "translate"
  | "match_pairs"
  | "fill_blank"
  | "type_answer";

export interface ChoiceOption {
  id: string;
  text: string;
  emoji: string | null;
}

export interface Tile {
  id: string;
  text: string;
}

export interface MatchItem {
  id: string;
  text: string;
  // Shared by the two items that belong together.
  pair: string;
}

interface ExerciseBase {
  id: number;
  prompt: string;
}

export interface MultipleChoiceExercise extends ExerciseBase {
  type: "multiple_choice";
  payload: { options: ChoiceOption[] };
}

export interface TranslateExercise extends ExerciseBase {
  type: "translate";
  payload: { source_text: string; tiles: Tile[] };
}

export interface MatchPairsExercise extends ExerciseBase {
  type: "match_pairs";
  payload: { left: MatchItem[]; right: MatchItem[] };
}

export interface FillBlankExercise extends ExerciseBase {
  type: "fill_blank";
  payload: { before: string; after: string; options: string[] };
}

export interface TypeAnswerExercise extends ExerciseBase {
  type: "type_answer";
  payload: { source_text: string; input_language: string };
}

// Solutions never reach the client; only payloads do.
export type LessonExercise =
  | MultipleChoiceExercise
  | TranslateExercise
  | MatchPairsExercise
  | FillBlankExercise
  | TypeAnswerExercise;

export type ExerciseAnswer =
  | { option_id: string }
  | { tiles: string[] }
  | { pairs: [string, string][]; mismatches: number }
  | { text: string };

export type AttemptStatus = "in_progress" | "completed" | "failed" | "abandoned";

export interface AttemptResult {
  xp_earned: number;
  accuracy: number;
  mistakes: number;
  duration_s: number;
  streak: { count: number; extended: boolean };
  daily_goal: { today_xp: number; goal_xp: number; just_met: boolean };
  skill_completed: boolean;
  achievements_unlocked: { code: string; title: string; icon: string }[];
}

export interface AttemptResponse {
  attempt_id: number;
  mode: "learn" | "practice";
  status: AttemptStatus;
  lesson: { id: number; position: number; skill_title: string };
  exercises: LessonExercise[];
  hearts: number;
  answered: { exercise_id: number; is_correct: boolean }[];
  result: AttemptResult | null;
}

export interface AnswerResponse {
  correct: boolean;
  correct_solution: string | null;
  feedback_note: string | null;
  hearts: number;
  status: AttemptStatus;
  result: AttemptResult | null;
}

export interface QuitResponse {
  status: AttemptStatus;
}
