import streamlit as st
import random
from gtts import gTTS

# ======================
# PALABRAS
# ======================
words = {
    "sun": "sol",
    "moon": "luna",
    "star": "estrella",
    "city": "ciudad",
    "mountains": "montañas",
    "airport": "aeropuerto",

    "world": "mundo",
    "country": "pais",
    "valley": "valle",
    "sky": "cielo",
    "map": "mapa",
    "dawn": "amanecer",
    "night": "noche",
    "town": "pueblo",

    "bridge": "puente",
    "dam": "presa",
    "down": "abajo",
    "shore": "orilla",

    "neighborhood": "vecindario"
}

st.title("🎮 Inglés con Wada - Juego por niveles")

# ======================
# MODO
# ======================
modo = st.sidebar.selectbox(
    "Modo:",
    ["👀 Repaso", "🔁 Inglés → Español", "🔁 Español → Inglés", "🎧 Dictado"]
)

# ======================
# ESTADO
# ======================
if "score" not in st.session_state:
    st.session_state.score = 0

if "pregunta" not in st.session_state:
    st.session_state.pregunta = random.choice(list(words.keys()))

if "respondido" not in st.session_state:
    st.session_state.respondido = False

if "opciones" not in st.session_state:
    st.session_state.opciones = []

if "intentos" not in st.session_state:
    st.session_state.intentos = 0

# ======================
# NUEVA PREGUNTA
# ======================
def nueva_pregunta():
    st.session_state.pregunta = random.choice(list(words.keys()))
    st.session_state.respondido = False
    st.session_state.intentos = 0

    if modo == "🔁 Inglés → Español":
        opciones = list(words.values())
    else:
        opciones = list(words.keys())

    random.shuffle(opciones)
    st.session_state.opciones = opciones

# generar opciones si no existen
if not st.session_state.opciones:
    nueva_pregunta()

word = st.session_state.pregunta
translation = words[word]

# ======================
# 👀 REPASO
# ======================
if modo == "👀 Repaso":
    st.markdown(f"## {word.upper()} = {translation}")

    if st.button("🔊 Escuchar"):
        tts = gTTS(word, lang="en")
        tts.save("audio.mp3")
        st.audio("audio.mp3")

    if st.button("➡️ Siguiente"):
        nueva_pregunta()
        st.rerun()

# ======================
# 🔁 INGLÉS → ESPAÑOL
# ======================
elif modo == "🔁 Inglés → Español":

    st.markdown(f"## ¿Qué significa: {word.upper()}?")

    for i, op in enumerate(st.session_state.opciones):
        if st.button(op, key=f"ie_{i}"):
            if not st.session_state.respondido:
                st.session_state.respondido = True

                if op == translation:
                    st.success("✅ Correcto")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ Era: {translation}")

    if st.session_state.respondido:
        if st.button("➡️ Siguiente"):
            nueva_pregunta()
            st.rerun()

# ======================
# 🔁 ESPAÑOL → INGLÉS
# ======================
elif modo == "🔁 Español → Inglés":

    st.markdown(f"## ¿Cómo se dice: {translation.upper()}?")

    for i, op in enumerate(st.session_state.opciones):
        if st.button(op, key=f"ei_{i}"):
            if not st.session_state.respondido:
                st.session_state.respondido = True

                if op == word:
                    st.success("✅ Correcto")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ Era: {word}")

    if st.session_state.respondido:
        if st.button("➡️ Siguiente"):
            nueva_pregunta()
            st.rerun()

# ======================
# 🎧 DICTADO MEJORADO
# ======================
elif modo == "🎧 Dictado":

    st.markdown("## 🔊 Escucha y escribe")

    # audio
    tts = gTTS(word, lang="en")
    tts.save("audio.mp3")
    st.audio("audio.mp3")

    user_input = st.text_input("✍️ Escribe en inglés:")

    col1, col2, col3 = st.columns(3)

    # VALIDAR
    with col1:
        if st.button("Validar"):
            if user_input.lower().strip() == word:
                st.success("✅ Correcto")
                st.session_state.score += 1
                nueva_pregunta()
                st.rerun()
            else:
                st.session_state.intentos += 1

                if st.session_state.intentos < 3:
                    st.error(f"❌ Intento {st.session_state.intentos}/3")
                    st.info(f"Pista: empieza por '{word[0]}'")
                else:
                    st.warning("⚠️ Llegaste al límite de intentos")

    # MOSTRAR
    with col2:
        if st.session_state.intentos >= 3:
            if st.button("👀 Mostrar"):
                st.info(f"La palabra correcta es: **{word}**")

    # OMITIR
    with col3:
        if st.button("⏭️ Omitir"):
            nueva_pregunta()
            st.rerun()

# ======================
# SCORE
# ======================
st.sidebar.markdown(f"## 🏆 Puntaje: {st.session_state.score}")