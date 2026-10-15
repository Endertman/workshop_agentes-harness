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
]


def sin_busqueda(consulta):
    return "La búsqueda en arXiv está desactivada. Responde con lo que sepas."


def crear_herramientas(activas=True):
    return {"buscar_arxiv": arxiv.buscar if activas else sin_busqueda}
