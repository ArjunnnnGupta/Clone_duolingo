"""Unit 1: Form basic sentences."""

from app.seed.content.structures import SentenceItem, SkillContent, UnitContent, VocabItem

GREETINGS = SkillContent(
    title="Greetings",
    icon="wave",
    vocab=(
        VocabItem("hola", "hello", "👋"),
        VocabItem("adiós", "goodbye", "🚶"),
        VocabItem("gracias", "thanks", "🙏"),
        VocabItem("por favor", "please", "🤲"),
        VocabItem("sí", "yes", "✅"),
        VocabItem("no", "no", "❌"),
        VocabItem("buenos días", "good morning", "🌅"),
        VocabItem("buenas noches", "good night", "🌙"),
    ),
    sentences=(
        SentenceItem(
            "Hola me llamo Ana",
            "Hello my name is Ana",
            alternatives=("Hi my name is Ana",),
            blank_word="llamo",
            wrong_options=("llamas", "llama", "llamamos"),
        ),
        SentenceItem(
            "Muchas gracias amigo",
            "Thank you very much friend",
            alternatives=("Many thanks friend",),
            blank_word="Muchas",
            wrong_options=("Mucho", "Muchos", "Mucha"),
        ),
        SentenceItem(
            "Buenos días señor",
            "Good morning sir",
            alternatives=("Good morning mister",),
            blank_word="días",
            wrong_options=("noches", "tardes", "día"),
        ),
        SentenceItem(
            "Sí por favor",
            "Yes please",
            alternatives=("Yeah please",),
            blank_word="favor",
            wrong_options=("favores", "gracias", "hola"),
        ),
        SentenceItem(
            "Buenas noches amiga",
            "Good night friend",
            alternatives=("Good night my friend",),
            blank_word="noches",
            wrong_options=("días", "día", "noche"),
        ),
    ),
)

FOOD_AND_DRINK = SkillContent(
    title="Food & Drink",
    icon="apple",
    vocab=(
        VocabItem("agua", "water", "💧"),
        VocabItem("pan", "bread", "🍞"),
        VocabItem("leche", "milk", "🥛"),
        VocabItem("manzana", "apple", "🍎"),
        VocabItem("queso", "cheese", "🧀"),
        VocabItem("café", "coffee", "☕"),
        VocabItem("arroz", "rice", "🍚"),
        VocabItem("pollo", "chicken", "🍗"),
    ),
    sentences=(
        SentenceItem(
            "Yo bebo agua",
            "I drink water",
            alternatives=("I am drinking water",),
            blank_word="bebo",
            wrong_options=("bebes", "bebe", "bebemos"),
        ),
        SentenceItem(
            "El niño come pan",
            "The boy eats bread",
            alternatives=("The boy is eating bread",),
            blank_word="come",
            wrong_options=("como", "comes", "comemos"),
        ),
        SentenceItem(
            "Ella bebe leche",
            "She drinks milk",
            alternatives=("She is drinking milk",),
            blank_word="bebe",
            wrong_options=("bebo", "bebes", "bebemos"),
        ),
        SentenceItem(
            "Nosotros comemos arroz",
            "We eat rice",
            alternatives=("We are eating rice",),
            blank_word="comemos",
            wrong_options=("como", "comes", "come"),
        ),
        SentenceItem(
            "Tú bebes café",
            "You drink coffee",
            alternatives=("You are drinking coffee",),
            blank_word="bebes",
            wrong_options=("bebo", "bebe", "bebemos"),
        ),
    ),
)

FAMILY = SkillContent(
    title="Family",
    icon="family",
    vocab=(
        VocabItem("madre", "mother", "👩"),
        VocabItem("padre", "father", "👨"),
        VocabItem("hermano", "brother", "👦"),
        VocabItem("hermana", "sister", "👧"),
        VocabItem("abuelo", "grandfather", "👴"),
        VocabItem("abuela", "grandmother", "👵"),
        VocabItem("hijo", "son", "🧒"),
        VocabItem("tía", "aunt", "👩‍🦰"),
    ),
    sentences=(
        SentenceItem(
            "Mi madre es alta",
            "My mother is tall",
            alternatives=("My mom is tall",),
            blank_word="alta",
            wrong_options=("alto", "altos", "altas"),
        ),
        SentenceItem(
            "Tengo una hermana",
            "I have a sister",
            alternatives=("I have one sister",),
            blank_word="una",
            wrong_options=("un", "unos", "unas"),
        ),
        SentenceItem(
            "Mi abuelo come pan",
            "My grandfather eats bread",
            alternatives=("My grandfather is eating bread",),
            blank_word="come",
            wrong_options=("como", "comes", "comemos"),
        ),
        SentenceItem(
            "Su padre es simpático",
            "His father is nice",
            alternatives=("Her father is nice",),
            blank_word="es",
            wrong_options=("soy", "eres", "somos"),
        ),
        SentenceItem(
            "Mi hermano bebe leche",
            "My brother drinks milk",
            alternatives=("My brother is drinking milk",),
            blank_word="bebe",
            wrong_options=("bebo", "bebes", "bebemos"),
        ),
    ),
)

PEOPLE = SkillContent(
    title="People",
    icon="people",
    vocab=(
        VocabItem("niño", "boy", "👦"),
        VocabItem("niña", "girl", "👧"),
        VocabItem("hombre", "man", "👨"),
        VocabItem("mujer", "woman", "👩"),
        VocabItem("amigo", "friend", "🧑‍🤝‍🧑"),
        VocabItem("profesor", "teacher", "🧑‍🏫"),
        VocabItem("médico", "doctor", "🧑‍⚕️"),
        VocabItem("estudiante", "student", "🎓"),
    ),
    sentences=(
        SentenceItem(
            "El hombre es médico",
            "The man is a doctor",
            alternatives=("The man is a physician",),
            blank_word="es",
            wrong_options=("soy", "eres", "somos"),
        ),
        SentenceItem(
            "La mujer es profesora",
            "The woman is a teacher",
            alternatives=("The woman is a professor",),
            blank_word="profesora",
            wrong_options=("profesor", "profesores", "profesoras"),
        ),
        SentenceItem(
            "Ella es estudiante",
            "She is a student",
            alternatives=("She is a pupil",),
            blank_word="es",
            wrong_options=("soy", "eres", "somos"),
        ),
        SentenceItem(
            "El niño tiene un amigo",
            "The boy has a friend",
            alternatives=("The boy has one friend",),
            blank_word="un",
            wrong_options=("una", "unos", "unas"),
        ),
        SentenceItem(
            "La niña habla con el profesor",
            "The girl talks with the teacher",
            alternatives=("The girl speaks with the teacher",),
            blank_word="habla",
            wrong_options=("hablo", "hablas", "hablamos"),
        ),
    ),
)

UNIT_1 = UnitContent(
    description="Form basic sentences",
    color="green",
    skills=(GREETINGS, FOOD_AND_DRINK, FAMILY, PEOPLE),
)
