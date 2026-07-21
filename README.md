# Alura Agente 🎓

Asistente virtual de soporte para una escuela online, basado en **RAG
(Retrieval-Augmented Generation)**. Responde preguntas de estudiantes y
aspirantes usando como única fuente de verdad los documentos internos de la
escuela (reglamento, política de reembolso, FAQ, guía de la plataforma,
becas), cargados desde archivos CSV.

## Índice

- [Descripción general](#descripción-general)
- [Arquitectura](#arquitectura)
- [Tecnologías y herramientas](#tecnologías-y-herramientas)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Instrucciones para ejecutar el proyecto](#instrucciones-para-ejecutar-el-proyecto)
- [Ejemplos de preguntas y respuestas](#ejemplos-de-preguntas-y-respuestas)
- [Despliegue en producción](#despliegue-en-producción)
- [Próximos pasos](#próximos-pasos)

## Descripción general

**Alura Agente** es un chatbot de soporte para una escuela online que responde
preguntas de estudiantes, aspirantes y docentes sobre reglamento, políticas de
reembolso, preguntas frecuentes, uso de la plataforma y becas. En vez de que el
modelo de lenguaje invente respuestas, el agente busca primero en los
documentos oficiales de la escuela (cargados como CSV) y responde
**únicamente** con base en lo que encuentra ahí — si no encuentra la
información, lo dice explícitamente en vez de inventar datos.

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

**Flujo de datos:**
1. `ingesta.py` lee cada CSV y convierte cada fila en un documento de texto.
2. Los documentos se dividen en fragmentos pequeños (chunking) para mejorar la precisión de la búsqueda.
3. `agente.py` convierte cada fragmento en un vector (embedding) y lo indexa en ChromaDB.
4. Cuando llega una pregunta, se buscan los 4 fragmentos más relevantes (retriever) y se le pasan al LLM junto con un *prompt* que le prohíbe inventar información fuera de ese contexto.
5. `app.py` expone todo esto como una interfaz de chat web con Streamlit.

## Tecnologías y herramientas

| Categoría | Herramienta |
|---|---|
| Lenguaje | Python 3 |
| Orquestación LLM | LangChain |
| Modelo de lenguaje (LLM) | Groq — `llama-3.3-70b-versatile` |
| Embeddings | HuggingFace — `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` |
| Base vectorial | ChromaDB |
| Interfaz web | Streamlit |
| Procesamiento de datos | Pandas |
| Hosting | Streamlit Community Cloud |

## Estructura del repositorio

```
alura-agente/
├── ingesta.py              # Carga los CSV y los divide en fragmentos
├── agente.py               # Embeddings, base vectorial y cadena RAG
├── app.py                  # Interfaz de chat en Streamlit (punto de entrada)
├── requirements.txt        # Dependencias del proyecto
├── data/                   # Archivos CSV fuente (documentos de la escuela)
├── .streamlit/
│   └── secrets.toml.example  # Plantilla para tu API key (no subir la real)
├── .gitignore
├── DEPLOY_OCI.md           # Guía alternativa de despliegue en Oracle Cloud
└── README.md
```

> Los archivos `ingesta.py`, `agente.py` y `app.py` son el **código fuente**
> del proyecto: ahí vive toda la lógica de lectura de documentos, generación
> de embeddings, búsqueda semántica y generación de respuestas.

## Instrucciones para ejecutar el proyecto

### Requisitos previos
- Python 3.10 o superior
- Una cuenta gratuita en [Groq](https://console.groq.com/keys) para obtener tu API key

### Pasos

```bash
# 1. Clona el repositorio
git clone <url-de-tu-repo>
cd alura-agente

# 2. Crea un entorno virtual e instala dependencias
python3 -m venv venv
source venv/bin/activate          # En Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configura tu API key de Groq
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Abre .streamlit/secrets.toml y pega tu API key real de Groq

# 4. Coloca tus archivos CSV reales dentro de la carpeta data/

# 5. Ejecuta la app
streamlit run app.py
```

La app abrirá automáticamente en tu navegador en `http://localhost:8501`.

## Ejemplos de preguntas y respuestas

> Reemplaza los textos en *cursiva* con las respuestas reales que te dio el
> agente al correrlo (cópialas directo de tu app o de tu notebook de pruebas).

**Pregunta 1:** ¿Hasta cuántos días tengo para pedir la devolución de mi
dinero si el curso no cumple mis expectativas?
**Respuesta del agente:** *(pega aquí la respuesta real generada)*

**Pregunta 2:** ¿Cuáles son los requisitos mínimos para mantener una beca
académica activa?
**Respuesta del agente:** *(pega aquí la respuesta real generada)*

**Pregunta 3:** ¿Cómo puedo descargar mi certificado una vez finalizado el
curso?
**Respuesta del agente:** *(pega aquí la respuesta real generada)*

## Despliegue en producción

- **URL pública:** `<pega aquí el enlace de tu app en Streamlit Community Cloud>`
- **Captura de pantalla:**

  ```markdown
  ![Alura Agente funcionando](ruta/a/tu/captura.png)
  ```
  (sube tu imagen a una carpeta como `assets/` dentro del repo y ajusta la ruta)

## Próximos pasos

- [ ] Exponer también una API REST con FastAPI (para integraciones externas)
- [ ] Migrar el vector store a `persist_directory` con almacenamiento externo si el volumen de documentos crece
- [ ] Retomar el despliegue en OCI Compute como alternativa (ver `DEPLOY_OCI.md`)
