"""
proverka.py — Проверка обновлений через GitHub API
Версия: 1.0.0
"""

import json
import urllib.request
from datetime import datetime


class VersionChecker:
    """Проверка версий через GitHub API."""
    
    def __init__(self, repo_url: str, current_version: str):
        self.repo_url = repo_url
        self.current_version = current_version
    
    def check_for_updates(self) -> dict:
        """Проверить наличие новой версии через GitHub API."""
        try:
            # Запрашиваем последний релиз с GitHub
            url = f"https://api.github.com/repos/{self.repo_url}/releases/latest"
            req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})
            
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                latest_version = data.get("tag_name", "").lstrip("v")
                release_date = data.get("published_at", "")
                
                if not latest_version:
                    return {"has_update": False, "current": self.current_version, "latest": self.current_version}
                
                # Сравниваем версии
                def parse_version(v):
                    return [int(x) for x in v.split(".") if x.isdigit()]
                
                current_parts = parse_version(self.current_version)
                latest_parts = parse_version(latest_version)
                
                has_update = latest_parts > current_parts
                
                return {
                    "has_update": has_update,
                    "current": self.current_version,
                    "latest": latest_version,
                    "release_date": release_date,
                    "notes": data.get("body", "")
                }
                
        except Exception as e:
            print(f"Ошибка проверки обновлений: {e}")
            return {"has_update": False, "current": self.current_version, "latest": self.current_version, "error": str(e)}
    
    def get_release_info(self, version: str = "latest") -> dict:
        """Получить информацию о конкретном релизе."""
        try:
            url = f"https://api.github.com/repos/{self.repo_url}/releases/{version}"
            req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})
            
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                return {
                    "version": data.get("tag_name", "").lstrip("v"),
                    "name": data.get("name", ""),
                    "published_at": data.get("published_at", ""),
                    "body": data.get("body", ""),
                    "url": data.get("html_url", "")
                }
        except Exception as e:
            print(f"Ошибка получения информации о релизе: {e}")
            return {}
