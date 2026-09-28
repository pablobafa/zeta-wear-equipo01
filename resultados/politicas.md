# Políticas de gestión por celda de la matriz ABC × XYZ

Generado por `analisis/matriz.py` a partir de `resultados/clasificacion.csv`.
ABC por **margen anual**; XYZ por **CV mensual** (desviación muestral, umbrales 0,25 / 0,5).

## Recuento de la matriz

| | X (cv <= 0,25) | Y (0,25 < cv <= 0,5) | Z (cv > 0,5) |
|---|---|---|---|
| **A** | **3** | **3** | **0** |
| **B** | **3** | **1** | **4** |
| **C** | **1** | **1** | **4** |

Total: 20 referencias.

Celdas **vacías** (sin política, no hay a quién aplicársela): AZ.

> Que **AZ esté vacía es la mejor noticia del análisis**: ninguna referencia junta mucho margen con demanda errática, que es la combinación que obliga a poner un planificador dedicado. La atención humana se concentra entonces en la fila AY.

---

## AX — 3 referencias

`ZW-TEE-001`, `ZW-DEN-001`, `ZW-SAS-002`

- **Política:** Mucho valor y demanda predecible. Revisión continua (punto de pedido automático), nivel de servicio objetivo 98 %, lote fijo tipo EOQ y conteo cíclico mensual.
- **Quién decide:** Decide el SISTEMA: el reaprovisionamiento se automatiza de punta a punta y la persona solo ve las excepciones. Colchón pequeño, porque la previsión es fiable.

## AY — 3 referencias

`ZW-TEE-002`, `ZW-VES-002`, `ZW-DEN-002`

- **Política:** Mucho valor con variabilidad media. Revisión continua pero con previsión revisada cada mes, nivel de servicio 97-98 %, lote EOQ ajustado por campaña, conteo mensual.
- **Quién decide:** Decide el SISTEMA CON VISTO BUENO HUMANO: la propuesta la calcula la regla, pero un planificador la aprueba antes de lanzar. Colchón medio, dimensionado sobre la σ mensual.

## BX — 3 referencias

`ZW-ACC-004`, `ZW-ACC-001`, `ZW-TEE-003`

- **Política:** Valor medio y demanda estable. Revisión periódica mensual con punto de pedido, servicio 95 %, lote EOQ y conteo cíclico trimestral.
- **Quién decide:** Automatizable sin supervisión: es el caso más barato de gestionar de toda la matriz.

## BY — 1 referencia

`ZW-SAS-001`

- **Política:** Valor medio y variabilidad media. Revisión periódica mensual, servicio 93-95 %, colchón medio y conteo trimestral.
- **Quién decide:** Automatizable con alerta: la regla propone y solo salta a una persona si la desviación del mes supera el colchón previsto.

## BZ — 4 referencias

`ZW-VES-001`, `ZW-VES-003`, `ZW-CAZ-002`, `ZW-CAZ-001`

- **Política:** Valor medio y demanda errática (moda de temporada). Revisión periódica por campaña, no por calendario: servicio 90-93 %, compra en una o dos tandas y conteo trimestral.
- **Quién decide:** Decide una persona por TEMPORADA, no por SKU: no compensa un planificador dedicado, pero tampoco una regla automática. Gestión por surtido, con liquidación planificada.

## CX — 1 referencia

`ZW-ACC-002`

- **Política:** Poco valor y demanda estable: el caso ideal para no pensar. Revisión periódica trimestral, stock de seguridad generoso (es barato) y conteo anual.
- **Quién decide:** Totalmente automatizable: reponer por regla simple y no gastar análisis aquí.

## CY — 1 referencia

`ZW-PUN-001`

- **Política:** Poco valor, variabilidad media. Revisión periódica trimestral, lote grande para ahorrar pedidos, colchón holgado y conteo anual.
- **Quién decide:** Automatizable: el coste de equivocarse es bajo; el coste de analizarlo, no.

## CZ — 4 referencias

`ZW-ACC-003`, `ZW-PUN-002`, `ZW-DEN-003`, `ZW-SAS-003`

- **Política:** Poco valor y demanda errática. Revisión trimestral o bajo pedido, sin stock de seguridad dedicado, conteo anual y revisión de catálogo.
- **Quién decide:** Ni automatización fina ni persona: candidatas a reducir surtido, pasar a bajo pedido o descatalogar. Gastar análisis aquí es tan mal negocio como no gastarlo en AZ.
