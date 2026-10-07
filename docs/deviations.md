# Deviations from docs/plan.md

Running list of agreed departures from the plan. Each needs one line in the final README.

## Phase 3 (seed)
- Demo learner `total_xp` is 115 (10 lessons, 3 perfect), not ≈200; history is 10 active days over 11, not 14 days.
- `longest_streak = 9` is set directly; the record predates the seeded history window.
- Rivals below the demo learner fall under the 15 XP floor early in the week (the demo has little XP by then).
- Generator is seeded with `unit_position * 10 + skill_position`, not `random.seed(skill_id)`, so content never depends on database ids.
- Fill-blank wrong options are hand-picked grammar mistakes (verb form, gender, number) so exactly one option fits.
- Seeded wrong answers sit immediately before their correct answer; in a live lesson the client re-queues wrong exercises to the end (the server keeps no queue; see Phase 6).

## Phase 4 (backend APIs)

### Error codes beyond plan section 5
- `INVALID_ANSWER` (400): the answer body does not match the exercise's type, e.g. `tiles` sent for a multiple-choice exercise.
- `EXERCISE_ALREADY_CORRECT` (409): an exercise already answered correctly in this attempt is submitted again.
- `HEARTS_FULL` (409): a gem refill is requested while hearts are already full, so gems are never spent for nothing.
- `VALIDATION_ERROR` (422): malformed request bodies use the same `{error: {code, message}}` envelope as every other error instead of FastAPI's default `{detail: [...]}`.

### Structure
- Two services beyond the plan's list: `profile.py` (`/me`, profile, settings, achievements list, heart actions) and `dev_tools.py` (advance day, reset), because routers may not hold logic.
- The heart refill and practice endpoints call `profile.py`, not `hearts.py`: they return the `/me` view that `profile.py` builds, and `hearts.py` keeps only the pure rules (this also avoids the two modules importing each other).
- No `AnswerSubmission` union. Each type has an answer model (`MultipleChoiceAnswer`, `TranslateAnswer`, `MatchPairsAnswer`, `TextAnswer`), and `grading.py` picks it from the exercise's stored type, so the client never sends or relabels a type.

### Behaviour the plan left open
- Accuracy = exercises ÷ (exercises + mistakes), as a whole percent; one function (`lesson_engine.accuracy_percent`) used by both the engine and the seed.
- Practice lessons on a completed skill are picked with unseeded `random.choice`, so replays vary.
- The profile chart (`week_xp`) is the last 7 days ending today, not the Monday-Sunday leaderboard week.
- `correct_solution` is sent only when the answer was wrong or only nearly right (accent or typo note), never on a plain correct answer.
- Leaderboard ties are broken alphabetically by display name.
- `POST /attempts/{id}/quit` on an attempt that is already closed returns its current status instead of `abandoned`.
- `dev_tools.reset()` closes the request's database session before calling `reset_database(engine)`. The session keeps loaded objects after a commit (`expire_on_commit=False`), so without the close the response would show the pre-reset learner from that cache rather than the reseeded one.
- Dev tools are off by default (`ENABLE_DEV_TOOLS` defaults to false); local development enables them in `backend/.env`.

### Finalize race, guarded
- Simultaneous completing answers are guarded in the database, not just unobserved. Finalizing first claims the attempt with one conditional `UPDATE lesson_attempts SET status = 'completed' WHERE id = ? AND status = 'in_progress'`. Each request re-checks the `WHERE` when its `UPDATE` runs, so of two simultaneous requests only one changes the row. The other sees 0 rows changed, rolls back its writes (its answer row included) and returns the stored result, exactly like a retry. A request arriving after the attempt is already finalized is caught earlier, by the status check, and also gets the stored result.
- Evidence: `test_simultaneous_completing_answers_award_once` reproduces the race with two database sessions, so it does not depend on timing. 15 simultaneous double-submits against a live server gave one XP award each and identical results in both responses.

## Phase 5 (learning path)

### Visual scope
- Light theme only. The reference screenshots are Duolingo's dark mode; the plan's design tokens are the light palette, so light was built first and dark mode is deferred to Phase 9 as a token swap (components use tokens only, so no component changes are needed).
- Mascot is an original placeholder (a purple blob, `components/mascot/Mascot.tsx`), never Duolingo's owl, per CLAUDE.md. The sidebar wordmark is "lingoleap" and the course flag is an original badge, for the same reason.
- Path nodes show a star (active, locked) or a check (completed), not a per-skill icon; `skill.icon` is unused until Phase 9.
- No chest nodes, "JUMP HERE?" nodes, unit divider lines or "SECTION 1," banner prefix (shown in the references): none exist in the data model.
- Unit banner shows `unit.title` ("Unit 1") as the small line and `unit.description` ("Form basic sentences") as the heading, because the seed generates `title` as "Unit N" and stores the readable name in `description`.
- Mobile tab bar has 6 icon-only tabs (matching reference 06), not the plan's 4 (Learn, Leaderboard, Profile, More). The sidebar has no CHARACTERS item; "More" links to `/settings`.
- Right rail shows only the stats bar; the daily-quest and league cards are Phase 8.

### Behaviour
- Node popover subtitle is "{lessons_completed} of {lesson_count} lessons complete", not the plan's "Lesson 2 of 3" (section 6, step 1): the server picks the next lesson, so the client shows the server's counts instead of computing a next-lesson number.
- Popover button is START, not "START +10 XP": `/api/path` does not send a per-lesson XP value.
- Tapping a completed node opens the same popover with a PRACTICE button; the server starts a practice-mode lesson.
- Path node 3D edges use `shadow-node-*` box-shadow tokens in `tailwind.config.ts`; the locked node's edge is `#AFAFAF` (the existing muted-text grey), since no border/surface grey is darker than the `#E5E5E5` face.

### Tooling
- `frontend/AGENTS.md` and `frontend/CLAUDE.md` are gitignored: Next.js 16's `next dev` regenerates them whenever they are missing.

## Phase 6 (lesson player)

### Lesson flow
- Re-queueing is done by the client. The server keeps no queue: it accepts exercises in any order, rejects only re-answering one that is already correct, and finalizes once every exercise has a correct answer. The client moves a wrong exercise to the end of its queue; after a refresh it rebuilds the queue from the server's answer log (unanswered exercises in lesson order, then the ones answered wrong and not yet right).
- A "Let's review the ones you missed!" screen (from reference 15) appears before the first re-queued exercise; the plan did not list it.
- SKIP is hidden. The plan (sections 6 and 8) has SKIP send a wrong answer, but there is no skip endpoint, and sending a made-up answer would store a submission the learner never made.
- The "3 IN A ROW" combo label is deferred to Phase 9: it would be a number counted on the client.
- The lesson-complete screen was built in Phase 6 instead of Phase 7. It has two stat cards (Total XP, Accuracy) as in reference 16, not the plan's three (section 7 adds Time).
- Out of hearts: Phase 6 showed a plain "You ran out of hearts" screen as a stand-in; Phase 7 replaced it with the refill modal.
- Deferred to Phase 9: the mascot encouragement screens (references 07, 12), the "hard exercise" badge, green/red option cards after checking, and number keys on match pairs. The "REVIEW LESSON" button (reference 16) is omitted; there is no feature behind it.

### Reducer and components
- No `HYDRATE` action: the reducer is built once from the attempt with `createInitialState`. Actions beyond the plan's list: `CHECK_ERROR` (network error, answer kept), `LESSON_CLOSED` (server returned `ATTEMPT_CLOSED`, e.g. a lesson started in another tab) and, from Phase 7, `REFILLED`.
- `ExerciseProps` uses `isLocked` instead of the plan's `locked`. Each `EXERCISE_REGISTRY` entry has an `isSubmittedOnComplete` flag (true only for match pairs), so the player reads a flag instead of checking an exercise type.
- The type-answer input's placeholder is "Type your answer" and its `lang` attribute is `input_language`, because the payload's language is a code ("es"), not a display name.
- Enter and number-key shortcuts pause while the quit modal is open. X is disabled while an answer is being checked, and goes straight to `/learn` once the lesson has been finalized.

### Backend change (Phase 4 code)
- `quit_attempt` and `_abandon_open_attempts` set `abandoned` with a conditional `UPDATE ... WHERE status = 'in_progress'`, the same guard as finalize. Previously a quit sent while the completing answer was in flight could overwrite `completed` with `abandoned`. Evidence: `test_quit_racing_a_completion_leaves_the_attempt_completed` fails on the old code and passes on the new.

## Phase 7 (hearts, streak, daily goal)

### Backend additions to `/api/me`
- `stats.seconds_until_next_heart`, rounded up. `next_heart_at` is learner-local wall time with no timezone and is shifted by the dev day offset, so a browser cannot count down to it. Rounding up means the value is never 0 while a heart is still pending. `next_heart_at` is kept.
- To compute it, `profile.py` builds the stats from the full time of day (`now`) instead of only the date; every date-based value still uses `now.date()` from the same clock call. `clock.py` is unchanged.
- `stats.refill_cost_gems`: the refill price existed only as a constant in `hearts.py`.
- `recent_days`: the last 7 days ending today, each marked active when a lesson was finished that day (`lessons_completed > 0`), for the streak week strip.

### Hearts
- The countdown counts toward a deadline set from when `/me` arrived (React Query's `dataUpdatedAt`) plus the server's seconds, and restarts on every fetch. At zero it re-reads `/me`; it never adds a heart.
- The out-of-hearts modal offers REFILL and NO THANKS only. `POST /hearts/practice` grants a heart but does not reopen a failed attempt, so PRACTICE TO EARN HEARTS appears only in the top-bar hearts panel. Inside a lesson the modal ignores backdrop clicks and Escape, so only NO THANKS leaves the lesson.
- START at 0 hearts opens the same out-of-hearts modal instead of an inline error.
- The client never checks whether a refill is affordable or hearts are full; it shows the server's `NOT_ENOUGH_GEMS` or `HEARTS_FULL` message.
- The hearts panel omits "Unlimited hearts" (a paid Super feature in reference 05).

### Streak and daily goal
- The streak week strip shows the last 7 days ending today, not a Monday-Sunday calendar week as in reference 21.
- The post-lesson streak screen reads "{count} day streak!" instead of reference 17's "Can you make it to a {count + 1} day streak?", and the number scales in instead of counting from N−1 to N (plan section 8), so the client does no arithmetic on the streak.
- The streak panel omits "% of learners", Friend Streaks and Streak Society: there is no data for them.
- Hearts and streak panels open as full-width panels under the stats bar, without the pointer tail the references show under the badge.
- The daily-goal screen has no reference image; it uses the same layout, CONTINUE footer and tokens as the other post-lesson screens.

### Settings and shared UI
- `/settings` was built in Phase 7 instead of Phase 8, with only the daily-goal picker and the dev tools (ADVANCE DAY, RESET DEMO). The goal options mirror the server's `DAILY_GOAL_OPTIONS`, which still validates them.
- The dev-tools panel is always shown; when the server has dev tools off, its 404 is shown as "Dev tools are off on this server".
- The GUIDEBOOK button shows a "Coming soon!" toast; the guidebook itself is not built.
- `Modal` renders into `<body>` through a portal, so the out-of-hearts modal opened from the animated node popover is positioned against the screen rather than the popover.

## Phase 8 (profile, leaderboard, rail cards)

### Backend changes (Phase 4 code)
- `UserOut` gains `joined_at` (from `users.created_at`), so the profile can show "Joined {month year}".
- `SettingsUpdate` strips `display_name` before the length check: a name of only spaces is rejected and a padded name is saved trimmed.

### Profile
- Stat tiles are Day streak, Total XP, Longest streak and Skills completed. Plan section 7 lists a league tile; there are no league tiers in the data model.
- The edit button links to `/settings` (where the display name is edited), not to a Coming Soon toast as plan section 7 says.
- The chart is the last 7 days ending today (`week_xp`), titled "Last 7 days", to keep it distinct from the leaderboard's Monday-Sunday week.
- All achievements are listed, unlocked first with their date, then locked with server progress toward the threshold.
- No banner avatar, followers/following, friend suggestions, "Current league" or "Top 3 finishes" (reference 18): no data for them.

### Leaderboard
- The header shows the week's date range from `period_start`/`period_end`, not a countdown: the server sends no days-left value, and computing one would mean client date math against the browser clock.
- No league tiers, shields, promotion zone or "Set your status" (reference 19): no data for them. Rank numbers are a neutral colour, since there is no promotion zone.

### Rail and pages
- The rail shows a weekly-rank card (from the leaderboard's `is_me` entry) and a daily-goal card (from `/me.daily`), not a Daily Quests card (reference 20): there is no quest data model.
- Coming Soon pages exist for `/quests` and `/shop` (the two nav links). `/friends`, listed in plan section 7, is not built; nothing links to it.
