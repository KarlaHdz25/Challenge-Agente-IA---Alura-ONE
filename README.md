# Challenge-Agente-IA---Alura-ONE
Asistente virtual RAG para una escuela online. Responde preguntas de estudiantes y aspirantes (reembolsos, becas, plataforma, reglamento) usando LangChain + Groq (Llama 3.3) + embeddings de HuggingFace + ChromaDB. Interfaz en Streamlit.

# Alura Agente

Asistente virtual de soporte para una escuela online, basado en **RAG
(Retrieval-Augmented Generation)**. Responde preguntas de estudiantes y
aspirantes usando como única fuente de verdad los documentos internos de la
escuela (reglamento, política de reembolso, FAQ, guía de la plataforma,
becas), cargados desde archivos CSV.

## Arquitectura

```
CSV (data/)
   │
   ▼
ingesta.py  ──►  fragmentos de texto (chunking)
   │
   ▼
agente.py   ──►  embeddings (HuggingFace) ──► Chroma (vector store)
   │                                              │
   │                                              ▼
   └──►  cadena RAG: retriever → prompt → Groq (Llama 3.3) → respuesta
   │
   ▼
app.py      ──►  interfaz de chat (Streamlit)
```

- **Embeddings:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
  (HuggingFace, gratuito, corre localmente — sin límites de cuota de API).
- **LLM:** Groq (`llama-3.3-70b-versatile`) — free tier generoso y rápido.
- **Vector store:** ChromaDB, en memoria (se reconstruye al iniciar la app).
- **Interfaz:** Streamlit, con historial de conversación por sesión.

## Estructura del repositorio

| Archivo | Responsabilidad |
|---|---|
| `ingesta.py` | Carga los CSV y los divide en fragmentos |
| `agente.py` | Construye embeddings, base vectorial y la cadena RAG |
| `app.py` | Interfaz de chat en Streamlit (punto de entrada) |
| `data/` | Archivos CSV fuente (reglamento, FAQ, becas, etc.) |
| `requirements.txt` | Dependencias del proyecto |

## Ejemplos de preguntas y respuestas

**Pregunta:** ¿Hasta cuántos días tengo para pedir la devolución de mi dinero
si el curso no cumple mis expectativas?
**Alura Agente:** *(responde citando el plazo exacto encontrado en
`politica_de_reembolso.csv`, o indica que no tiene esa información si no
está en los documentos)*

**Pregunta:** ¿Cuáles son los requisitos mínimos para mantener una beca
académica activa?
**Alura Agente:** *(responde con base en `programa_de_becas_y_afiliados.csv`)*

**Pregunta:** ¿Cómo puedo descargar mi certificado una vez finalizado el curso?
**Alura Agente:** *(responde con base en `guia_de_uso_de_la_plataforma.csv`)*
