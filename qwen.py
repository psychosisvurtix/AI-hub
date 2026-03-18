"""
qwen.py — Установка Qwen Code CLI
Версия: 1.0.0
"""

import subprocess
import shutil
import sys


class QwenCodeInstaller:
    """Установка Qwen Code через npm/winget/choco."""
    
    def __init__(self):
        self.package_name = "@qwen-code/qwen-code"
        self.package_version = "0.12.6"
    
    def check_command(self, cmd: str) -> bool:
        """Проверить доступность команды."""
        return shutil.which(cmd) is not None
    
    def run_install_command(self, cmd: str, args: list, run_after: str = None) -> bool:
        """Выполнить команду установки в новом CMD окне."""
        try:
            print(f"Выполнение: {cmd} {' '.join(args)}")
            
            if sys.platform == 'win32':
                # Открываем новое CMD окно для Windows
                install_cmd = f'{cmd} {" ".join(args)}'
                if run_after:
                    # После установки запускаем qwen
                    command = f'start "Qwen Code" cmd /k "{install_cmd} && echo. && echo ✅ Qwen Code установлен! && echo. && echo 🚀 Запуск Qwen Code... && echo. && {run_after}"'
                else:
                    command = f'start "Qwen Code Installation" cmd /k "{install_cmd} & pause"'
                subprocess.Popen(
                    command,
                    shell=True,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                # Для Linux/macOS
                subprocess.run(
                    [cmd] + args,
                    shell=True,
                    check=True
                )
                if run_after:
                    subprocess.run(run_after, shell=True)
            return True
        except Exception as e:
            print(f"Ошибка {cmd}: {e}")
            return False
    
    def install(self) -> dict:
        """Установить Qwen Code через npm/winget/choco."""
        print("Установка Qwen Code...")
        
        # Пробуем npm
        if self.check_command("npm"):
            print("npm найден, установка через npm...")
            if self.run_install_command("npm", ["install", "-g", f"{self.package_name}@{self.package_version}"], run_after="qwen"):
                print("Qwen Code успешно установлен через npm")
                return {"success": True, "method": "npm"}
        
        # Пробуем winget
        if self.check_command("winget"):
            print("winget найден, установка через winget...")
            if self.run_install_command("winget", ["install", "-e", "-i", "Qwen.QwenCode"], run_after="qwen"):
                print("Qwen Code успешно установлен через winget")
                return {"success": True, "method": "winget"}
        
        # Пробуем choco
        if self.check_command("choco"):
            print("choco найден, установка через choco...")
            if self.run_install_command("choco", ["install", "qwen-code", "-y"], run_after="qwen"):
                print("Qwen Code успешно установлен через choco")
                return {"success": True, "method": "choco"}
        
        print("Не удалось установить Qwen Code - ни один менеджер пакетов не найден")
        return {"success": False, "method": None}
    
    def is_installed(self) -> bool:
        """Проверить, установлен ли Qwen Code."""
        return self.check_command("qwen-code")
