# Bitácora de prompts — Proyecto Grupal AndinaRetail S.A.C.

Herramienta utilizada en todos los prompts: **Claude (Anthropic), vía Claude
Code**. Todas las salidas fueron ejecutadas, revisadas y validadas por el
equipo antes de incorporarlas al proyecto (ver columna "Salida y
validación" de cada fila); ningún resultado se copió sin verificación.

| ID | Parte | Objetivo del prompt | Prompt utilizado (resumen) | Herramienta/modelo | Salida y validación |
|---|---|---|---|---|---|
| P-01 | Datos | Generar el dataset sintético completo de AndinaRetail S.A.C. | Ver prompt completo en la Sección 2 de este documento. | Claude (Claude Code) | Script `generar_datos.py` ejecutado (5.2 s); se verificaron volúmenes (13 tiendas, 800 productos, 15,000 clientes, 249,892 ventas, 179,928 filas de inventario), % de faltantes (~2%) y los 4 patrones exigidos mediante `groupby`/`describe` manuales (estacionalidad, canal digital creciente, caída de margen en Trujillo desde 2025-Q2, correlación recencia-frecuencia para churn). Se corrigió manualmente un error (locale `es_PE` no disponible en la versión de Faker instalada; se sustituyó por `es_CO`, documentado en `data_dictionary.md`). |
| P-02 | Parte 1 | Construir el notebook de estadística descriptiva e inferencial siguiendo la Sección 6.1 del PG. | "Construye el notebook 01_estadistica.ipynb con: exploración inicial, estadística descriptiva (media/mediana/moda/desviación/asimetría/curtosis) para monto/edad/cantidad/precio, tablas de frecuencia y visualizaciones uni/bivariadas, correlaciones (descuento vs cantidad, precio vs cantidad), al menos 3 pruebas de hipótesis con supuestos verificados (t-test canal, ANOVA ciudad, chi-cuadrado categoría-método de pago) e intervalos de confianza para ticket promedio y tasa de churn, con celdas Markdown de objetivo/método/resultado/interpretación." | Claude (Claude Code) | Notebook ejecutado de punta a punta con `jupyter nbconvert --execute` (0 errores en 38 celdas). Se revisaron manualmente los resultados de las 3 pruebas de hipótesis y los intervalos de confianza para confirmar que fueran coherentes con los datos generados; se corrigió una expresión de código confusa en la celda de correlaciones antes de la ejecución final. |
| P-03 | Parte 2 | Construir el notebook descriptivo/diagnóstico: series de tiempo, Pareto 80/20, RFM + clustering, y diagnóstico de la caída de margen en Trujillo. | "Construye 02_descriptivo_diagnostico.ipynb con series de tiempo de ventas/margen por canal-ciudad-categoría, análisis de Pareto 80/20 para productos/clientes/categorías, segmentación RFM heurística y K-Means (con método del codo), y un diagnóstico de causa raíz de la caída de margen en Trujillo con drill-down mensual, comparación de cohortes trimestrales y descomposición de la variación en efecto descuento vs. efecto costo de almacenamiento." | Claude (Claude Code) | Notebook ejecutado sin errores (35 celdas). Se validó que la descomposición de la variación sumara exactamente el total (−6.73% = −5.57% + −1.17%) y que el heatmap de cohortes mostrara visualmente el deterioro de Trujillo únicamente desde 2025-Q2. |
| P-04 | Parte 3 | Diseñar y construir el pipeline de modelos predictivos (regresión de demanda y clasificación de churn) evitando fuga de información. | "Construye 03_predictivo.ipynb con dos problemas: (1) regresión de unidades vendidas por categoría-ciudad-mes con partición temporal train=2023-2024/test=2025 y TimeSeriesSplit; (2) clasificación de churn con fecha de corte de features en 2025-09-30 y target observado en la ventana 2025-10-01 a 2025-12-31 para evitar leakage. Entrena modelos base (lineal/logística, árbol) y avanzados (Random Forest, Gradient Boosting) con GridSearchCV/RandomizedSearchCV, compara con métricas estándar (MAE/RMSE/R²; accuracy/precision/recall/F1/AUC-ROC) e interpreta con feature importance y SHAP." | Claude (Claude Code) | Notebook ejecutado sin errores (32 celdas). Se revisaron las métricas finales (mejor modelo de regresión: Gradient Boosting, R²=0.903; mejor modelo de clasificación: Gradient Boosting, AUC-ROC=0.911) y se confirmó que las variables más importantes (recencia, frecuencia) coincidieran con el patrón de churn diseñado en los datos sintéticos, como control de sanidad del pipeline. |
| P-05 | Parte 4 | Formular y resolver el problema de optimización de reposición de inventario con PuLP, incluyendo análisis de sensibilidad. | "Construye 04_prescriptivo.ipynb con un modelo de programación lineal en PuLP para decidir cuántas unidades reponer por producto-tienda física, minimizando costo de almacenamiento + penalización por incumplir un stock de seguridad (nivel de servicio 95%), sujeto a la capacidad de cada tienda. Documenta la formulación matemática completa, resuelve con PULP_CBC_CMD, y agrega análisis de escenarios (variar nivel de servicio y capacidad) y precios sombra de la restricción de capacidad." | Claude (Claude Code) | Notebook ejecutado sin errores (21 celdas). Se detectó y corrigió un error real de la librería PuLP (`addConstraint` no retorna el objeto restricción; hubo que recuperarlo desde `prob.constraints[nombre]` tras resolver para poder leer el precio sombra `.pi`). Se recalibró el parámetro `FACTOR_DENSIDAD` (de 5 a 2 unidades/m²) tras detectar que con el valor inicial ninguna tienda quedaba restringida por capacidad (nivel de servicio 100% trivial), lo que anulaba el análisis de sensibilidad; con el valor recalibrado, 2 de 8 tiendas quedan efectivamente restringidas, generando precios sombra no nulos y una historia de negocio interpretable. |
| P-06 | Datos | Generar un diagrama entidad-relación (DBML) de los 5 datasets para documentar el modelo de datos en dbdiagram.io. | "Ayúdame creando un diagrama que muestre la relación de cada dataset y las columnas que tienen, me lo das en un formato donde yo pueda pegarlo en dbdiagram." | Claude (Claude Code) | Se inspeccionaron los encabezados reales de los 5 CSV en `datos/` (no se asumieron columnas) para construir el DBML de `clientes`, `tiendas`, `productos`, `ventas` e `inventario`, con `ventas` e `inventario` como tablas de hechos referenciando (`ref: >`) a las 3 dimensiones y clave compuesta (`id_producto`, `id_tienda`, `periodo`) en `inventario`. Se validó manualmente en dbdiagram.io; un primer intento de pegado del equipo duplicó el bloque completo (tablas `ventas`/`inventario` repetidas) y se corrigió indicando limpiar el editor antes de pegar de nuevo. |
| P-07 | Presentación | Estructurar y generar la presentación final (.pptx) de la defensa oral (12 min, 3 integrantes x 4 min), enfocada en objetivos y respuestas a las preguntas de negocio de cada parte. | "Tienes todo el contexto del proyecto, revísalo. Harás la presentación final en ppt. En mi grupo somos 3 integrantes y tenemos 4 minutos cada uno para exponer. Ayúdame a estructurar mi presentación, enfocada en los objetivos de cada parte y las respuestas a las preguntas de negocio." | Claude (Claude Code) | Se releyeron las celdas Markdown de objetivo/pregunta de negocio/conclusión de los 4 notebooks para extraer únicamente cifras y hallazgos ya validados (sin inventar datos nuevos), y se generó `presentacion/generar_presentacion.py` (python-pptx, reproducible) que produce `AndinaRetail_Presentacion_Final.pptx` (21 slides, 3 bloques de 4 min). Se verificó programáticamente la integridad del archivo (recuento de slides y títulos) al reabrirlo con python-pptx; queda pendiente una revisión visual del equipo en PowerPoint/Keynote (no se pudo renderizar a imagen en este entorno por falta de LibreOffice) y completar los nombres reales de los integrantes. |
| P-08 | Presentación | Rediseñar las 4 diapositivas de "Objetivo" como tarjetas visuales (en vez de bullets) y agregar los gráficos de los notebooks que respaldan cada afirmación ya presente en las diapositivas. | (1) "Coloca el objetivo, la pregunta y el método en 3 cuadros al centro. Usar bullets es un poco aburrido" (adjuntando captura de la diapositiva). (2) "Siento que faltan imágenes y gráficos [...] Agrega solo las imágenes que corresponden a lo que actualmente se menciona en las ppts." | Claude (Claude Code) | (1) Se añadió `objetivo_slide()` (3 tarjetas con círculo numerado, etiqueta y línea divisora) y se aplicó a las 4 diapositivas de Objetivo. (2) Se extrajeron las 25 imágenes de salida (PNG en base64) de los 4 notebooks ejecutados y se revisó cada una visualmente antes de asignarla, seleccionando solo las 8 que corresponden 1 a 1 con una afirmación ya escrita en una diapositiva (p. ej. el drill-down de margen de Trujillo, la curva ROC/matriz de confusión de churn, el nivel de servicio por tienda de la Parte 4); se descartaron el resto (~17) por no tener una mención textual correspondiente en el deck. Se implementó `nb_image()` para leer las imágenes directamente del `.ipynb` en tiempo de generación (sin duplicar binarios) y se verificó programáticamente que ninguna imagen excediera los límites de la diapositiva (máx. altura 7.5in). Pendiente: revisión visual final del equipo en PowerPoint (sin LibreOffice en este entorno para renderizar a imagen). |

## Prompt obligatorio de generación de datos sintéticos (Sección 7.2)

Prompt efectivamente utilizado para producir `datos/generar_datos.py` (adaptado
del ejemplo de referencia del PG; los cambios respecto al ejemplo se explican
al final):

```
Actúa como ingeniero de datos senior. Genera un único script de Python (3.12)
que use pandas, numpy y Faker (locale 'es_CO', el más cercano disponible a
'es_PE' en esta versión de la librería). Fija las semillas
numpy.random.seed(2026), random.seed(2026) y Faker.seed(2026) para
reproducibilidad. Crea los datos sintéticos de la empresa ficticia
'AndinaRetail S.A.C.' (retail omnicanal peruano con tiendas físicas y canal
digital) y expórtalos como CSV en la carpeta 'datos/'. Genera:

1) tiendas.csv (13 tiendas: 1-2 físicas + 1 virtual por cada una de las 5
   ciudades Lima, Arequipa, Trujillo, Cusco, Piura): id_tienda, nombre,
   ciudad, region, tipo (Fisica/Virtual), area_m2, fecha_apertura.
2) productos.csv (800): id_producto, nombre, categoria (Abarrotes, Bebidas,
   Limpieza, Cuidado Personal, Electrohogar, Hogar), subcategoria, marca,
   precio_lista, costo_unitario (60%-80% del precio), fecha_alta. Asignar un
   peso de popularidad tipo Zipf para habilitar un patrón de Pareto 80/20.
3) clientes.csv (15,000): id_cliente, nombre, edad (normal media 38, desv.
   12, truncada 18-80), genero, ciudad, distrito, fecha_registro
   (2022-2025), canal_preferido, segmento. Asignar un nivel de frecuencia de
   compra latente por cliente (gamma) para habilitar el patrón de churn.
4) ventas.csv (~250,000 líneas, 2023-01-01 a 2025-12-31): id_venta, fecha,
   id_cliente, id_tienda, id_producto, cantidad (1-8, sesgada a 1-2),
   precio_unitario, descuento_pct (0-35%), monto_total, canal
   (Tienda/Web/App), metodo_pago. Generar de forma vectorizada (matriz
   cliente x mes de intensidad esperada de compra vía Poisson) para que sea
   eficiente con 15,000 clientes y 36 meses.
5) inventario.csv (snapshot mensual por producto-tienda, restringido a un
   surtido parcial por tienda): id_producto, id_tienda, periodo (AAAA-MM),
   stock_inicial, unidades_vendidas (agregado real de ventas.csv),
   reabastecimiento, stock_final, costo_almacenamiento_unitario.

Incorpora estos patrones, verificables estadísticamente después de generar:
- Estacionalidad: picos en julio (factor x1.6) y diciembre (factor x2.0);
  crecimiento sostenido de la participación del canal digital (Web+App) de
  ~20% en 2023 a ~45% en 2025.
- Diagnóstico: desde 2025-04-01 (2025-Q2), las tiendas de Trujillo muestran
  mayor descuento_pct promedio y mayor costo_almacenamiento_unitario que el
  resto del país en el mismo periodo.
- Churn: un cliente se considera inactivo sin compras en los últimos 90 días
  al 2025-12-31; la probabilidad de inactividad debe depender negativamente
  de la frecuencia histórica de compra y positivamente de la antigüedad de
  la última compra, de forma que un modelo de clasificación pueda
  aprenderlo (correlación frecuencia-recencia negativa y clara).
- Demanda predecible: la cantidad vendida por categoría depende del mes,
  el canal y el descuento, con ruido aleatorio moderado (Poisson).
- Calidad de datos: entre 1% y 3% de valores faltantes (MCAR) en columnas no
  clave de ventas.csv e inventario.csv, y ~0.5% de outliers controlados en
  cantidad/monto_total.

Entrega además datos/data_dictionary.md describiendo cada tabla, campo, tipo
y dominio, documentando los patrones incorporados. Todos los nombres deben
ser ficticios; no uses datos reales.
```

**Adaptaciones realizadas por el equipo respecto al ejemplo de referencia
del PG:** cambio de locale `es_PE` → `es_CO` (no disponible en la versión de
Faker instalada, documentado en `data_dictionary.md`); implementación
vectorizada (matrices NumPy) en vez de generación fila por fila, necesaria
para producir 250,000 ventas en segundos en lugar de minutos; inclusión
explícita del peso Zipf en productos y la frecuencia latente Gamma en
clientes como mecanismos concretos para que los patrones de Pareto y churn
exigidos por la Sección 5.1 del PG fueran estadísticamente detectables (y no
solo declarados).

## Ejemplos de prompts adicionales por parte (Sección 7.3 del PG)

- **Parte 1:** "A partir de este DataFrame de ventas, propón tres hipótesis
  contrastables y el test estadístico adecuado para cada una, indicando los
  supuestos a verificar." → Usado para elegir t-test (canal), ANOVA
  (ciudad) y chi-cuadrado (categoría vs. método de pago).
- **Parte 2:** "Explica cómo construir una segmentación RFM en pandas y cómo
  interpretar cada segmento para un retail." → Usado para diseñar la
  función `etiquetar_segmento` y la caracterización de clusters K-Means.
- **Parte 3:** "Diseña un pipeline de scikit-learn para predecir churn con
  validación cruzada y comparación de Random Forest vs. Gradient Boosting,
  reportando AUC y F1." → Usado como base del `ColumnTransformer` +
  `Pipeline` + `GridSearchCV`/`RandomizedSearchCV` de la Parte 3.
- **Parte 4:** "Formula como programación lineal en PuLP el problema de
  reponer inventario minimizando costos con un nivel de servicio mínimo del
  95%." → Usado como base de la formulación matemática y el código PuLP de
  la Parte 4.

## Uso responsable

Todas las salidas generadas con IA fueron ejecutadas de punta a punta
(`jupyter nbconvert --execute`), revisadas celda por celda para verificar
ausencia de errores, y contrastadas contra chequeos de sanidad manuales
(valores de patrones esperados, coherencia de resultados de negocio) antes
de incorporarse al proyecto. Los dos errores de código detectados durante la
validación (locale de Faker no disponible; acceso incorrecto al precio
sombra en PuLP) se corrigieron manualmente y quedan documentados en la tabla
anterior como evidencia del proceso de revisión crítica.
