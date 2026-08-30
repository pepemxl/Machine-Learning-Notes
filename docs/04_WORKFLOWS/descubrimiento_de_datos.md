# Descubrimiento de Datos

El **descubrimiento de datos** (*data discovery*) consiste en identificar qué conjuntos de
datos existen en la organización, cuáles son críticos para el negocio y cuáles contienen
**datos sensibles** que puedan estar sujetos a regulaciones de cumplimiento.

## Por qué importa

Sin descubrimiento de datos no hay reutilización posible: los equipos reconstruyen datasets que
ya existen, o peor, entrenan modelos sobre datos que no deberían usar. Es el paso previo a
cualquier [feature store](feature_stores.md) que aspire a ser compartido.

## Qué hay que registrar

- **Inventario** — qué datasets existen, dónde viven y en qué formato.
- **Propiedad** — quién es responsable de cada uno.
- **Linaje** (*lineage*) — de qué fuentes deriva cada dataset y qué depende de él. Registrarlo a
  mano no funciona: ver [OpenLineage](openlineage.md), el estándar para que lo emitan las
  propias herramientas de ejecución.
- **Clasificación de sensibilidad** — datos personales, financieros, de salud.
- **Frescura y calidad** — cada cuánto se actualiza y qué garantías ofrece.

## Relación con el cumplimiento

Identificar dónde están los datos sensibles es requisito previo para aplicar las
transformaciones de anonimización o agregación que exige la regulación. Como se señala en
[Feature stores](feature_stores.md), esas transformaciones reducen la reutilización de los
estados intermedios, así que conviene saber desde el principio qué datos las requieren.
