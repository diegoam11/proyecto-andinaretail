# Parte 5 — Power BI

`andinaRetail.pbix` y su exportación `andinaRetail.pdf` (8 páginas),
exigidos en la Sección 6.5 del PG. Se construyó en un equipo con Windows
(Power BI Desktop es una aplicación exclusiva de esa plataforma) a partir
de los 5 CSV de `../datos/`.

Contenido del tablero:

1. **Modelo de datos:** relaciones entre `tiendas`, `productos`, `clientes`,
   `ventas` e `inventario`, con medidas DAX para los KPI clave (Ventas
   Totales, % Margen, Ticket Promedio, Clientes Activos, Tasa de
   Inactividad %, segmentación RFM y churn).
2. **8 páginas de tablero:** (1) ejecutivo con KPIs y ventas por
   mes/categoría/canal; (2)-(3) ventas por ciudad (mapa + drill-down);
   (4) diagnóstico de la caída de margen en Trujillo; (5)-(6) segmentación
   RFM y detalle de clientes con churn; (7) key influencers de churn +
   simulador what-if de descuento; (8) decomposition tree de ventas.
3. **Interactividad:** segmentadores (canal, ciudad, año), drill-down por
   AñoMes/AñoTrimestre, drill-through desde el mapa al detalle de ciudad,
   árbol de decomposición y parámetro what-if de descuento simulado.
4. **Storytelling:** la página de Trujillo incluye el hallazgo de negocio
   como texto explícito ("pierde ~7 pts de margen desde 2025-T2 por mayor
   descuento y costo de almacenamiento — acción: revisar política de
   descuentos"), conectado con el diagnóstico de `notebooks/02_descriptivo_diagnostico.ipynb`.
