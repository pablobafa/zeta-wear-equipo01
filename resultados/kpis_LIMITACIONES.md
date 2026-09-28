# Encargo 4 · Por qué `kpis.csv` va lleno de «n/d»

**Resumen en una línea:** los dos KPIs que pide dirección no se pueden calcular
con los datos de este repositorio, así que el script no los calcula. Ponerles un
número habría sido inventarlo.

---

## 1. Rotación anual = demanda anual / stock medio

`datos/ex2_sku_master.csv` tiene exactamente estas columnas:

```
sku, name, category, price, cost, lead_time_days, annual_demand
```

**No hay ninguna columna de stock.** Ni stock medio, ni stock inicial, ni
inventario final, ni existencias por fecha. Y no hay ningún otro fichero en
`datos/` que lo traiga.

El numerador (demanda anual) está; el denominador no existe. Cualquier número
que apareciese en la columna `rotacion_anual` vendría de un supuesto sobre el
stock medio, no de un dato de Zeta Wear.

> **Por qué esto importa más de lo que parece.** El PR congelado de
> `planB/REVISION_SIN_AGENTE.md` resuelve justo este hueco suponiendo «el stock
> medio típico del sector textil (5 semanas)». Al hacerlo,
> `rotacion = demanda / (demanda × 5/52)` = **52/5 = 10,4 para todas las
> referencias**, siempre, sea cual sea el SKU: un KPI que no distingue un
> producto de otro no es un KPI, es una constante disfrazada. Y esa constante es
> la que acaba en el memo como «10,4 vueltas/año, por encima del sector».

## 2. Días con rotura de stock de cada SKU en 2026

El único fichero del repo con una columna `stockout_flag` es
`datos/ex1_demand_daily.csv`, y no sirve para esto por tres motivos
independientes, cada uno suficiente por sí solo:

| | Problema | Comprobación |
|---|---|---|
| a | **No tiene columna `sku`.** Es UNA sola referencia, no 20. | Cabecera: `date, sales, price, promo_flag, holiday_flag, stockout_flag` |
| b | **No es de Zeta Wear.** Es la serie de **Fast&City**, otra cadena. | `README.md` del repo: «la serie diaria de Fast&City» |
| c | **No cubre 2026.** Son 120 días, del 2026-09-01 al 2026-12-29. | 120 filas; primera y última fecha del fichero |

En total ese fichero tiene **3 días** con `stockout_flag = 1`. Repartir 3 días de
otra empresa entre los 20 SKU de Zeta Wear —o asignárselos a todos— sería
fabricar el dato.

## 3. Qué haría falta, exactamente

`analisis/kpis.py` **ya está preparado**: en cuanto aparezcan estos ficheros los
lee y calcula los dos KPIs sin tocar una línea de código.

```
datos/stock_medio.csv       ->  sku, stock_medio_unidades
datos/roturas_diarias.csv   ->  fecha, sku, stockout_flag
```

Con `stock_medio.csv`: `rotacion_anual = annual_demand / stock_medio_unidades`.
Con `roturas_diarias.csv`: `dias_rotura_2026` = número de filas de ese SKU con
`stockout_flag = 1` y fecha que empiece por `2026`.

## 4. Si dirección quiere un número hoy

No lo metemos en `kpis.csv` para que nadie lo confunda con una medición, pero
esto es lo único que el repo permite estimar y con qué supuesto:

- **Cobertura de plazo** = `lead_time_days / 365`. Es el único dato temporal real
  que hay por SKU. Da una cota: una referencia con 60 días de plazo no puede
  rotar más de ~6 veces al año sin romper, por mucho que venda.
- Eso **no es la rotación**: es una cota superior teórica bajo el supuesto de que
  el stock medio equivale a la cobertura del plazo de entrega. Sirve para
  ordenar referencias entre sí, no para comparar con un sector.

Sin datos de inventario reales, la respuesta honesta al comité es: *«este
indicador nos lo tenéis que dar vosotros, o dadnos acceso al ERP; hoy no lo
tenemos»*. Pedirlo es más barato que un KPI inventado que luego dimensione
stocks.
