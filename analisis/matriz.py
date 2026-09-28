"""Encargo 3 - Matriz ABC x XYZ y politica de gestion por celda ocupada.

Entradas : resultados/abc.csv y resultados/xyz.csv (encargos 1 y 2 ya mergeados)
Salidas  : resultados/clasificacion.csv (sku, clase_abc, cv, clase_xyz, celda)
           resultados/politicas.md      (politica por cada celda OCUPADA)

El orden del CSV se mantiene por margen descendente (el del encargo 1), para que
la primera fila siga siendo la referencia que mas dinero deja.
Solo biblioteca estandar.
"""
import csv
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(RAIZ, "resultados")

# Politica por celda: (revision, colchon, automatizacion / quien decide)
POLITICAS = {
    "AX": (
        "Mucho valor y demanda predecible. Revisión continua (punto de pedido automático), "
        "nivel de servicio objetivo 98 %, lote fijo tipo EOQ y conteo cíclico mensual.",
        "Decide el SISTEMA: el reaprovisionamiento se automatiza de punta a punta y la "
        "persona solo ve las excepciones. Colchón pequeño, porque la previsión es fiable.",
    ),
    "AY": (
        "Mucho valor con variabilidad media. Revisión continua pero con previsión revisada "
        "cada mes, nivel de servicio 97-98 %, lote EOQ ajustado por campaña, conteo mensual.",
        "Decide el SISTEMA CON VISTO BUENO HUMANO: la propuesta la calcula la regla, pero un "
        "planificador la aprueba antes de lanzar. Colchón medio, dimensionado sobre la σ mensual.",
    ),
    "AZ": (
        "Mucho valor y demanda errática: la celda que quita el sueño. Revisión periódica corta "
        "(semanal) con reunión de excepciones, servicio 95-97 %, lotes pequeños y frecuentes.",
        "Decide una PERSONA: aquí la previsión vale poco y automatizar a ciegas es caro en los dos "
        "sentidos (rotura de un artículo estrella o montaña de stock invendible).",
    ),
    "BX": (
        "Valor medio y demanda estable. Revisión periódica mensual con punto de pedido, "
        "servicio 95 %, lote EOQ y conteo cíclico trimestral.",
        "Automatizable sin supervisión: es el caso más barato de gestionar de toda la matriz.",
    ),
    "BY": (
        "Valor medio y variabilidad media. Revisión periódica mensual, servicio 93-95 %, "
        "colchón medio y conteo trimestral.",
        "Automatizable con alerta: la regla propone y solo salta a una persona si la desviación "
        "del mes supera el colchón previsto.",
    ),
    "BZ": (
        "Valor medio y demanda errática (moda de temporada). Revisión periódica por campaña, "
        "no por calendario: servicio 90-93 %, compra en una o dos tandas y conteo trimestral.",
        "Decide una persona por TEMPORADA, no por SKU: no compensa un planificador dedicado, "
        "pero tampoco una regla automática. Gestión por surtido, con liquidación planificada.",
    ),
    "CX": (
        "Poco valor y demanda estable: el caso ideal para no pensar. Revisión periódica "
        "trimestral, stock de seguridad generoso (es barato) y conteo anual.",
        "Totalmente automatizable: reponer por regla simple y no gastar análisis aquí.",
    ),
    "CY": (
        "Poco valor, variabilidad media. Revisión periódica trimestral, lote grande para "
        "ahorrar pedidos, colchón holgado y conteo anual.",
        "Automatizable: el coste de equivocarse es bajo; el coste de analizarlo, no.",
    ),
    "CZ": (
        "Poco valor y demanda errática. Revisión trimestral o bajo pedido, sin stock de "
        "seguridad dedicado, conteo anual y revisión de catálogo.",
        "Ni automatización fina ni persona: candidatas a reducir surtido, pasar a bajo pedido "
        "o descatalogar. Gastar análisis aquí es tan mal negocio como no gastarlo en AZ.",
    ),
}

ORDEN = ["AX", "AY", "AZ", "BX", "BY", "BZ", "CX", "CY", "CZ"]


def leer(nombre):
    with open(os.path.join(RES, nombre), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    abc = leer("abc.csv")
    xyz = {r["sku"]: r for r in leer("xyz.csv")}

    faltan = [r["sku"] for r in abc if r["sku"] not in xyz]
    if faltan:
        raise SystemExit(f"Estos SKU estan en abc.csv pero no en xyz.csv: {faltan}")

    salida = []
    for r in abc:  # conserva el orden por margen descendente
        x = xyz[r["sku"]]
        salida.append({
            "sku": r["sku"],
            "clase_abc": r["clase_abc"],
            "cv": x["cv"],
            "clase_xyz": x["clase_xyz"],
            "celda": r["clase_abc"] + x["clase_xyz"],
        })

    with open(os.path.join(RES, "clasificacion.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["sku", "clase_abc", "cv", "clase_xyz", "celda"])
        w.writeheader()
        w.writerows(salida)

    # --- politicas.md: SOLO las celdas ocupadas -----------------------------
    por_celda = {c: [r["sku"] for r in salida if r["celda"] == c] for c in ORDEN}
    ocupadas = [c for c in ORDEN if por_celda[c]]
    vacias = [c for c in ORDEN if not por_celda[c]]

    lineas = [
        "# Políticas de gestión por celda de la matriz ABC × XYZ",
        "",
        "Generado por `analisis/matriz.py` a partir de `resultados/clasificacion.csv`.",
        "ABC por **margen anual**; XYZ por **CV mensual** (desviación muestral, umbrales 0,25 / 0,5).",
        "",
        "## Recuento de la matriz",
        "",
        "| | X (cv <= 0,25) | Y (0,25 < cv <= 0,5) | Z (cv > 0,5) |",
        "|---|---|---|---|",
    ]
    for fila in "ABC":
        celdas = [f"**{len(por_celda[fila + col])}**" for col in "XYZ"]
        lineas.append(f"| **{fila}** | " + " | ".join(celdas) + " |")
    lineas += ["", f"Total: {len(salida)} referencias.", ""]

    if vacias:
        lineas += [
            f"Celdas **vacías** (sin política, no hay a quién aplicársela): {', '.join(vacias)}.",
            "",
        ]
        if "AZ" in vacias:
            lineas += [
                "> Que **AZ esté vacía es la mejor noticia del análisis**: ninguna referencia junta "
                "mucho margen con demanda errática, que es la combinación que obliga a poner un "
                "planificador dedicado. La atención humana se concentra entonces en la fila AY.",
                "",
            ]

    lineas += ["---", ""]
    for c in ocupadas:
        skus = por_celda[c]
        gestion, decisor = POLITICAS[c]
        lineas += [
            f"## {c} — {len(skus)} referencia{'s' if len(skus) != 1 else ''}",
            "",
            f"`{'`, `'.join(skus)}`",
            "",
            f"- **Política:** {gestion}",
            f"- **Quién decide:** {decisor}",
            "",
        ]

    with open(os.path.join(RES, "politicas.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print("Matriz (celda: n referencias):")
    for c in ORDEN:
        print(f"  {c}: {len(por_celda[c])}")
    print(f"Escrito: {os.path.join(RES, 'clasificacion.csv')}")
    print(f"Escrito: {os.path.join(RES, 'politicas.md')}")


if __name__ == "__main__":
    main()
