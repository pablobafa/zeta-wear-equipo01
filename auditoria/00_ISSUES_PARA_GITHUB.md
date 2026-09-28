# Los 5 issues, listos para pegar en GitHub

La guía (paso 3.1) dice: *Issues → New issue → copiad tal cual el texto de
`encargos/NN-*.md`, título incluido*. Eso es el **cuerpo obligatorio**.

Debajo de cada uno añadimos un bloque **«Criterios de aceptación»**. No cambia el
encargo: lo hace verificable. La guía evalúa *«la calidad de los issues»*, y un
issue que no dice cómo se comprueba el resultado obliga a discutirlo después, en
el PR, cuando ya está escrito el código.

**Frase que se le añade SIEMPRE al agente** (paso 3.2 de la guía, literal):

> Trabaja en una rama nueva y abre un pull request. No toques nada fuera de lo
> que pide el encargo.

---

## Issue 1 — Encargo 1 · Clasificación ABC por margen

*(cuerpo: `encargos/01-abc-por-margen.md` tal cual)*

**Criterios de aceptación**
- [ ] El criterio de valor es **margen**, y está escrito en la descripción del PR. Ni cantidad, ni precio unitario, ni facturación.
- [ ] `resultados/abc.csv` tiene 20 filas y las 4 columnas pedidas.
- [ ] Ordenado de mayor a menor `margen_anual`; el último `pct_acumulado` es 100,00.
- [ ] Si se excluye o se limpia alguna fila, se declara en el PR. Sin declarar = se rechaza.
- [ ] Solo biblioteca estándar (sin pandas ni numpy).

## Issue 2 — Encargo 2 · Clasificación XYZ (coeficiente de variación)

*(cuerpo: `encargos/02-xyz-cv-mensual.md` tal cual)*

**Criterios de aceptación**
- [ ] El CV se calcula sobre `ex2_monthly_sales.csv` (**mensual**). Usar la serie diaria es motivo de rechazo directo.
- [ ] La descripción del PR declara si la desviación típica es **poblacional (n)** o **muestral (n−1)**.
- [ ] Los meses con venta 0 **no se eliminan**; si se eliminan, se declara y se justifica.
- [ ] Umbrales exactos: X ≤ 0,25 · Y hasta 0,5 · Z > 0,5.
- [ ] Se señalan las referencias fronterizas y a qué lado caen.

## Issue 3 — Encargo 3 · Matriz ABC×XYZ y políticas

*(cuerpo: `encargos/03-matriz-politicas.md` tal cual)*

**Criterios de aceptación**
- [ ] `clasificacion.csv` cruza por `sku`; si un SKU falta en uno de los dos ficheros, el script falla en vez de inventárselo.
- [ ] `celda` es la concatenación literal `clase_abc + clase_xyz`.
- [ ] `politicas.md` cubre **solo las celdas ocupadas**. Escribir una política para una celda vacía es relleno.
- [ ] Cada política dice algo sobre revisión, colchón y automatización.

## Issue 4 — Encargo 4 · KPIs adicionales para el comité

*(cuerpo: `encargos/04-kpis-adicionales.md` tal cual)*

**Criterios de aceptación**
- [ ] **Todo dato de partida existe en este repo.** Si un KPI necesita un dato que no está, el PR lo dice y no lo calcula.
- [ ] Ni «medias del sector», ni «benchmarks habituales», ni supuestos sin declarar.
- [ ] Si un indicador sale idéntico para las 20 referencias, hay que explicar por qué antes de aceptarlo.

> **Nota del equipo:** revisamos los datos antes de abrir este issue y creemos que
> ninguno de los dos KPIs es calculable con lo que hay (no existe columna de stock
> y la única serie con `stockout_flag` es de otra empresa y sin `sku`). Lo dejamos
> en el issue igualmente para ver qué hace el agente: si se lo inventa, ya sabemos
> qué buscar. Ver `resultados/kpis_LIMITACIONES.md`.

## Issue 5 — Encargo 5 · El escaparate (dashboard + Vercel)

*(cuerpo: `encargos/05-escaparate-vercel.md` tal cual)*

**Criterios de aceptación**
- [ ] `index.html` en la **raíz** del repo (si no, Vercel sirve el README).
- [ ] `fetch` con **ruta relativa** `resultados/clasificacion.csv`, sin barra inicial.
- [ ] Los recuentos se leen del CSV en tiempo de ejecución; **no se escriben a mano** en el HTML.
- [ ] La celda **AZ está vacía** en nuestros datos: el aviso tiene que comportarse bien con 0 referencias, no quedarse en blanco ni romper.
- [ ] Legible en móvil (375 px de ancho) y sin dependencias externas.
