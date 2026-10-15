from contexto import SISTEMA, recortar_contexto
from herramientas import DEFINICIONES
from limites import revisar_limites
from modelo import llamar_modelo


def correr_bucle(mensajes, herramientas, revisar_paso):
    pasos = []
    iteracion = 0

    while True:
        iteracion += 1
        mensajes = recortar_contexto(mensajes)
        motivo = revisar_limites(iteracion)
        if motivo:
            return {"respuesta": motivo, "detenido_por": "límite", "pasos": pasos}

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

        aviso = revisar_paso()
        if aviso:
            resultados.append({"type": "text", "text": aviso})

        mensajes.append({"role": "user", "content": resultados})


def ejecutar(herramientas, nombre, entrada):
    try:
        return herramientas[nombre](**entrada)
    except Exception as error:
        return f"Error: {error}"
