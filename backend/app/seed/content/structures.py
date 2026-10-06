"""Shapes of the hand-written course content, checked when the data is defined."""

from dataclasses import dataclass


@dataclass(frozen=True)
class VocabItem:
    es: str
    en: str
    emoji: str


@dataclass(frozen=True)
class SentenceItem:
    es: str
    en: str
    alternatives: tuple[str, ...]  # other accepted English translations
    blank_word: str  # the word the fill-blank exercise removes from `es`
    # Hand-picked (wrong verb form, gender or number) so none of them also fits the gap.
    wrong_options: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.es.split().count(self.blank_word) != 1:
            raise ValueError(f"{self.blank_word!r} must appear exactly once in {self.es!r}")
        if self.blank_word in self.wrong_options:
            raise ValueError(f"{self.blank_word!r} is listed as its own wrong option")
        if len(set(self.wrong_options)) != len(self.wrong_options):
            raise ValueError(f"duplicate wrong options for {self.es!r}")


@dataclass(frozen=True)
class SkillContent:
    title: str
    icon: str
    vocab: tuple[VocabItem, ...]
    sentences: tuple[SentenceItem, ...]


@dataclass(frozen=True)
class UnitContent:
    description: str
    color: str  # Tailwind token name, never a hex code
    skills: tuple[SkillContent, ...]
