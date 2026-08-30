# Guía Rápida de Uso

## Instalación

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Verificar instalación
python src/filesystem_server.py --help
```

## Uso Rápido

### Con Claude Desktop

1. Edita `%APPDATA%\Claude\claude_desktop_config.json`:

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

2. Reinicia Claude Desktop

3. Prueba con: "Lista los archivos en este directorio"

### Con VSCode

1. Instala la extensión Claude Dev

2. Crea `.vscode/mcp_settings.json`:

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

3. Recarga VSCode (Ctrl+Shift+P → Reload Window)

## Comandos de Ejemplo

```
"Lee el archivo README.md"

"Lista todos los archivos Python en src/"

"Crea un archivo test.txt con contenido de ejemplo"

"Busca archivos .md en este proyecto"

"Dame información sobre filesystem_server.py"
```

## Herramientas Disponibles

- `read_file` - Leer archivos
- `write_file` - Escribir archivos
- `list_directory` - Listar directorios
- `create_directory` - Crear directorios
- `search_files` - Buscar archivos
- `get_file_info` - Info de archivos
- `delete_file` - Eliminar archivos
- `move_file` - Mover/renombrar archivos

## Troubleshooting

### Problema: Python no encontrado
```bash
where python
# Usa la ruta completa en la configuración
```

### Problema: MCP no instalado
```bash
pip install mcp
```

### Problema: Servidor no aparece
1. Revisa logs en `%APPDATA%\Claude\logs\`
2. Verifica JSON con jsonlint.com
3. Reinicia Claude Desktop completamente

## Documentación Completa

- Claude Desktop: `CLAUDE_DESKTOP_SETUP.md`
- VSCode: `VSCODE_SETUP.md`
- Proyecto: `README.md`
