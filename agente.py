"""
agente.py
Construye la base vectorial (Chroma + HuggingFace embeddings) y la cadena
conversacional RAG (Groq/Llama) del asistente de la escuela online.
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

MODELO_EMBEDDINGS = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
MODELO_LLM = "llama-3.3-70b-versatile"

PROMPT_TEMPLATE = ChatPromptTemplate.from_template(
    """Eres el asistente virtual de soporte de una escuela online.
Responde la pregunta del estudiante o aspirante de forma clara, breve y amable,
basándote ÚNICAMENTE en el siguiente contexto extraído de los documentos oficiales de la escuela.

Si la información no está en el contexto, responde exactamente:
"No tengo esa información en los documentos disponibles. Te recomiendo contactar al equipo de soporte."
No inventes datos, plazos ni porcentajes que no estén en el contexto.

Contexto:
{contexto}

Pregunta: {pregunta}

Respuesta:"""
)


def construir_vectorstore(fragmentos: list[Document]) -> Chroma:
    """
    Crea la base vectorial en memoria (sin persist_directory) para evitar
    problemas de dimensiones al redesplegar en un entorno con disco efímero
    como Streamlit Community Cloud.
    """
    embeddings = HuggingFaceEmbeddings(model_name=MODELO_EMBEDDINGS)
    return Chroma.from_documents(documents=fragmentos, embedding=embeddings)


def formatear_contexto(docs: list[Document]) -> str:
    return "\n\n".join(
        f"[Fuente: {d.metadata.get('fuente', 'desconocida')}]\n{d.page_content}" for d in docs
    )


def construir_cadena_rag(vectorstore: Chroma, k: int = 4):
    """Arma la cadena RAG completa: retriever -> prompt -> Groq -> parser de texto."""
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    llm = ChatGroq(model=MODELO_LLM, temperature=0.2)

    return (
        {"contexto": retriever | formatear_contexto, "pregunta": RunnablePassthrough()}
        | PROMPT_TEMPLATE
        | llm
        | StrOutputParser()
    )


def construir_agente(fragmentos: list[Document]):
    """Función de conveniencia: arma vectorstore + cadena en un solo paso."""
    vectorstore = construir_vectorstore(fragmentos)
    return construir_cadena_rag(vectorstore)
