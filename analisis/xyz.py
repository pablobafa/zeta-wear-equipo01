"""Encargo 2 - Clasificacion XYZ (coeficiente de variacion) de Zeta Wear.

Serie de referencia: la MENSUAL (datos/ex2_monthly_sales.csv, 12 meses de 2026).
NO se usa la serie diaria: los apuntes del curso (4.2) avisan de que el CV sobre
datos diarios sale inflado por los ceros y las roturas.

Desviacion tipica: MUESTRAL (n-1). Se declara aqui y en el PR. Motivo: los 12
meses son una muestra del comportamiento del articulo, no toda su historia, y es
el convenio con el que cuadran los CV publicados en los apuntes del curso
(camiseta basica 0,08 y vestido 0,72 -> ver auditoria/01_MUESTREO_MANUAL.md).
Con desviacion poblacional (n) solo cambiaria de clase ZW-CAZ-001 (0,4956 -> Y
en vez de 0,5176 -> Z); esa frontera esta documentada en el PR.

Umbrales del curso: X: cv <= 0,25 | Y: 0,25 < cv <= 0,5 | Z: cv > 0,5

Entrada : datos/ex2_monthly_sales.csv
Salida  : resultados/xyz.csv (sku, media_mensual, desv_tipica, cv, clase_xyz)
Solo biblioteca estandar.
"""
import csv
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRADA = os.path.join(RAIZ, "datos", "ex2_monthly_sales.csv")
SALIDA = os.path.join(RAIZ, "resultados", "xyz.csv")


def media(valores):
    return sum(valores) / len(valores)


def desv_muestral(valores):
    """Desviacion tipica muestral (n-1), sin importar statistics: stdlib pura."""
    n = len(valores)
    mu = media(valores)
    return (sum((v - mu) ** 2 for v in valores) / (n - 1)) ** 0.5


def clase(cv):
    if cv <= 0.25:
        return "X"
    if cv <= 0.5:
        return "Y"
    return "Z"


def main():
    with open(ENTRADA, newline="", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))

    meses = [c for c in filas[0].keys() if c != "sku"]

    salida = []
    for r in filas:
        # Los ceros mensuales (p. ej. ZW-DEN-003 en marzo) NO se excluyen: son
        # meses reales sin venta, y quitarlos seria limpiar sin justificacion.
        ventas = [float(r[m]) for m in meses]
        mu = media(ventas)
        sigma = desv_muestral(ventas)
        cv = round(sigma / mu, 4)
        salida.append({
            "sku": r["sku"],
            "media_mensual": round(mu, 2),
            "desv_tipica": round(sigma, 2),
            "cv": cv,
            # clase sobre el cv YA REDONDEADO que se publica, para que el CSV
            # sea autoconsistente para quien lo audite
            "clase_xyz": clase(cv),
        })

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["sku", "media_mensual", "desv_tipica", "cv", "clase_xyz"])
        w.writeheader()
        w.writerows(salida)

    reparto = {c: sum(1 for r in salida if r["clase_xyz"] == c) for c in "XYZ"}
    print(f"Meses usados: {len(meses)} ({meses[0]} .. {meses[-1]})")
    print(f"Reparto X/Y/Z: {reparto['X']}/{reparto['Y']}/{reparto['Z']} referencias")
    print(f"Escrito: {SALIDA}")


if __name__ == "__main__":
    main()
