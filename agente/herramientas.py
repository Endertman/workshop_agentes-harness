DEFINICIONES = [
    {
        "name": "ir_a",
        "description": "Abre una URL en el navegador.",
        "input_schema": {
            "type": "object",
            "properties": {"url": {"type": "string"}},
            "required": ["url"],
        },
    },
    {
        "name": "leer_texto",
        "description": "Devuelve el texto visible de la página actual.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "leer_historias",
        "description": "Devuelve las historias de Hacker News de la página actual: posición, id, título y si ya está votada.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "clic",
        "description": "Hace clic en un elemento de la página usando un selector CSS.",
        "input_schema": {
            "type": "object",
            "properties": {"selector": {"type": "string", "description": 'Por ejemplo: a[id="up_123"]'}},
            "required": ["selector"],
        },
    },
]


def crear_herramientas(navegador):
    return {
        "ir_a": navegador.ir_a,
        "leer_texto": navegador.leer_texto,
        "leer_historias": navegador.leer_historias,
        "clic": navegador.clic,
    }
