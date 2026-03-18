"""
AI Hub — Лаунчер для ИИ-чатов
Версия: 5.6.0 (Modular)

Запуск: python main.py
"""

import os
import sys

# ВАЖНО: Отключаем все GUI бэкенды кроме edgechromium ДО импорта webview
os.environ['PYWEBVIEW_GUI'] = 'edgechromium'
os.environ['PYWEBVIEW_DISABLE_QT'] = '1'
os.environ['PYWEBVIEW_DISABLE_GTK'] = '1'
os.environ['PYWEBVIEW_DISABLE_CEF'] = '1'

import webview
from pathlib import Path
from typing import Dict, Optional

# Импорт модулей
from proverka import VersionChecker
from qwen import QwenCodeInstaller
from index import get_menu_html, get_chat_window_html

# =============================================================================
# КОНФИГУРАЦИЯ
# =============================================================================

APP_NAME = "AI Hub"
APP_VERSION = "5.6.0"
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"

# Репозиторий GitHub для проверки обновлений
GITHUB_REPO = "your-username/ai-hub"  # ЗАМЕНИТЕ на ваш репозиторий!

# Конфигурация ИИ-сервисов
AI_SERVICES = {
    "grok": {
        "name": "Grok",
        "url": "https://grok.x.ai/",
        "color": "#7c3aed",
        "color2": "#4c1d95",
        "icon": "🧠",
        "description": "ИИ от xAI",
        "features": ["Реальное время", "Доступ к X", "Без цензуры"]
    },
    "chatgpt": {
        "name": "ChatGPT",
        "url": "https://chatgpt.com/",
        "color": "#10a37f",
        "color2": "#0d8a6a",
        "icon": "💬",
        "description": "ИИ от OpenAI",
        "features": ["Универсальный", "Плагины", "GPT-4"]
    },
    "claude": {
        "name": "Claude",
        "url": "https://claude.ai/",
        "color": "#d97757",
        "color2": "#9a4f3a",
        "icon": "🎭",
        "description": "ИИ от Anthropic",
        "features": ["Безопасный", "Анализ файлов", "Длинный контекст"]
    },
    "qwen": {
        "name": "Qwen",
        "url": "https://chat.qwen.ai/",
        "color": "#3b82f6",
        "color2": "#1d4ed8",
        "icon": "🌊",
        "description": "ИИ от Alibaba",
        "features": ["Мультиязычный", "Кодирование", "Анализ"]
    },
    "deepseek": {
        "name": "DeepSeek",
        "url": "https://chat.deepseek.com/",
        "color": "#06b6d4",
        "color2": "#0e7490",
        "icon": "🔮",
        "description": "Глубокий поиск",
        "features": ["Поиск в вебе", "Анализ", "Бесплатный"]
    },
    "qwen-code": {
        "name": "Qwen Code",
        "url": "",
        "color": "#6366f1",
        "color2": "#4f46e5",
        "icon": "💻",
        "description": "Qwen Code CLI",
        "features": ["CLI инструмент", "Автономный", "Умный"],
        "is_cli": True
    }
}

# Глобальное состояние
current_view = "menu"  # "menu" или "chat"
current_service_id: Optional[str] = None
chat_windows: Dict[str, webview.Window] = {}  # Словарь окон чатов

# Глобальные объекты
_main_window: Optional[webview.Window] = None
_chat_window: Optional[webview.Window] = None
_version_checker: Optional[VersionChecker] = None
_qwen_installer: Optional[QwenCodeInstaller] = None


# =============================================================================
# API ДЛЯ JS
# =============================================================================


class API:
    """Мост между JavaScript и Python (главное окно)."""

    def __init__(self):
        global _version_checker, _qwen_installer
        _version_checker = VersionChecker(GITHUB_REPO, APP_VERSION)
        _qwen_installer = QwenCodeInstaller()

    # Методы для JS
    def minimize_window(self):
        if _main_window:
            _main_window.minimize()

    def toggle_maximize(self):
        if _main_window:
            if hasattr(_main_window, 'maximized') and _main_window.maximized:
                _main_window.restore()
            else:
                _main_window.maximize()

    def open_chat(self, service_id: str):
        """Открыть чат в отдельном окне WebView с прямым URL."""
        global chat_windows, _main_window

        service = AI_SERVICES.get(service_id)
        if not service:
            return

        # Если уже открыто - фокус на существующее
        if service_id in chat_windows:
            try:
                chat_windows[service_id].show()
                chat_windows[service_id].restore()
                chat_windows[service_id].focus()
                print(f"Окно {service['name']} уже открыто, активируем")
                return
            except:
                if service_id in chat_windows:
                    del chat_windows[service_id]

        print(f"Открываем {service['name']}...")

        # Создаём окно с ПРЯМЫМ URL (не iframe!)
        try:
            chat_window = webview.create_window(
                title=f"{service['name']} — {APP_NAME}",
                url=service["url"],
                width=1200,
                height=800,
                min_size=(900, 600),
                resizable=True,
                fullscreen=False,
                frameless=True,
                easy_drag=True,
                text_select=True,
                background_color="#0a0a0f",
            )
            chat_windows[service_id] = chat_window
            print(f"Window {service['name']} created (total: {len(chat_windows)})")
        except Exception as e:
            print(f"Error: {e}")
            import webbrowser
            webbrowser.open(service["url"])

    def back_to_menu(self):
        """Вернуться в меню."""
        global _main_window

        print("Возврат в меню...")
        if _main_window:
            _main_window.show()
            _main_window.restore()

    def quit_app(self):
        """Закрыть приложение."""
        print("Закрытие приложения...")
        # Закрываем все окна чатов
        for win in list(chat_windows.values()):
            try:
                win.destroy()
            except:
                pass
        chat_windows.clear()
        # Закрываем главное окно
        if _main_window:
            _main_window.destroy()

    def log_message(self, message: str):
        print(f"[JS] {message}")

    def check_for_updates(self):
        """Проверить наличие новой версии через GitHub API."""
        global _version_checker
        if _version_checker:
            result = _version_checker.check_for_updates()
            if result.get("has_update"):
                print(f"🎉 Доступна новая версия: {result['latest']}")
                print(f"Дата выпуска: {result['release_date']}")
                print(f"Изменения: {result['notes']}")
            else:
                print("✅ Установлена актуальная версия")
            return result
        return {"has_update": False, "current": APP_VERSION, "latest": APP_VERSION}

    def install_qwen_code(self):
        """Установить Qwen Code через npm/winget/choco."""
        global _qwen_installer
        if _qwen_installer:
            return _qwen_installer.install()
        return {"success": False, "method": None}


# =============================================================================
# ЗАПУСК
# =============================================================================


def main():
    """Точка входа."""
    global _main_window

    print(f"{APP_NAME} v{APP_VERSION}")
    print(f"Directory: {BASE_DIR}")
    print(f"Services: {', '.join(AI_SERVICES.keys())}")
    print("-" * 50)

    api = API()

    # Создаём главное окно с меню
    _main_window = webview.create_window(
        title=APP_NAME,
        html=get_menu_html(APP_VERSION, AI_SERVICES),
        width=1200,
        height=800,
        min_size=(1000, 700),
        resizable=True,
        fullscreen=False,
        frameless=True,
        easy_drag=True,
        text_select=True,
        background_color="#0a0a0f",
        js_api=api,
    )

    print("Starting...")
    webview.start()
    print("Finished")


if __name__ == "__main__":
    main()
