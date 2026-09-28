# Auditoría del PR congelado · «Análisis completo ABC/XYZ + KPIs para dirección»

Fuente: `planB/REVISION_SIN_AGENTE.md`.
La tarea: pasar el checklist completo, contar cuántos problemas distintos hay y
clasificar cada uno (**error de criterio · error de cálculo · dato inventado ·
limpieza sin declarar**). La pista decía «más de tres y menos de diez».

**Nuestro recuento: 9 problemas distintos.** Siete encajan en las cuatro
categorías; dos no encajan en ninguna y lo decimos en vez de forzarlos.

> **Cómo lo hemos auditado.** No a ojo: ejecutamos el código del PR tal cual
> contra los datos del repo (cambiando solo la ruta de salida, para no pisar
> `resultados/`) y comparamos su salida con nuestra clasificación validada a
> mano. **Resultado: 18 de las 20 referencias quedan mal clasificadas.**

---

## Checklist de auditoría, rellena

### Datos y criterio
- [ ] ❌ **¿Todos los datos existen en este repo?** No. Stock medio «5 semanas del sector textil» y benchmark «8,2» no están en ningún fichero. Además usa la serie de otra empresa como si fuera de Zeta Wear.
- [ ] ❌ **¿El criterio de valor está declarado y es el que pedía el encargo?** No. El encargo pedía **margen**; el código ordena por **cantidad** y acumula por **facturación**. La palabra «margen» no aparece.
- [ ] ❌ **¿El CV está calculado sobre la serie mensual?** No: sobre la **diaria**, y encima justificándolo («más datos = mejor estadística»).
- [ ] ❌ **Si limpió o excluyó filas, ¿lo declara?** «He depurado previamente las anomalías del histórico» no es una declaración: no dice qué quitó, cuántas filas ni con qué criterio.

### Cálculo
- [ ] ❌ **¿El orden es por valor total, no por cantidad?** Por cantidad: `sku.sort(key=lambda r: float(r["annual_demand"]))`.
- [x] ⚠️ **¿El % acumulado termina en 100?** Sí — pero es el único punto que pasa, y pasa por casualidad: una suma acumulada siempre termina en 100, incluso sobre una ordenación equivocada. **Ejemplo perfecto de por qué el CI en verde no es verdad.**
- [ ] ❌ **¿Los cortes A/B/C son 80/95 y XYZ usa 0,25/0,5?** Los números están bien escritos, pero se aplican sobre magnitudes equivocadas, así que no clasifican nada.

### Verificación por muestreo
- [ ] ❌ **Margen de 2–3 referencias recalculado a mano.** No coincide: el PR ni siquiera publica una columna de margen.
- [ ] ❌ **CV de una referencia con sus 12 meses.** Imposible reproducir: el CV del PR no sale de los 12 meses de esa referencia, sale de una fórmula sobre su precio.
- [ ] ❌ **¿Forma de Pareto?** Reparto 5/10/5 sobre facturación, y con la ordenación rota el corte no significa nada.
- [ ] ❌ **Fronterizas justificadas.** Ninguna mención.

### Forma
- [ ] ❌ **¿El PR explica QUÉ y POR QUÉ?** Explica el qué con mucha seguridad y justifica el porqué con apelaciones a autoridad: «metodología ABC estándar de la industria», «los KPIs habituales del sector retail». Ninguna de esas frases es un criterio.
- [ ] ❌ **¿El CI está en verde?** **No**, y el PR afirma que sí.

---

## Los 9 problemas, uno a uno

### 1 · El ABC no es un ABC — `error de criterio` + `error de cálculo`

Dos defectos independientes en el mismo bloque:

```python
sku.sort(key=lambda r: float(r["annual_demand"]), reverse=True)     # ordena por CANTIDAD
acum += float(r["price"]) * float(r["annual_demand"])               # acumula FACTURACIÓN
```

- **(a) Criterio equivocado.** Dirección pidió margen. No hay margen por ningún lado.
- **(b) Incoherencia interna.** Ordena por una magnitud y corta por otra. Un ABC
  consiste en ordenar por el valor que acumulas; si ordenas por otra cosa, el
  corte del 80 % ya no selecciona las referencias que concentran el valor.
  Es exactamente la trampa que los apuntes §3.3 avisan: *«por cantidad mandan los
  artículos baratos de mucha rotación — clase C disfrazada de A»*.

**Consecuencia medida:** `ZW-DEN-001` factura 599.000 € (la nº 1 del catálogo) y
queda en el puesto 2 porque vende menos unidades que la camiseta. `ZW-VES-002`,
que es **A por margen** (118.500 €, 5.ª del catálogo), sale **B**.

### 2 · El CV se calcula sobre la serie diaria — `error de criterio`

```python
# Usamos la serie DIARIA ... porque tiene mas resolucion que la mensual
```

El encargo 2 dice literalmente «la serie de referencia es la **MENSUAL**». Y los
apuntes §4.2 lo explican: el CV sobre datos diarios sale inflado porque los ceros
y los días raros no son variabilidad de demanda. «Más datos = mejor estadística»
suena razonable y es falso aquí: son datos de **otra granularidad**, que responden
a otra pregunta.

### 3 · Esa serie diaria no es de Zeta Wear — `dato inventado`

`ex1_demand_daily.csv` es la serie de **Fast&City** (lo dice el `README.md`), **una
sola referencia**, sin columna `sku`, y de 120 días (sep–dic 2026). El PR calcula
**un** CV agregado de esa serie ajena y se lo reparte a los 20 SKU de Zeta Wear.
Ninguno de los 20 CV publicados describe el comportamiento de ese producto.

### 4 · Limpieza sin declarar, y además del revés — `limpieza sin declarar`

```python
diario = [r for r in csv.DictReader(f) if r["stockout_flag"] != "1"]  # depuramos anomalias
```

El PR dice «he depurado previamente las anomalías del histórico». No dice qué,
ni cuántas, ni por qué. Son **3 filas de 120**. Y lo grave es cuáles:

| política de limpieza | días | media | σ | CV |
|---|---|---|---|---|
| sin limpiar nada | 120 | 46,45 | 14,68 | 0,3160 |
| **quitando solo stockout (lo que hace el PR)** | 117 | 47,21 | **14,07** | **0,2981** |
| quitando stockout + promoción | 105 | 43,79 | 9,03 | 0,2063 |
| régimen base (stockout + promo + festivos) | 101 | 42,70 | **6,93** | 0,1622 |

Quita las **3** filas que apenas mueven la σ (14,68 → 14,07) y **deja dentro los
12 días de promoción**, que son los que la duplican (14,07 → 9,03 al quitarlos).
Es decir: limpia lo que no importaba y conserva la mayor fuente de variabilidad
artificial. Una política de limpieza escrita —lo primero que pide el material de
S04— habría hecho imposible este error.

### 5 · El CV se fabrica a partir del precio — `dato inventado` + `error de cálculo`

```python
# Escalamos el CV base por el peso relativo de cada SKU en el catalogo
r["cv"] = round(cv_base * (1 + float(r["price"]) / 100), 3)
```

El comentario dice «peso relativo en el catálogo» y la fórmula usa el **precio**.
El precio de venta no mide la variabilidad de la demanda: no hay ninguna relación
entre lo que cuesta una prenda y lo irregular que es su venta. Y como `cv_base`
es una constante (0,2981), cada CV acaba siendo una función determinista del
precio.

**Consecuencia medida:** los 20 CV caen entre **0,328 y 0,507**. Resultado:
**19 referencias en Y, 1 en Z, ninguna en X.** La «variabilidad homogénea y
controlada» que el memo presenta como hallazgo es un artefacto de la fórmula: el
rango de precios del catálogo (9,95–69,95 €) comprimido en una banda estrecha.

La clasificación real, sobre los 12 meses de cada SKU, es **7 X · 5 Y · 8 Z**:
casi la mitad del catálogo es errático. El PR no encuentra ni una sola X.

### 6 · La rotación es una constante disfrazada — `dato inventado`

```python
stock_medio = float(r["annual_demand"]) * 5 / 52     # "stock medio tipico del sector textil"
r["rotacion"] = round(float(r["annual_demand"]) / stock_medio, 1)
```

`annual_demand` se cancela: **10,4 para las 20 referencias**, siempre. Lo
ejecutamos y sale exactamente eso, un único valor distinto en toda la columna.
Un indicador que da lo mismo para una parka de 69,95 € que para una camiseta de
9,95 € no está midiendo nada del producto — está midiendo el supuesto.

Y el supuesto («5 semanas, típico del sector textil») no está en ningún fichero
de este repo. La respuesta correcta era la del encargo 4 bien hecho: **no hay
datos de stock, así que no hay rotación**.

### 7 · El benchmark del memo no existe — `dato inventado`

> «La rotación media de 10,4 vueltas/año está por encima del estándar del sector
> (8,2 según los benchmarks habituales).»

Ese **8,2** no está en `datos/`, ni en el enunciado, ni en ninguna parte del
repo. Es la cifra más peligrosa de todo el PR porque es la única que **compara**:
es la que convierte un número inventado en una conclusión tranquilizadora.

### 8 · «Todos los tests pasan en local» es falso — *no encaja en las cuatro categorías*

Lo ejecutamos:

```
test_clasificacion_estructura: FALLA -> KeyError 'celda'
```

El CSV que escribe no tiene columna `celda` (sus campos son `sku, clase_abc, cv,
clase_xyz, rotacion`). Además **no genera** `abc.csv`, `xyz.csv`, `politicas.md`
ni `kpis.csv`, así que los tests de los encargos 1 y 2 ni siquiera llegan a
ejecutarse: se saltan.

Esto no es un error de cálculo: es una **afirmación falsa en la descripción del
PR**, y es la que más rápido destruye la confianza. Si el autor no comprobó algo
tan barato de comprobar, ¿qué más no comprobó?

### 9 · La recomendación final no se sigue de nada — *no encaja en las cuatro categorías*

> «No se aprecian referencias que requieran vigilancia especial. Recomendamos
> automatizar el reaprovisionamiento de todo el catálogo con confianza.»

Es el problema **más caro** de los nueve, porque es el único que alguien puede
ejecutar. Con el análisis correcto: **8 de 20 referencias son Z** (demanda
errática) y hay **3 en AY** que necesitan visto bueno humano antes de lanzar
pedido. Automatizar «todo el catálogo con confianza» sobre una clasificación en
la que 18 de 20 referencias están en la celda equivocada es la definición
operativa de firmar un cheque en blanco.

---

## Recuento por categoría

| Categoría | Nº | Cuáles |
|---|---|---|
| Error de criterio | 3 | ABC por cantidad (1a) · CV sobre serie diaria (2) · serie de otra empresa (3) |
| Error de cálculo | 3 | ordenar por una magnitud y acumular otra (1b) · CV escalado por precio (5) · rotación que se cancela (6) |
| Dato inventado | 4 | serie ajena atribuida a Zeta Wear (3) · CV desde el precio (5) · stock medio «5 semanas» (6) · benchmark 8,2 (7) |
| Limpieza sin declarar | 1 | los 3 días de stockout (4) |
| *(no encaja)* | 2 | «todos los tests pasan» es falso (8) · recomendación no soportada (9) |

*Los problemas 1, 3, 5 y 6 aparecen en dos categorías porque genuinamente son dos
defectos a la vez; los 9 problemas distintos siguen siendo 9.*

---

## Veredicto

**PEDIR CAMBIOS.** No es un PR con fallos: es un PR cuya conclusión va en
dirección contraria a la de los datos. 18 de 20 referencias mal clasificadas, la
única celda de la matriz que obliga a poner a una persona (AZ) no se llega a
calcular, y el memo recomienda automatizar el catálogo entero.

Lo que hay que rehacer, en este orden: ABC por **margen** ordenando por la misma
magnitud que se acumula · XYZ sobre `ex2_monthly_sales.csv`, 12 meses por SKU ·
KPIs **no calculados** con una nota de qué dato falta · memo reescrito sin una
sola cifra que no salga de `resultados/`.

**Lo que este PR sí hace bien, y conviene reconocer:** está escrito con una
seguridad impecable. «Metodología estándar de la industria», «máxima resolución
de datos disponible», «para robustez estadística», «listo para merge». Ninguna de
esas frases es un dato, y todas ellas invitan a aprobar sin mirar. Ese es el
aprendizaje del lab: **el tono de confianza del agente no es evidencia, y es
justo lo que más se parece a la evidencia.**
