"""Hand-written Spanish course content; the generator turns it into exercises.

Each skill has 8 vocabulary items and 5 sentences. Sentences carry no punctuation so they can
be split into word tiles on spaces.
"""

from app.seed.content.structures import SentenceItem, SkillContent, UnitContent, VocabItem
from app.seed.content.unit_1 import UNIT_1
from app.seed.content.unit_2 import UNIT_2
from app.seed.content.unit_3 import UNIT_3

COURSE_CODE = "es-en"
COURSE_TITLE = "Spanish"
LEARNING_LANGUAGE = "Spanish"
FROM_LANGUAGE = "English"

UNITS: tuple[UnitContent, ...] = (UNIT_1, UNIT_2, UNIT_3)

__all__ = [
    "COURSE_CODE",
    "COURSE_TITLE",
    "FROM_LANGUAGE",
    "LEARNING_LANGUAGE",
    "UNITS",
    "SentenceItem",
    "SkillContent",
    "UnitContent",
    "VocabItem",
]
