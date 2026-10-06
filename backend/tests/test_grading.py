import pytest

from app.errors import AppError
from app.models import Exercise
from app.models.content import EXERCISE_TYPES
from app.services.grading import ACCENT_NOTE, GRADERS, TYPO_NOTE, edit_distance, grade, normalize


def make_exercise(exercise_type: str, payload: dict, solution: dict) -> Exercise:
    return Exercise(type=exercise_type, prompt="", payload=payload, solution=solution)


MULTIPLE_CHOICE = make_exercise(
    "multiple_choice",
    {"options": [{"id": "o1", "text": "agua"}, {"id": "o2", "text": "pan"}]},
    {"option_id": "o2"},
)
TRANSLATE = make_exercise(
    "translate",
    {"source_text": "Yo bebo agua", "tiles": []},
    {"accepted": [["I", "drink", "water"], ["I", "am", "drinking", "water"]]},
)
MATCH_PAIRS = make_exercise(
    "match_pairs",
    {
        "left": [
            {"id": "l1", "text": "agua", "pair": "p1"},
            {"id": "l2", "text": "pan", "pair": "p2"},
        ],
        "right": [
            {"id": "r1", "text": "bread", "pair": "p2"},
            {"id": "r2", "text": "water", "pair": "p1"},
        ],
    },
    {},
)
FILL_BLANK = make_exercise(
    "fill_blank",
    {"before": "Yo", "after": "agua", "options": ["bebo", "bebes"]},
    {"accepted": ["bebo"]},
)
TYPE_ANSWER = make_exercise(
    "type_answer",
    {"source_text": "I drink coffee", "input_language": "es"},
    {"accepted": ["Yo bebo café"]},
)


def test_every_exercise_type_has_a_grader() -> None:
    assert set(GRADERS) == set(EXERCISE_TYPES)


def test_multiple_choice() -> None:
    assert grade(MULTIPLE_CHOICE, {"option_id": "o2"}).is_correct
    wrong = grade(MULTIPLE_CHOICE, {"option_id": "o1"})
    assert not wrong.is_correct and wrong.correct_solution == "pan"


def test_translate_accepts_any_listed_answer_ignoring_case() -> None:
    assert grade(TRANSLATE, {"tiles": ["i", "drink", "water"]}).is_correct
    assert grade(TRANSLATE, {"tiles": ["I", "am", "drinking", "water"]}).is_correct
    wrong = grade(TRANSLATE, {"tiles": ["water", "drink", "I"]})
    assert not wrong.is_correct and wrong.correct_solution == "I drink water"


def test_match_pairs_never_costs_a_heart() -> None:
    right = grade(MATCH_PAIRS, {"pairs": [["l1", "r2"], ["l2", "r1"]], "mismatches": 3})
    assert right.is_correct and not right.costs_heart
    crossed = grade(MATCH_PAIRS, {"pairs": [["l1", "r1"], ["l2", "r2"]], "mismatches": 0})
    assert not crossed.is_correct and not crossed.costs_heart


def test_match_pairs_rejects_incomplete_or_same_column_pairs() -> None:
    assert not grade(MATCH_PAIRS, {"pairs": [["l1", "r2"]], "mismatches": 0}).is_correct
    # Pairing l1 with itself shares a pair key, but a left item is not a right-column answer.
    assert not grade(
        MATCH_PAIRS, {"pairs": [["l1", "l1"], ["l2", "r1"]], "mismatches": 0}
    ).is_correct


def test_fill_blank() -> None:
    assert grade(FILL_BLANK, {"text": "Bebo"}).is_correct
    wrong = grade(FILL_BLANK, {"text": "bebes"})
    assert not wrong.is_correct and wrong.correct_solution == "Yo bebo agua"


def test_type_answer_ignores_case_and_punctuation() -> None:
    outcome = grade(TYPE_ANSWER, {"text": "  yo BEBO café! "})
    assert outcome.is_correct and outcome.feedback_note is None


def test_type_answer_missing_accent_passes_with_a_note() -> None:
    outcome = grade(TYPE_ANSWER, {"text": "yo bebo cafe"})
    assert outcome.is_correct and outcome.feedback_note == ACCENT_NOTE


def test_type_answer_one_letter_typo_passes_with_a_note() -> None:
    outcome = grade(TYPE_ANSWER, {"text": "yo bebo caffé"})
    assert outcome.is_correct and outcome.feedback_note == TYPO_NOTE


def test_type_answer_typo_on_a_short_word_fails() -> None:
    short = make_exercise(
        "type_answer", {"source_text": "", "input_language": "es"}, {"accepted": ["pan"]}
    )
    assert not grade(short, {"text": "pon"}).is_correct


def test_type_answer_wrong_word_fails() -> None:
    outcome = grade(TYPE_ANSWER, {"text": "yo como pan"})
    assert not outcome.is_correct and outcome.correct_solution == "Yo bebo café"


def test_answer_of_the_wrong_shape_is_rejected() -> None:
    with pytest.raises(AppError) as raised:
        grade(MULTIPLE_CHOICE, {"tiles": ["agua"]})
    assert raised.value.code == "INVALID_ANSWER"


def test_normalize_and_edit_distance() -> None:
    assert normalize("¿Hola,  amigo?") == "hola amigo"
    assert edit_distance("kitten", "sitting") == 3
    assert edit_distance("same", "same") == 0
