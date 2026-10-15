import arxiv

DEFINICIONES = [
    {
        "name": "buscar_arxiv",
        "description": "Busca papers en arXiv. Devuelve id, título, autores y resumen de los 5 primeros resultados.",
        "input_schema": {
            "type": "object",
            "properties": {"consulta": {"type": "string", "description": 'Por ejemplo: "P versus NP"'}},
            "required": ["consulta"],
        },
    },
    {
        "name": "descargar_paper",
        "description": "Descarga el PDF de un paper de arXiv y lo agrega a la biblioteca para poder consultarlo.",
        "input_schema": {
            "type": "object",
            "properties": {"arxiv_id": {"type": "string", "description": "Por ejemplo: 1708.03486"}},
            "required": ["arxiv_id"],
        },
    },
    {
        "name": "consultar_rag",
        "description": "Busca en los papers descargados los 5 fragmentos más parecidos a la pregunta. Devuelve el texto de cada fragmento y de qué paper sale.",
        "input_schema": {
            "type": "object",
            "properties": {"pregunta": {"type": "string", "description": "Escríbela en el idioma de los papers"}},
            "required": ["pregunta"],
        },
    },
]


def crear_herramientas(biblioteca):
    return {
        "buscar_arxiv": arxiv.buscar,
        "descargar_paper": biblioteca.descargar,
        "consultar_rag": biblioteca.consultar,
    }
