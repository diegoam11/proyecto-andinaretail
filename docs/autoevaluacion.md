# Cuadro de autoevaluación — Proyecto Grupal AndinaRetail S.A.C.

Réplica del cuadro de la Sección 11 del PG. Niveles: E=Excelente (100%),
B=Bueno (75%), R=Regular (50%), D=Deficiente (25% o menos). Completar/ajustar
antes de la entrega final, en particular las filas de la Parte 5
(Power BI, pendiente) y la Presentación.

| Criterio (puntaje máx.) | Pts máx. | Nivel | Evidencia (ubicación) | Pts estimados |
|---|---|---|---|---|
| P1 · Datos sintéticos reproducibles | 3 | E | `datos/generar_datos.py` (semillas fijas), `datos/data_dictionary.md` | 3 |
| P1 · Estadística descriptiva | 3 | E | `notebooks/01_estadistica.ipynb`, secc. 3 | 3 |
| P1 · Inferencia y pruebas de hipótesis | 4 | E | `notebooks/01_estadistica.ipynb`, secc. 6 (3 pruebas + supuestos) | 4 |
| P1 · Interpretación de negocio | 3 | E | `notebooks/01_estadistica.ipynb`, secc. 7-8 | 3 |
| P1 · Calidad del notebook | 2 | E | Ejecutado sin errores, 38 celdas, Markdown en cada sección | 2 |
| P2 · Retrospectivo y estacionalidad | 3 | E | `notebooks/02_descriptivo_diagnostico.ipynb`, secc. 1 | 3 |
| P2 · Identificación de patrones | 3 | E | `notebooks/02_descriptivo_diagnostico.ipynb`, secc. 2 (Pareto) | 3 |
| P2 · Segmentación RFM/clustering | 4 | E | `notebooks/02_descriptivo_diagnostico.ipynb`, secc. 3 (RFM + K-Means) | 4 |
| P2 · Análisis diagnóstico | 3 | E | `notebooks/02_descriptivo_diagnostico.ipynb`, secc. 4 (drill-down + descomposición Trujillo) | 3 |
| P2 · Calidad del notebook | 2 | E | Ejecutado sin errores, 35 celdas | 2 |
| P3 · Preparación y variables | 3 | E | `notebooks/03_predictivo.ipynb`, secc. 1.1 y 2.1 (anti-leakage) | 3 |
| P3 · Modelado predictivo | 5 | E | 2 problemas (regresión + clasificación), 4 modelos c/u | 5 |
| P3 · Evaluación de modelos | 5 | E | Validación cruzada temporal/estratificada, métricas completas | 5 |
| P3 · Técnicas avanzadas | 4 | E | GridSearchCV/RandomizedSearchCV, Random Forest, Gradient Boosting | 4 |
| P3 · Interpretabilidad y conclusiones | 3 | E | Feature importance + SHAP, conclusiones de negocio | 3 |
| P4 · Formulación del problema | 5 | E | `notebooks/04_prescriptivo.ipynb`, secc. 1 (formulación matemática completa) | 5 |
| P4 · Implementación y solución | 5 | E | PuLP + CBC, solución óptima verificada | 5 |
| P4 · Escenarios / sensibilidad | 4 | E | Escenarios NS y capacidad + precios sombra | 4 |
| P4 · Recomendaciones prescriptivas | 4 | E | Conectadas explícitamente con Partes 2 y 3 | 4 |
| P4 · Calidad del notebook | 2 | E | Ejecutado sin errores, 21 celdas | 2 |
| P5 · Modelo de datos y DAX | 4 | D | **Pendiente** — Power BI requiere Windows; se completará por separado | 0 |
| P5 · Diseño y claridad | 3 | D | **Pendiente** | 0 |
| P5 · Cobertura analítica | 4 | D | **Pendiente** | 0 |
| P5 · Interactividad | 2 | D | **Pendiente** | 0 |
| P5 · Storytelling y decisión | 2 | D | **Pendiente** | 0 |
| Bitácora · Registro de prompts | 2 | E | `docs/bitacora_prompts.md`, tabla completa | 2 |
| Bitácora · Prompt de datos detallado | 2 | E | `docs/bitacora_prompts.md`, Sección 7.2 | 2 |
| Bitácora · Validación crítica de la IA | 1 | E | `docs/bitacora_prompts.md`, errores detectados y corregidos documentados | 1 |
| Presentación · Claridad y estructura | 3 | D | **Pendiente** — preparar antes de la defensa oral | 0 |
| Presentación · Dominio y respuestas | 4 | D | **Pendiente** — depende del dominio real del equipo sobre el trabajo | 0 |
| Presentación · Participación del equipo | 3 | D | **Pendiente** — depende de la distribución real de roles del equipo | 0 |
| **TOTAL ESTIMADO (sobre 100)** | **100** | | | **75** |

## Cómo usar este cuadro

- El puntaje estimado de las **Partes 1-4 y la Bitácora (75 pts)** refleja
  el trabajo ya desarrollado y ejecutado sin errores en este repositorio.
- La **Parte 5 (15 pts)** está **pendiente**: requiere Microsoft Power BI
  (solo Windows). El modelo de datos (los 5 CSV en `datos/`) ya está listo
  para importar; falta construir el `.pbix` con las medidas DAX y las 3-4
  páginas de tablero exigidas.
- La **Presentación final (10 pts)** depende de la preparación real del
  equipo para la defensa oral y no puede autocompletarse.
- **Antes de entregar:** revisar cada fila marcada "Pendiente", completarla,
  y volver a calcular el total. Cualquier criterio en nivel Regular o
  Deficiente debe corregirse antes de la fecha límite.
