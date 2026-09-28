# Verificación por muestreo · nuestra verdad-terreno

> Esto es lo que exige la regla de oro de `GUIA_EQUIPO.md`: **recalcular a mano**
> una muestra antes de firmar nada. Todos los números de abajo salen de sumar,
> restar y dividir sobre los CSV de `datos/`, sin ejecutar el código del agente.
> Son reproducibles en una hoja de cálculo o en papel con calculadora.

---

## 0. Antes de mirar el PR: qué esperábamos ver

Apuntado **antes** de que el agente terminara (paso 3.4 de la guía):

- Forma de Pareto: entre 4 y 7 referencias en A. *(Si salen ~10, está mal ordenado
  — el checkpoint de los apuntes §3.3 dice literalmente que ~50 % en A = orden mal hecho.)*
- La camiseta básica `ZW-TEE-001` tiene que ser la nº 1 por margen: 60.000 u/año
  es la demanda más alta del catálogo con diferencia.
- `ZW-DEN-002` (vaquero wide leg) tiene que quedar **mal parado por margen**:
  cuesta 30,50 € y se vende a 35,95 €. Los apuntes §3.4 lo usan como ejemplo.

Las tres se cumplieron. Eso no valida el PR, pero si alguna hubiera fallado
habríamos sabido dónde mirar.

---

## 1. Margen anual de 3 referencias, a mano

Fórmula: `margen_anual = annual_demand × (price − cost)`

| SKU | price | cost | margen unitario | demanda | **margen anual** | `abc.csv` dice | ¿? |
|---|---|---|---|---|---|---|---|
| ZW-TEE-001 | 9,95 | 3,10 | 9,95 − 3,10 = **6,85** | 60.000 | 6,85 × 60.000 = **411.000,00 €** | 411000.0 | ✅ |
| ZW-DEN-002 | 35,95 | 30,50 | 35,95 − 30,50 = **5,45** | 8.000 | 5,45 × 8.000 = **43.600,00 €** | 43600.0 | ✅ |
| ZW-CAZ-001 | 45,95 | 17,90 | 45,95 − 17,90 = **28,05** | 900 | 28,05 × 900 = **25.245,00 €** | 25245.0 | ✅ |

**Margen total del catálogo (suma de los 20): 1.663.175,00 €.**
Lo hemos sumado aparte porque es el denominador de todos los porcentajes: si
está mal, los cortes A/B/C están mal aunque cada margen individual esté bien.

### % acumulado de esas mismas 3

| SKU | puesto | margen acumulado hasta él | % = acum / 1.663.175 | `abc.csv` | clase | ¿? |
|---|---|---|---|---|---|---|
| ZW-TEE-001 | 1.º | 411.000 | 24,71 % | 24.71 | A | ✅ |
| ZW-DEN-002 | 6.º | 1.316.350 | 79,15 % | 79.15 | A | ✅ |
| ZW-CAZ-001 | 14.º | 1.558.595 | 93,71 % | 93.71 | B | ✅ |

---

## 2. CV a mano de UNA referencia: `ZW-CAZ-001`

La elegimos a propósito: es **la fronteriza**. Sus 12 meses de 2026:

```
52, 71, 62, 75, 14, 123, 65, 116, 43, 78, 154, 47
```

**Media:** suma = 900 → 900 / 12 = **75,00 u/mes**

**Desviaciones respecto a la media y sus cuadrados:**

| mes | venta | x − 75 | (x − 75)² |
|---|---|---|---|
| 01 | 52 | −23 | 529 |
| 02 | 71 | −4 | 16 |
| 03 | 62 | −13 | 169 |
| 04 | 75 | 0 | 0 |
| 05 | 14 | −61 | 3.721 |
| 06 | 123 | +48 | 2.304 |
| 07 | 65 | −10 | 100 |
| 08 | 116 | +41 | 1.681 |
| 09 | 43 | −32 | 1.024 |
| 10 | 78 | +3 | 9 |
| 11 | 154 | +79 | 6.241 |
| 12 | 47 | −28 | 784 |
| | **900** | **0** | **16.578** |

**Y aquí está el hallazgo del muestreo:**

| convenio | varianza | desviación típica | CV = σ / 75 | clase |
|---|---|---|---|---|
| **Muestral (n−1)** | 16.578 / 11 = 1.507,09 | **38,82** | **0,5176** | **Z** |
| Poblacional (n) | 16.578 / 12 = 1.381,50 | 37,17 | 0,4956 | **Y** |

`xyz.csv` dice `38.82` y `0.5176` → **Z**. Coincide con el convenio muestral. ✅

### Por qué aceptamos el convenio muestral (y no es una decisión cómoda)

Es la **única** referencia de las 20 que cambia de clase según el convenio, y
cambia justo en el corte de 0,5. No vale con decir «el agente eligió uno».
Lo hemos anclado a los números publicados en los apuntes del curso (§4.2):

| El apunte dice | Con σ muestral sale | Con σ poblacional sale |
|---|---|---|
| «CV = 0,08 (camiseta básica)» → `ZW-TEE-001` | 0,0765 → **0,08** ✅ | 0,0732 → 0,07 ❌ |
| «CV = 0,72 (vestido…)» → `ZW-VES-001` | 0,7244 → **0,72** ✅ | 0,6935 → 0,69 ❌ |

Los dos CV que el curso imprime solo salen con la desviación **muestral**.

*Matiz honesto, por si lo pregunta el profesor:* el apunte llama a ese 0,72
«vestido de fiesta», que es el nombre de `ZW-VES-003`; pero `ZW-VES-003` da 0,64
muestral / 0,61 poblacional, y el 0,72 corresponde a `ZW-VES-001` (vestido midi
flores). Parece un lapsus de etiqueta en los apuntes: el **número** 0,72 solo
existe en este dataset bajo el convenio muestral, que es lo que estábamos
comprobando.

---

## 3. Segunda fronteriza, que casi se nos escapa: `ZW-ACC-002`

CV muestral = **0,2489**. El corte X/Y está en 0,25. Se queda en **X** por
**0,0011**.

- A 4 decimales (los que publica el CSV): 0,2489 ≤ 0,25 → X. Correcto.
- Pero redondeado a 2 decimales «0,25» — que es como aparecería en un informe —
  sigue siendo X por el «≤» del umbral. Se sostiene.
- **Con desviación poblacional daría 0,2383**, también X. Aquí el convenio no
  cambia nada, así que no hay debate: **X**, y lo dejamos escrito.

Lo anotamos porque un cambio pequeño en el dataset la movería de celda, y pasaría
de «automatizar y olvidarse» (CX) a «revisar con alerta» (CY).

---

## 4. Cruce de las celdas de nuestra muestra

| SKU | clase_abc (§1) | clase_xyz (§2) | celda esperada | `clasificacion.csv` | ¿? |
|---|---|---|---|---|---|
| ZW-TEE-001 | A | X (0,0765) | **AX** | AX | ✅ |
| ZW-DEN-002 | A | Y (0,3670) | **AY** | AY | ✅ |
| ZW-CAZ-001 | B | Z (0,5176) | **BZ** | BZ | ✅ |

---

## 5. Comprobación de integridad que no pedía el checklist (y que aporta)

Sumamos los 12 meses de cada SKU en `ex2_monthly_sales.csv` y lo comparamos con
su `annual_demand` en `ex2_sku_master.csv`:

**Los 20 cuadran exactamente.** (ZW-TEE-001: 60.000 = 60.000; ZW-CAZ-001:
900 = 900; …)

Esto nos dio confianza en que los dos ficheros describen el mismo catálogo y en
que nadie había tocado una fila. Si alguno hubiera descuadrado, el ABC (que usa
`annual_demand`) y el XYZ (que usa los meses) estarían hablando de productos
distintos sin avisar.

---

## 6. ¿Tiene forma de Pareto?

| clase | referencias | % del catálogo | % del margen |
|---|---|---|---|
| A | 6 | 30 % | **79,15 %** |
| B | 8 | 40 % | 14,56 % |
| C | 6 | 30 % | 6,29 % |

Sí: el 30 % de las referencias concentra casi el 80 % del margen. Ni «media clase
en A» ni un reparto plano. ✅

**Contraste externo:** los apuntes del curso (§3.4) dicen que `ZW-DEN-002` es
«4.º por facturación (287.600 €)» y que «por margen cae al 6.º puesto rozando la
frontera A/B». Nuestro resultado: 4.º por facturación con 8.000 × 35,95 =
**287.600 €**, y 6.º por margen con **79,15 %** acumulado, a 0,85 puntos del
corte de 80. Coincide al euro. Es la validación más fuerte que teníamos
disponible sin el solucionario.
