# Configuración del MCP Filesystem en Claude Desktop

Esta guía te llevará paso a paso para configurar tu servidor MCP de sistema de archivos en Python con Claude Desktop.

## 📋 Prerrequisitos

Antes de comenzar, asegúrate de tener:

- ✅ Python 3.10+ instalado
- ✅ Claude Desktop instalado
- ✅ Dependencias instaladas (`pip install -r requirements.txt`)

## 🔍 Paso 1: Verificar que Python funciona

Abre PowerShell o CMD y ejecuta:

```bash
python --version
```

Deberías ver algo como: `Python 3.10.x` o superior.

Si dice "Python no reconocido", instala Python desde [python.org](https://www.python.org/downloads/) y marca "Add Python to PATH".

## 📁 Paso 2: Verificar la ruta del servidor

Asegúrate de que el archivo del servidor existe en:

```
D:\SANDBOX\practica_03\src\filesystem_server.py
```

Puedes verificarlo desde PowerShell:

```bash
Test-Path "D:\SANDBOX\practica_03\src\filesystem_server.py"
```

Debe devolver `True`.

## ⚙️ Paso 3: Localizar el archivo de configuración de Claude

El archivo de configuración se encuentra en:

```
%APPDATA%\Claude\claude_desktop_config.json
```

Para abrirlo rápidamente:

### Opción A: Usar el Explorador de Windows

1. Presiona `Win + R`
2. Escribe: `%APPDATA%\Claude`
3. Presiona Enter
4. Busca el archivo `claude_desktop_config.json`

### Opción B: Usar PowerShell

```powershell
notepad "$env:APPDATA\Claude\claude_desktop_config.json"
```

## 📝 Paso 4: Configurar el servidor MCP

Abre el archivo `claude_desktop_config.json` y agrega tu servidor:

### Configuración Básica (Un directorio)

```json
{
  "mcpServers": {
    "filesystem-python": {
      "command": "python",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "D:\\SANDBOX\\practica_03"
      ]
    }
  }
}
```

### Configuración Avanzada (Múltiples directorios)

```json
{
  "mcpServers": {
    "filesystem-python": {
      "command": "python",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "D:\\SANDBOX\\practica_03",
        "D:\\SANDBOX\\practica_01",
        "C:\\Users\\TuUsuario\\Documents\\Proyectos"
      ]
    }
  }
}
```

### Si ya tienes otros servidores MCP

Si ya tienes otros servidores configurados, simplemente agrega el nuestro:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "D:\\otros\\directorios"]
    },
    "filesystem-python": {
      "command": "python",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "D:\\SANDBOX\\practica_03"
      ]
    }
  }
}
```

## ⚠️ Notas Importantes sobre las Rutas

1. **Usar doble barra invertida**: En JSON, usa `\\` en lugar de `\`
   - ✅ Correcto: `"D:\\SANDBOX\\practica_03"`
   - ❌ Incorrecto: `"D:\SANDBOX\practica_03"`

2. **Rutas absolutas**: Siempre usa rutas completas desde la raíz del disco

3. **Sin espacios al final**: Asegúrate de no dejar espacios extras

4. **Verificar existencia**: Los directorios deben existir antes de iniciar

## 🔄 Paso 5: Reiniciar Claude Desktop

Después de editar la configuración:

1. **Cierra completamente Claude Desktop**
   - Haz clic derecho en la bandeja del sistema (system tray)
   - Selecciona "Salir" o "Quit"
   - O usa el Administrador de Tareas para cerrar todos los procesos de Claude

2. **Reinicia Claude Desktop**
   - Abre Claude Desktop nuevamente
   - El servidor MCP se cargará automáticamente

## ✅ Paso 6: Verificar que funciona

Una vez que Claude Desktop esté abierto:

### Verificación Visual

Busca el icono 🔌 o 🔧 en la interfaz de Claude que indica herramientas disponibles.

### Verificación mediante Preguntas

Pregúntale a Claude:

```
¿Qué herramientas tienes disponibles?
```

Deberías ver algo como:
- `read_file`
- `write_file`
- `list_directory`
- etc.

### Prueba Práctica

Prueba con comandos simples:

```
Lista los archivos en el directorio D:\SANDBOX\practica_03
```

```
Lee el archivo README.md y dime de qué trata
```

```
Crea un archivo de prueba llamado test.txt con el contenido "Hola mundo"
```

## 🐛 Solución de Problemas

### Problema 1: El servidor no aparece en Claude

**Solución:**

1. Verifica el archivo de configuración:
   ```powershell
   cat "$env:APPDATA\Claude\claude_desktop_config.json"
   ```

2. Revisa los logs de Claude:
   ```powershell
   notepad "$env:APPDATA\Claude\logs\mcp.log"
   ```

3. Verifica que Python funciona:
   ```bash
   python -c "import mcp; print('MCP instalado correctamente')"
   ```

### Problema 2: Error "Python no encontrado"

**Solución:**

Si usas una ruta completa a Python en lugar de solo `python`:

```json
{
  "mcpServers": {
    "filesystem-python": {
      "command": "C:\\Python310\\python.exe",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "D:\\SANDBOX\\practica_03"
      ]
    }
  }
}
```

Para encontrar la ruta de Python:
```bash
where python
```

### Problema 3: Error "Acceso denegado"

**Solución:**

Asegúrate de que:
1. El directorio existe
2. Tienes permisos de lectura/escritura
3. No es un directorio del sistema protegido

Prueba con un directorio de usuario:
```json
"args": [
  "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
  "C:\\Users\\TuUsuario\\Documents"
]
```

### Problema 4: Claude no responde a comandos de archivos

**Solución:**

1. Verifica que estás usando rutas dentro de directorios permitidos
2. Prueba con rutas absolutas en tus preguntas:
   ```
   Lee el archivo D:\SANDBOX\practica_03\README.md
   ```

### Problema 5: Error en el JSON

**Solución:**

Valida tu JSON en [jsonlint.com](https://jsonlint.com/)

Errores comunes:
- Falta una coma
- Falta cerrar una llave `}`
- Falta cerrar un corchete `]`
- Comillas no cerradas

## 📊 Configuración Recomendada para Desarrollo

Para trabajar cómodamente en tus proyectos:

```json
{
  "mcpServers": {
    "filesystem-python": {
      "command": "python",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "D:\\SANDBOX",
        "C:\\Users\\TuUsuario\\Documents",
        "C:\\Users\\TuUsuario\\Desktop"
      ]
    }
  }
}
```

## 🔒 Mejores Prácticas de Seguridad

1. **Principio de Menor Privilegio**: Solo permite acceso a directorios necesarios
   - ✅ Bueno: `"D:\\SANDBOX\\practica_03"`
   - ❌ Malo: `"C:\\"`

2. **Directorios Específicos**: Evita directorios raíz o del sistema
   - ✅ Bueno: `"C:\\Users\\TuUsuario\\Proyectos"`
   - ❌ Malo: `"C:\\Windows"`

3. **Backups**: Mantén respaldos de archivos importantes

4. **Prueba Primero**: Prueba con directorios de prueba antes de usar directorios importantes

## 📝 Ejemplo de Configuración Completa

```json
{
  "mcpServers": {
    "filesystem-python": {
      "command": "python",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "D:\\SANDBOX\\practica_01",
        "D:\\SANDBOX\\practica_02",
        "D:\\SANDBOX\\practica_03"
      ]
    }
  }
}
```

## 🎯 Próximos Pasos

Una vez que todo funciona:

1. Experimenta con diferentes comandos
2. Crea archivos y directorios de prueba
3. Prueba búsquedas de archivos
4. Intenta operaciones más complejas

## 📚 Comandos Útiles para Probar

```
"Lista todos los archivos en D:\SANDBOX\practica_03"

"Lee el contenido del archivo README.md"

"Crea un directorio llamado 'tests' en D:\SANDBOX\practica_03"

"Busca todos los archivos .py en D:\SANDBOX\practica_03"

"Dame información sobre el archivo src/filesystem_server.py"

"Crea un archivo llamado notas.txt con una lista de tareas pendientes"

"Mueve el archivo test.txt a la carpeta tests"
```

## 🆘 Soporte

Si tienes problemas:

1. Revisa los logs en `%APPDATA%\Claude\logs\`
2. Verifica que Python y MCP estén instalados correctamente
3. Prueba el servidor manualmente desde la línea de comandos
4. Verifica que el JSON de configuración es válido

---

**¡Listo!** Ahora tienes tu servidor MCP de sistema de archivos funcionando con Claude Desktop.

**Próximo paso**: Lee [VSCODE_SETUP.md](VSCODE_SETUP.md) si quieres usar este servidor con VSCode.
