"""
ingesta.py
Carga los documentos fuente (CSV) de la escuela y los divide en fragmentos
listos para ser convertidos en embeddings.
"""

import os
import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 👉 Nombres de los archivos CSV dentro de la carpeta data/
ARCHIVOS_CSV = [
    "reglamento_del_estudiante.csv",
    "politica_de_reembolso.csv",
    "preguntas_frecuentes.csv",
    "guia_de_uso_de_la_plataforma.csv",
    "programa_de_becas_y_afiliados.csv",
]

CARPETA_DATA = os.path.join(os.path.dirname(__file__), "data")


def cargar_documentos(carpeta_data: str = CARPETA_DATA, archivos: list[str] = ARCHIVOS_CSV) -> list[Document]:
    """
    Lee cada CSV fila por fila, concatena todas sus columnas en un texto
    (columna: valor) y guarda el nombre del archivo como metadato 'fuente'.
    Es agnóstico a la estructura de cada CSV.
    """
    documentos = []

    for archivo in archivos:
        ruta = os.path.join(carpeta_data, archivo)
        try:
            df = pd.read_csv(ruta)
        except FileNotFoundError:
            print(f"⚠️  No se encontró {ruta}, se omite.")
            continue

        for _, fila in df.iterrows():
            texto = "\n".join(f"{col}: {fila[col]}" for col in df.columns if pd.notna(fila[col]))
            documentos.append(Document(page_content=texto, metadata={"fuente": archivo}))

    return documentos


def fragmentar_documentos(documentos: list[Document]) -> list[Document]:
    """Divide los documentos en fragmentos pequeños para mejorar la búsqueda semántica."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(documentos)


def obtener_fragmentos() -> list[Document]:
    """Función de conveniencia: carga y fragmenta en un solo paso."""
    documentos = cargar_documentos()
    return fragmentar_documentos(documentos)
