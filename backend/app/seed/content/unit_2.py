"""Unit 2: Get around a city."""

from app.seed.content.structures import SentenceItem, SkillContent, UnitContent, VocabItem

PLACES = SkillContent(
    title="Places",
    icon="building",
    vocab=(
        VocabItem("casa", "house", "🏠"),
        VocabItem("escuela", "school", "🏫"),
        VocabItem("tienda", "store", "🏪"),
        VocabItem("parque", "park", "🌳"),
        VocabItem("hospital", "hospital", "🏥"),
        VocabItem("banco", "bank", "🏦"),
        VocabItem("playa", "beach", "🏖️"),
        VocabItem("restaurante", "restaurant", "🍽️"),
    ),
    sentences=(
        SentenceItem(
            "Yo estoy en casa",
            "I am at home",
            alternatives=("I am in the house",),
            blank_word="estoy",
            wrong_options=("estás", "está", "estamos"),
        ),
        SentenceItem(
            "El parque es grande",
            "The park is big",
            alternatives=("The park is large",),
            blank_word="es",
            wrong_options=("soy", "eres", "somos"),
        ),
        SentenceItem(
            "Ella va a la escuela",
            "She goes to school",
            alternatives=("She goes to the school",),
            blank_word="va",
            wrong_options=("voy", "vas", "vamos"),
        ),
        SentenceItem(
            "Nosotros comemos en el restaurante",
            "We eat at the restaurant",
            alternatives=("We eat in the restaurant", "We are eating at the restaurant"),
            blank_word="comemos",
            wrong_options=("como", "comes", "come"),
        ),
        SentenceItem(
            "El banco está cerca",
            "The bank is close",
            alternatives=("The bank is near",),
            blank_word="está",
            wrong_options=("estoy", "estás", "estamos"),
        ),
    ),
)

TRAVEL = SkillContent(
    title="Travel",
    icon="plane",
    vocab=(
        VocabItem("avión", "plane", "✈️"),
        VocabItem("tren", "train", "🚆"),
        VocabItem("autobús", "bus", "🚌"),
        VocabItem("taxi", "taxi", "🚕"),
        VocabItem("barco", "boat", "⛴️"),
        VocabItem("maleta", "suitcase", "🧳"),
        VocabItem("hotel", "hotel", "🏨"),
        VocabItem("boleto", "ticket", "🎫"),
    ),
    sentences=(
        SentenceItem(
            "Yo viajo en tren",
            "I travel by train",
            alternatives=("I travel on the train",),
            blank_word="viajo",
            wrong_options=("viajas", "viaja", "viajamos"),
        ),
        SentenceItem(
            "El avión es rápido",
            "The plane is fast",
            alternatives=("The airplane is fast",),
            blank_word="rápido",
            wrong_options=("rápida", "rápidos", "rápidas"),
        ),
        SentenceItem(
            "Necesito un boleto",
            "I need a ticket",
            alternatives=("I need one ticket",),
            blank_word="un",
            wrong_options=("una", "unos", "unas"),
        ),
        SentenceItem(
            "Ella tiene una maleta",
            "She has a suitcase",
            alternatives=("She has one suitcase",),
            blank_word="tiene",
            wrong_options=("tengo", "tienes", "tenemos"),
        ),
        SentenceItem(
            "El hotel está cerca",
            "The hotel is close",
            alternatives=("The hotel is near",),
            blank_word="está",
            wrong_options=("estoy", "estás", "estamos"),
        ),
    ),
)

DIRECTIONS = SkillContent(
    title="Directions",
    icon="signpost",
    vocab=(
        VocabItem("izquierda", "left", "⬅️"),
        VocabItem("derecha", "right", "➡️"),
        VocabItem("recto", "straight ahead", "⬆️"),
        VocabItem("cerca", "near", "📍"),
        VocabItem("lejos", "far", "🔭"),
        VocabItem("esquina", "corner", "🔲"),
        VocabItem("calle", "street", "🛣️"),
        VocabItem("mapa", "map", "🗺️"),
    ),
    sentences=(
        SentenceItem(
            "Gira a la izquierda",
            "Turn left",
            alternatives=("Turn to the left",),
            blank_word="la",
            wrong_options=("el", "los", "las"),
        ),
        SentenceItem(
            "Gira a la derecha",
            "Turn right",
            alternatives=("Turn to the right",),
            blank_word="derecha",
            wrong_options=("derecho", "derechos", "derechas"),
        ),
        SentenceItem(
            "Sigue recto por la calle",
            "Go straight down the street",
            alternatives=("Go straight along the street",),
            blank_word="calle",
            wrong_options=("calles", "camino", "caminos"),
        ),
        SentenceItem(
            "El parque está lejos",
            "The park is far",
            alternatives=("The park is far away",),
            blank_word="está",
            wrong_options=("estoy", "estás", "estamos"),
        ),
        SentenceItem(
            "Mira el mapa",
            "Look at the map",
            alternatives=("Take a look at the map",),
            blank_word="el",
            wrong_options=("la", "los", "las"),
        ),
    ),
)

TIME = SkillContent(
    title="Time",
    icon="clock",
    vocab=(
        VocabItem("hora", "hour", "⏰"),
        VocabItem("día", "day", "☀️"),
        VocabItem("noche", "night", "🌙"),
        VocabItem("semana", "week", "📅"),
        VocabItem("hoy", "today", "📆"),
        VocabItem("ayer", "yesterday", "⏪"),
        VocabItem("tarde", "afternoon", "🌇"),
        VocabItem("reloj", "clock", "🕰️"),
    ),
    sentences=(
        SentenceItem(
            "Hoy es lunes",
            "Today is Monday",
            alternatives=("It is Monday today",),
            blank_word="es",
            wrong_options=("soy", "eres", "somos"),
        ),
        SentenceItem(
            "Ayer fue domingo",
            "Yesterday was Sunday",
            alternatives=("It was Sunday yesterday",),
            blank_word="fue",
            wrong_options=("fui", "fuiste", "fuimos"),
        ),
        SentenceItem(
            "Tengo clase por la tarde",
            "I have class in the afternoon",
            alternatives=("I have a class in the afternoon",),
            blank_word="la",
            wrong_options=("el", "los", "las"),
        ),
        SentenceItem(
            "El reloj está en la mesa",
            "The clock is on the table",
            alternatives=("The watch is on the table",),
            blank_word="está",
            wrong_options=("estoy", "estás", "estamos"),
        ),
        SentenceItem(
            "Una semana tiene siete días",
            "A week has seven days",
            alternatives=("One week has seven days",),
            blank_word="tiene",
            wrong_options=("tengo", "tienes", "tenemos"),
        ),
    ),
)

UNIT_2 = UnitContent(
    description="Get around a city",
    color="blue",
    skills=(PLACES, TRAVEL, DIRECTIONS, TIME),
)
