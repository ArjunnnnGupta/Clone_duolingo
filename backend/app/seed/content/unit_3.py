"""Unit 3: Talk about your day."""

from app.seed.content.structures import SentenceItem, SkillContent, UnitContent, VocabItem

ROUTINE = SkillContent(
    title="Routine",
    icon="sunrise",
    vocab=(
        VocabItem("desayuno", "breakfast"),
        VocabItem("almuerzo", "lunch"),
        VocabItem("cena", "dinner"),
        VocabItem("ducha", "shower"),
        VocabItem("trabajo", "work"),
        VocabItem("cama", "bed"),
        VocabItem("ropa", "clothes"),
        VocabItem("dientes", "teeth"),
    ),
    sentences=(
        SentenceItem(
            "Yo desayuno a las siete",
            "I eat breakfast at seven",
            alternatives=("I have breakfast at seven",),
            blank_word="desayuno",
            wrong_options=("desayunas", "desayuna", "desayunamos"),
        ),
        SentenceItem(
            "Ella toma una ducha",
            "She takes a shower",
            alternatives=("She is taking a shower",),
            blank_word="toma",
            wrong_options=("tomo", "tomas", "tomamos"),
        ),
        SentenceItem(
            "Nosotros trabajamos por la mañana",
            "We work in the morning",
            alternatives=("We work during the morning",),
            blank_word="trabajamos",
            wrong_options=("trabajo", "trabajas", "trabaja"),
        ),
        SentenceItem(
            "Mi hermano se lava los dientes",
            "My brother brushes his teeth",
            alternatives=("My brother is brushing his teeth",),
            blank_word="los",
            wrong_options=("el", "la", "las"),
        ),
        SentenceItem(
            "Yo ceno con mi familia",
            "I eat dinner with my family",
            alternatives=("I have dinner with my family",),
            blank_word="ceno",
            wrong_options=("cenas", "cena", "cenamos"),
        ),
    ),
)

WEATHER = SkillContent(
    title="Weather",
    icon="cloud",
    vocab=(
        VocabItem("sol", "sun"),
        VocabItem("lluvia", "rain"),
        VocabItem("nieve", "snow"),
        VocabItem("viento", "wind"),
        VocabItem("nube", "cloud"),
        VocabItem("calor", "heat"),
        VocabItem("frío", "cold"),
        VocabItem("tormenta", "storm"),
    ),
    sentences=(
        SentenceItem(
            "Hoy hace sol",
            "Today it is sunny",
            alternatives=("It is sunny today",),
            blank_word="hace",
            wrong_options=("hago", "haces", "hacemos"),
        ),
        SentenceItem(
            "Hay mucha lluvia",
            "There is a lot of rain",
            alternatives=("There is much rain",),
            blank_word="mucha",
            wrong_options=("mucho", "muchos", "muchas"),
        ),
        SentenceItem(
            "Hace mucho frío",
            "It is very cold",
            alternatives=("It is really cold",),
            blank_word="mucho",
            wrong_options=("mucha", "muchos", "muchas"),
        ),
        SentenceItem(
            "El viento es fuerte",
            "The wind is strong",
            alternatives=("It is a strong wind",),
            blank_word="es",
            wrong_options=("soy", "eres", "somos"),
        ),
        SentenceItem(
            "Hay una tormenta",
            "There is a storm",
            alternatives=("There is one storm",),
            blank_word="una",
            wrong_options=("un", "unos", "unas"),
        ),
    ),
)

HOBBIES = SkillContent(
    title="Hobbies",
    icon="palette",
    vocab=(
        VocabItem("música", "music"),
        VocabItem("libro", "book"),
        VocabItem("fútbol", "soccer"),
        VocabItem("baile", "dance"),
        VocabItem("pintura", "painting"),
        VocabItem("cine", "movies"),
        VocabItem("foto", "photo"),
        VocabItem("juego", "game"),
    ),
    sentences=(
        SentenceItem(
            "Me gusta la música",
            "I like music",
            alternatives=("I like the music",),
            blank_word="gusta",
            wrong_options=("gusto", "gustas", "gustamos"),
        ),
        SentenceItem(
            "Ella lee un libro",
            "She reads a book",
            alternatives=("She is reading a book",),
            blank_word="lee",
            wrong_options=("leo", "lees", "leemos"),
        ),
        SentenceItem(
            "Nosotros jugamos al fútbol",
            "We play soccer",
            alternatives=("We play football", "We are playing soccer"),
            blank_word="jugamos",
            wrong_options=("juego", "juegas", "juega"),
        ),
        SentenceItem(
            "Mi amigo pinta un cuadro",
            "My friend paints a picture",
            alternatives=("My friend is painting a picture",),
            blank_word="pinta",
            wrong_options=("pinto", "pintas", "pintamos"),
        ),
        SentenceItem(
            "Me gusta el cine",
            "I like the movies",
            alternatives=("I like the cinema",),
            blank_word="el",
            wrong_options=("la", "los", "las"),
        ),
    ),
)

FEELINGS = SkillContent(
    title="Feelings",
    icon="smile",
    vocab=(
        VocabItem("feliz", "happy"),
        VocabItem("triste", "sad"),
        VocabItem("cansado", "tired"),
        VocabItem("enojado", "angry"),
        VocabItem("nervioso", "nervous"),
        VocabItem("emocionado", "excited"),
        VocabItem("tranquilo", "calm"),
        VocabItem("hambre", "hunger"),
    ),
    sentences=(
        SentenceItem(
            "Yo estoy feliz",
            "I am happy",
            alternatives=("I feel happy",),
            blank_word="estoy",
            wrong_options=("estás", "está", "estamos"),
        ),
        SentenceItem(
            "Ella está triste",
            "She is sad",
            alternatives=("She feels sad",),
            blank_word="está",
            wrong_options=("estoy", "estás", "estamos"),
        ),
        SentenceItem(
            "Nosotros estamos cansados",
            "We are tired",
            alternatives=("We feel tired",),
            blank_word="estamos",
            wrong_options=("estoy", "estás", "está"),
        ),
        SentenceItem(
            "Tengo mucha hambre",
            "I am very hungry",
            alternatives=("I am really hungry",),
            blank_word="mucha",
            wrong_options=("mucho", "muchos", "muchas"),
        ),
        SentenceItem(
            "Él está nervioso hoy",
            "He is nervous today",
            alternatives=("He feels nervous today",),
            blank_word="nervioso",
            wrong_options=("nerviosa", "nerviosos", "nerviosas"),
        ),
    ),
)

UNIT_3 = UnitContent(
    description="Talk about your day",
    color="purple",
    skills=(ROUTINE, WEATHER, HOBBIES, FEELINGS),
)
