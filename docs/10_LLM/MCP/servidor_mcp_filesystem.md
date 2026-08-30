# MCP Filesystem Server - Servidor de Sistema de Archivos para Claude

Este proyecto implementa un servidor MCP (Model Context Protocol) en Python que permite a Claude interactuar con el sistema de archivos de Windows de manera segura y controlada.

## ¿Qué es este proyecto?

Un servidor MCP personalizado que expone operaciones de sistema de archivos a Claude, permitiéndole:
- Leer y escribir archivos
- Listar directorios
- Buscar archivos
- Crear y eliminar archivos/directorios
- Mover y renombrar archivos
- Obtener información detallada de archivos

## Seguridad

El servidor solo permite acceso a directorios específicamente autorizados que definiremos al configurarlo. Claude **no puede** acceder a ningún archivo fuera de estos directorios permitidos.

## Requisitos

- Python 3.10+
- Claude Desktop (para uso con Claude)
- VSCode con extensión Claude (opcional, para uso en VSCode)

## Instalación Rápida

1. **Instalar dependencias**:
   ```bash
   cd src/10_LLMS/MCP/practice_01
   pip install -r requirements.txt
   ```

2. **Verificar instalación**:
   ```bash
   python src/filesystem_server.py --help
   ```

## Estructura del Proyecto

```text

├── src/
│   └── filesystem_server.py    # Servidor MCP principal
├── requirements.txt             # Dependencias Python
├── README.md                    # Archivo con la estructura del proyecto
├── CLAUDE_DESKTOP_SETUP.md      # Instrucciones para Claude Desktop
└── VSCODE_SETUP.md              # Instrucciones para VSCode
```

## 🛠️ Herramientas Disponibles

El servidor MCP proporciona las siguientes herramientas a Claude:

| Herramienta | Descripción |
|-------------|-------------|
| `read_file` | Lee el contenido de un archivo |
| `write_file` | Escribe contenido en un archivo |
| `list_directory` | Lista archivos y directorios |
| `create_directory` | Crea un nuevo directorio |
| `search_files` | Busca archivos por patrón |
| `get_file_info` | Obtiene metadatos de un archivo |
| `delete_file` | Elimina un archivo |
| `move_file` | Mueve o renombra un archivo |

## 🎮 Uso Básico

### Prueba Manual (sin Claude)

Puedes probar el servidor directamente desde la línea de comandos:

```bash
python src/filesystem_server.py "D:\SANDBOX\practica_03"
```

El servidor quedará en espera de comandos. Para probarlo, necesitas enviarle mensajes JSON en formato MCP.

### Uso con Claude Desktop

Lee las instrucciones detalladas en el archivo **`CLAUDE_DESKTOP_SETUP.md`** que se genera en la raiz del proyecto.

### Uso con VSCode

Lee las instrucciones detalladas en el archivo **`VSCODE_SETUP.md`** que se genera en la raiz del proyecto.

## 📝 Ejemplos de Uso con Claude

Una vez configurado, puedes pedirle a Claude cosas como:

```text
"Lee el archivo README.md y dime de qué trata"

"Crea un archivo llamado notas.txt con una lista de tareas"

"Busca todos los archivos .py en este directorio"

"Lista todos los archivos en la carpeta src"

"Dame información sobre el archivo filesystem_server.py"
```

## 🔧 Configuración Avanzada

### Múltiples Directorios Permitidos

Puedes permitir acceso a múltiples directorios:

```json
{
  "mcpServers": {
    "filesystem-python": {
      "command": "python",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "D:\\SANDBOX\\practica_03",
        "D:\\MisProyectos",
        "C:\\Users\\TuUsuario\\Documents"
      ]
    }
  }
}
```

### Variables de Entorno

Puedes usar variables de entorno para configurar rutas:

```json
{
  "mcpServers": {
    "filesystem-python": {
      "command": "python",
      "args": [
        "D:\\SANDBOX\\practica_03\\src\\filesystem_server.py",
        "${WORKSPACE_DIR}",
        "${DOCUMENTS_DIR}"
      ],
      "env": {
        "WORKSPACE_DIR": "D:\\SANDBOX",
        "DOCUMENTS_DIR": "C:\\Users\\TuUsuario\\Documents"
      }
    }
  }
}
```

## 🐛 Solución de Problemas

### Error: "No module named 'mcp'"

```bash
pip install mcp
```

### Error: "Python no reconocido como comando"

Asegúrate de que Python está en tu PATH. Reinstala Python y marca "Add Python to PATH".

### Error: "Acceso denegado"

Verifica que:
1. Los directorios permitidos existen
2. Tienes permisos de lectura/escritura en esos directorios
3. Las rutas están escritas correctamente (usa `\\` en Windows)

### El servidor no aparece en Claude

1. Cierra completamente Claude Desktop
2. Verifica el archivo de configuración `claude_desktop_config.json`
3. Revisa los logs en `%APPDATA%\Claude\logs\`
4. Reinicia Claude Desktop

## 📚 Recursos Adicionales

- [Documentación oficial MCP](https://modelcontextprotocol.io)
- [Especificación del protocolo](https://spec.modelcontextprotocol.io)
- [SDK Python de MCP](https://github.com/modelcontextprotocol/python-sdk)

## 🤝 Contribuciones

Este es un proyecto educativo. Siéntete libre de:
- Agregar más herramientas
- Mejorar la seguridad
- Optimizar el rendimiento
- Documentar mejores prácticas

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

## ⚠️ Advertencias

- **Seguridad**: Solo permite directorios en los que confías
- **Permisos**: Claude puede leer/escribir/eliminar archivos en directorios permitidos
- **Backups**: Mantén respaldos de archivos importantes
- **Producción**: Este es un proyecto educativo, no para uso en producción sin auditoría de seguridad

---

**Versión**: 1.0.0  
**Autor**: Proyecto Educativo MCP  
**Última actualización**: Noviembre 2025
