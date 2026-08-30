# RAG para Documentación Técnica

## Construir aplicaciones de IA multimodal con LangChain y la API de OpenAI

### Hugging Face Falcon 7b

```python
from langchain_huggingface import HuggingFaceEndpoint
llm = (    
    repo_id='tiiuae/falcon-7b-instruct',    
    huggingfacehub_api_token=huggingfacehub_api_token)
question = 'Can you still have fun'
output = llm.invoke(question)print(output) 
```
```bash
in the rain?Yes, you can still have fun in the rain! There are plenty of
```

### OpenAI (gpt-3.5-turbo-instruct):

```python
from langchain_openai import OpenAI
llm = OpenAI(    
    openai_api_key=openai_api_key
)
question = 'Can you still have fun'
output = llm.invoke(question)
print(output) 
```

```bash
without spending a lot of money?Yes, you can still have fun without spending a lot of money. You could do activities like hiking, biking, playingsports, going to the beach, camping...
```



El manual del coche en HTML se ha cargado en la variable `car_docs`. Usando *Retrieval Augmented Generation* (RAG), responde a la consulta del usuario:

"Ha aparecido el aviso *Gasoline Particulate Filter Full*. ¿Qué significa y qué debo hacer?"

Guarda la respuesta en la variable `answer`.



Trabajas para un fabricante de coches conocido que quiere integrar [LLMs](../introduccion.md) en sus vehículos para orientar a los conductores. Te han pedido experimentar con la integración de los manuales del coche y un LLM, para crear un chatbot consciente del contexto. La idea es que ese LLM pueda conectarse después a un software de texto a voz que lea la respuesta en voz alta.

Como prueba de concepto, integrarás varias páginas de un manual que contiene los mensajes de aviso del coche, su significado y las acciones recomendadas. Este manual concreto, almacenado como archivo HTML `mg-zs-warning-messages.html`, corresponde a un MG ZS, un SUV compacto. Con lo aprendido sobre LLMs y [LangChain](langchain.md), implementarás RAG para construir el chatbot.

## Antes de empezar

Para completar el proyecto necesitarás crear una cuenta de desarrollador en OpenAI y guardar tu clave API como variable de entorno segura. Los pasos se detallan a continuación.

### Crear una cuenta de desarrollador en OpenAI

1. Ve a la [página de registro de la API](https://platform.openai.com/signup).

2. Crea tu cuenta (necesitarás proporcionar tu correo electrónico y tu número de teléfono).

3. Ve a la [página de claves API](https://platform.openai.com/account/api-keys).

4. Crea una nueva clave secreta.

5. **Cópiala y guárdala.** Si la pierdes, borra la clave y crea una nueva.

### Añadir un método de pago

OpenAI a veces ofrece créditos gratuitos para la API, pero esto varía según la región. Puede que necesites añadir los datos de una tarjeta de débito o crédito.

**Este proyecto debería costar menos de 1 centavo de dólar con GPT-3.5-Turbo, pero si repites las tareas se te cobrará cada vez.**

1. Ve a la [página de métodos de pago](https://platform.openai.com/account/billing/payment-methods).

2. Haz clic en *Add payment method*.

3. Rellena los datos de tu tarjeta.

### Añadir una variable de entorno con tu clave de OpenAI

1. En el cuaderno, haz clic en *Environment* en la barra superior y selecciona *Environment variables*.

2. Haz clic en *Add* para añadir variables de entorno.

3. En el campo *Name* escribe `OPENAI_API_KEY`. En el campo *Value* pega tu clave secreta.

4. Haz clic en *Create*; verás la siguiente ventana emergente. Pulsa *Connect* y espera de 5 a 10 segundos a que el kernel se reinicie, o reinícialo manualmente desde el menú *Run*.

### Actualizar a Python 3.10

Dada la frecuencia con la que se actualizan las librerías necesarias para este proyecto, tendrás que actualizar tu entorno a Python 3.10:

1. En el cuaderno, haz clic en *Environment* en la barra superior y selecciona *Session details*.

2. En el desplegable de lenguaje, selecciona *Python 3.10*.

3. Pulsa *Confirm* y después *Done* cuando la sesión esté lista.



```python
# Update your environment to Python 3.10 as described above before running this cell
import subprocess
import pkg_resources

def install_if_needed(package, version):
    '''Function to ensure that the libraries used are consistent to avoid errors.'''
    try:
        pkg = pkg_resources.get_distribution(package)
        if pkg.version != version:
            subprocess.check_call(["pip", "install", f"{package}=={version}"])
    except pkg_resources.DistributionNotFound:
        try:
            subprocess.check_call(["pip", "install", f"{package}=={version}"])
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}=={version}. Error: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}=={version}. Error: {e}")
    except pkg_resources.VersionConflict as e:
        print(f"Version conflict for {package}: {e}")
        try:
            subprocess.check_call(["pip", "install", f"{package}=={version}"])
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}=={version}. Error: {e}")

install_if_needed("langchain", "0.2.2")
install_if_needed("langchain-openai", "0.1.8")
install_if_needed("langchain-community", "0.2.3")
install_if_needed("unstructured", "0.14.4")
install_if_needed("chromadb", "0.5.0")
```

```python

# Set your API key to a variable
import os
openai_api_key = os.environ["OPENAI_API_KEY"]

# Import the required packages
import langchain
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain_openai import OpenAIEmbeddings
from langchain.schema.runnable import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.document_loaders import UnstructuredHTMLLoader
```

```python 
# Load the HTML as a LangChain document loader
loader = UnstructuredHTMLLoader(file_path="data/mg-zs-warning-messages.html")
car_docs = loader.load()
```


