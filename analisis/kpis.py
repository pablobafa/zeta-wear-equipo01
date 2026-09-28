"""Encargo 4 - KPIs adicionales para el comite: rotacion anual y dias de rotura.

AVISO IMPORTANTE (leer antes de mergear)
----------------------------------------
Los dos KPIs que pide direccion NO SE PUEDEN CALCULAR con los datos que hay en
este repositorio. El script no se los inventa: emite "n/d" y el motivo.

1) Rotacion anual = demanda anual / STOCK MEDIO.
   `datos/ex2_sku_master.csv` trae sku, name, category, price, cost,
   lead_time_days y annual_demand. **No hay ninguna columna de stock.** Sin
   stock medio no hay rotacion; suponer un stock medio "tipico del sector"
   convierte el KPI en una constante inventada, no en una medida.

2) Dias con rotura de stock de cada SKU en 2026.
   El unico fichero con `stockout_flag` es `datos/ex1_demand_daily.csv`, y ese
   fichero: (a) NO tiene columna `sku` -- es UNA sola referencia; (b) es de
   **Fast&City**, otra cadena, no de Zeta Wear (ver README del repo); y (c)
   cubre 120 dias (2026-09-01 a 2026-12-29), no el ano 2026 completo.
   Repartir sus 3 dias de rotura entre los 20 SKU de Zeta Wear seria fabricar
   un dato.

Que haria falta para calcularlos de verdad (y este script los calcula solo en
cuanto aparezcan, sin tocar el codigo):
  - `datos/stock_medio.csv`     con columnas  sku, stock_medio_unidades
  - `datos/roturas_diarias.csv` con columnas  fecha, sku, stockout_flag

Entradas : datos/ex2_sku_master.csv (+ los dos opcionales de arriba)
Salida   : resultados/kpis.csv
Solo biblioteca estandar.
"""
import csv
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAT = os.path.join(RAIZ, "datos")
SALIDA = os.path.join(RAIZ, "resultados", "kpis.csv")

ANO = "2026"
NO_DISPONIBLE = "n/d"

MOTIVO_ROTACION = (
    "falta stock medio: ninguna columna de stock en datos/ (hace falta "
    "datos/stock_medio.csv con sku,stock_medio_unidades)"
)
MOTIVO_ROTURAS = (
    "falta historico de roturas por SKU: ex1_demand_daily.csv es una sola "
    "referencia de Fast&City (sin columna sku, 120 dias) -- hace falta "
    "datos/roturas_diarias.csv con fecha,sku,stockout_flag"
)


def cargar_opcional(nombre):
    ruta = os.path.join(DAT, nombre)
    if not os.path.exists(ruta):
        return None
    with open(ruta, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    with open(os.path.join(DAT, "ex2_sku_master.csv"), newline="", encoding="utf-8") as f:
        catalogo = list(csv.DictReader(f))

    stock = cargar_opcional("stock_medio.csv")
    stock_por_sku = (
        {r["sku"]: float(r["stock_medio_unidades"]) for r in stock} if stock else {}
    )

    roturas = cargar_opcional("roturas_diarias.csv")
    roturas_por_sku = {}
    if roturas:
        for r in roturas:
            if str(r.get("stockout_flag", "")).strip() == "1" and str(r.get("fecha", "")).startswith(ANO):
                roturas_por_sku[r["sku"]] = roturas_por_sku.get(r["sku"], 0) + 1

    filas = []
    for r in catalogo:
        demanda = float(r["annual_demand"])

        if r["sku"] in stock_por_sku and stock_por_sku[r["sku"]] > 0:
            rotacion = round(demanda / stock_por_sku[r["sku"]], 2)
            motivo_rot = ""
        else:
            rotacion = NO_DISPONIBLE
            motivo_rot = MOTIVO_ROTACION

        if roturas is not None:
            dias = roturas_por_sku.get(r["sku"], 0)
            motivo_dias = ""
        else:
            dias = NO_DISPONIBLE
            motivo_dias = MOTIVO_ROTURAS

        filas.append({
            "sku": r["sku"],
            "demanda_anual": int(demanda),
            "stock_medio_unidades": stock_por_sku.get(r["sku"], NO_DISPONIBLE),
            "rotacion_anual": rotacion,
            f"dias_rotura_{ANO}": dias,
            "motivo_si_nd": "; ".join(m for m in (motivo_rot, motivo_dias) if m),
        })

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    campos = ["sku", "demanda_anual", "stock_medio_unidades", "rotacion_anual",
              f"dias_rotura_{ANO}", "motivo_si_nd"]
    with open(SALIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(filas)

    pendientes = sum(1 for r in filas if r["rotacion_anual"] == NO_DISPONIBLE)
    print(f"Escrito: {SALIDA} ({len(filas)} referencias)")
    if pendientes:
        print("")
        print("  !! NO SE HA CALCULADO NINGUNA ROTACION NI NINGUN DIA DE ROTURA.")
        print("     El dato de partida no existe en este repositorio.")
        print("     Detalle y lo que haria falta: resultados/kpis_LIMITACIONES.md")


if __name__ == "__main__":
    main()
