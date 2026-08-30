#!/usr/bin/env python3
"""
Script de prueba para verificar que el servidor MCP funciona correctamente
"""

import sys
from pathlib import Path

def test_imports():
    """Verifica que las dependencias están instaladas"""
    print("🔍 Verificando dependencias...")
    
    try:
        import mcp
        print("✅ Paquete 'mcp' instalado correctamente")
        return True
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("   Ejecuta: pip install mcp")
        return False

def test_server_file():
    """Verifica que el archivo del servidor existe"""
    print("\n🔍 Verificando archivo del servidor...")
    
    server_path = Path(__file__).parent / "src" / "filesystem_server.py"
    
    if server_path.exists():
        print(f"✅ Servidor encontrado en: {server_path}")
        return True
    else:
        print(f"❌ Servidor no encontrado en: {server_path}")
        return False

def test_python_version():
    """Verifica la versión de Python"""
    print("\n🔍 Verificando versión de Python...")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 10:
        print(f"✅ Python {version_str} (compatible)")
        return True
    else:
        print(f"❌ Python {version_str} (se requiere 3.10+)")
        return False

def test_directories():
    """Verifica que los directorios necesarios existen"""
    print("\n🔍 Verificando estructura de directorios...")
    
    base_path = Path(__file__).parent
    directories = {
        "src": base_path / "src",
        "raíz": base_path
    }
    
    all_ok = True
    for name, path in directories.items():
        if path.exists():
            print(f"✅ Directorio '{name}': {path}")
        else:
            print(f"❌ Directorio '{name}' no encontrado: {path}")
            all_ok = False
    
    return all_ok

def test_server_import():
    """Intenta importar el servidor"""
    print("\n🔍 Intentando importar el servidor...")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        from filesystem_server import FilesystemServer
        print("✅ Servidor se puede importar correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al importar servidor: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("🧪 TEST DE CONFIGURACIÓN DEL SERVIDOR MCP")
    print("=" * 60)
    
    tests = [
        ("Versión de Python", test_python_version),
        ("Dependencias", test_imports),
        ("Archivo del servidor", test_server_file),
        ("Estructura de directorios", test_directories),
        ("Importación del servidor", test_server_import),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error inesperado en '{name}': {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n📈 Resultado: {passed}/{total} pruebas pasadas")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron!")
        print("\n📝 Próximos pasos:")
        print("   1. Lee CLAUDE_DESKTOP_SETUP.md para configurar Claude Desktop")
        print("   2. Lee VSCODE_SETUP.md para configurar VSCode")
        print("   3. Lee QUICKSTART.md para empezar rápidamente")
        return 0
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
        print("\n📝 Soluciones comunes:")
        print("   - Instalar Python 3.10+")
        print("   - Ejecutar: pip install -r requirements.txt")
        print("   - Verificar que estás en el directorio correcto")
        return 1

if __name__ == "__main__":
    sys.exit(main())
