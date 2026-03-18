"""
index.py — HTML генератор для AI Hub
Версия: 5.6.0
"""

import json
from typing import Dict


def get_menu_html(app_version: str, services: Dict) -> str:
    """HTML главного меню."""
    services_json = json.dumps(services)

    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Hub</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: transparent;
            color: #ffffff;
            overflow: hidden;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }}

        /* Эффект 240 Гц монитора */
        * {{
            transition-timing-function: cubic-bezier(0.34, 1.56, 0.64, 1);
        }}

        html {{
            scroll-behavior: smooth;
        }}
        
        /* Закруглённый контейнер */
        .app-container {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: #0a0a0f;
            border-radius: 16px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1);
        }}

        /* Titlebar macOS */
        .titlebar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 52px;
            padding: 0 16px;
            background: linear-gradient(180deg, #1a1a25 0%, #12121a 100%);
            border-bottom: 1px solid #1f1f2e;
            -webkit-app-region: drag;
            flex-shrink: 0;
        }}

        .titlebar-left {{
            display: flex;
            align-items: center;
            gap: 14px;
            -webkit-app-region: no-drag;
            flex: 1;
        }}

        .titlebar-right {{
            display: flex;
            align-items: center;
            gap: 14px;
            -webkit-app-region: no-drag;
        }}

        .window-controls {{
            display: flex;
            gap: 8px;
        }}

        .mac-btn {{
            width: 14px;
            height: 14px;
            border-radius: 50%;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
            -webkit-app-region: no-drag;
        }}

        .mac-btn:hover {{
            transform: scale(1.15);
        }}

        .mac-btn.close {{
            background: linear-gradient(180deg, #ff5f57 0%, #ff3b30 100%);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.3), 0 1px 2px rgba(0,0,0,0.3);
        }}

        .mac-btn.minimize {{
            background: linear-gradient(180deg, #febc2e 0%, #ff9500 100%);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.3), 0 1px 2px rgba(0,0,0,0.3);
        }}

        .mac-btn.maximize {{
            background: linear-gradient(180deg, #28c840 0%, #34c759 100%);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.3), 0 1px 2px rgba(0,0,0,0.3);
        }}
        
        .logo {{ font-size: 22px; }}
        
        .app-name {{
            font-size: 16px;
            font-weight: 600;
            background: linear-gradient(135deg, #6366f1, #8b5cf6, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .version {{
            font-size: 10px;
            padding: 2px 8px;
            background: #1a1a25;
            border: 1px solid #252535;
            border-radius: 10px;
            color: #555560;
        }}

        /* Контент */
        .main-content {{
            flex: 1;
            overflow-y: auto;
            padding: 40px;
            opacity: 1;
            transition: opacity 0.3s ease;
        }}

        .main-content.hiding {{
            opacity: 0;
        }}

        .hero {{
            text-align: center;
            padding: 30px 0 60px;
        }}

        .hero-icon {{
            font-size: 72px;
            margin-bottom: 20px;
            filter: drop-shadow(0 0 30px rgba(99, 102, 241, 0.4));
        }}

        .hero-title {{
            font-size: 44px;
            font-weight: 700;
            background: linear-gradient(135deg, #6366f1, #8b5cf6, #c084fc, #e879f9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 16px;
        }}

        .hero-subtitle {{
            font-size: 17px;
            color: #a1a1aa;
            max-width: 500px;
            margin: 0 auto;
        }}

        /* Карточки */
        .cards-section {{
            max-width: 1100px;
            margin: 0 auto;
        }}

        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 24px;
        }}

        .card {{
            background: linear-gradient(180deg, #1a1a25, #15151f);
            border-radius: 16px;
            padding: 28px 24px;
            cursor: pointer;
            transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
            border: 1px solid #252535;
            position: relative;
            overflow: hidden;
        }}

        .card:hover {{
            transform: translateY(-8px) scale(1.02);
            border-color: var(--color);
            box-shadow: 0 10px 40px var(--shadow), 0 0 60px var(--shadow-glow);
        }}

        .card-content {{
            position: relative;
            z-index: 1;
            text-align: center;
        }}

        .card-icon {{
            width: 72px;
            height: 72px;
            margin: 0 auto 16px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 36px;
            background: var(--color);
            box-shadow: 0 4px 20px var(--shadow);
            transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        }}

        .card:hover .card-icon {{
            transform: scale(1.1) rotate(5deg);
        }}

        .card-title {{
            font-size: 19px;
            font-weight: 700;
            margin-bottom: 6px;
            color: #fff;
        }}

        .card-desc {{
            font-size: 13px;
            color: #a1a1aa;
            margin-bottom: 16px;
        }}

        .card-features {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 6px;
            margin-bottom: 14px;
        }}

        .card-feature {{
            font-size: 11px;
            padding: 4px 10px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            color: #d4d4d8;
            font-weight: 500;
        }}

        .card-dots {{
            display: flex;
            justify-content: center;
            gap: 6px;
        }}

        .card-dots span {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            border: 2px solid #1a1a25;
        }}

        .footer {{
            text-align: center;
            padding: 20px 0;
            color: #555560;
            font-size: 12px;
            border-top: 1px solid #1a1a25;
            margin-top: 40px;
        }}

        /* Скроллбар */
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: #12121a; }}
        ::-webkit-scrollbar-thumb {{ background: #333340; border-radius: 4px; }}

        /* Анимация свёртывания */
        .minimize-animation {{
            animation: minimizeWindow 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        @keyframes minimizeWindow {{
            0% {{
                transform: scale(1) translateY(0);
                opacity: 1;
            }}
            100% {{
                transform: scale(0.8) translateY(50px);
                opacity: 0.5;
            }}
        }}

        /* Анимация развёртывания */
        .restore-animation {{
            animation: restoreWindow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        @keyframes restoreWindow {{
            0% {{
                transform: scale(0.8) translateY(50px);
                opacity: 0.5;
            }}
            100% {{
                transform: scale(1) translateY(0);
                opacity: 1;
            }}
        }}

        /* Анимации */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateX(30px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}

        .hero {{ animation: fadeIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) backwards; }}
        .card {{ animation: fadeIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) backwards; }}
        .card:nth-child(1) {{ animation-delay: 0.05s; }}
        .card:nth-child(2) {{ animation-delay: 0.1s; }}
        .card:nth-child(3) {{ animation-delay: 0.15s; }}
        .card:nth-child(4) {{ animation-delay: 0.2s; }}
        .card:nth-child(5) {{ animation-delay: 0.25s; }}
        .card:nth-child(6) {{ animation-delay: 0.3s; }}

        /* Fullscreen анимация */
        .fullscreen-transition {{
            animation: fullscreenExpand 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        }}

        @keyframes fullscreenExpand {{
            from {{
                transform: scale(0.92) translateY(20px);
                opacity: 0.7;
                filter: blur(10px);
            }}
            to {{
                transform: scale(1) translateY(0);
                opacity: 1;
                filter: blur(0);
            }}
        }}

        .fullscreen-exit {{
            animation: fullscreenCollapse 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        }}

        @keyframes fullscreenCollapse {{
            from {{
                transform: scale(1);
                opacity: 1;
                filter: blur(0);
            }}
            to {{
                transform: scale(0.92) translateY(20px);
                opacity: 0.7;
                filter: blur(10px);
            }}
        }}

        /* Кнопка выхода из fullscreen */
        .fullscreen-exit-btn {{
            position: fixed;
            top: 20px;
            right: 20px;
            width: 40px;
            height: 40px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            cursor: pointer;
            display: none;
            align-items: center;
            justify-content: center;
            transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
            z-index: 1000;
            -webkit-app-region: no-drag;
        }}

        .fullscreen-exit-btn:hover {{
            background: rgba(255, 59, 48, 0.8);
            transform: scale(1.1);
            box-shadow: 0 4px 20px rgba(255, 59, 48, 0.4);
        }}

        .fullscreen-exit-btn svg {{
            width: 20px;
            height: 20px;
            fill: #ffffff;
        }}

        .fullscreen-exit-btn.visible {{
            display: flex;
        }}
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Заголовок macOS -->
        <div class="titlebar">
            <div class="titlebar-left">
                <span class="logo">🧠</span>
                <span class="app-name">AI Hub</span>
                <span class="version">v{app_version}</span>
            </div>
            <div class="titlebar-right">
                <div class="window-controls">
                    <button class="mac-btn close" onclick="closeApp()" title="Закрыть"></button>
                    <button class="mac-btn minimize" onclick="minimizeWindow()" title="Свернуть"></button>
                    <button class="mac-btn maximize" onclick="toggleMaximize()" title="Развернуть"></button>
                </div>
            </div>
        </div>

        <!-- Кнопка выхода из fullscreen -->
        <button class="fullscreen-exit-btn" id="fullscreenExitBtn" onclick="exitFullscreen()" title="Выйти из полноэкранного режима">
            <svg viewBox="0 0 24 24"><path d="M5 16H3v4h2v-4zm14 0h2v4h-2v-4zM3 5v4h2V5H3zm18 0v4h-2V5h2zM17 17h-4v4h-2v-4H7v-2h4v-4h2v4h4v2z"/></svg>
        </button>

        <!-- Контент -->
        <div class="main-content" id="mainContent">
        <section class="hero">
            <div class="hero-icon">🧠</div>
            <h1 class="hero-title">Добро пожаловать в AI Hub</h1>
            <p class="hero-subtitle">Ваш универсальный лаунчер для ведущих языковых моделей ИИ</p>
        </section>

        <section class="cards-section">
            <div class="cards-grid" id="cardsGrid"></div>
        </section>

        <footer class="footer">
            <p>AI Hub © 2026 • v{app_version}</p>
        </footer>
    </div>

    <script>
        const SERVICES = {services_json};
        let isOpening = false;

        document.addEventListener('DOMContentLoaded', () => {{
            console.log('🚀 AI Hub запущен');
            renderCards();
            checkForUpdates();
        }});

        function renderCards() {{
            const grid = document.getElementById('cardsGrid');
            if (!grid) return;

            for (const [id, data] of Object.entries(SERVICES)) {{
                const card = createCard(id, data);
                grid.appendChild(card);
            }}
        }}

        function createCard(id, data) {{
            const card = document.createElement('div');
            card.className = 'card';
            card.style.setProperty('--color', data.color);
            card.style.setProperty('--glow', data.color);
            card.style.setProperty('--shadow', data.color + '40');
            card.style.setProperty('--shadow-glow', data.color + '20');

            const features = data.features || [];
            const featuresHtml = features.map(f => `<span class="card-feature">${{f}}</span>`).join('');

            card.innerHTML = `
                <div class="card-content">
                    <div class="card-icon">${{data.icon}}</div>
                    <div class="card-title">${{data.name}}</div>
                    <div class="card-desc">${{data.description}}</div>
                    <div class="card-features">${{featuresHtml}}</div>
                    <div class="card-dots">
                        <span style="background:${{data.color}}"></span>
                        <span style="background:${{data.color2}}"></span>
                        <span style="background:${{data.color}}"></span>
                    </div>
                </div>
            `;

            card.addEventListener('click', () => openChat(id));
            return card;
        }}

        function openChat(serviceId) {{
            if (isOpening) return;
            isOpening = true;

            console.log(`Открываем: ${{serviceId}}`);

            // Проверяем, является ли сервис CLI
            const service = SERVICES[serviceId];
            if (service && service.is_cli) {{
                // Для CLI сервисов запускаем установку
                if (pywebview && pywebview.api && pywebview.api.install_qwen_code) {{
                    pywebview.api.install_qwen_code();
                }}
            }} else {{
                // Обычные чаты
                if (pywebview && pywebview.api && pywebview.api.open_chat) {{
                    pywebview.api.open_chat(serviceId);
                }}
            }}

            setTimeout(() => {{ isOpening = false; }}, 500);
        }}

        function closeApp() {{
            if (pywebview && pywebview.api && pywebview.api.quit_app) {{
                pywebview.api.quit_app();
            }}
        }}

        function minimizeWindow() {{
            const content = document.getElementById('mainContent');
            if (content) {{
                content.classList.add('minimize-animation');
            }}
            setTimeout(() => {{
                if (pywebview && pywebview.api && pywebview.api.minimize_window) {{
                    pywebview.api.minimize_window();
                }}
                setTimeout(() => {{
                    if (content) {{
                        content.classList.remove('minimize-animation');
                    }}
                }}, 250);
            }}, 50);
        }}

        function checkForUpdates() {{
            if (pywebview && pywebview.api && pywebview.api.check_for_updates) {{
                pywebview.api.check_for_updates();
            }}
        }}
        
        function toggleMaximize() {{
            const content = document.getElementById('mainContent');
            if (content) {{
                content.classList.add('fullscreen-transition');
                setTimeout(() => content.classList.remove('fullscreen-transition'), 500);
            }}
            if (pywebview && pywebview.api && pywebview.api.toggle_maximize) {{
                pywebview.api.toggle_maximize();
            }}
        }}

        function exitFullscreen() {{
            if (pywebview && pywebview.api && pywebview.api.toggle_maximize) {{
                pywebview.api.toggle_maximize();
            }}
        }}

        function updateFullscreenButton(isMaximized) {{
            const btn = document.getElementById('fullscreenExitBtn');
            if (btn) {{
                if (isMaximized) {{
                    btn.classList.add('visible');
                }} else {{
                    btn.classList.remove('visible');
                }}
            }}
        }}

        window.addEventListener('pywebview.restored', () => {{
            const content = document.getElementById('mainContent');
            if (content) {{
                content.classList.add('restore-animation');
                content.classList.add('fullscreen-exit');
                setTimeout(() => {{
                    content.classList.remove('restore-animation');
                    content.classList.remove('fullscreen-exit');
                }}, 400);
            }}
            updateFullscreenButton(false);
        }});

        window.addEventListener('pywebview.maximized', () => {{
            const content = document.getElementById('mainContent');
            if (content) {{
                content.classList.add('fullscreen-transition');
                setTimeout(() => content.classList.remove('fullscreen-transition'), 500);
            }}
            updateFullscreenButton(true);
        }});

        function log(msg) {{
            console.log(`[AI Hub] ${{msg}}`);
            if (pywebview && pywebview.api && pywebview.api.log_message) {{
                pywebview.api.log_message(msg);
            }}
        }}
    </script>
    </div>
</body>
</html>'''


def get_chat_window_html(service_id: str, services: Dict) -> str:
    """HTML-обёртка для окна чата — перенаправление на URL."""
    service = services.get(service_id, {})
    service_name = service.get("name", "Chat")
    service_url = service.get("url", "")

    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0;url={service_url}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Переход на {service_name}...</title>
    <style>
        body {{
            background: #0a0a0f;
            color: #fff;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }}
        .loading {{
            text-align: center;
        }}
        .spinner {{
            width: 40px;
            height: 40px;
            border: 3px solid #333;
            border-top-color: #6366f1;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }}
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="loading">
        <div class="spinner"></div>
        <p>Переход на {service_name}...</p>
    </div>
    <script>
        window.location.href = "{service_url}";
    </script>
</body>
</html>'''
