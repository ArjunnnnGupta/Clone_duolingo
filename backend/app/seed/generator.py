"""Turns a skill's vocabulary and sentences into 3 lessons of 8 exercises.

Position order is fixed so even lesson 1 shows all five exercise types:
1 multiple choice, 2 match pairs, 3 translate to English, 4 fill blank,
5 multiple choice (reverse), 6 translate to Spanish, 7 fill blank, 8 type answer.
"""

import random
from collections import Counter
from typing import Any

from app.schemas.exercises import EXERCISE_ADAPTER, ExerciseDefinition
from app.seed.content import SentenceItem, SkillContent, VocabItem

LESSONS_PER_SKILL = 3
MATCH_PAIR_COUNT = 5
DISTRACTOR_COUNT = 3

Draft = dict[str, Any]


def generate_skill_exercises(
    generator_seed: int, content: SkillContent
) -> list[list[ExerciseDefinition]]:
    """Return one list of 8 validated exercises per lesson.

    The same seed always produces the same exercises, so a re-seed never changes the
    content a learner already saw.
    """
    randomizer = random.Random(generator_seed)
    return [
        _build_lesson(randomizer, content, lesson_index)
        for lesson_index in range(LESSONS_PER_SKILL)
    ]


def _build_lesson(
    randomizer: random.Random, content: SkillContent, lesson_index: int
) -> list[ExerciseDefinition]:
    vocab = content.vocab

    def sentence_at(offset: int) -> SentenceItem:
        # Each lesson starts one sentence later, so the 3 lessons use sentences in new slots.
        return content.sentences[(lesson_index + offset) % len(content.sentences)]

    # Lesson n quizzes vocab items 2n and 2n+1 in its two multiple-choice slots, so the
    # 3 lessons cover items 0-5 without repeats. The modulo only guards a short vocab list.
    forward_word = vocab[(2 * lesson_index) % len(vocab)]
    reverse_word = vocab[(2 * lesson_index + 1) % len(vocab)]
    spanish_pool = _distinct_words([item.es for item in vocab])
    english_pool = _distinct_words([item.en for item in vocab])
    drafts = [
        _multiple_choice_to_spanish(randomizer, vocab, forward_word),
        _match_pairs(randomizer, randomizer.sample(vocab, MATCH_PAIR_COUNT)),
        _translate_to_english(randomizer, sentence_at(0), english_pool),
        _fill_blank(randomizer, sentence_at(1)),
        _multiple_choice_to_english(randomizer, vocab, reverse_word),
        _translate_to_spanish(randomizer, sentence_at(2), spanish_pool),
        _fill_blank(randomizer, sentence_at(3)),
        _type_answer(sentence_at(4)),
    ]
    # A malformed draft fails here, at seed time, rather than in front of a learner.
    return [EXERCISE_ADAPTER.validate_python(draft) for draft in drafts]


def _distinct_words(phrases: list[str]) -> list[str]:
    # Sorted so the pool order, and therefore the random picks, never depend on hash order.
    return sorted({word.lower() for phrase in phrases for word in phrase.split()})


def _multiple_choice_to_spanish(
    randomizer: random.Random, vocab: tuple[VocabItem, ...], correct: VocabItem
) -> Draft:
    items = [correct, *_other_vocab(randomizer, vocab, correct)]
    return _multiple_choice(
        randomizer,
        prompt=f"Which one of these is “{correct.en}”?",
        choices=[item.es for item in items],
        correct_text=correct.es,
    )


def _multiple_choice_to_english(
    randomizer: random.Random, vocab: tuple[VocabItem, ...], correct: VocabItem
) -> Draft:
    items = [correct, *_other_vocab(randomizer, vocab, correct)]
    return _multiple_choice(
        randomizer,
        prompt=f"What does “{correct.es}” mean?",
        choices=[item.en for item in items],
        correct_text=correct.en,
    )


def _other_vocab(
    randomizer: random.Random, vocab: tuple[VocabItem, ...], correct: VocabItem
) -> list[VocabItem]:
    return randomizer.sample([item for item in vocab if item != correct], DISTRACTOR_COUNT)


def _multiple_choice(
    randomizer: random.Random, *, prompt: str, choices: list[str], correct_text: str
) -> Draft:
    randomizer.shuffle(choices)
    options = [{"id": f"o{number}", "text": text} for number, text in enumerate(choices, start=1)]
    correct_id = next(option["id"] for option in options if option["text"] == correct_text)
    return {
        "type": "multiple_choice",
        "prompt": prompt,
        "payload": {"options": options},
        "solution": {"option_id": correct_id},
    }


def _match_pairs(randomizer: random.Random, items: list[VocabItem]) -> Draft:
    left = [{"text": item.es, "pair": f"p{number}"} for number, item in enumerate(items, start=1)]
    right = [{"text": item.en, "pair": f"p{number}"} for number, item in enumerate(items, start=1)]
    randomizer.shuffle(left)
    randomizer.shuffle(right)
    for prefix, column in (("l", left), ("r", right)):
        for number, entry in enumerate(column, start=1):
            entry["id"] = f"{prefix}{number}"
    return {
        "type": "match_pairs",
        "prompt": "Tap the matching pairs",
        "payload": {"left": left, "right": right},
        "solution": {},
    }


def _tile_words(sentence: str) -> list[str]:
    """Split a sentence into tile texts.

    Only the sentence-initial capital is dropped, so it cannot mark the first tile. "I" and
    names keep their capitals because they have them anywhere in a sentence.
    """
    first_word, *other_words = sentence.split()
    return [first_word if first_word == "I" else first_word.lower(), *other_words]


def _tile_bank(
    randomizer: random.Random, accepted: list[list[str]], word_pool: list[str]
) -> list[Draft]:
    """Tiles that can build every accepted answer, plus distractors from the skill."""
    # Union keeps each word's highest count across the answers ("the ... the" needs two).
    needed_words: Counter[str] = Counter()
    for answer in accepted:
        needed_words |= Counter(answer)
    already_used = {word.lower() for word in needed_words}
    distractors = randomizer.sample(
        [word for word in word_pool if word not in already_used], DISTRACTOR_COUNT
    )
    texts = [*needed_words.elements(), *distractors]
    randomizer.shuffle(texts)
    return [{"id": f"t{number}", "text": text} for number, text in enumerate(texts, start=1)]


def _translate_to_english(
    randomizer: random.Random, sentence: SentenceItem, english_pool: list[str]
) -> Draft:
    accepted = [_tile_words(sentence.en), *map(_tile_words, sentence.alternatives)]
    return {
        "type": "translate",
        "prompt": "Write this in English",
        "payload": {
            "source_text": sentence.es,
            "tiles": _tile_bank(randomizer, accepted, english_pool),
        },
        "solution": {"accepted": accepted},
    }


def _translate_to_spanish(
    randomizer: random.Random, sentence: SentenceItem, spanish_pool: list[str]
) -> Draft:
    accepted = [_tile_words(sentence.es)]
    return {
        "type": "translate",
        "prompt": "Write this in Spanish",
        "payload": {
            "source_text": sentence.en,
            "tiles": _tile_bank(randomizer, accepted, spanish_pool),
        },
        "solution": {"accepted": accepted},
    }


def _fill_blank(randomizer: random.Random, sentence: SentenceItem) -> Draft:
    tokens = sentence.es.split()
    blank_index = tokens.index(sentence.blank_word)
    options = [sentence.blank_word, *sentence.wrong_options]
    randomizer.shuffle(options)
    return {
        "type": "fill_blank",
        "prompt": "Select the missing word",
        "payload": {
            "before": " ".join(tokens[:blank_index]),
            "after": " ".join(tokens[blank_index + 1 :]),
            "options": options,
        },
        "solution": {"accepted": [sentence.blank_word]},
    }


def _type_answer(sentence: SentenceItem) -> Draft:
    return {
        "type": "type_answer",
        "prompt": "Type this in Spanish",
        "payload": {"source_text": sentence.en, "input_language": "es"},
        "solution": {"accepted": [sentence.es]},
    }
