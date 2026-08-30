# Configuración del MCP Filesystem en VSCode

Esta guía te mostrará cómo usar tu servidor MCP de sistema de archivos en Python con Visual Studio Code.

## 📋 Prerrequisitos

- ✅ Python 3.10+ instalado
- ✅ VSCode instalado
- ✅ Extensión Claude Dev para VSCode instalada
- ✅ Dependencias instaladas (`pip install -r requirements.txt`)

## 🔌 Paso 1: Instalar la Extensión Claude Dev

1. Abre VSCode
2. Ve a la pestaña de Extensiones (Ctrl+Shift+X)
3. Busca "Claude Dev" o "Anthropic Claude"
4. Haz clic en "Install"
5. Recarga VSCode si es necesario

## 📁 Paso 2: Ubicar el archivo de configuración

VSCode con Claude Dev usa un archivo de configuración similar al de Claude Desktop, pero ubicado en:

### Windows
```
%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json
```

### Ruta alternativa (depende de la extensión)
```
%USERPROFILE%\.claude\mcp_settings.json
```

### O en el workspace de VSCode
```
.vscode/mcp_settings.json
```

## 🔍 Encontrar el archivo correcto

Para encontrar exactamente dónde está el archivo:

### Método 1: Desde VSCode

1. Presiona `Ctrl+Shift+P`
2. Escribe "Claude: Open MCP Settings"
3. Si aparece esta opción, úsala

### Método 2: Buscar manualmente

```powershell
# En PowerShell
Get-ChildItem -Path $env:APPDATA\Code -Recurse -Filter "*mcp*.json" | Select-Object FullName
```

## ⚙️ Paso 3: Configurar el MCP en VSCode

Una vez que localices el archivo de configuración, editalo:

### Configuración Básica

```json
{
  "mcpServers": {
    "filesystem-python": {
      "command": "python",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "${workspaceFolder}"
      ]
    }
  }
}
```

### Configuración con Múltiples Directorios

```json
{
  "mcpServers": {
    "filesystem-python": {
      "command": "python",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "${workspaceFolder}",
        "D:\\SANDBOX\\practica_01",
        "D:\\SANDBOX\\practica_02",
        "C:\\Users\\TuUsuario\\Documents\\Proyectos"
      ]
    }
  }
}
```

## 🎯 Variables de VSCode

VSCode proporciona variables útiles que puedes usar:

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `${workspaceFolder}` | Directorio raíz del workspace | `D:\SANDBOX\mi-proyecto` |
| `${workspaceFolderBasename}` | Nombre del directorio del workspace | `mi-proyecto` |
| `${file}` | Archivo actual abierto | `D:\SANDBOX\mi-proyecto\src\main.py` |
| `${fileWorkspaceFolder}` | Workspace del archivo actual | `D:\SANDBOX\mi-proyecto` |

### Ejemplo con Variables

```json
{
  "mcpServers": {
    "filesystem-python": {
      "command": "python",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "${workspaceFolder}",
        "${workspaceFolder}\\src",
        "${workspaceFolder}\\tests"
      ]
    }
  }
}
```

## 🚀 Configuración por Workspace (Recomendado)

Para tener diferentes configuraciones por proyecto:

1. Crea `.vscode/mcp_settings.json` en tu proyecto:

```bash
mkdir .vscode
```

2. Crea el archivo de configuración:

```json
{
  "mcpServers": {
    "filesystem-python": {
      "command": "python",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "${workspaceFolder}"
      ]
    }
  }
}
```

3. Agrega a `.gitignore` si no quieres versionarlo:

```
.vscode/mcp_settings.json
```

## 🔄 Paso 4: Recargar VSCode

Después de configurar:

1. Presiona `Ctrl+Shift+P`
2. Escribe "Developer: Reload Window"
3. Presiona Enter

O simplemente cierra y abre VSCode.

## ✅ Paso 5: Verificar que funciona

### Método 1: Panel de Claude

1. Abre el panel de Claude (usualmente en la barra lateral)
2. Deberías ver tu servidor MCP listado
3. Verifica que aparezcan las herramientas disponibles

### Método 2: Comando directo

Abre el chat de Claude en VSCode y prueba:

```
¿Qué herramientas tienes disponibles?
```

### Método 3: Prueba práctica

```
Lista los archivos en el directorio actual del workspace
```

```
Lee el archivo README.md
```

## 🛠️ Configuración Avanzada para Desarrollo

### Configuración para Proyectos Python

```json
{
  "mcpServers": {
    "filesystem-python": {
      "command": "python",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "${workspaceFolder}",
        "${workspaceFolder}\\src",
        "${workspaceFolder}\\tests",
        "${workspaceFolder}\\docs"
      ]
    }
  }
}
```

### Configuración con Variables de Entorno

```json
{
  "mcpServers": {
    "filesystem-python": {
      "command": "python",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "${workspaceFolder}"
      ],
      "env": {
        "PYTHONPATH": "${workspaceFolder}\\src",
        "DEBUG": "true"
      }
    }
  }
}
```

### Configuración con Python Virtual Environment

Si usas un entorno virtual:

```json
{
  "mcpServers": {
    "filesystem-python": {
      "command": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "${workspaceFolder}"
      ]
    }
  }
}
```

## 🎨 Configuración Multi-Servidor

Puedes tener múltiples servidores MCP activos:

```json
{
  "mcpServers": {
    "filesystem-python": {
      "command": "python",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "${workspaceFolder}"
      ]
    },
    "filesystem-oficial": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "${workspaceFolder}"
      ]
    },
    "git": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-git",
        "${workspaceFolder}"
      ]
    }
  }
}
```

## 🐛 Solución de Problemas en VSCode

### Problema 1: El servidor no aparece

**Solución:**

1. Verifica que la extensión Claude Dev está instalada y habilitada
2. Recarga la ventana: `Ctrl+Shift+P` → "Reload Window"
3. Verifica los logs de la extensión:
   - Abre la consola de desarrollador: `Help` → `Toggle Developer Tools`
   - Ve a la pestaña "Console"
   - Busca errores relacionados con MCP

### Problema 2: Error de ruta de Python

**Solución:**

Usa la ruta completa a Python:

```powershell
# Encuentra la ruta de Python
where python
```

Luego úsala en la configuración:

```json
{
  "mcpServers": {
    "filesystem-python": {
      "command": "C:\\Python310\\python.exe",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "${workspaceFolder}"
      ]
    }
  }
}
```

### Problema 3: Variables no se resuelven

**Solución:**

Verifica que estás usando el archivo de configuración correcto:
- Global: Para todos los proyectos
- Workspace: Solo para el proyecto actual

Si `${workspaceFolder}` no funciona, usa rutas absolutas:

```json
{
  "mcpServers": {
    "filesystem-python": {
      "command": "python",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "D:\\SANDBOX\\mi-proyecto"
      ]
    }
  }
}
```

### Problema 4: Permisos en Windows

**Solución:**

Si VSCode no puede ejecutar el servidor:

1. Ejecuta VSCode como administrador (temporalmente para probar)
2. Verifica permisos del directorio
3. Verifica que Python tiene permisos de ejecución

### Problema 5: Puerto/Socket en uso

**Solución:**

El servidor MCP usa stdio, no puertos, pero si hay conflictos:

1. Cierra todas las instancias de VSCode
2. Cierra Python en el Administrador de Tareas
3. Reinicia VSCode

## 📊 Estructura Recomendada de Proyecto

```
mi-proyecto/
├── .vscode/
│   ├── settings.json
│   └── mcp_settings.json          # Configuración MCP del proyecto
├── src/
│   └── mi_codigo.py
├── tests/
│   └── test_mi_codigo.py
├── docs/
│   └── README.md
└── .gitignore
```

Ejemplo de `.vscode/mcp_settings.json`:

```json
{
  "mcpServers": {
    "filesystem-python": {
      "command": "python",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "${workspaceFolder}",
        "${workspaceFolder}\\src",
        "${workspaceFolder}\\tests"
      ]
    }
  }
}
```

## 🎯 Comandos Útiles para VSCode

Una vez configurado, puedes usar Claude en VSCode para:

### Exploración de Código

```
"Analiza la estructura de este proyecto"

"Lista todos los archivos Python en src/"

"Muéstrame el contenido de main.py"
```

### Generación de Código

```
"Crea un archivo test_utils.py con pruebas unitarias básicas"

"Genera un README.md para este proyecto"

"Crea una estructura de directorios para un proyecto Flask"
```

### Refactorización

```
"Lee todos los archivos .py y sugiere mejoras"

"Busca archivos con TODO o FIXME"

"Lista archivos duplicados o similares"
```

### Documentación

```
"Lee todos los archivos Python y genera documentación en docs/"

"Crea un índice de todos los módulos del proyecto"
```

## 🔐 Mejores Prácticas de Seguridad en VSCode

1. **Configuración por Workspace**: Usa `.vscode/mcp_settings.json` en cada proyecto

2. **Limita el acceso**: Solo permite directorios del proyecto actual

   ```json
   {
     "mcpServers": {
       "filesystem-python": {
         "command": "python",
         "args": [
           "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
           "${workspaceFolder}"
         ]
       }
     }
   }
   ```

3. **No versionar credenciales**: Agrega a `.gitignore`:
   ```
   .vscode/mcp_settings.json
   ```

4. **Usa variables de entorno**: Para rutas sensibles

## 🚦 Testing del Servidor

Crea un script de prueba en tu proyecto:

**test_mcp.py**:
```python
"""Script de prueba para verificar el servidor MCP"""

import sys
import json
from pathlib import Path

def test_mcp_connection():
    """Prueba básica del servidor MCP"""
    print("✅ Servidor MCP puede importarse")
    
    # Importa el servidor
    sys.path.insert(0, "D:\\SANDBOX\\practica_03\\src")
    from filesystem_server import FilesystemServer
    
    # Crea instancia de prueba
    server = FilesystemServer(["D:\\SANDBOX\\practica_03"])
    print("✅ Servidor MCP inicializado correctamente")
    
    return True

if __name__ == "__main__":
    test_mcp_connection()
```

## 📚 Integración con Otras Extensiones

El servidor MCP puede trabajar junto con:

- **Python**: Para ejecución de código Python
- **Pylint/Flake8**: Para linting de código
- **Git**: Para control de versiones
- **Jupyter**: Para notebooks interactivos

## 🆘 Obtener Ayuda

Si tienes problemas:

1. **Logs de la Extensión**:
   - `Help` → `Toggle Developer Tools` → `Console`

2. **Logs de VSCode**:
   - `Help` → `Toggle Developer Tools` → `Console`

3. **Logs del Servidor**:
   - El servidor MCP imprime logs en la terminal

4. **Output de Claude**:
   - Ve a `View` → `Output`
   - Selecciona "Claude Dev" en el dropdown

## 🎓 Recursos Adicionales

- [VSCode Variables Reference](https://code.visualstudio.com/docs/editor/variables-reference)
- [VSCode Workspace Settings](https://code.visualstudio.com/docs/getstarted/settings)
- [Python in VSCode](https://code.visualstudio.com/docs/python/python-tutorial)

## 🔄 Actualización del Servidor

Para actualizar el servidor:

1. Modifica `filesystem_server.py`
2. Recarga VSCode: `Ctrl+Shift+P` → "Reload Window"
3. El nuevo código se cargará automáticamente

## ✨ Ejemplos Prácticos Completos

### Ejemplo 1: Análisis de Proyecto

```
"Analiza todos los archivos Python en este proyecto y genera un reporte con:
- Número total de archivos
- Líneas de código por archivo
- Funciones y clases principales
- Posibles mejoras"
```

### Ejemplo 2: Limpieza de Código

```
"Busca todos los archivos .pyc y __pycache__ en el proyecto y dame un resumen"
```

### Ejemplo 3: Estructura de Proyecto

```
"Genera una estructura de proyecto Django en este workspace con:
- Aplicación de usuarios
- Aplicación de productos  
- Configuración básica
- Requirements.txt"
```

---

**¡Listo!** Ahora puedes usar tu servidor MCP de sistema de archivos en VSCode.

**Siguiente paso**: Experimenta con diferentes comandos y personaliza la configuración según tus necesidades.
