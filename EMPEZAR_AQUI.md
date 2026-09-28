# Empezar aquí · estado del lab y lo que falta

Todo el trabajo **analítico** del lab está hecho, ejecutado y verificado a mano en
esta carpeta. Lo que falta es lo que necesita **vuestras cuentas**: GitHub, el
agente, los PRs y Vercel. Nadie puede hacer esa parte por vosotros.

---

## 1. Qué hay hecho (y comprobado)

| Encargo | Entregable | Estado |
|---|---|---|
| 1 · ABC por margen | `analisis/abc.py` → `resultados/abc.csv` | ✅ ejecutado · muestra de 3 referencias recalculada a mano |
| 2 · XYZ | `analisis/xyz.py` → `resultados/xyz.csv` | ✅ ejecutado · CV de ZW-CAZ-001 recalculado a mano, 12 meses |
| 3 · Matriz + políticas | `analisis/matriz.py` → `clasificacion.csv` + `politicas.md` | ✅ ejecutado · cruce de la muestra verificado |
| 4 · KPIs | `analisis/kpis.py` → `kpis.csv` + `kpis_LIMITACIONES.md` | ✅ **no calcula los KPIs a propósito**: el dato no existe en el repo |
| 5 · Dashboard | `index.html` | ✅ probado sirviendo la carpeta en local, y a 375 px de ancho |
| Memo | `resultados/memo.md` | ✅ escrito y auditado · faltan nombres y URL de Vercel |

**Auditoría** (`auditoria/`):

- `00_ISSUES_PARA_GITHUB.md` — los 5 issues listos para pegar, con criterios de aceptación.
- `01_MUESTREO_MANUAL.md` — **la verdad-terreno**: todo recalculado a mano, con las tablas paso a paso. Es la pieza que más puntúa.
- `02_REVIEWS_PR.md` — el `CHECKLIST_AUDITORIA.md` relleno para los 5 PR, con comentarios de línea y veredicto.
- `03_PLANB_PR_CONGELADO.md` — auditoría completa del PR congelado: **9 problemas** clasificados, con el código ejecutado para demostrarlos.

**Los guardarraíles pasan:** las 4 comprobaciones de `tests/test_estructura.py`
dan verde (replicadas sin pytest, que no está instalado en este equipo; en GitHub
las ejecutará el CI).

### Los tres números que conviene que os sepáis de memoria

- Margen total del catálogo: **1.663.175 €**. Clase A = **6 referencias (30 %) con el 79,15 %** del margen.
- Matriz: AX 3 · AY 3 · **AZ 0** · BX 3 · BY 1 · BZ 4 · CX 1 · CY 1 · CZ 4.
- La fronteriza: **ZW-CAZ-001**, CV 0,5176 (muestral) → **Z**, pero 0,4956 (poblacional) → Y.

---

## 2. Lo que solo podéis hacer vosotros

### Paso 0–1 · Cuentas y repo (20')
1. Cuenta de GitHub por miembro. **Pedid hoy GitHub Education** (tarda días): education.github.com → *Student Developer Pack*.
2. Repo plantilla del curso (URL en el campus) → **Use this template** → nombre `zeta-wear-equipoNN` → **Public**.
3. *Settings → Collaborators* → añadid al resto del equipo.
4. *Actions* → comprobad que está el workflow «guardarrailes».

### Paso 2 · Agente (10')
Jules (jules.google.com, recomendado) · Copilot coding agent · o Gemini CLI.
**Obligatorio para todos:** instalad **Gemini Code Assist** (github.com/apps/gemini-code-assist) en el repo.

### Paso 3–4 · Un encargo = un issue = un PR
Pegad los issues de `auditoria/00_ISSUES_PARA_GITHUB.md` y añadidle siempre al agente:
> Trabaja en una rama nueva y abre un pull request. No toques nada fuera de lo que pide el encargo.

Los encargos **1→3 son secuenciales** (mergead antes de encargar el siguiente). El 4 y el 5 van en paralelo.

### Paso 5 · Vercel (15')
vercel.com → *Continue with GitHub* → *Add New… → Project* → Import del repo →
Framework Preset **Other**, sin build command → Deploy.
Abrid la URL **en el móvil** y comprobad que los avisos AZ/AY dicen lo mismo que `clasificacion.csv`.

### Paso 6 · Cerrar el memo
Rellenad en `resultados/memo.md` los nombres del equipo y la URL de Vercel (están como `___`).

---

## 3. Cómo usar este material sin hacer trampa

Lo que se evalúa es **vuestra auditoría**, no el código. Si subís lo que hay aquí
como si lo hubiera escrito vuestro agente, no tenéis lab: tenéis un repo sin PRs,
sin reviews y sin la comparación final, que es justo lo que puntúa.

**El uso honesto es el que la propia guía pide** en el paso 3.4: *«mientras el
agente trabaja, preparad la auditoría: apuntad ya las 2–3 referencias que vais a
recalcular a mano y qué esperáis ver»*. Eso es exactamente
`auditoria/01_MUESTREO_MANUAL.md`. Encargad los 5 issues a vuestro agente y
auditad **su** PR contra estos números:

- Si su margen de ZW-TEE-001 no da 411.000 €, hay algo mal en su PR.
- Si su reparto A/B/C no es 6/8/6 con el 79,15 % en A, mirad por qué magnitud ordena.
- Si no encuentra ninguna X en el XYZ, está usando la serie diaria.
- Si su `rotacion` da el mismo número para las 20 referencias, se ha inventado el stock medio.
- Si ZW-CAZ-001 le sale Y, preguntadle qué desviación típica usó — y que lo justifique.

Cuando su PR difiera del vuestro, **no asumáis que el equivocado sois vosotros**:
tenéis la aritmética escrita paso a paso para defenderlo. Y si el agente acierta
en algo que aquí está mal, mejor todavía: eso también se escribe en la review.

Si vuestro agente se queda sin cuota, la guía os deja auditar el PR congelado del
plan B: esa auditoría ya está hecha y completa en `auditoria/03_PLANB_PR_CONGELADO.md`.

**Si preferís subir esto como punto de partida**, decidlo en el repo. Un PR que
diga «esto lo generamos nosotros con ayuda de IA, y esta es la auditoría» es
honesto; uno que lo presente como salida del agente, no.

---

## 4. Dos trampas del repo que conviene conocer antes de empezar

**a) `.gitignore` ignoraba `index.html`.** La plantilla trae `*.html`, así que el
dashboard del encargo 5 **nunca se habría subido**: `git add .` lo salta en
silencio y Vercel acaba sirviendo el README. Es literalmente el fallo que avisa
la guía en «Si algo falla». Ya está corregido al final de `.gitignore` con
`!index.html`. Si vuestro agente crea el `index.html` y «desaparece» al hacer
commit, es esto.

**b) El CI en verde no valida los números.** `test_xyz_estructura` solo comprueba
que la clase sea coherente con **el CV que el propio fichero publica**: si el CV
está mal calculado, el test sigue en verde. Y `test_abc_estructura` se **salta**
(no falla) si el fichero no existe. El PR congelado del plan B afirma «todos los
tests pasan» y en realidad uno falla y dos se saltan.

---

## 5. La comparación final (rellenar al terminar)

La guía la evalúa: *«¿qué cazasteis vosotros que la IA revisora no vio?»*
Solo se puede rellenar cuando Gemini Code Assist haya comentado vuestros PRs.

| Hallazgo | ¿Lo vio Gemini Code Assist? | ¿Lo vimos nosotros? |
|---|---|---|
| Criterio de valor equivocado (cantidad/facturación en vez de margen) | | ✅ |
| CV sobre la serie diaria en vez de la mensual | | ✅ |
| La serie diaria es de otra empresa y no tiene columna `sku` | | ✅ |
| Limpieza de filas sin declarar el criterio | | ✅ |
| CV fabricado a partir del precio | | ✅ |
| Rotación constante (10,4) para las 20 referencias | | ✅ |
| Benchmark de sector inventado en el memo | | ✅ |
| ZW-CAZ-001 cambia de clase según el convenio de σ | | ✅ |
| AZ vacía: el aviso del dashboard tiene que funcionar con 0 referencias | | ✅ |
| `.gitignore` se traga `index.html` | | ✅ |

> **Predicción, para contrastarla luego:** un revisor automático de código
> detecta bien lo sintáctico y lo estructural (rutas relativas, falta de
> `try/except`, columnas que no cuadran, código duplicado). Lo que difícilmente
> detecta es que el **criterio de negocio** sea el equivocado: un ABC ordenado por
> cantidad es código perfectamente correcto que responde a la pregunta que nadie
> hizo. Eso solo lo caza quien conoce el encargo — vosotros.
