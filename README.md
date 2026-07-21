# Alura Agente 🎓

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

## Cómo correrlo en local

```bash
git clone <url-de-tu-repo>
cd alura-agente
pip install -r requirements.txt

cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edita .streamlit/secrets.toml y pega tu API key de Groq (gratis en https://console.groq.com/keys)

streamlit run app.py
```

## Despliegue en Streamlit Community Cloud (gratis)

1. Sube este repositorio a GitHub (asegúrate de que `data/` incluya tus CSV reales).
2. Entra a [share.streamlit.io](https://share.streamlit.io) e inicia sesión con tu cuenta de GitHub.
3. Crea una app nueva, selecciona el repo y `app.py` como archivo principal.
4. En **Settings → Secrets**, agrega:
   ```toml
   GROQ_API_KEY = "tu_api_key_de_groq"
   ```
5. Despliega. Streamlit te da una URL pública (`tu-app.streamlit.app`).

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

## Enlace a la app en producción

> _Pendiente — agrega aquí el enlace o una captura una vez desplegada._

## Próximos pasos

- [ ] Exponer también una API REST con FastAPI (para integraciones externas)
- [ ] Migrar el vector store a `persist_directory` con almacenamiento externo si el volumen de documentos crece
- [ ] Desplegar alternativamente en OCI Compute / Render / Railway como servicio persistente
