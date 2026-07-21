"""
app.py
Interfaz de chat en Streamlit para el Alura Agente (asistente RAG de la
escuela online). Punto de entrada para despliegue en Streamlit Community Cloud.
"""

import os
import streamlit as st

from ingesta import obtener_fragmentos
from agente import construir_agente

st.set_page_config(page_title="Alura Agente", page_icon="🎓")

# --- Configuración de la API Key de Groq ---
# En local: crea un archivo .streamlit/secrets.toml con GROQ_API_KEY = "tu_key"
# En Streamlit Community Cloud: agrégala en el panel "Secrets" de la app.
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
elif not os.environ.get("GROQ_API_KEY"):
    st.error(
        "⚠️ No se encontró GROQ_API_KEY. Agrégala en .streamlit/secrets.toml "
        "(local) o en el panel de Secrets de Streamlit Cloud (producción)."
    )
    st.stop()


@st.cache_resource(show_spinner="Cargando documentos y preparando el agente...")
def cargar_cadena_rag():
    """
    Se ejecuta una sola vez por sesión de servidor (no en cada mensaje):
    carga los CSV, genera embeddings y arma la cadena RAG con Groq.
    """
    fragmentos = obtener_fragmentos()
    return construir_agente(fragmentos)


cadena_rag = cargar_cadena_rag()

st.title("🎓 Alura Agente")
st.caption("Asistente virtual de soporte para estudiantes y aspirantes")

if "historial" not in st.session_state:
    st.session_state.historial = []

# Muestra el historial de la conversación
for mensaje in st.session_state.historial:
    with st.chat_message(mensaje["rol"]):
        st.markdown(mensaje["contenido"])

# Entrada de chat
pregunta = st.chat_input("Escribe tu pregunta...")

if pregunta:
    st.session_state.historial.append({"rol": "user", "contenido": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            respuesta = cadena_rag.invoke(pregunta)
        st.markdown(respuesta)

    st.session_state.historial.append({"rol": "assistant", "contenido": respuesta})
