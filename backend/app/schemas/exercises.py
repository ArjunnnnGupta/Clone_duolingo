"""Exercise payload/solution shapes, one pair per type, joined in a discriminated union.

`payload` is what the client may see; `solution` never leaves the server.
"""

from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, model_validator


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ChoiceOption(_Strict):
    id: str
    text: str
    emoji: str | None = None


class Tile(_Strict):
    id: str
    text: str


class MatchItem(_Strict):
    id: str
    text: str
    # Shared by the two items that belong together, so the client can validate taps.
    pair: str


class MultipleChoicePayload(_Strict):
    options: list[ChoiceOption] = Field(min_length=2)


class MultipleChoiceSolution(_Strict):
    option_id: str


class TranslatePayload(_Strict):
    source_text: str
    tiles: list[Tile] = Field(min_length=2)


class TranslateSolution(_Strict):
    accepted: list[list[str]] = Field(min_length=1)


class MatchPairsPayload(_Strict):
    left: list[MatchItem] = Field(min_length=2)
    right: list[MatchItem] = Field(min_length=2)

    @model_validator(mode="after")
    def _pair_keys_line_up(self) -> Self:
        left_keys = sorted(item.pair for item in self.left)
        right_keys = sorted(item.pair for item in self.right)
        if left_keys != right_keys or len(set(left_keys)) != len(left_keys):
            raise ValueError("each pair key must appear exactly once on each side")
        return self


class MatchPairsSolution(_Strict):
    """Pairs are intrinsic to the payload, so there is nothing secret to store."""


class FillBlankPayload(_Strict):
    before: str
    after: str
    options: list[str] = Field(min_length=2)


class FillBlankSolution(_Strict):
    accepted: list[str] = Field(min_length=1)


class TypeAnswerPayload(_Strict):
    source_text: str
    input_language: str


class TypeAnswerSolution(_Strict):
    accepted: list[str] = Field(min_length=1)


class MultipleChoiceExercise(_Strict):
    type: Literal["multiple_choice"]
    prompt: str
    payload: MultipleChoicePayload
    solution: MultipleChoiceSolution

    @model_validator(mode="after")
    def _solution_is_an_option(self) -> Self:
        if self.solution.option_id not in {option.id for option in self.payload.options}:
            raise ValueError("solution option_id is not among the options")
        return self


class TranslateExercise(_Strict):
    type: Literal["translate"]
    prompt: str
    payload: TranslatePayload
    solution: TranslateSolution


class MatchPairsExercise(_Strict):
    type: Literal["match_pairs"]
    prompt: str
    payload: MatchPairsPayload
    solution: MatchPairsSolution


class FillBlankExercise(_Strict):
    type: Literal["fill_blank"]
    prompt: str
    payload: FillBlankPayload
    solution: FillBlankSolution

    @model_validator(mode="after")
    def _solution_is_an_option(self) -> Self:
        if not set(self.solution.accepted) <= set(self.payload.options):
            raise ValueError("accepted words must all appear among the options")
        return self


class TypeAnswerExercise(_Strict):
    type: Literal["type_answer"]
    prompt: str
    payload: TypeAnswerPayload
    solution: TypeAnswerSolution


ExerciseDefinition = Annotated[
    MultipleChoiceExercise
    | TranslateExercise
    | MatchPairsExercise
    | FillBlankExercise
    | TypeAnswerExercise,
    Field(discriminator="type"),
]

EXERCISE_ADAPTER: TypeAdapter[ExerciseDefinition] = TypeAdapter(ExerciseDefinition)
