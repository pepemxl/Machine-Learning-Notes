# Tipos de Memoria y Almacenamiento

La jerarquía de memoria explica buena parte de las decisiones de diseño de los sistemas de
datos: cada nivel es entre 10 y 1000 veces más lento que el anterior, y proporcionalmente más
barato por byte.

## Jerarquía

| Nivel | Latencia aproximada | Capacidad típica | Volátil |
|---|---|---|---|
| Registros de CPU | < 1 ns | bytes | Sí |
| Caché L1 / L2 / L3 | 1–40 ns | KB – MB | Sí |
| RAM | ~100 ns | GB – TB | Sí |
| SSD NVMe | 10–100 µs | TB | No |
| Disco duro (HDD) | 5–10 ms | TB | No |
| Almacenamiento de objetos (S3, GCS) | 10–100 ms | Ilimitado | No |

La consecuencia práctica: **cada salto hacia abajo cuesta un orden de magnitud en latencia**.
Un algoritmo que cabe en RAM y otro que va a disco no se diferencian en constantes, sino en
comportamiento.

## Por qué importa en machine learning

- El salto de rendimiento de [Spark](../spark/spark.md) frente a MapReduce viene precisamente
  de **mantener los datos en memoria** entre etapas, en lugar de escribir a disco.
- Los [requerimientos de hardware para LLMs](../../10_LLM/requerimientos_de_hardware.md) están
  dominados por la VRAM disponible: si el modelo no cabe, hay que cuantizar o repartirlo.
- Las [bases de datos de series de tiempo](../databases/goku.md) como Goku sirven las últimas
  24 horas desde memoria y el histórico desde disco, precisamente por esta jerarquía.

## Volátil vs. persistente

- **Volátil** — pierde el contenido al cortar la alimentación (registros, caché, RAM).
- **Persistente** — sobrevive al apagado (SSD, HDD, almacenamiento de objetos).

Los sistemas que sirven desde memoria pero necesitan durabilidad escriben además un **log de
escritura anticipada** (*write-ahead log*) a disco, para poder reconstruir el estado tras un
reinicio.
