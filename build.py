"""
Скрипт для компиляции AI Hub в .exe
Запуск: python build.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# =============================================================================
# КОНФИГУРАЦИЯ
# =============================================================================

APP_NAME = "AI Hub"
BASE_DIR = Path(__file__).parent
BUILD_DIR = BASE_DIR / "build"
DIST_DIR = BASE_DIR / "dist"
SPEC_FILE = BASE_DIR / f"{APP_NAME}.spec"

# =============================================================================
# ФУНКЦИИ
# =============================================================================


def check_dependencies():
    """Проверить наличие PyInstaller."""
    print("🔍 Проверка зависимостей...")
    
    try:
        import PyInstaller
        print(f"   ✅ PyInstaller {PyInstaller.__version__}")
        return True
    except ImportError:
        print("   ❌ PyInstaller не установлен!")
        print("   Установите: pip install pyinstaller")
        return False


def clean_build():
    """Очистить папки сборки."""
    print("🧹 Очистка папок сборки...")
    
    for folder in [BUILD_DIR, DIST_DIR]:
        if folder.exists():
            shutil.rmtree(folder)
            print(f"   Удалено: {folder}")
    
    if SPEC_FILE.exists():
        SPEC_FILE.unlink()
        print(f"   Удалено: {SPEC_FILE}")


def build():
    """Собрать приложение."""
    print("📦 Сборка приложения...")
    
    # Команда для Windows (без PyQt5, используем edgechromium)
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", APP_NAME,
        "--windowed",      # Без консоли
        "--onefile",       # Один файл
        "--clean",         # Очистка
        "--exclude-module", "PyQt5",
        "--exclude-module", "PyQt6",
        "--exclude-module", "wx",
        "--add-data", f"{BASE_DIR / 'assets'}{os.pathsep}assets",
        "--hidden-import=webview",
        "--collect-all=webview",
        str(BASE_DIR / "main.py"),
    ]
    
    # Иконка (если есть)
    icon_file = BASE_DIR / "icon.ico"
    if icon_file.exists():
        cmd.extend(["--icon", str(icon_file)])
        print(f"   ✅ Иконка: {icon_file}")
    else:
        print(f"   ⚠️ Иконка не найдена: {icon_file}")
    
    print(f"   Команда: {' '.join(cmd)}")
    
    # Запуск сборки
    try:
        subprocess.run(cmd, check=True, cwd=str(BASE_DIR))
        print("   ✅ Сборка завершена!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Ошибка сборки: {e}")
        return False
    except FileNotFoundError:
        print("   ❌ PyInstaller не найден!")
        return False


def print_result(success: bool):
    """Вывести результат."""
    print("\n" + "=" * 50)
    
    if success:
        exe_path = DIST_DIR / f"{APP_NAME}.exe"
        print(f"🎉 Сборка успешна!")
        print(f"📁 Файл: {exe_path}")
        print(f"\nДля запуска:")
        print(f"   Дважды кликните по {APP_NAME}.exe")
    else:
        print("❌ Сборка не удалась!")
        print("Проверьте ошибки выше.")
    
    print("=" * 50)


# =============================================================================
# ТОЧКА ВХОДА
# =============================================================================


def main():
    """Точка входа."""
    print(f"🚀 Сборка {APP_NAME}")
    print("=" * 50)
    
    # Проверка
    if not check_dependencies():
        print_result(False)
        return
    
    # Очистка
    clean_build()
    
    # Сборка
    success = build()
    
    # Результат
    print_result(success)


if __name__ == "__main__":
    main()
