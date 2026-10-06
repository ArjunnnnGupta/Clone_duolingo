"""Answer grading: one grader per exercise type, looked up in a registry.

This is the only module that knows exercise types exist. Callers pass an exercise and the
raw answer body and get back a GradeOutcome.
"""

import unicodedata
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, ValidationError

from app.errors import AppError
from app.models import Exercise
from app.schemas.exercises import (
    MatchPairsAnswer,
    MultipleChoiceAnswer,
    TextAnswer,
    TranslateAnswer,
)

ACCENT_NOTE = "Pay attention to the accents."
TYPO_NOTE = "You have a typo."
# Typos are forgiven only on longer answers; on short words one letter changes the meaning.
MIN_LENGTH_FOR_TYPO = 5
IGNORED_PUNCTUATION = ".,!?¿¡"


@dataclass(frozen=True)
class GradeOutcome:
    is_correct: bool
    # Shown in the feedback footer when the answer was wrong or only nearly right.
    correct_solution: str | None = None
    feedback_note: str | None = None
    costs_heart: bool = True


def _grade_multiple_choice(exercise: Exercise, answer: MultipleChoiceAnswer) -> GradeOutcome:
    correct_id = exercise.solution["option_id"]
    if answer.option_id == correct_id:
        return GradeOutcome(is_correct=True)
    correct_text = next(
        option["text"] for option in exercise.payload["options"] if option["id"] == correct_id
    )
    return GradeOutcome(is_correct=False, correct_solution=correct_text)


def _grade_translate(exercise: Exercise, answer: TranslateAnswer) -> GradeOutcome:
    accepted = exercise.solution["accepted"]
    submitted = [tile.lower() for tile in answer.tiles]
    if any(submitted == [word.lower() for word in sequence] for sequence in accepted):
        return GradeOutcome(is_correct=True)
    return GradeOutcome(is_correct=False, correct_solution=" ".join(accepted[0]))


def _grade_match_pairs(exercise: Exercise, answer: MatchPairsAnswer) -> GradeOutcome:
    """Re-check the client's pairs: every left item matched once, each to its own partner.

    Mismatched taps are rejected on the client as they happen, so this exercise never
    costs a heart even when the final submission is wrong.
    """
    pair_key_by_id = {
        item["id"]: item["pair"] for item in exercise.payload["left"] + exercise.payload["right"]
    }
    left_ids = {item["id"] for item in exercise.payload["left"]}
    right_ids = {item["id"] for item in exercise.payload["right"]}
    matched_left_ids = [left_id for left_id, _ in answer.pairs]
    is_each_pair_valid = all(
        left_id in left_ids
        and right_id in right_ids
        and pair_key_by_id[left_id] == pair_key_by_id[right_id]
        for left_id, right_id in answer.pairs
    )
    is_complete = sorted(matched_left_ids) == sorted(left_ids)
    return GradeOutcome(is_correct=is_each_pair_valid and is_complete, costs_heart=False)


def _grade_fill_blank(exercise: Exercise, answer: TextAnswer) -> GradeOutcome:
    accepted = exercise.solution["accepted"]
    if normalize(answer.text) in {normalize(word) for word in accepted}:
        return GradeOutcome(is_correct=True)
    parts = [exercise.payload["before"], accepted[0], exercise.payload["after"]]
    return GradeOutcome(is_correct=False, correct_solution=" ".join(part for part in parts if part))


def _grade_type_answer(exercise: Exercise, answer: TextAnswer) -> GradeOutcome:
    """Exact match after normalizing. An accent slip or a one-letter typo still passes,
    with a note telling the learner what to watch."""
    submitted = normalize(answer.text)
    best_note: str | None = None
    for accepted in exercise.solution["accepted"]:
        target = normalize(accepted)
        if submitted == target:
            return GradeOutcome(is_correct=True)
        if strip_accents(submitted) == strip_accents(target):
            best_note = ACCENT_NOTE
        elif best_note is None and _is_typo(strip_accents(submitted), strip_accents(target)):
            best_note = TYPO_NOTE
    correct_solution = exercise.solution["accepted"][0]
    if best_note is not None:
        return GradeOutcome(
            is_correct=True, correct_solution=correct_solution, feedback_note=best_note
        )
    return GradeOutcome(is_correct=False, correct_solution=correct_solution)


@dataclass(frozen=True)
class _Grader:
    answer_model: type[BaseModel]
    grade: Callable[[Exercise, Any], GradeOutcome]


GRADERS: dict[str, _Grader] = {
    "multiple_choice": _Grader(MultipleChoiceAnswer, _grade_multiple_choice),
    "translate": _Grader(TranslateAnswer, _grade_translate),
    "match_pairs": _Grader(MatchPairsAnswer, _grade_match_pairs),
    "fill_blank": _Grader(TextAnswer, _grade_fill_blank),
    "type_answer": _Grader(TextAnswer, _grade_type_answer),
}


def grade(exercise: Exercise, raw_answer: dict[str, Any]) -> GradeOutcome:
    """Validate the answer against this exercise type's model, then grade it."""
    grader = GRADERS[exercise.type]
    try:
        answer = grader.answer_model.model_validate(raw_answer)
    except ValidationError as error:
        raise AppError(
            "INVALID_ANSWER", f"That answer does not fit a {exercise.type} exercise.", 400
        ) from error
    return grader.grade(exercise, answer)


def normalize(text: str) -> str:
    """Lowercase, drop the punctuation learners rarely type, and collapse spaces."""
    without_punctuation = text.lower().translate(str.maketrans("", "", IGNORED_PUNCTUATION))
    return " ".join(without_punctuation.split())


def strip_accents(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def _is_typo(submitted: str, target: str) -> bool:
    return len(target) >= MIN_LENGTH_FOR_TYPO and edit_distance(submitted, target) <= 1


def edit_distance(first: str, second: str) -> int:
    """Levenshtein distance: the fewest single-letter inserts, deletes or swaps."""
    previous_row = list(range(len(second) + 1))
    for row_index, first_char in enumerate(first, start=1):
        current_row = [row_index]
        for column_index, second_char in enumerate(second, start=1):
            current_row.append(
                min(
                    previous_row[column_index] + 1,
                    current_row[column_index - 1] + 1,
                    previous_row[column_index - 1] + (first_char != second_char),
                )
            )
        previous_row = current_row
    return previous_row[-1]
