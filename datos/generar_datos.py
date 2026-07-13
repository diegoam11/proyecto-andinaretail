"""
Generador de datos sinteticos para AndinaRetail S.A.C.

Genera tiendas.csv, productos.csv, clientes.csv, ventas.csv e inventario.csv
en la carpeta datos/, con semillas fijas para reproducibilidad total.

Uso:
    python generar_datos.py
"""

import random
from datetime import date

import numpy as np
import pandas as pd
from faker import Faker

# ---------------------------------------------------------------------------
# 0. Reproducibilidad
# ---------------------------------------------------------------------------
SEED = 2026
np.random.seed(SEED)
random.seed(SEED)
# Nota: Faker no incluye el locale "es_PE" en esta version de la libreria.
# Se usa "es_CO" (espanol latinoamericano) como el mas cercano disponible para
# generar nombres; ciudades, distritos y demas atributos peruanos se definen
# manualmente mas abajo para mantener coherencia con el caso AndinaRetail.
fake = Faker("es_CO")
Faker.seed(SEED)
rng = np.random.default_rng(SEED)

OUT_DIR = "."  # el script se ejecuta desde datos/

FECHA_REF = date(2025, 12, 31)  # fecha de referencia para churn (inactividad)
MESES = pd.period_range("2023-01", "2025-12", freq="M")  # 36 periodos
N_MESES = len(MESES)

CIUDADES = ["Lima", "Arequipa", "Trujillo", "Cusco", "Piura"]
REGION_POR_CIUDAD = {
    "Lima": "Lima",
    "Arequipa": "Arequipa",
    "Trujillo": "La Libertad",
    "Cusco": "Cusco",
    "Piura": "Piura",
}
DISTRITOS_POR_CIUDAD = {
    "Lima": ["Miraflores", "San Isidro", "Surco", "Los Olivos", "San Juan de Lurigancho",
             "La Molina", "Comas", "Ate", "Villa El Salvador", "San Borja"],
    "Arequipa": ["Cercado", "Yanahuara", "Cayma", "Cerro Colorado", "Paucarpata"],
    "Trujillo": ["Trujillo Cercado", "La Esperanza", "El Porvenir", "Victor Larco", "Huanchaco"],
    "Cusco": ["Cusco Cercado", "Wanchaq", "San Sebastian", "Santiago", "San Jeronimo"],
    "Piura": ["Piura Cercado", "Castilla", "Veintiseis de Octubre", "Catacaos"],
}

CATEGORIAS = ["Abarrotes", "Bebidas", "Limpieza", "Cuidado Personal", "Electrohogar", "Hogar"]
SUBCATEGORIAS = {
    "Abarrotes": ["Arroz", "Menestras", "Aceites", "Fideos", "Azucar y sal", "Conservas", "Panaderia"],
    "Bebidas": ["Gaseosas", "Jugos", "Agua", "Cervezas", "Energizantes", "Cafe e infusiones"],
    "Limpieza": ["Detergentes", "Lejia", "Limpiadores de superficie", "Bolsas", "Papel higienico"],
    "Cuidado Personal": ["Shampoo", "Jabon", "Cuidado dental", "Desodorantes", "Cuidado facial"],
    "Electrohogar": ["Licuadoras", "Planchas", "Microondas", "Ventiladores", "Televisores", "Refrigeradoras"],
    "Hogar": ["Menaje de cocina", "Textiles de hogar", "Decoracion", "Organizadores", "Iluminacion"],
}
# Rango de precio_lista (S/) por categoria: (min, max)
RANGO_PRECIO = {
    "Abarrotes": (3, 35),
    "Bebidas": (2, 25),
    "Limpieza": (4, 40),
    "Cuidado Personal": (5, 45),
    "Electrohogar": (60, 1800),
    "Hogar": (10, 250),
}
MARCAS = [
    "Andina", "Sureña", "Costa Real", "Valle Norte", "Wari", "Inca Blanco", "Sol Peruano",
    "Kallpa", "Rimac Hogar", "Nortex", "Amauta", "Pacifico Home", "Cusco Natural",
    "Piurana", "Trujillana", "Limax", "MaxHogar", "Selecta", "Vital", "Frescor",
]

N_TIENDAS_FISICAS = {"Lima": 2, "Arequipa": 2, "Trujillo": 2, "Cusco": 1, "Piura": 1}  # + 1 virtual c/u
N_PRODUCTOS = 800
N_CLIENTES = 15000
TARGET_VENTAS = 250000

MISSING_FRAC = 0.02  # ~2%, dentro del rango 1-3% exigido


def inject_missing(df: pd.DataFrame, cols: list[str], frac: float = MISSING_FRAC) -> pd.DataFrame:
    """Introduce valores faltantes aleatorios (MCAR) en columnas no clave."""
    df = df.copy()
    n = len(df)
    for col in cols:
        mask = rng.random(n) < frac
        df.loc[mask, col] = np.nan
    return df


def random_dates(start: str, end: str, n: int) -> pd.Series:
    start_ts, end_ts = pd.Timestamp(start), pd.Timestamp(end)
    delta_days = (end_ts - start_ts).days
    offsets = rng.integers(0, delta_days + 1, size=n)
    return pd.to_datetime(start_ts) + pd.to_timedelta(offsets, unit="D")


# ---------------------------------------------------------------------------
# 1. tiendas.csv
# ---------------------------------------------------------------------------
def generar_tiendas() -> pd.DataFrame:
    filas = []
    tid = 1
    for ciudad in CIUDADES:
        n_fis = N_TIENDAS_FISICAS[ciudad]
        for i in range(n_fis):
            filas.append({
                "id_tienda": f"T{tid:03d}",
                "nombre": f"AndinaRetail {ciudad} {i + 1}",
                "ciudad": ciudad,
                "region": REGION_POR_CIUDAD[ciudad],
                "tipo": "Fisica",
                "area_m2": int(rng.integers(180, 900)),
                "fecha_apertura": random_dates("2015-01-01", "2022-12-31", 1)[0].date(),
            })
            tid += 1
        # una tienda virtual (centro de despacho e-commerce) por ciudad
        filas.append({
            "id_tienda": f"T{tid:03d}",
            "nombre": f"AndinaRetail Virtual {ciudad}",
            "ciudad": ciudad,
            "region": REGION_POR_CIUDAD[ciudad],
            "tipo": "Virtual",
            "area_m2": int(rng.integers(400, 1200)),  # centro logistico
            "fecha_apertura": random_dates("2019-01-01", "2022-12-31", 1)[0].date(),
        })
        tid += 1
    return pd.DataFrame(filas)


# ---------------------------------------------------------------------------
# 2. productos.csv
# ---------------------------------------------------------------------------
def generar_productos() -> pd.DataFrame:
    filas = []
    for i in range(1, N_PRODUCTOS + 1):
        categoria = CATEGORIAS[rng.integers(0, len(CATEGORIAS))]
        subcat = SUBCATEGORIAS[categoria][rng.integers(0, len(SUBCATEGORIAS[categoria]))]
        marca = MARCAS[rng.integers(0, len(MARCAS))]
        pmin, pmax = RANGO_PRECIO[categoria]
        # distribucion log-uniforme para reflejar variedad de precios dentro de la categoria
        precio_lista = round(float(np.exp(rng.uniform(np.log(pmin), np.log(pmax)))), 2)
        margen_costo = rng.uniform(0.60, 0.80)  # costo = 60%-80% del precio
        costo_unitario = round(precio_lista * margen_costo, 2)
        filas.append({
            "id_producto": f"P{i:04d}",
            "nombre": f"{subcat} {marca} {rng.integers(1, 999)}",
            "categoria": categoria,
            "subcategoria": subcat,
            "marca": marca,
            "precio_lista": precio_lista,
            "costo_unitario": costo_unitario,
            "fecha_alta": random_dates("2018-01-01", "2024-06-30", 1)[0].date(),
        })
    df = pd.DataFrame(filas)
    # Pareto: asignar peso de popularidad tipo Zipf a cada producto (fijo, reproducible)
    ranks = rng.permutation(len(df)) + 1
    df["peso_popularidad"] = 1.0 / np.power(ranks, 1.05)
    df["peso_popularidad"] /= df["peso_popularidad"].sum()
    return df


# ---------------------------------------------------------------------------
# 3. clientes.csv
# ---------------------------------------------------------------------------
def generar_clientes() -> pd.DataFrame:
    edades = rng.normal(38, 12, N_CLIENTES)
    edades = np.clip(edades, 18, 80).round().astype(int)
    generos = rng.choice(["Femenino", "Masculino"], size=N_CLIENTES, p=[0.52, 0.48])
    ciudades = rng.choice(CIUDADES, size=N_CLIENTES, p=[0.45, 0.16, 0.16, 0.14, 0.09])
    canal_pref = rng.choice(["Tienda", "Web", "App"], size=N_CLIENTES, p=[0.55, 0.20, 0.25])
    segmentos = rng.choice(
        ["Nuevo", "Regular", "Premium", "Ocasional"], size=N_CLIENTES, p=[0.20, 0.45, 0.15, 0.20]
    )
    fechas_registro = random_dates("2022-01-01", "2025-11-30", N_CLIENTES)

    filas = []
    for i in range(N_CLIENTES):
        ciudad = ciudades[i]
        distrito = DISTRITOS_POR_CIUDAD[ciudad][rng.integers(0, len(DISTRITOS_POR_CIUDAD[ciudad]))]
        nombre = fake.name_female() if generos[i] == "Femenino" else fake.name_male()
        filas.append({
            "id_cliente": f"C{i + 1:05d}",
            "nombre": nombre,
            "edad": edades[i],
            "genero": generos[i],
            "ciudad": ciudad,
            "distrito": distrito,
            "fecha_registro": fechas_registro[i].date(),
            "canal_preferido": canal_pref[i],
            "segmento": segmentos[i],
        })
    df = pd.DataFrame(filas)
    # Latente para churn: nivel de frecuencia de compra relativo por cliente
    df["_freq_level"] = rng.gamma(shape=2.0, scale=1.0, size=N_CLIENTES)
    return df


# ---------------------------------------------------------------------------
# 4. ventas.csv
# ---------------------------------------------------------------------------
def factor_estacional(mes_num: int) -> float:
    """Factor de estacionalidad: picos en julio (Fiestas Patrias) y diciembre (Navidad)."""
    if mes_num == 7:
        return 1.6
    if mes_num == 12:
        return 2.0
    if mes_num == 11:
        return 1.2  # previa navideña
    if mes_num in (1, 2):
        return 0.85  # temporada baja post-fiestas
    return 1.0


def generar_ventas(clientes: pd.DataFrame, tiendas: pd.DataFrame, productos: pd.DataFrame) -> pd.DataFrame:
    n_clientes = len(clientes)
    meses_num = np.array([p.month for p in MESES])
    meses_anio = np.array([p.year for p in MESES])

    seasonal = np.array([factor_estacional(m) for m in meses_num])  # (36,)
    freq_level = clientes["_freq_level"].to_numpy()  # (n_clientes,)

    # --- Churn: clientes que dejan de comprar antes de fin de periodo ---
    p_churn = np.clip(0.55 - 0.12 * freq_level, 0.08, 0.55)
    es_churner = rng.random(n_clientes) < p_churn
    # mes (indice 0-35) en que ocurre la ultima compra para los que "abandonan";
    # sesgado a ocurrir mas temprano cuanto menor es freq_level (mas inactivos = menos frecuentes)
    ultimo_mes_churner = rng.integers(5, 33, size=n_clientes)  # entre jun-2023 y sep-2025

    active_mask = np.ones((n_clientes, N_MESES), dtype=bool)
    for c in range(n_clientes):
        if es_churner[c]:
            active_mask[c, ultimo_mes_churner[c] + 1:] = False

    # --- Matriz de intensidad esperada de compra (cliente x mes) ---
    raw_lambda = np.outer(freq_level, seasonal) * active_mask
    base_rate = TARGET_VENTAS / raw_lambda.sum()
    lambda_matrix = raw_lambda * base_rate
    counts = rng.poisson(lambda_matrix)  # (n_clientes, 36)

    cliente_idx, mes_idx = np.nonzero(counts)
    reps = counts[cliente_idx, mes_idx]
    cliente_idx = np.repeat(cliente_idx, reps)
    mes_idx = np.repeat(mes_idx, reps)
    n = len(cliente_idx)

    id_cliente_arr = clientes["id_cliente"].to_numpy()[cliente_idx]
    ciudad_cliente_arr = clientes["ciudad"].to_numpy()[cliente_idx]
    canal_pref_arr = clientes["canal_preferido"].to_numpy()[cliente_idx]
    anio_arr = meses_anio[mes_idx]
    mesnum_arr = meses_num[mes_idx]

    # --- Fecha exacta dentro del mes ---
    dias_en_mes = pd.PeriodIndex(MESES[mes_idx]).days_in_month.to_numpy()
    dia_arr = rng.integers(1, dias_en_mes + 1)
    fecha_arr = pd.to_datetime({"year": anio_arr, "month": mesnum_arr, "day": dia_arr})

    # --- Canal: tendencia creciente del canal digital (20% en 2023 -> 45% en 2025) ---
    frac_anio = (anio_arr - 2023) + (mesnum_arr - 1) / 12.0
    prob_digital_base = 0.20 + (0.45 - 0.20) * (frac_anio / 3.0)
    boost_pref = np.where(np.isin(canal_pref_arr, ["Web", "App"]), 0.15, 0.0)
    prob_digital = np.clip(prob_digital_base + boost_pref, 0.05, 0.75)
    es_digital = rng.random(n) < prob_digital
    canal_arr = np.where(
        es_digital,
        rng.choice(["Web", "App"], size=n, p=[0.5, 0.5]),
        "Tienda",
    )

    # --- Tienda asignada segun ciudad del cliente y canal ---
    id_tienda_arr = np.empty(n, dtype=object)
    for ciudad in CIUDADES:
        tiendas_ciudad = tiendas[tiendas["ciudad"] == ciudad]
        fisicas = tiendas_ciudad[tiendas_ciudad["tipo"] == "Fisica"]["id_tienda"].to_numpy()
        virtual = tiendas_ciudad[tiendas_ciudad["tipo"] == "Virtual"]["id_tienda"].to_numpy()[0]

        mask_ciudad = ciudad_cliente_arr == ciudad
        mask_fis = mask_ciudad & (canal_arr == "Tienda")
        mask_virt = mask_ciudad & (canal_arr != "Tienda")

        id_tienda_arr[mask_fis] = rng.choice(fisicas, size=mask_fis.sum())
        id_tienda_arr[mask_virt] = virtual

    # --- Categoria por transaccion (con estacionalidad propia por categoria) ---
    cat_boost = {"Abarrotes": 7, "Bebidas": 7, "Electrohogar": 12, "Hogar": 12}  # meses de mayor boost
    categoria_arr = np.empty(n, dtype=object)
    for m in range(1, 13):
        mask_mes = mesnum_arr == m
        if not mask_mes.any():
            continue
        pesos = []
        for cat in CATEGORIAS:
            w = 1.0
            if cat_boost.get(cat) == m:
                w *= 1.8
            pesos.append(w)
        pesos = np.array(pesos) / np.sum(pesos)
        categoria_arr[mask_mes] = rng.choice(CATEGORIAS, size=mask_mes.sum(), p=pesos)

    # --- Producto dentro de categoria (peso Pareto/Zipf) ---
    id_producto_arr = np.empty(n, dtype=object)
    precio_lista_arr = np.empty(n, dtype=float)
    for cat in CATEGORIAS:
        prod_cat = productos[productos["categoria"] == cat]
        pesos = (prod_cat["peso_popularidad"] / prod_cat["peso_popularidad"].sum()).to_numpy()
        mask_cat = categoria_arr == cat
        n_cat = mask_cat.sum()
        elegidos = rng.choice(prod_cat.index.to_numpy(), size=n_cat, p=pesos)
        id_producto_arr[mask_cat] = productos.loc[elegidos, "id_producto"].to_numpy()
        precio_lista_arr[mask_cat] = productos.loc[elegidos, "precio_lista"].to_numpy()

    # --- Descuento: base + caida de margen en Trujillo desde 2025-Q2 ---
    tienda_ciudad_map = dict(zip(tiendas["id_tienda"], tiendas["ciudad"]))
    ciudad_tienda_arr = np.vectorize(tienda_ciudad_map.get)(id_tienda_arr)
    es_trujillo_post = (ciudad_tienda_arr == "Trujillo") & (fecha_arr >= pd.Timestamp("2025-04-01"))

    descuento_base = np.clip(rng.beta(2, 10, size=n) * 0.35, 0, 0.35)  # media ~10%
    descuento_trujillo = np.clip(rng.beta(3, 5, size=n) * 0.35, 0, 0.35)  # media ~22%
    descuento_pct = np.where(es_trujillo_post, descuento_trujillo, descuento_base)
    descuento_pct = np.round(descuento_pct, 3)

    # --- Precio unitario con pequeño ruido respecto al precio de lista ---
    precio_unitario = np.round(precio_lista_arr * rng.uniform(0.97, 1.03, size=n), 2)

    # --- Cantidad: sesgada a 1-2, con leve incremento por descuento ---
    cantidad_base = 1 + rng.poisson(0.6, size=n)
    cantidad = np.clip(np.round(cantidad_base * (1 + 0.4 * descuento_pct)), 1, 8).astype(int)

    monto_total = np.round(precio_unitario * cantidad * (1 - descuento_pct), 2)

    # --- Metodo de pago, condicionado al canal ---
    metodo_pago_arr = np.empty(n, dtype=object)
    mask_tienda = canal_arr == "Tienda"
    metodo_pago_arr[mask_tienda] = rng.choice(
        ["Efectivo", "Tarjeta debito", "Tarjeta credito", "Billetera digital"],
        size=mask_tienda.sum(), p=[0.35, 0.25, 0.20, 0.20],
    )
    metodo_pago_arr[~mask_tienda] = rng.choice(
        ["Tarjeta debito", "Tarjeta credito", "Billetera digital"],
        size=(~mask_tienda).sum(), p=[0.30, 0.35, 0.35],
    )

    df = pd.DataFrame({
        "id_venta": [f"V{ i +1:07d}" for i in range(n)],
        "fecha": fecha_arr,
        "id_cliente": id_cliente_arr,
        "id_tienda": id_tienda_arr,
        "id_producto": id_producto_arr,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "descuento_pct": descuento_pct,
        "monto_total": monto_total,
        "canal": canal_arr,
        "metodo_pago": metodo_pago_arr,
    })
    df = df.sort_values("fecha").reset_index(drop=True)
    df["id_venta"] = [f"V{i + 1:07d}" for i in range(len(df))]

    # --- Outliers controlados (~0.5%) ---
    idx_outliers = rng.choice(df.index, size=int(len(df) * 0.005), replace=False)
    factor_outlier = rng.uniform(5, 10, size=len(idx_outliers))
    df.loc[idx_outliers, "cantidad"] = np.clip(
        (df.loc[idx_outliers, "cantidad"] * factor_outlier).round(), 9, 40
    ).astype(int)
    df.loc[idx_outliers, "monto_total"] = np.round(
        df.loc[idx_outliers, "precio_unitario"] * df.loc[idx_outliers, "cantidad"]
        * (1 - df.loc[idx_outliers, "descuento_pct"]), 2
    )

    # --- Valores faltantes (1-3%) en columnas no clave ---
    df = inject_missing(df, ["descuento_pct", "metodo_pago", "cantidad"])
    return df


# ---------------------------------------------------------------------------
# 5. inventario.csv
# ---------------------------------------------------------------------------
def generar_inventario(tiendas: pd.DataFrame, productos: pd.DataFrame, ventas: pd.DataFrame) -> pd.DataFrame:
    # Cada tienda fisica stockea un subconjunto de productos; las virtuales, catalogo casi completo
    asignacion = {}
    for _, t in tiendas.iterrows():
        if t["tipo"] == "Fisica":
            n_surtido = rng.integers(150, 320)
        else:
            n_surtido = rng.integers(500, 800)
        surtido = rng.choice(productos["id_producto"].to_numpy(), size=n_surtido, replace=False)
        asignacion[t["id_tienda"]] = set(surtido)

    ventas_agg = ventas.copy()
    ventas_agg["periodo"] = ventas_agg["fecha"].dt.to_period("M").astype(str)
    ventas_mensuales = (
        ventas_agg.groupby(["id_producto", "id_tienda", "periodo"])["cantidad"]
        .sum(min_count=1).fillna(0).reset_index()
        .rename(columns={"cantidad": "unidades_vendidas"})
    )

    costo_base_categoria = {
        "Abarrotes": 0.8, "Bebidas": 0.9, "Limpieza": 0.7, "Cuidado Personal": 0.7,
        "Electrohogar": 4.5, "Hogar": 2.0,
    }
    prod_cat_map = dict(zip(productos["id_producto"], productos["categoria"]))
    tienda_ciudad_map = dict(zip(tiendas["id_tienda"], tiendas["ciudad"]))

    filas = []
    periodos_str = [str(p) for p in MESES]
    for _, t in tiendas.iterrows():
        tid = t["id_tienda"]
        productos_tienda = list(asignacion[tid])
        for periodo in periodos_str:
            sub = ventas_mensuales[
                (ventas_mensuales["id_tienda"] == tid) & (ventas_mensuales["periodo"] == periodo)
            ].set_index("id_producto")["unidades_vendidas"]
            for pid in productos_tienda:
                vendidas = int(sub.get(pid, 0))
                stock_inicial = int(max(vendidas * rng.uniform(1.2, 2.2), rng.integers(5, 40)))
                reabastecimiento = int(max(vendidas - stock_inicial + rng.integers(10, 60), 0))
                stock_final = max(stock_inicial + reabastecimiento - vendidas, 0)

                categoria = prod_cat_map[pid]
                costo_base = costo_base_categoria[categoria] * float(rng.uniform(0.85, 1.15))
                if tienda_ciudad_map[tid] == "Trujillo" and periodo >= "2025-04":
                    costo_base *= rng.uniform(1.4, 1.8)  # mayor costo de almacenamiento (caida de margen)

                filas.append({
                    "id_producto": pid,
                    "id_tienda": tid,
                    "periodo": periodo,
                    "stock_inicial": stock_inicial,
                    "unidades_vendidas": vendidas,
                    "reabastecimiento": reabastecimiento,
                    "stock_final": stock_final,
                    "costo_almacenamiento_unitario": round(costo_base, 2),
                })
    df = pd.DataFrame(filas)
    df = inject_missing(df, ["costo_almacenamiento_unitario"])
    return df


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Generando tiendas...")
    tiendas = generar_tiendas()

    print("Generando productos...")
    productos = generar_productos()

    print("Generando clientes...")
    clientes = generar_clientes()

    print("Generando ventas (puede tardar unos segundos)...")
    ventas = generar_ventas(clientes, tiendas, productos)

    print("Generando inventario...")
    inventario = generar_inventario(tiendas, productos, ventas)

    # Limpiar columnas auxiliares antes de exportar
    productos_out = productos.drop(columns=["peso_popularidad"])
    clientes_out = clientes.drop(columns=["_freq_level"])

    tiendas.to_csv(f"{OUT_DIR}/tiendas.csv", index=False)
    productos_out.to_csv(f"{OUT_DIR}/productos.csv", index=False)
    clientes_out.to_csv(f"{OUT_DIR}/clientes.csv", index=False)
    ventas.to_csv(f"{OUT_DIR}/ventas.csv", index=False)
    inventario.to_csv(f"{OUT_DIR}/inventario.csv", index=False)

    print("\nResumen de generacion:")
    print(f"  tiendas.csv    : {len(tiendas):,} filas")
    print(f"  productos.csv  : {len(productos_out):,} filas")
    print(f"  clientes.csv   : {len(clientes_out):,} filas")
    print(f"  ventas.csv     : {len(ventas):,} filas")
    print(f"  inventario.csv : {len(inventario):,} filas")
    print("\nListo. Archivos guardados en datos/.")


if __name__ == "__main__":
    main()
