from bucle import correr_bucle
from contexto import crear_contexto
from herramientas import crear_herramientas
from navegador import Navegador

TAREA = """Vota por una historia en Hacker News.

Entra a https://news.ycombinator.com.
Usa leer_historias para ver las historias con su posición, id y si ya está votada.
Elige la historia mejor ubicada que todavía no esté votada.
Haz clic en su flecha de voto con el selector exacto a[id="up_ID"] (cambia ID por el id real)."""

navegador = Navegador()
navegador.abrir()
try:
    herramientas = crear_herramientas(navegador)
    mensajes = crear_contexto(TAREA)
    resultado = correr_bucle(mensajes, herramientas)
finally:
    navegador.cerrar()

print("\n--- Resultado ---")
print(resultado["respuesta"])
print(f"Detenido por: {resultado['detenido_por']}")
