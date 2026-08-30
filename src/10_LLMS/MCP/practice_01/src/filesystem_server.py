#!/usr/bin/env python3
"""
MCP Filesystem Server - Servidor de sistema de archivos para Claude
Proporciona operaciones de lectura/escritura de archivos en directorios permitidos
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Any, Sequence
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from mcp.server.models import InitializationOptions
    from mcp.server import NotificationOptions, Server
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        Resource,
        Tool,
        TextContent,
        ImageContent,
        EmbeddedResource,
    )
except ImportError:
    logger.error("Error: El paquete 'mcp' no está instalado. Ejecuta: pip install mcp")
    sys.exit(1)


class FilesystemServer:
    """Servidor MCP para operaciones de sistema de archivos"""
    
    def __init__(self, allowed_directories: list[str]):
        """
        Inicializa el servidor con directorios permitidos
        
        Args:
            allowed_directories: Lista de rutas absolutas permitidas
        """
        self.allowed_directories = [Path(d).resolve() for d in allowed_directories]
        self.server = Server("filesystem-mcp-server")
        
        # Verificar que los directorios existen
        for directory in self.allowed_directories:
            if not directory.exists():
                logger.warning(f"Directorio no existe: {directory}")
            else:
                logger.info(f"Directorio permitido: {directory}")
        
        self._setup_handlers()
    
    def _is_path_allowed(self, path: Path) -> bool:
        """Verifica si una ruta está dentro de los directorios permitidos"""
        try:
            resolved_path = path.resolve()
            return any(
                resolved_path == allowed_dir or 
                resolved_path.is_relative_to(allowed_dir)
                for allowed_dir in self.allowed_directories
            )
        except Exception as e:
            logger.error(f"Error verificando ruta: {e}")
            return False
    
    def _setup_handlers(self):
        """Configura los manejadores de herramientas y recursos"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            """Lista todas las herramientas disponibles"""
            return [
                Tool(
                    name="read_file",
                    description="Lee el contenido completo de un archivo",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Ruta del archivo a leer"
                            }
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="write_file",
                    description="Escribe contenido en un archivo (crea o sobrescribe)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Ruta del archivo a escribir"
                            },
                            "content": {
                                "type": "string",
                                "description": "Contenido a escribir en el archivo"
                            }
                        },
                        "required": ["path", "content"]
                    }
                ),
                Tool(
                    name="list_directory",
                    description="Lista archivos y directorios en una ruta",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Ruta del directorio a listar"
                            }
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="create_directory",
                    description="Crea un nuevo directorio",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Ruta del directorio a crear"
                            }
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="search_files",
                    description="Busca archivos por nombre o patrón",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "directory": {
                                "type": "string",
                                "description": "Directorio donde buscar"
                            },
                            "pattern": {
                                "type": "string",
                                "description": "Patrón de búsqueda (ej: *.py, README*)"
                            }
                        },
                        "required": ["directory", "pattern"]
                    }
                ),
                Tool(
                    name="get_file_info",
                    description="Obtiene información detallada de un archivo",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Ruta del archivo"
                            }
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="delete_file",
                    description="Elimina un archivo",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Ruta del archivo a eliminar"
                            }
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="move_file",
                    description="Mueve o renombra un archivo",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "source": {
                                "type": "string",
                                "description": "Ruta origen"
                            },
                            "destination": {
                                "type": "string",
                                "description": "Ruta destino"
                            }
                        },
                        "required": ["source", "destination"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent]:
            """Maneja las llamadas a las herramientas"""
            
            try:
                if name == "read_file":
                    return await self._read_file(arguments["path"])
                    
                elif name == "write_file":
                    return await self._write_file(arguments["path"], arguments["content"])
                    
                elif name == "list_directory":
                    return await self._list_directory(arguments["path"])
                    
                elif name == "create_directory":
                    return await self._create_directory(arguments["path"])
                    
                elif name == "search_files":
                    return await self._search_files(arguments["directory"], arguments["pattern"])
                    
                elif name == "get_file_info":
                    return await self._get_file_info(arguments["path"])
                    
                elif name == "delete_file":
                    return await self._delete_file(arguments["path"])
                    
                elif name == "move_file":
                    return await self._move_file(arguments["source"], arguments["destination"])
                    
                else:
                    raise ValueError(f"Herramienta desconocida: {name}")
                    
            except Exception as e:
                logger.error(f"Error ejecutando {name}: {e}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def _read_file(self, path: str) -> Sequence[TextContent]:
        """Lee un archivo"""
        file_path = Path(path)
        
        if not self._is_path_allowed(file_path):
            raise ValueError(f"Acceso denegado: {path}")
        
        if not file_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {path}")
        
        try:
            content = file_path.read_text(encoding='utf-8')
            return [TextContent(type="text", text=content)]
        except UnicodeDecodeError:
            # Si no es texto, intentar leer como binario
            content = file_path.read_bytes()
            return [TextContent(type="text", text=f"Archivo binario, tamaño: {len(content)} bytes")]
    
    async def _write_file(self, path: str, content: str) -> Sequence[TextContent]:
        """Escribe un archivo"""
        file_path = Path(path)
        
        if not self._is_path_allowed(file_path):
            raise ValueError(f"Acceso denegado: {path}")
        
        # Crear directorios padres si no existen
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_path.write_text(content, encoding='utf-8')
        return [TextContent(type="text", text=f"Archivo escrito exitosamente: {path}")]
    
    async def _list_directory(self, path: str) -> Sequence[TextContent]:
        """Lista contenido de un directorio"""
        dir_path = Path(path)
        
        if not self._is_path_allowed(dir_path):
            raise ValueError(f"Acceso denegado: {path}")
        
        if not dir_path.exists():
            raise FileNotFoundError(f"Directorio no encontrado: {path}")
        
        if not dir_path.is_dir():
            raise ValueError(f"No es un directorio: {path}")
        
        items = []
        for item in sorted(dir_path.iterdir()):
            item_type = "[DIR]" if item.is_dir() else "[FILE]"
            items.append(f"{item_type} {item.name}")
        
        result = "\n".join(items) if items else "Directorio vacío"
        return [TextContent(type="text", text=result)]
    
    async def _create_directory(self, path: str) -> Sequence[TextContent]:
        """Crea un directorio"""
        dir_path = Path(path)
        
        if not self._is_path_allowed(dir_path):
            raise ValueError(f"Acceso denegado: {path}")
        
        dir_path.mkdir(parents=True, exist_ok=True)
        return [TextContent(type="text", text=f"Directorio creado: {path}")]
    
    async def _search_files(self, directory: str, pattern: str) -> Sequence[TextContent]:
        """Busca archivos por patrón"""
        dir_path = Path(directory)
        
        if not self._is_path_allowed(dir_path):
            raise ValueError(f"Acceso denegado: {directory}")
        
        if not dir_path.exists():
            raise FileNotFoundError(f"Directorio no encontrado: {directory}")
        
        matches = list(dir_path.rglob(pattern))
        
        if not matches:
            return [TextContent(type="text", text="No se encontraron archivos")]
        
        results = [str(match.relative_to(dir_path)) for match in matches]
        return [TextContent(type="text", text="\n".join(results))]
    
    async def _get_file_info(self, path: str) -> Sequence[TextContent]:
        """Obtiene información de un archivo"""
        file_path = Path(path)
        
        if not self._is_path_allowed(file_path):
            raise ValueError(f"Acceso denegado: {path}")
        
        if not file_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {path}")
        
        stat = file_path.stat()
        info = {
            "nombre": file_path.name,
            "ruta_completa": str(file_path),
            "tamaño": f"{stat.st_size} bytes",
            "tipo": "Directorio" if file_path.is_dir() else "Archivo",
            "última_modificación": stat.st_mtime,
        }
        
        return [TextContent(type="text", text=json.dumps(info, indent=2, ensure_ascii=False))]
    
    async def _delete_file(self, path: str) -> Sequence[TextContent]:
        """Elimina un archivo"""
        file_path = Path(path)
        
        if not self._is_path_allowed(file_path):
            raise ValueError(f"Acceso denegado: {path}")
        
        if not file_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {path}")
        
        if file_path.is_dir():
            raise ValueError("Use rmdir para eliminar directorios")
        
        file_path.unlink()
        return [TextContent(type="text", text=f"Archivo eliminado: {path}")]
    
    async def _move_file(self, source: str, destination: str) -> Sequence[TextContent]:
        """Mueve o renombra un archivo"""
        source_path = Path(source)
        dest_path = Path(destination)
        
        if not self._is_path_allowed(source_path):
            raise ValueError(f"Acceso denegado (origen): {source}")
        
        if not self._is_path_allowed(dest_path):
            raise ValueError(f"Acceso denegado (destino): {destination}")
        
        if not source_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {source}")
        
        source_path.rename(dest_path)
        return [TextContent(type="text", text=f"Archivo movido: {source} -> {destination}")]
    
    async def run(self):
        """Ejecuta el servidor MCP"""
        logger.info("Iniciando servidor MCP Filesystem...")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="filesystem-mcp-server",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )


def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("Error: Debe proporcionar al menos un directorio permitido")
        print("Uso: python filesystem_server.py <directorio1> [directorio2] ...")
        sys.exit(1)
    
    allowed_directories = sys.argv[1:]
    
    logger.info(f"Servidor MCP Filesystem iniciando con directorios: {allowed_directories}")
    
    server = FilesystemServer(allowed_directories)
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
