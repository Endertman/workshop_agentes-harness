from contexto import SISTEMA
from herramientas import DEFINICIONES
from modelo import llamar_modelo


def correr_bucle(mensajes, herramientas):
    pasos = []
    iteracion = 0

    while True:
        iteracion += 1
        print(f"[iteración {iteracion}] llamando al modelo ({len(mensajes)} mensajes en contexto)")
        respuesta = llamar_modelo(SISTEMA, mensajes, DEFINICIONES)
        mensajes.append({"role": "assistant", "content": respuesta.content})

        if respuesta.stop_reason != "tool_use":
            texto = "".join(bloque.text for bloque in respuesta.content if bloque.type == "text")
            return {"respuesta": texto, "detenido_por": "modelo", "pasos": pasos}

        resultados = []
        for bloque in respuesta.content:
            if bloque.type == "tool_use":
                print(f"    → {bloque.name}({bloque.input})")
                resultado = ejecutar(herramientas, bloque.name, bloque.input)
                pasos.append({"herramienta": bloque.name, "entrada": bloque.input, "resultado": resultado})
                resultados.append({"type": "tool_result", "tool_use_id": bloque.id, "content": resultado})

        mensajes.append({"role": "user", "content": resultados})


def ejecutar(herramientas, nombre, entrada):
    try:
        return herramientas[nombre](**entrada)
    except Exception as error:
        return f"Error: {error}"
