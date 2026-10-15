from biblioteca import Biblioteca
from bucle import correr_bucle
from contexto import crear_contexto
from herramientas import crear_herramientas


def correr_harness(tarea, verificar, intentos=3):
    tarea_intento = tarea
    for intento in range(1, intentos + 1):
        print(f"\n--- Intento {intento} de {intentos} ---")
        resultado = correr_intento(tarea_intento, verificar)
        if resultado["verificado"]:
            break
        # El reintento ya no es a ciegas: el modelo sabe por qué falló
        tarea_intento = f"{tarea}\n\nEl verificador rechazó tu respuesta anterior: {resultado['motivo']}"
    return resultado


def correr_intento(tarea, verificar):
    biblioteca = Biblioteca()  # el entorno de este intento, como antes el navegador
    herramientas = crear_herramientas(biblioteca)
    mensajes = crear_contexto(tarea)
    resultado = correr_bucle(mensajes, herramientas, revisar_paso=lambda: None)
    verificado, motivo = verificar(resultado["respuesta"], resultado["pasos"])
    resultado["verificado"] = verificado
    resultado["motivo"] = motivo
    print(f"[harness] Verificación: {'PASA' if verificado else 'FALLA'} - {motivo}")
    return resultado
