from bucle import correr_bucle
from contexto import crear_contexto
from herramientas import crear_herramientas
from login import revisar_login
from navegador import Navegador


def correr_harness(tarea, verificar, intentos=3):
    for intento in range(1, intentos + 1):
        print(f"\n--- Intento {intento} de {intentos} ---")
        resultado = correr_intento(tarea, verificar)
        if resultado["verificado"]:
            break
    return resultado


def correr_intento(tarea, verificar):
    navegador = Navegador()
    navegador.abrir()
    try:
        herramientas = crear_herramientas(navegador)
        mensajes = crear_contexto(tarea)
        resultado = correr_bucle(mensajes, herramientas, revisar_paso=lambda: revisar_login(navegador))
        verificado, motivo = verificar(navegador, resultado["pasos"])
        resultado["verificado"] = verificado
        resultado["motivo"] = motivo
        return resultado
    finally:
        navegador.cerrar()
