# Titanic


El hundimiento del Titanic es uno de los naufragios más célebres de la historia.

El 15 de abril de 1912, durante su viaje inaugural, el RMS Titanic —considerado por muchos «insumergible»— se hundió tras chocar con un iceberg. No había suficientes botes salvavidas para todos los que iban a bordo, lo que provocó la muerte de 1502 de las 2224 personas entre pasaje y tripulación.

Aunque sobrevivir tuvo un componente de suerte, parece que **algunos grupos de personas tenían más probabilidades de sobrevivir** que otros.

En este reto se pide construir un modelo predictivo que responda a la pregunta: **¿qué tipo de personas tenían más probabilidades de sobrevivir?**, usando datos del pasaje (nombre, edad, género, clase socioeconómica, etc.).



Tendrás acceso a dos conjuntos de datos similares con información del pasaje: uno llamado `train.csv` y otro `test.csv`.

`train.csv` contiene los detalles de un subconjunto de los pasajeros a bordo (891 exactamente) y, lo más importante, revela si sobrevivieron o no: la llamada *ground truth* o verdad de referencia.

`test.csv` contiene información similar pero **no revela** la verdad de referencia de cada pasajero. Tu trabajo es predecir esos resultados.

Usando los patrones que encuentres en `train.csv`, predice si los otros 418 pasajeros de `test.csv` sobrevivieron.


## Descripción general

Los datos se han dividido en dos grupos:

- conjunto de entrenamiento (`train.csv`)
- conjunto de prueba (`test.csv`)

El **conjunto de entrenamiento** se usa para construir los modelos. Para él se proporciona el resultado —la verdad de referencia— de cada pasajero. El modelo se basará en *features* como el género y la clase del pasajero; también puedes aplicar ingeniería de features para crear nuevas variables.

El **conjunto de prueba** sirve para ver qué tal se comporta tu modelo con datos no vistos. Para él no se proporciona la verdad de referencia: tu tarea es predecir, para cada pasajero, si sobrevivió al hundimiento.

También se incluye `gender_submission.csv`, un conjunto de predicciones que asume que sobreviven todas —y solo— las mujeres, como ejemplo del formato que debe tener un archivo de envío.


### Diccionario de datos

| Variable | Definición | Valores |
| ---       | ---        | --- |
| survival | Supervivencia | 0 = No, 1 = Sí |
| pclass | Clase del billete | 1 = 1ª, 2 = 2ª, 3 = 3ª |
| sex | Sexo | |
| age | Edad en años | |
| sibsp | Nº de hermanos o cónyuges a bordo | |
| parch | Nº de padres o hijos a bordo | |
| ticket | Número de billete | |
| fare | Tarifa pagada | |
| cabin | Número de camarote | |
| embarked | Puerto de embarque | C = Cherburgo, Q = Queenstown, S = Southampton |


#### Notas sobre las variables

**pclass**: sirve como aproximación del estatus socioeconómico.

- 1ª = alto
- 2ª = medio
- 3ª = bajo

**age**: la edad es fraccionaria si es menor que 1. Si la edad está estimada, aparece en la forma `xx.5`.

**sibsp**: el dataset define las relaciones familiares así:

- *Hermano* = hermano, hermana, hermanastro, hermanastra.
- *Cónyuge* = marido, esposa (se ignoraron amantes y prometidos).

**parch**: el dataset define las relaciones familiares así:

- *Padre/madre* = madre, padre.
- *Hijo/a* = hija, hijo, hijastra, hijastro.

Algunos niños viajaban solo con una niñera, por lo que para ellos `parch = 0`.

## Enfoque sugerido

1. **EDA** — ver [las seis fases del análisis de datos](../../00_DATA/fases_analisis_datos.md).
2. **Tratar los valores faltantes** — `age` y `cabin` tienen muchos huecos.
3. **Ingeniería de features** — extraer el título del nombre (Mr., Mrs., Master), combinar
   `sibsp` y `parch` en un tamaño de familia, discretizar la tarifa.
4. **Modelo base** — [regresión logística](../../01_SUPERVISED_LEARNING/introduccion.md) para
   tener una referencia contra la que comparar.
5. **Modelos de árboles** — Random Forest o *gradient boosting*, que suelen rendir mejor aquí.
6. **Validación cruzada estratificada**, ya que las clases están desbalanceadas.
