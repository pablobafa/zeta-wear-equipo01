"""Encargo 1 - Clasificacion ABC del catalogo Zeta Wear POR MARGEN.

Criterio de valor: MARGEN ANUAL = annual_demand * (price - cost).
Lo pide expresamente direccion (encargos/01-abc-por-margen.md): no se ordena
por cantidad ni por precio unitario ni por facturacion.

Cortes: A hasta el 80 % acumulado, B hasta el 95 %, C el resto. Un SKU entra
en A si SU porcentaje acumulado (una vez sumado el suyo) no pasa de 80.

Entrada : datos/ex2_sku_master.csv
Salida  : resultados/abc.csv  (sku, margen_anual, pct_acumulado, clase_abc)
Solo biblioteca estandar.
"""
import csv
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRADA = os.path.join(RAIZ, "datos", "ex2_sku_master.csv")
SALIDA = os.path.join(RAIZ, "resultados", "abc.csv")

CORTE_A = 80.0
CORTE_B = 95.0


def clase(pct_acumulado):
    if pct_acumulado <= CORTE_A:
        return "A"
    if pct_acumulado <= CORTE_B:
        return "B"
    return "C"


def main():
    with open(ENTRADA, newline="", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))

    # Ninguna fila se excluye ni se depura: el catalogo son 20 SKU y los 20 salen.
    for r in filas:
        r["margen_anual"] = float(r["annual_demand"]) * (float(r["price"]) - float(r["cost"]))

    total = sum(r["margen_anual"] for r in filas)
    filas.sort(key=lambda r: r["margen_anual"], reverse=True)

    acumulado = 0.0
    salida = []
    for r in filas:
        acumulado += r["margen_anual"]
        pct = round(100.0 * acumulado / total, 2)
        salida.append({
            "sku": r["sku"],
            "margen_anual": round(r["margen_anual"], 2),
            "pct_acumulado": pct,
            # se clasifica sobre el pct YA REDONDEADO que se publica en el CSV,
            # para que quien audite el fichero llegue a la misma clase que el script
            "clase_abc": clase(pct),
        })

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["sku", "margen_anual", "pct_acumulado", "clase_abc"])
        w.writeheader()
        w.writerows(salida)

    reparto = {c: sum(1 for r in salida if r["clase_abc"] == c) for c in "ABC"}
    margen_a = sum(r["margen_anual"] for r in salida if r["clase_abc"] == "A")
    print(f"Margen total del catalogo: {total:,.2f} EUR")
    print(f"Reparto A/B/C: {reparto['A']}/{reparto['B']}/{reparto['C']} referencias")
    print(f"La clase A concentra el {100 * margen_a / total:.2f} % del margen")
    print(f"Escrito: {SALIDA}")


if __name__ == "__main__":
    main()
