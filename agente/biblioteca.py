import io
import json
import logging
import re
import time
import unicodedata
import urllib.request
from pathlib import Path

import numpy as np
from model2vec import StaticModel
from pypdf import PdfReader

logging.getLogger("pypdf").setLevel(logging.ERROR)

CARPETA = Path(__file__).resolve().parent.parent / "papers"
EMBEDDINGS = "minishlab/potion-base-8M"  # ~30 MB, vectores de 256 dimensiones
PALABRAS_POR_FRAGMENTO = 120
SOLAPE = 30


def limpiar(texto):
    texto = unicodedata.normalize("NFKC", texto)  # "ﬁ" → "fi"
    texto = re.sub(r"-\n(\w)", r"\1", texto)       # une palabras cortadas al final de línea
    return " ".join(texto.split())


def cortar(texto):
    palabras = texto.split()
    paso = PALABRAS_POR_FRAGMENTO - SOLAPE
    return [" ".join(palabras[i:i + PALABRAS_POR_FRAGMENTO]) for i in range(0, len(palabras), paso)]


class Biblioteca:
    """El RAG: cada fragmento de cada paper es una fila de la matriz M."""

    def __init__(self):
        self.modelo = StaticModel.from_pretrained(EMBEDDINGS)
        self.fragmentos = []  # (arxiv_id, texto), en el mismo orden que las filas de M
        self.M = None

    def vectorizar(self, textos):
        V = self.modelo.encode(textos)
        return V / np.linalg.norm(V, axis=1, keepdims=True)  # normalizados: producto punto = coseno

    def descargar(self, arxiv_id):
        if any(id_ == arxiv_id for id_, _ in self.fragmentos):
            return f"arXiv:{arxiv_id} ya está en la biblioteca"

        archivo = CARPETA / f"{arxiv_id}.pdf"
        if not archivo.exists():
            time.sleep(3)  # arXiv pide como máximo una consulta cada 3 segundos
            with urllib.request.urlopen(f"https://arxiv.org/pdf/{arxiv_id}", timeout=60) as respuesta:
                CARPETA.mkdir(exist_ok=True)
                archivo.write_bytes(respuesta.read())

        paginas = PdfReader(io.BytesIO(archivo.read_bytes())).pages
        fragmentos = cortar(limpiar("\n".join(pagina.extract_text() or "" for pagina in paginas)))
        V = self.vectorizar(fragmentos)
        self.M = V if self.M is None else np.vstack([self.M, V])
        self.fragmentos += [(arxiv_id, texto) for texto in fragmentos]
        return f"arXiv:{arxiv_id} descargado: {len(fragmentos)} fragmentos en la biblioteca ({len(self.fragmentos)} en total)"

    # simplified: búsqueda exacta O(N) sobre la matriz en memoria; con miles de papers, un índice aproximado (FAISS)
    def consultar(self, pregunta, k=5):
        if self.M is None:
            return "La biblioteca está vacía. Descarga papers primero con descargar_paper."
        q = self.vectorizar([pregunta])[0]
        puntajes = self.M @ q  # similitud coseno con cada fragmento
        mejores = np.argsort(puntajes)[::-1][:k]
        return json.dumps([
            {"arxiv_id": self.fragmentos[i][0], "similitud": round(float(puntajes[i]), 3), "texto": self.fragmentos[i][1]}
            for i in mejores
        ], ensure_ascii=False, indent=2)
