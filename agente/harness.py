from bucle import correr_bucle
from contexto import crear_contexto
from herramientas import crear_herramientas
from navegador import Navegador


def correr_harness(tarea):
    navegador = Navegador()
    navegador.abrir()
    try:
        herramientas = crear_herramientas(navegador)
        mensajes = crear_contexto(tarea)
        return correr_bucle(mensajes, herramientas)
    finally:
        navegador.cerrar()
