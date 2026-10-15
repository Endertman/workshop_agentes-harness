import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

API = "https://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"


def _consultar(parametros):
    time.sleep(3)  # arXiv pide como máximo una consulta cada 3 segundos
    with urllib.request.urlopen(f"{API}?{urllib.parse.urlencode(parametros)}", timeout=30) as respuesta:
        feed = ET.fromstring(respuesta.read())
    papers = []
    for entrada in feed.findall(f"{ATOM}entry"):
        papers.append({
            "id": entrada.findtext(f"{ATOM}id").rsplit("/abs/", 1)[-1].rsplit("v", 1)[0],
            "titulo": " ".join(entrada.findtext(f"{ATOM}title").split()),
            "autores": [autor.findtext(f"{ATOM}name") for autor in entrada.findall(f"{ATOM}author")],
            "resumen": " ".join(entrada.findtext(f"{ATOM}summary").split()),
        })
    return papers


def buscar(consulta):
    # "P versus NP" → all:P AND all:versus AND all:NP (sin el AND, arXiv mezcla resultados de cada palabra)
    papers = _consultar({"search_query": " AND ".join(f"all:{palabra}" for palabra in consulta.split()), "max_results": 5})
    return json.dumps(papers, ensure_ascii=False, indent=2)


# Devuelve el título real del paper, o None si no existe
def obtener(arxiv_id):
    papers = _consultar({"id_list": arxiv_id})
    return papers[0]["titulo"] if papers else None
