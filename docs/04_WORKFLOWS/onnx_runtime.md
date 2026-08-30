# ONNX Runtime

El formato [ONNX](onnx.md) describe **qué** calcula un modelo. **ONNX Runtime** (ORT) es el
motor que lo ejecuta: carga el grafo, lo optimiza y lo despacha sobre el hardware disponible.

Es el runtime de referencia —desarrollado por Microsoft, de código abierto— pero no el único:
TensorRT, OpenVINO o CoreML también consumen ONNX directamente. La ventaja de ORT es que actúa
como capa unificadora sobre todos ellos.

## Inferencia básica

```bash
pip install onnxruntime          # CPU
pip install onnxruntime-gpu      # CPU + CUDA / TensorRT
```

```python
import numpy as np
import onnxruntime as ort

sesion = ort.InferenceSession("modelo.onnx", providers=["CPUExecutionProvider"])

# Inspeccionar el contrato del modelo antes de llamarlo
for e in sesion.get_inputs():
    print("entrada:", e.name, e.shape, e.type)
for s in sesion.get_outputs():
    print("salida:", s.name, s.shape, s.type)

x = np.random.randn(4, 10).astype(np.float32)
salida = sesion.run(None, {"entrada": x})[0]      # None = todas las salidas
```

Dos cosas que causan casi todos los errores en la primera ejecución:

- **El tipo debe coincidir exactamente.** ORT no promociona `float64` a `float32`. Si el modelo
  espera `tensor(float)` y le pasas un array de NumPy sin castear, falla. Por defecto NumPy crea
  `float64`, así que el `.astype(np.float32)` es obligatorio, no cosmético.
- **Las dimensiones fijas son realmente fijas.** Si al exportar no declaraste el lote como
  dinámico, pasar un lote distinto da `INVALID_ARGUMENT: Got invalid dimensions for input`.

## Execution Providers

Un **Execution Provider** (EP) es el backend que ejecuta los nodos del grafo. Es el mecanismo
central de ORT: el mismo `.onnx` corre en CPU, en GPU NVIDIA o en un acelerador de móvil sin
tocar el modelo.

| Execution Provider | Destino |
|---|---|
| `CPUExecutionProvider` | CPU. Siempre disponible, es el respaldo final |
| `CUDAExecutionProvider` | GPU NVIDIA |
| `TensorrtExecutionProvider` | GPU NVIDIA con compilación TensorRT; el más rápido, el que más tarda en arrancar |
| `OpenVINOExecutionProvider` | CPU, GPU integrada y VPU de Intel |
| `DmlExecutionProvider` | DirectML: cualquier GPU en Windows |
| `CoreMLExecutionProvider` | Apple: Neural Engine y GPU |
| `NnapiExecutionProvider` | Android |
| `QNNExecutionProvider` | NPU de Qualcomm |
| `ROCMExecutionProvider` | GPU AMD |
| `WebGPU` / `WebNN` | Navegador, vía ONNX Runtime Web |

Los EPs se pasan **en orden de prioridad**. ORT asigna cada nodo al primer proveedor de la lista
que sepa ejecutarlo, y deja el resto en CPU:

```python
sesion = ort.InferenceSession(
    "modelo.onnx",
    providers=["TensorrtExecutionProvider", "CUDAExecutionProvider", "CPUExecutionProvider"],
)
print("en uso:", sesion.get_providers())
```

Conviene comprobar qué hay instalado antes de asumir nada:

```python
print(ort.get_available_providers())
```

!!! warning "El reparto entre proveedores puede salir caro"
    Si un solo operador no está soportado por el EP acelerado, el grafo se **parte**: ese nodo
    cae a CPU y los tensores viajan de vuelta y adelante entre dispositivos. Copiar entre GPU y
    CPU en mitad del grafo puede anular por completo la ganancia. Si aceleras y no mejora,
    revisa cuántas particiones se crearon.

## Optimización del grafo

Antes de ejecutar, ORT reescribe el grafo: elimina nodos redundantes, pliega constantes y
**fusiona** secuencias de operadores en kernels únicos (por ejemplo `Conv` + `BatchNorm` + `Relu`
en uno solo).

```python
opciones = ort.SessionOptions()
opciones.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

# Guardar el grafo ya optimizado evita repetir el trabajo en cada arranque
opciones.optimized_model_filepath = "modelo_opt.onnx"

sesion = ort.InferenceSession("modelo.onnx", opciones, providers=["CPUExecutionProvider"])
```

Los niveles disponibles son `ORT_DISABLE_ALL`, `ORT_ENABLE_BASIC`, `ORT_ENABLE_EXTENDED`,
`ORT_ENABLE_LAYOUT` y `ORT_ENABLE_ALL` (el valor por defecto).

Guardar el modelo optimizado tiene una contrapartida: queda **ligado al hardware y a la versión
de ORT** con la que se generó. Sirve para acortar el arranque en un despliegue concreto, no como
artefacto portable.

### Control de hilos

```python
opciones = ort.SessionOptions()
opciones.intra_op_num_threads = 4      # paralelismo dentro de un operador
opciones.inter_op_num_threads = 1      # operadores en paralelo entre si
opciones.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
```

En un servidor que ya atiende varias peticiones en paralelo, lo habitual es **bajar** estos
valores. Dejar que cada sesión abra tantos hilos como núcleos provoca sobresuscripción y
empeora la latencia de cola.

## Cuantización

Reducir la precisión de los pesos de `float32` a `int8` disminuye el tamaño del modelo y acelera
la inferencia en CPU. ORT ofrece tres vías:

| Método | Necesita datos | Cuándo usarlo |
|---|---|---|
| **Dinámica** | No | Punto de partida. Cuantiza pesos; las activaciones, al vuelo |
| **Estática** | Sí, muestras de calibración | Mayor aceleración; requiere un `CalibrationDataReader` |
| **QAT** | Sí, reentrenamiento | Máxima precisión; se cuantiza durante el entrenamiento |

```python
from onnxruntime.quantization import quantize_dynamic, QuantType

quantize_dynamic("modelo.onnx", "modelo_int8.onnx", weight_type=QuantType.QInt8)
```

Dos advertencias comprobadas sobre modelos reales:

**En modelos pequeños la cuantización puede aumentar el tamaño.** Los nodos de
cuantización y descuantización que se insertan tienen un coste fijo. En una red diminuta de dos
capas, el archivo pasó de 2 297 a 2 825 bytes: *creció*. La cuantización compensa a partir de
modelos con muchos megabytes de pesos.

**La pérdida de precisión es real y hay que medirla.** En la misma red, la diferencia máxima
frente a la salida en `float32` pasó de 6e-08 a **0.12**. Para logits que después van a un
`argmax` puede ser irrelevante; para una regresión, no. Compara siempre contra el modelo
original sobre datos representativos, no sobre ruido aleatorio.

### Incompatibilidad conocida: exportador dynamo y cuantizador

Con `onnx` 1.22 y `onnxruntime` 1.23, un modelo exportado desde PyTorch con **`dynamo=True`**
hace fallar a `quantize_dynamic`:

```text
InferenceError: [ShapeInferenceError] Inferred shape and existing shape
differ in dimension 0: (10) vs (32)
```

La causa es que el exportador dynamo escribe los inicializadores **también** como entradas de
`value_info`, y la reinferencia de formas que hace el cuantizador se atraganta con ellas. El
modelo en sí es válido: pasa `check_model` y `infer_shapes` sin problema.

Hay dos salidas. Limpiar el `value_info` redundante:

```python
import onnx

g = onnx.load("modelo.onnx")
nombres_init = {i.name for i in g.graph.initializer}
limpio = [v for v in g.graph.value_info if v.name not in nombres_init]
del g.graph.value_info[:]
g.graph.value_info.extend(limpio)
onnx.save(g, "modelo_limpio.onnx")      # ya se cuantiza sin errores
```

O exportar con el trazador antiguo, `dynamo=False`, para la rama que va a cuantizarse.

## Medir antes de optimizar

ORT trae un perfilador que emite un rastro por operador:

```python
opciones = ort.SessionOptions()
opciones.enable_profiling = True

sesion = ort.InferenceSession("modelo.onnx", opciones, providers=["CPUExecutionProvider"])
for _ in range(100):
    sesion.run(None, {"entrada": x})

ruta = sesion.end_profiling()      # JSON, se abre en chrome://tracing
print(ruta)
```

Para medir latencia de forma honesta:

```python
import time

for _ in range(10):                        # calentamiento: descarta las primeras
    sesion.run(None, {"entrada": x})

t = time.perf_counter()
for _ in range(100):
    sesion.run(None, {"entrada": x})
print(f"latencia media: {(time.perf_counter() - t) / 100 * 1000:.3f} ms")
```

El **calentamiento** no es opcional: la primera ejecución incluye la asignación de buffers y,
con TensorRT, la compilación de kernels, que puede tardar minutos.

## Dónde se despliega

- **Servidor** — ORT embebido en un servicio Python, C++, Java, C# o Rust. Para servir a escala,
  Triton Inference Server usa ORT como backend.
- **Móvil** — ONNX Runtime Mobile, con un binario reducido que solo incluye los operadores que
  tu modelo usa.
- **Navegador** — ONNX Runtime Web, sobre WebAssembly o WebGPU. Permite inferencia sin enviar
  datos al servidor, lo que resuelve de raíz ciertos problemas de privacidad.
- **Edge** — OpenVINO en hardware Intel, QNN en NPU de Qualcomm.

## Lista de comprobación antes de producción

1. `onnx.checker.check_model` pasa sin errores.
2. Las salidas coinciden con las del modelo original (diferencia < 1e-4) sobre **datos reales**,
   no aleatorios.
3. Los ejes que deben ser dinámicos aparecen como `dim_param`, no como un número.
4. El `opset` del modelo está soportado por el runtime de destino.
5. `get_providers()` confirma que el EP esperado está realmente en uso.
6. La latencia está medida tras calentamiento, con el número de hilos del entorno real.
7. Si cuantizaste, la caída de métrica está medida sobre el conjunto de validación.
8. El preprocesamiento en producción es **idéntico** al del entrenamiento.

## Ver también

- [ONNX](onnx.md) — el formato y cómo exportar.
- [Sistemas de machine learning](sistemas_de_machine_learning.md)
- [Bibliotecas de IA de Ray](ray_bibliotecas_ia.md) — Ray Serve como capa de servicio.
- [MLflow en la práctica](mlflow_en_practica.md) — de dónde sale el modelo que se sirve.
- [Requerimientos de hardware](../10_LLM/requerimientos_de_hardware.md)

## Referencias

- [onnxruntime.ai](https://onnxruntime.ai/) — sitio oficial.
- [Execution Providers](https://onnxruntime.ai/docs/execution-providers/) — la lista completa y
  cómo configurar cada uno.
- [Quantize ONNX models](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html)
