# Memo al director de operaciones · Zeta Wear

**De:** equipo ___ · **Asunto:** las 5 referencias que merecen atención de gestión
**Base:** `resultados/clasificacion.csv` (ABC por margen anual, XYZ por CV de las 12 ventas mensuales de 2026)

1. **Ninguna referencia está en AZ**, la celda que obligaría a poner un planificador dedicado: el 79,15 % del margen (1.316.350 € de un total de **1.663.175 €**) está en 6 referencias de clase A y ninguna de ellas es errática. La atención humana se concentra, por tanto, en las 3 de **AY**.
2. **ZW-TEE-002** (camiseta gráfica limited) — celda **AY**, **150.600 €** de margen anual, CV 0,2952: cuarta referencia del catálogo por margen, con variabilidad media. La regla puede proponer el pedido, pero que lo apruebe una persona antes de lanzarlo.
3. **ZW-VES-002** (vestido negro básico) — celda **AY**, **118.500 €** de margen anual, CV 0,3873: es **la más variable de toda la fila A**. Es la que más se beneficia de revisar la previsión cada mes en lugar de cada trimestre.
4. **ZW-DEN-002** (vaquero wide leg) — celda **AY**, **43.600 €** de margen frente a **287.600 €** de facturación: cuarta en ventas y solo sexta en margen, porque deja **5,45 €** por unidad sobre un PVP de 35,95 €. Entra en clase A por 79,15 % acumulado, a 0,85 puntos de caer a B: gestionarla por volumen de ventas sobreinvierte colchón en la referencia que menos margen deja de las seis grandes.
5. **ZW-VES-001** (vestido midi flores, **39.525 €**, CV 0,7244) y **ZW-CAZ-001** (cazadora bomber, **25.245 €**, CV 0,5176) — ambas en **BZ**: margen medio y demanda errática. No compensa un planificador para ellas, pero tampoco una regla automática: compra por campaña, en una o dos tandas, con liquidación planificada.

---

**Nota de auditoría (esto no va en el memo, va para nosotros).** Antes de dar el
borrador por bueno comprobamos, uno a uno, que:

- Las 5 cifras en euros salen de `abc.csv`; los 5 CV, de `xyz.csv`; las 5 celdas,
  de `clasificacion.csv`. Ninguna cifra viene de fuera de `resultados/`.
- **No hay ningún benchmark de sector, ni ninguna comparación externa.** Es el
  error que hunde el memo del PR congelado (`auditoria/03_PLANB_PR_CONGELADO.md`),
  que se inventa un «8,2 del sector» para poder decir que vamos bien.
- **No citamos rotación de inventario**, aunque el comité la pidiera: no hay datos
  de stock en el repositorio (`resultados/kpis_LIMITACIONES.md`). Un hueco
  declarado es mejor que un número inventado.
- La conclusión de la línea 1 (AZ vacía) la comprobamos con los dos convenios de
  desviación típica: con la poblacional, ZW-CAZ-001 pasaría de BZ a BY y **AZ
  seguiría vacía**. El titular del memo no depende de esa decisión técnica.

---

*Equipo: ___________, ___________, ___________ · Dashboard público: https://___________.vercel.app*
