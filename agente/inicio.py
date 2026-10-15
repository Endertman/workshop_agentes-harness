from harness import correr_harness
from verificar import verificar_voto

TAREA = """Vota por una historia en Hacker News.

Entra a https://news.ycombinator.com.
Usa leer_historias para ver las historias con su posición, id y si ya está votada.
Elige la historia mejor ubicada que todavía no esté votada.
Haz clic en su flecha de voto con el selector exacto a[id="up_ID"] (cambia ID por el id real)."""

resultado = correr_harness(TAREA, verificar_voto)

print("\n--- Resultado ---")
print(resultado["respuesta"])
print(f"Detenido por: {resultado['detenido_por']}")
print(f"Verificación: {'PASA' if resultado['verificado'] else 'FALLA'} - {resultado['motivo']}")
