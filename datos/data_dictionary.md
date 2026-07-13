# Diccionario de datos — AndinaRetail S.A.C.

Todos los datos son **sintéticos**, generados con el script `generar_datos.py`
(pandas, numpy, Faker locale `es_CO`), con semilla fija `2026`
(`numpy.random.seed`, `random.seed`, `Faker.seed`). Ningún nombre, dirección o
identificador corresponde a personas o empresas reales.

> Nota de locale: la guía sugiere Faker `es_PE`, pero esta versión de la
> librería no incluye ese locale. Se usó `es_CO` (español latinoamericano) para
> generar nombres de clientes; las ciudades, distritos, categorías y demás
> atributos del negocio se definieron manualmente para reflejar el contexto
> peruano del caso (Lima, Arequipa, Trujillo, Cusco, Piura).

## 1. tiendas.csv (13 filas)

| Campo | Tipo | Dominio | Descripción |
|---|---|---|---|
| id_tienda | string | T001…T013 | Identificador único |
| nombre | string | — | Nombre comercial de la tienda |
| ciudad | string | Lima, Arequipa, Trujillo, Cusco, Piura | Ciudad de operación |
| region | string | Lima, Arequipa, La Libertad, Cusco, Piura | Región administrativa |
| tipo | string | Fisica, Virtual | Tienda física o centro de despacho e-commerce |
| area_m2 | int | 180–1200 | Área del local / centro logístico |
| fecha_apertura | date | 2015-01-01 a 2022-12-31 | Fecha de apertura |

Cada ciudad tiene 1–2 tiendas físicas y exactamente 1 tienda "Virtual" que
concentra las ventas del canal Web/App originadas por clientes de esa ciudad.

## 2. productos.csv (800 filas)

| Campo | Tipo | Dominio | Descripción |
|---|---|---|---|
| id_producto | string | P0001…P0800 | Identificador único |
| nombre | string | — | Nombre descriptivo (subcategoría + marca + código) |
| categoria | string | Abarrotes, Bebidas, Limpieza, Cuidado Personal, Electrohogar, Hogar | Categoría de catálogo |
| subcategoria | string | ver script | Subcategoría dentro de la categoría |
| marca | string | 20 marcas ficticias | Marca del producto |
| precio_lista | float | según categoría (S/ 2 – S/ 1800) | Precio de lista |
| costo_unitario | float | 60%–80% del precio_lista | Costo unitario |
| fecha_alta | date | 2018-01-01 a 2024-06-30 | Fecha de alta en catálogo |

**Patrón Pareto:** internamente cada producto recibe un peso de popularidad
tipo Zipf (no exportado) que determina su probabilidad de ser vendido, de
forma que ~20% de los productos concentran la mayor parte de las ventas
(a verificar y explotar en la Parte 2 — análisis 80/20).

## 3. clientes.csv (15 000 filas)

| Campo | Tipo | Dominio | Descripción |
|---|---|---|---|
| id_cliente | string | C00001…C15000 | Identificador único |
| nombre | string | — | Nombre completo (ficticio) |
| edad | int | 18–80 (Normal μ=38, σ=12, truncada) | Edad del cliente |
| genero | string | Femenino, Masculino | Género |
| ciudad | string | Lima (45%), Arequipa/Trujillo (16%), Cusco (14%), Piura (9%) | Ciudad de residencia |
| distrito | string | ver script | Distrito dentro de la ciudad |
| fecha_registro | date | 2022-01-01 a 2025-11-30 | Fecha de registro como cliente |
| canal_preferido | string | Tienda, Web, App | Canal declarado como preferido |
| segmento | string | Nuevo, Regular, Premium, Ocasional | Segmento comercial declarado (CRM); **no** confundir con el segmento RFM que se calcula analíticamente en la Parte 2 |

Cada cliente tiene además un nivel de frecuencia de compra latente (usado
solo internamente para simular ventas y churn, no exportado).

## 4. ventas.csv (~250 000 filas, 2023-01-01 a 2025-12-31)

| Campo | Tipo | Dominio | Descripción |
|---|---|---|---|
| id_venta | string | V0000001… | Identificador único de línea de venta |
| fecha | date | 2023-01-01 a 2025-12-31 | Fecha de la transacción |
| id_cliente | string | FK clientes | Cliente que compra |
| id_tienda | string | FK tiendas | Tienda/canal donde se registra la venta |
| id_producto | string | FK productos | Producto vendido |
| cantidad | int | 1–8 (sesgada a 1–2); outliers hasta 40 | Unidades vendidas en la línea |
| precio_unitario | float | ≈ precio_lista ± 3% | Precio unitario aplicado |
| descuento_pct | float | 0–0.35 | Descuento aplicado (fracción) |
| monto_total | float | — | precio_unitario × cantidad × (1 − descuento_pct) |
| canal | string | Tienda, Web, App | Canal de la transacción |
| metodo_pago | string | Efectivo, Tarjeta débito, Tarjeta crédito, Billetera digital | Medio de pago |

### Patrones incorporados (verificados tras la generación)

- **Estacionalidad:** ventas totales por mes muestran pico en julio
  (Fiestas Patrias, factor ×1.6) y el pico más alto en diciembre (Navidad,
  factor ×2.0); enero-febrero por debajo del promedio (factor ×0.85).
- **Canal digital creciente:** participación conjunta Web+App pasa de
  ~31% (2023) a ~48% (2025).
- **Caída de margen en Trujillo (desde 2025-Q2):** descuento promedio en
  Trujillo pasa de 5.8% (antes de abril 2025) a 13.0% (desde abril 2025),
  frente a 5.8% del resto del país en el mismo periodo posterior.
- **Demanda por categoría/mes/canal:** la categoría comprada en cada
  transacción depende de un peso estacional (p. ej. Electrohogar y Hogar con
  mayor probabilidad en diciembre), y la cantidad depende levemente del
  descuento aplicado, con ruido aleatorio moderado (Poisson).
- **Churn:** un cliente se considera inactivo si no registra compras en los
  90 días previos al 2025-12-31. Se verificó correlación negativa
  (r ≈ −0.55) entre frecuencia histórica de compra y recencia, y los
  clientes inactivos tienen una frecuencia promedio (8.4) muy inferior a la
  de los activos (24.6) — señal aprendible para un modelo de clasificación.
- **Calidad de datos:** ~2% de valores faltantes (MCAR) en `cantidad`,
  `descuento_pct` y `metodo_pago`; ~0.5% de outliers controlados en
  `cantidad`/`monto_total` (compras atípicamente grandes).

## 5. inventario.csv (~180 000 filas, snapshot mensual 2023-01 a 2025-12)

| Campo | Tipo | Dominio | Descripción |
|---|---|---|---|
| id_producto | string | FK productos | Producto |
| id_tienda | string | FK tiendas | Tienda |
| periodo | string | AAAA-MM | Mes del snapshot |
| stock_inicial | int | ≥0 | Stock al inicio del periodo |
| unidades_vendidas | int | ≥0 | Unidades vendidas ese periodo (agregado real de ventas.csv) |
| reabastecimiento | int | ≥0 | Unidades reabastecidas en el periodo |
| stock_final | int | ≥0 | stock_inicial + reabastecimiento − unidades_vendidas |
| costo_almacenamiento_unitario | float | por categoría, S/ | Costo unitario de almacenamiento del periodo |

No todas las combinaciones producto-tienda existen: cada tienda física tiene
un surtido de 150–320 productos y cada tienda virtual, de 500–800 (catálogo
casi completo).

**Patrón incorporado:** el costo de almacenamiento unitario en las tiendas de
Trujillo se incrementa entre 40% y 80% desde el periodo 2025-04 en adelante
(verificado: 1.65 → 2.64 en promedio, frente a 1.61 del resto del país en el
mismo periodo), reforzando junto con `ventas.csv` el patrón diagnóstico de
caída de margen en esa plaza.

## Trazabilidad

El prompt completo utilizado para generar `generar_datos.py` está registrado
en `docs/bitacora_prompts.md` (ID **P-01**), junto con las adaptaciones
manuales realizadas (p. ej. cambio de locale `es_PE` → `es_CO`).
