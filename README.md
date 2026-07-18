# GRUPO DED - Proyecto Grupal — AndinaRetail S.A.C.

Analítica de Datos (código 2011104, Plan 2018) — E.P. Ingeniería de
Software, FISI, UNMSM. Ciclo 10 — Semestre 2026-1 — Docente: Mg. Juan
Gamarra Moreno.

Caso integrador: **AndinaRetail S.A.C.**, empresa ficticia de retail
omnicanal peruano (tiendas físicas + canal digital) en Lima, Arequipa,
Trujillo, Cusco y Piura. Todos los datos son sintéticos (ver
`datos/data_dictionary.md`).

## Integrantes y roles

> Completar con los datos reales del equipo antes de la entrega (mínimo 4,
> máximo 6 integrantes).

| Integrante | Rol |
|---|---|
| Diego Alvarez | Líder de proyecto / Data PM |
| Diego Alvarez | Ingeniero(a) de datos |
| Diego Linares | Analista estadístico / descriptivo |
| Diego Linares | Científico(a) de datos |
| Enzo Osorio | Analista de optimización / BI |

## Estructura del repositorio

```
proyecto-andinaretail/
├── requirements.txt
├── datos/
│   ├── generar_datos.py          # script reproducible (semilla 2026)
│   ├── data_dictionary.md
│   ├── tiendas.csv / productos.csv / clientes.csv / ventas.csv / inventario.csv
├── notebooks/
│   ├── 01_estadistica.ipynb              # Parte 1
│   ├── 02_descriptivo_diagnostico.ipynb  # Parte 2
│   ├── 03_predictivo.ipynb               # Parte 3
│   └── 04_prescriptivo.ipynb             # Parte 4
├── docs/
│   ├── bitacora_prompts.md
│   └── autoevaluacion.md
├── powerbi/       # Parte 5
│   ├── README.md
│   ├── andinaRetail.pbix
│   └── andinaRetail_tableros.pdf
├── presentacion/
│   └── AndinaRetail_Presentacion_Final.pdf
└── exposicion/
    ├── orden_exposicion.txt      
    └── enlace_video.txt          # enlace al video de la exposición grabada
```

## Cómo ejecutar el proyecto

```bash
# 1. Crear y activar el entorno virtual
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Generar los datos sintéticos (reproducible, semilla 2026)
cd datos && python generar_datos.py && cd ..

# 4. Abrir y ejecutar los notebooks en orden (01 -> 02 -> 03 -> 04)
jupyter lab notebooks/
```

Los notebooks ya están entregados **ejecutados** (con salidas visibles),
pero pueden volver a correrse de punta a punta sin errores siempre que
`datos/` contenga los CSV generados en el paso 3.

## Resumen de resultados clave

- **Parte 1:** se contrastaron 3 hipótesis (t-test canal, ANOVA ciudad,
  chi-cuadrado categoría-método de pago) con supuestos verificados; ninguna
  resultó significativa (p=0.373, p=0.677 y p=0.230 respectivamente), lo
  que indica un comportamiento homogéneo de ticket promedio entre canales y
  ciudades. Se añadió una cuarta prueba (ANOVA de ticket promedio por
  categoría) que sí resultó altamente significativa (p<0.0001, Electrohogar
  muy por encima del resto), respondiendo así la pregunta de negocio sobre
  diferencias por categoría. Se calcularon además intervalos de confianza
  para el ticket promedio y la tasa de churn.
- **Parte 2:** se confirmó estadísticamente la caída de margen en Trujillo
  desde 2025-Q2 (−6.73 p.p., explicada en −5.57 p.p. por mayor descuento y
  −1.17 p.p. por mayor costo de almacenamiento), y se segmentó a los
  clientes vía RFM y K-Means.
- **Parte 3:** el modelo de demanda (Gradient Boosting) alcanzó R²=0.90 en
  el conjunto de prueba (2025); el modelo de churn (Gradient Boosting)
  alcanzó AUC-ROC=0.91, con recencia y frecuencia como variables más
  influyentes (validado con SHAP).
- **Parte 4:** el modelo de reposición de inventario (PuLP) identificó 2 de
  8 tiendas físicas con capacidad efectivamente restrictiva (Lima-T002 y
  Cusco-T010), cuantificando el precio sombra de ampliar su capacidad y
  priorizando automáticamente los productos de mayor margen.

Ver el detalle completo, gráficos e interpretación de negocio en cada
notebook.
