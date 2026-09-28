# Reviews de los 5 PR · checklist punto a punto y veredicto

> **Antes de copiar nada:** esto es la auditoría del código **que está ahora en
> este repo**. Si vuestro agente escribe otra cosa (y escribirá otra cosa), las
> casillas cambian. Usadlo como plantilla y como lista de dónde mirar, no como
> texto para pegar a ciegas: pegar una review que no corresponde al diff es
> exactamente el pecado que este lab enseña a no cometer.
>
> La verdad-terreno de todos los números está en `01_MUESTREO_MANUAL.md`.

---

## PR #1 — Encargo 1 · ABC por margen

**Descripción del PR (lo que debe declarar el autor):**
> Criterio de valor: **margen anual** = `annual_demand × (price − cost)`, porque
> es lo que pidió dirección: dónde se *gana* dinero, no dónde se factura.
> Cortes 80/95 sobre el % acumulado ya redondeado que se publica en el CSV, para
> que quien audite el fichero llegue a la misma clase. No se excluye ni se limpia
> ninguna fila: salen los 20 SKU.

### Datos y criterio
- [x] **Datos existentes en el repo** — única entrada `datos/ex2_sku_master.csv`. Ningún literal numérico ajeno en el script.
- [x] **Criterio de valor declarado y correcto** — margen, declarado en el docstring (`analisis/abc.py:3`) y en el PR.
- [ ] *(no aplica a este PR — el CV es del encargo 2)*
- [x] **No limpia ni excluye nada, y lo declara** — comentario en `analisis/abc.py:37`.

### Cálculo
- [x] **Orden por valor total, no por cantidad** — `filas.sort(key=... r["margen_anual"], reverse=True)`. Contraste: por cantidad la nº 2 sería ZW-DEN-001 igual, pero la nº 3 sería ZW-SAS-002 vs ZW-ACC-004… lo comprobamos y el orden por margen es el que sale.
- [x] **% acumulado termina en 100** — última fila `ZW-SAS-003 → 100.0`.
- [x] **Cortes 80/95** — `CORTE_A = 80.0`, `CORTE_B = 95.0`, constantes con nombre.

### Verificación por muestreo
- [x] **Margen de 3 referencias recalculado a mano** — ZW-TEE-001 411.000 €, ZW-DEN-002 43.600 €, ZW-CAZ-001 25.245 €. Los tres cuadran al céntimo.
- [x] **Forma de Pareto** — 6 refs (30 %) concentran el 79,15 % del margen. No hay «media clase en A».
- [x] **Fronterizas justificadas** — dos, y las dos merecen comentario (abajo).

### Comentarios en líneas concretas

**`resultados/abc.csv` línea 7 — `ZW-DEN-002,43600.0,79.15,A`**
> Esta es la frontera del PR. Entra en A con 79,15 % acumulado: le sobran
> **0,85 puntos**. Si el siguiente (ZW-ACC-004, 40.600 €) fuese un 6 % mayor, el
> corte caería antes y esta referencia sería B. Lo aceptamos porque la regla del
> encargo es «A hasta el 80 % acumulado» y 79,15 ≤ 80, pero queda anotado: es la
> referencia del catálogo cuya clase es menos estable.
> Contexto que refuerza la decisión: por **facturación** es la 4.ª (287.600 €) y
> por margen la 6.ª, porque su margen unitario es de 5,45 € sobre un PVP de
> 35,95 €. Gestionarla como A por ventas sobreinvertiría colchón en una
> referencia que apenas deja dinero.

**`resultados/abc.csv` línea 16 — `ZW-PUN-001,24975.0,95.21,C`**
> La otra frontera, y esta duele más: se queda fuera de B por **0,21 puntos**.
> 24.975 € de margen frente a los 25.245 € de ZW-CAZ-001, que sí es B. Una
> diferencia del 1 % en margen la cambia de política de gestión. Aceptamos la
> regla literal (95,21 > 95 → C), pero si alguien la gestiona como B tampoco
> estaría cometiendo un error material, y conviene que dirección lo sepa.

**`analisis/abc.py:55` — `"clase_abc": clase(pct)`**
> Nos gusta que clasifique sobre el `pct` **ya redondeado** y no sobre el float
> completo: así, quien abra `abc.csv` y aplique la regla a mano obtiene la misma
> clase que el script. Es una decisión pequeña que hace el fichero auditable.
> Con estos datos ninguna referencia cae lo bastante cerca del corte como para
> que las dos formas difieran, pero la propiedad se sostiene igual.

### Forma
- [x] El PR explica qué hizo y por qué.
- [x] CI en verde (4/4 comprobaciones). *Recordatorio: verde = forma correcta, no verdad.*

**Veredicto: APROBAR y mergear.** El criterio es el que pidió dirección, el orden
y los cortes son correctos, y nuestra muestra de 3 referencias cuadra al céntimo
contra un total de margen (1.663.175 €) que recalculamos aparte. Las dos
fronterizas quedan documentadas arriba.

---

## PR #2 — Encargo 2 · XYZ por CV mensual

**Descripción del PR (lo que debe declarar el autor):**
> CV sobre la serie **mensual** (12 meses de 2026). Desviación típica
> **muestral (n−1)**, declarada. Umbrales 0,25 / 0,5. Los meses con venta 0 no se
> eliminan. Fronteriza: ZW-CAZ-001.

### Datos y criterio
- [x] **Datos existentes en el repo** — única entrada `datos/ex2_monthly_sales.csv`.
- [x] **Criterio declarado** — CV = σ / μ, con el convenio de σ escrito.
- [x] **CV sobre la serie MENSUAL, no la diaria** — `ENTRADA = .../ex2_monthly_sales.csv` (`analisis/xyz.py:24`). *Este es el punto 3 del checklist, el que la guía marca «con especial cariño»: la trampa natural es usar `ex1_demand_daily.csv` porque «tiene más datos».*
- [x] **No limpia ni excluye, y lo declara** — comentario explícito en `analisis/xyz.py:55` sobre los ceros mensuales.

### Cálculo
- [x] **Umbrales 0,25 / 0,5** — función `clase()`, con `<=` en los dos cortes, igual que la tabla de los apuntes.
- [x] Reparto X/Y/Z = 7/5/8, suma 20.

### Verificación por muestreo
- [x] **CV de una referencia recalculado a mano** — ZW-CAZ-001: media 75,00, Σ(x−μ)² = 16.578, σ muestral = 38,82, CV = **0,5176** → Z. Coincide con el CSV.
- [x] **Fronteriza identificada y defendida** — ver comentario abajo.

### Comentarios en líneas concretas

**`analisis/xyz.py:32` — `def desv_muestral(valores)`**
> **El punto que había que cazar en este PR.** ZW-CAZ-001 da CV = 0,5176 con
> desviación muestral (n−1) → **Z**, y 0,4956 con poblacional (n) → **Y**. Es la
> única de las 20 que cambia de clase según el convenio, y cambia justo sobre el
> corte de 0,5. Que el PR *declare* el convenio no basta: hay que justificar
> **cuál** y por qué.
>
> Lo hemos resuelto anclándolo a los CV que publican los apuntes del curso
> (§4.2): «camiseta básica 0,08» y «vestido 0,72». Con σ muestral salen 0,0765 →
> 0,08 y 0,7244 → 0,72. Con σ poblacional saldrían 0,07 y 0,69, que no aparecen
> en ningún sitio. El convenio del curso es el **muestral**, así que ZW-CAZ-001
> es **Z**. Detalle completo en `auditoria/01_MUESTREO_MANUAL.md` §2.
>
> Consecuencia práctica, que es lo que importa: como Z pasa a gestionarse por
> campaña con compra en una o dos tandas; como Y iría a revisión mensual
> automatizable con alerta. No es un matiz decorativo.

**`resultados/xyz.csv` — `ZW-ACC-002,100.0,24.89,0.2489,X`**
> Segunda fronteriza, y esta casi se nos escapa porque no cambia con el convenio:
> 0,2489 contra un corte de 0,25. Se queda X por **0,0011**. Aquí sí estamos
> tranquilos (con σ poblacional daría 0,2383, también X), pero lo dejamos escrito
> porque mueve la referencia entre CX («automatizar y olvidarse») y CY («revisar
> con alerta»).

**`analisis/xyz.py:36` — `(sum((v - mu) ** 2 for v in valores) / (n - 1)) ** 0.5`**
> Implementa la desviación a mano en vez de importar `statistics.stdev`. El
> encargo pide solo biblioteca estándar y `statistics` **lo es**, así que no era
> obligatorio. Lo damos por bueno —es auditable línea a línea y equivale
> exactamente a lo que recalculamos en la tabla— pero no lo tomamos como mérito.

### Forma
- [x] El PR explica qué hizo y por qué.
- [x] CI en verde. Ojo: el test `test_xyz_estructura` solo comprueba que la clase sea coherente con el CV **que el propio fichero publica**. Si el CV estuviera mal calculado, el test seguiría en verde. La verdad la puso nuestra tabla de 12 filas.

**Veredicto: APROBAR y mergear**, una vez aclarado el convenio de σ. Sin esa
aclaración habría sido **PEDIR CAMBIOS**: un PR que dice «uso desviación
muestral» sin justificar por qué está dejando sin decidir la clase de una
referencia.

---

## PR #3 — Encargo 3 · Matriz y políticas

### Datos y criterio
- [x] **Solo usa `abc.csv` y `xyz.csv`** — no vuelve a `datos/`, así que no puede contradecir a los encargos 1 y 2.
- [x] **Falla en vez de inventar** — `analisis/matriz.py:86`: si un SKU está en `abc.csv` y no en `xyz.csv`, corta con `SystemExit` y dice cuál. Un `.get()` silencioso aquí habría dejado celdas vacías sin que nadie se enterase.

### Cálculo
- [x] `celda = clase_abc + clase_xyz`, concatenación literal.
- [x] Recuento: AX 3 · AY 3 · AZ 0 · BX 3 · BY 1 · BZ 4 · CX 1 · CY 1 · CZ 4 = **20**.
- [x] **Cruce a mano de nuestra muestra** — ZW-TEE-001 → AX, ZW-DEN-002 → AY, ZW-CAZ-001 → BZ. Los tres coinciden.

### Comentarios en líneas concretas

**`resultados/politicas.md` — celdas vacías**
> Bien resuelto: `politicas.md` escribe política **solo para las 8 celdas
> ocupadas** y lista AZ aparte como vacía. El encargo pedía «una política por
> cada celda ocupada»; rellenar las 9 habría sido cumplir de más y decir de
> menos.

**El hallazgo de fondo: AZ está vacía, y eso es la noticia**
> Ninguna referencia junta mucho margen con demanda errática. Es literalmente la
> celda que los apuntes (§5) llaman «la que quita el sueño», y en Zeta Wear no
> hay nadie. Consecuencia para dirección: **no hace falta un planificador
> dedicado**, y la atención humana se concentra en las 3 de AY.
> Comprobamos además que esta conclusión **no depende del convenio de σ**: con
> desviación poblacional, ZW-CAZ-001 pasaría de BZ a BY y AZ seguiría vacía. Es
> una conclusión robusta, y por eso nos atrevemos a ponerla en el memo.

**`analisis/matriz.py` — diccionario `POLITICAS`**
> Las políticas están escritas a mano en el código, no generadas. Correcto: son
> criterio de gestión, no un cálculo. Lo que sí hace el script es decidir **a
> quién se le aplican**, leyendo las celdas ocupadas del CSV. Si mañana cambia la
> clasificación, `politicas.md` se regenera solo y no queda desincronizado.

### Forma
- [x] CI en verde (`test_clasificacion_estructura`).

**Veredicto: APROBAR y mergear.**

---

## PR #4 — Encargo 4 · KPIs para el comité

> La guía avisa: *«Pasad el checklist ENTERO antes de opinar. Entero.»* Con razón:
> **este encargo pide dos KPIs que no se pueden calcular con los datos del repo.**

### Datos y criterio
- [x] **¿Todos los datos existen en el repo?** — **NO, y el PR lo dice.** Es justamente el punto: `rotacion_anual` necesita stock medio, y en `datos/` no hay ninguna columna de stock. `dias_rotura_2026` necesita roturas por SKU, y el único fichero con `stockout_flag` (`ex1_demand_daily.csv`) no tiene columna `sku`, es de **Fast&City** (otra empresa) y cubre 120 días, no el año.
- [x] **Declara lo que no hace** — `resultados/kpis.csv` lleva `n/d` y una columna `motivo_si_nd` en cada fila; el detalle está en `resultados/kpis_LIMITACIONES.md`.
- [x] **No hay supuestos encubiertos** — ni «media del sector», ni «5 semanas de cobertura», ni benchmarks.

### Cálculo
- [x] Lo único que se publica calculado es `demanda_anual`, que sí está en el repo.
- [x] El script deja preparado el cálculo real: si aparecen `datos/stock_medio.csv` y `datos/roturas_diarias.csv`, calcula los dos KPIs sin tocar código.

### Comentario principal

**`resultados/kpis.csv` — columna `rotacion_anual` = `n/d`**
> Un `n/d` justificado vale más que un número inventado, y aquí hay una prueba
> concreta de lo que pasa cuando se hace lo contrario. El PR congelado de
> `planB/` resuelve este mismo hueco suponiendo «stock medio típico del sector
> textil (5 semanas)»:
>
> ```
> stock_medio = annual_demand * 5 / 52
> rotacion    = annual_demand / stock_medio   =  52/5  =  10,4
> ```
>
> `annual_demand` se cancela: **sale 10,4 para las 20 referencias**, siempre, sea
> cual sea el producto. Un indicador que no distingue una parka de una camiseta
> no mide nada — y es el número que acaba en el memo como «10,4 vueltas/año, por
> encima del estándar del sector».
>
> Petición al comité: o nos dan el inventario medio (o acceso al ERP), o este KPI
> no existe. Pedirlo hoy es más barato que dimensionar stocks con una constante.

**Veredicto: APROBAR y mergear**, precisamente **porque no calcula los KPIs**.
La regla 4 del `README.md` dice que usar un dato que no existe es motivo de
rechazo; este PR hace lo contrario: lo detecta, lo documenta y deja el cálculo
listo para cuando llegue el dato.

---

## PR #5 — Encargo 5 · El escaparate

### Datos y criterio
- [x] **Los recuentos salen del CSV, no del HTML** — lo comprobamos de la única forma que vale: mirando si algún número está escrito en el fichero. No lo está; todo se construye en `pintar(filas)` a partir del `fetch`.
- [x] **Sin dependencias externas** — un solo `index.html`, cero `<script src=...>`, cero `<link>` a CDN.
- [x] **Ruta relativa** — `var FUENTE = 'resultados/clasificacion.csv'`, sin barra inicial. Con barra inicial funciona en Vercel y falla en cualquier subcarpeta.

### Cálculo / comportamiento
- [x] **Matriz 3×3 con recuento por celda** — 3/3/0 · 3/1/4 · 1/1/4.
- [x] **Clic en celda → lista de referencias** — probado: BZ muestra ZW-VES-001, ZW-VES-003, ZW-CAZ-002, ZW-CAZ-001 con su CV.
- [x] **Aviso destacado con AZ y AY** — los dos bloques están.
- [x] **Legible en móvil** — probado a 375 px: la tabla no desborda y no hay scroll horizontal.

### Comentarios en líneas concretas

**El caso que rompe los dashboards: AZ con 0 referencias**
> Es la comprobación que había que hacer sí o sí, porque el encargo pide «un
> aviso destacado con las referencias de la celda AZ» y **en nuestros datos AZ
> está vacía**. Un dashboard ingenuo enseñaría un recuadro de alarma vacío, o
> directamente nada.
> Aquí el bloque cambia de color (verde, no ámbar) y dice qué significa que esté
> vacía. Además el botón de una celda con 0 sale `disabled`, así que no se puede
> hacer clic para ver una lista vacía. Bien.

**Error de carga con `file://`**
> Si abrís `index.html` haciendo doble clic, el navegador bloquea el `fetch` por
> CORS y la página sale en blanco. No es un fallo del dashboard, pero la primera
> vez asusta. El PR lo detecta (`location.protocol === 'file:'`) y lo explica en
> pantalla con la solución (`python -m http.server` o abrirlo ya en Vercel).
> Comprobado sirviendo la carpeta en local.

**Lo que este dashboard NO hace, y no pasa nada**
> Muestra el código del SKU, no el nombre comercial. El nombre está en
> `ex2_sku_master.csv`, que el encargo **no** manda cargar. Preferimos que la
> página tenga **una sola fuente de datos declarada** a que sea más bonita: si
> mañana los dos ficheros se desincronizan, el dashboard no puede mentir.

### Forma
- [x] El PR explica qué hizo y por qué.

**Veredicto: APROBAR y mergear.** Después, desplegar en Vercel (paso 5 de la
guía) y volver a abrirlo **en el móvil** para comprobar que los avisos AZ/AY
dicen lo mismo que `clasificacion.csv`.

---

## Resumen para la entrega

| PR | Encargo | Veredicto | Lo que cazamos nosotros |
|---|---|---|---|
| #1 | ABC por margen | APROBAR | Dos fronterizas (ZW-DEN-002 a 0,85 pp de B; ZW-PUN-001 a 0,21 pp de B) |
| #2 | XYZ | APROBAR con aclaración | ZW-CAZ-001 cambia de Y a Z según el convenio de σ; lo resolvimos contra los CV publicados en los apuntes |
| #3 | Matriz + políticas | APROBAR | AZ vacía es el titular del análisis, y es robusto al convenio de σ |
| #4 | KPIs | APROBAR *porque no calcula* | Ningún KPI es calculable: falta stock, y la serie de roturas es de otra empresa y sin `sku` |
| #5 | Dashboard | APROBAR | El aviso de AZ tenía que funcionar con 0 referencias; y el fallo de `fetch` con `file://` |
