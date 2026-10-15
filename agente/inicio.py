from harness import correr_harness
from verificar import verificar_citas

TAREA = """Busca en arXiv papers sobre las barreras para resolver P vs NP (relativización, pruebas naturales, algebrización).
Descarga los 2 más relevantes y responde: ¿por qué las técnicas actuales no alcanzan para probar P ≠ NP?
Respalda cada idea con una cita textual de los papers, una por línea, con este formato exacto:
- [arXiv:ID] "cita textual en el idioma original" — tu explicación
Cita frases en prosa, no fórmulas: al pasar el PDF a texto, la notación matemática se rompe."""

resultado = correr_harness(TAREA, verificar_citas)

print("\n--- Resultado ---")
print(resultado["respuesta"])
print(f"Detenido por: {resultado['detenido_por']}")
print(f"Verificación: {'PASA' if resultado['verificado'] else 'FALLA'} - {resultado['motivo']}")
