# Series de Tiempo

**Definición**: una serie de tiempo es un conjunto de puntos de datos **ordenados en el
tiempo**. Los datos están igualmente espaciados temporalmente, es decir, se registraron cada
hora, minuto, mes o trimestre. Ejemplos típicos son el valor de cierre de una acción o la
temperatura exterior.

## Tipos de problema

- **Análisis de regresión** sobre series de tiempo.
- **Pronóstico** (*forecasting*):
    - modelo de media móvil,
    - modelos autorregresivos.

## Métodos tradicionales de suavizado

- **ARMA** — autorregresivo de media móvil.
- **ARIMA** — añade diferenciación para manejar series no estacionarias.
- **SARIMA** — añade componente estacional.
- **SARIMAX** — añade variables exógenas.
- **VAR** — vectorial autorregresivo, para series multivariadas.
- **VARMA** — vectorial autorregresivo de media móvil.

## Conceptos clave

**Estacionariedad**. La mayoría de estos métodos asumen que las propiedades estadísticas
—media, varianza, autocorrelación— no cambian con el tiempo. Cuando no se cumple, se
diferencia la serie hasta lograrlo; ese es el papel de la *I* en ARIMA.

**Descomposición**. Una serie se puede separar en tendencia, estacionalidad y residuo, sea de
forma aditiva ($y_t = T_t + S_t + R_t$) o multiplicativa ($y_t = T_t \cdot S_t \cdot R_t$).

**Validación temporal**. No se puede usar validación cruzada aleatoria: mezclaría el futuro con
el pasado. Hay que usar validación por ventanas deslizantes o expansivas, respetando siempre el
orden temporal.

## Ver también

- [Bases de datos de series de tiempo](../00_DATA/introduccion_bases_de_datos.md):
  [OpenTSDB](../00_DATA/databases/opentsdb.md) y [Goku](../00_DATA/databases/goku.md).
- [Detección de anomalías](../02_UNSUPERVISED_LEARNING/deteccion_de_anomalias.md) — aplicada a
  series temporales.
