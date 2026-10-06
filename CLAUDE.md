# Duolingo Clone — Project Guide for Claude Code

Full plan: `docs/plan.md`. Read the relevant section before each phase.

## Stack
- Frontend: Next.js (App Router) + TypeScript (strict) + Tailwind CSS + Framer Motion + TanStack Query + canvas-confetti + Nunito (next/font)
- Backend: Python FastAPI + SQLAlchemy 2.0 + Pydantic v2 + pydantic-settings
- Database: SQLite (`backend/data/app.db`, gitignored), schema created with `create_all`, populated by the seeder
- Tests: pytest + httpx (backend)

## Structure
```
backend/app/
  main.py        app factory, CORS, router registration
  config.py      env settings
  db.py          engine, session, PRAGMA foreign_keys=ON on every connection
  deps.py        get_db, get_current_user (default learner, id 1)
  models/        SQLAlchemy models (14 tables, see plan section 4)
  schemas/       Pydantic request/response models; exercise payloads as a discriminated union
  services/      clock, hearts, streak, path, grading, lesson_engine, achievements, leaderboard, profile, dev_tools
  api/           routers: me, path, lessons, hearts, leaderboard, dev
  seed/          content/ (vocab: structures.py + unit_1..3.py), generator.py, attempt_history.py, run.py
backend/tests/
frontend/src/
  app/(main)/    learn, leaderboard, profile, settings, quests/shop/friends (Coming Soon)
  app/lesson/[attemptId]/   full-screen lesson player
  components/    ui/ layout/ path/ lesson/ lesson/exercises/ gamification/ mascot/
  lib/           api.ts, types.ts, queries.ts, lessonReducer.ts
```

## Core rules
- The server owns every number: XP, hearts, gems, streak, progress, unlocks, answer grading. The frontend renders server values only.
- No optimistic updates for gamified values. Patch React Query caches from responses.
- Exercise solutions are never sent to the client (`solution` column stays server-side).
- Lesson finalize (XP, streak, daily activity, skill progress, achievements) runs in one transaction inside the answer call that completes the lesson, and is idempotent.
- Locked/active/completed skill state is derived, never stored.
- Match pairs never cost hearts.
- Original icons and mascot only. Never use Duolingo's owl, logo, illustrations or font files.
- Top bar shows streak, total XP, hearts and gems.

## Design tokens (Tailwind config only, never hex in components)
| Token | Main | Shade (bottom edge) |
|---|---|---|
| green | #58CC02 | #58A700 |
| blue | #1CB0F6 | #1899D6 |
| red | #FF4B4B | #EA2B2B |
| orange | #FF9600 | #CD7900 |
| gold | #FFC800 | #E5B400 |
| purple | #CE82FF | #A568CC |
| text | #4B4B4B | muted #777777 / #AFAFAF |
| border | #E5E5E5 | surface #FFFFFF / #F7F7F7 |
| correct footer | bg #D7FFB8, text #58A700 | |
| wrong footer | bg #FFDFE0, text #EA2B2B | |

Buttons: rounded-2xl, 50px tall, border-b-4 in shade colour, uppercase 800 weight; active = translate-y 4px and no bottom border.

## Commands
- Backend: `cd backend && uvicorn app.main:app --reload`
- Seed/reset: `cd backend && python -m app.seed.run`
- Tests: `cd backend && pytest`
- Lint backend: `cd backend && ruff check .`
- Frontend: `cd frontend && npm run dev`
- Lint frontend: `cd frontend && npm run lint`

## Code standards (apply to every change)

Readability
- Optimize for a reviewer reading the code cold in an interview. Prefer obvious over clever.
- Functions under ~40 lines; files under ~600 lines. Split when exceeded.
- Descriptive names (no abbreviations like usr, ex, tmp). Booleans read as is_/has_.
- Comment WHY for non-obvious rules (streak math, heart regen, finalize guard). No comments that restate the code.
- No dead code, commented-out blocks, console.log or print statements in commits.

Backend (FastAPI)
- Routers: HTTP only. Parse request, call ONE service function, return a schema. No business logic, no queries.
- Services: all business rules, plain functions taking (db, user, ...). Own the transaction for multi-row writes.
- One grader function per exercise type, registered in a dict. Never branch on exercise type outside grading.py.
- All dates/times come from services/clock.py. Never call datetime.now() or date.today() elsewhere.
- Type hints everywhere; SQLAlchemy 2.0 Mapped[] models; Pydantic models for every request and response.
- Errors: raise AppError(code, message, status). No bare HTTPException in services.
- Ruff clean.

Frontend (Next.js)
- TypeScript strict; no `any`. Shared API types in lib/types.ts.
- All fetch calls go through lib/api.ts; all React Query hooks in lib/queries.ts.
- One component per file. Components under ~150 lines; extract subcomponents when larger.
- Exercise components implement ExerciseProps and are registered in EXERCISE_REGISTRY. LessonPlayer never branches on exercise type.
- Never compute XP, hearts, streak or unlocks on the client. Render server values only.
- Colors, radii and shadows only via Tailwind tokens. No hex codes in components.
- Reuse ui/ primitives (Button, Modal, Card, ProgressBar) instead of restyling raw elements.
- ESLint clean.

## Process
- Before writing code for a phase, show a plan listing files to create/modify, and wait for approval.
- Build only the current phase; do not touch files outside its scope.
- No new dependencies without asking.
- Small commits with clear messages.
- After each phase, run tests and lint, then summarize what changed in 5 bullets.
