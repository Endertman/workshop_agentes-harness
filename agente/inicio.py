from harness import correr_harness
from verificar import verificar_citas

# Ponlo en False para que el agente responda de memoria, sin buscar en arXiv
CON_BUSQUEDA = True

TAREA = """Recomiéndame 3 papers de arXiv sobre el problema P vs NP.
Responde con una línea por paper, con este formato exacto:
- [arXiv:ID] Título"""

resultado = correr_harness(TAREA, verificar_citas, herramientas_activas=CON_BUSQUEDA)

print("\n--- Resultado ---")
print(resultado["respuesta"])
print(f"Detenido por: {resultado['detenido_por']}")
print(f"Verificación: {'PASA' if resultado['verificado'] else 'FALLA'} - {resultado['motivo']}")
