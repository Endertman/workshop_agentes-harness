SISTEMA = """Eres un asistente con acceso a herramientas.
Usa las herramientas siempre que te ayuden a dar una respuesta más precisa.
Cuando tengas suficiente información, responde de forma directa y breve.
Responde siempre en español."""


def crear_contexto(tarea):
    return [{"role": "user", "content": tarea}]


# Conserva la tarea y solo las últimas rondas (respuesta del modelo + resultados)
def recortar_contexto(mensajes, rondas=8):
    tarea, resto = mensajes[0], mensajes[1:]
    return [tarea] + resto[-2 * rondas:]
