# Deviations from docs/plan.md

Running list of agreed departures from the plan. Each needs one line in the final README.

## Phase 3 (seed)
- Demo learner `total_xp` is 115 (10 lessons, 3 perfect), not ≈200; history is 10 active days over 11, not 14 days.
- `longest_streak = 9` is set directly; the record predates the seeded history window.
- Rivals below the demo learner fall under the 15 XP floor early in the week (the demo has little XP by then).
- Generator is seeded with `unit_position * 10 + skill_position`, not `random.seed(skill_id)`, so content never depends on database ids.
- Fill-blank wrong options are hand-picked grammar mistakes (verb form, gender, number) so exactly one option fits.
- Seeded wrong answers sit immediately before their correct answer; the live engine re-queues wrong exercises to the end.

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
