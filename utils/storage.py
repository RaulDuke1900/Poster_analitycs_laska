import json
from pathlib import Path
from abc import ABC, abstractmethod

class StorageInterface(ABC):
    @abstractmethod
    def load_settings(self) -> dict:
        """Читает конфиг (data/user_settings.json) и возвращает его."""
        pass

    @abstractmethod
    def save_settings(self, settings: dict) -> None:
        """Перезаписывает data/user_settings.json."""
        pass

    @abstractmethod
    def save_report(self, report_type: str, period: str, data: dict) -> None:
        """Сохраняет сгенерированный отчёт в data/reports/."""
        pass

    @abstractmethod
    def load_report(self, report_type: str, period: str) -> dict | None:
        """Загружает ранее сохранённый отчёт."""
        pass


class JsonStorage(StorageInterface):
    def __init__(self, settings_path: Path | str = "data/user_settings.json"):
        self.settings_path = Path(settings_path)
        self.reports_dir = Path("data/reports")
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def load_settings(self) -> dict:
        with open(self.settings_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_settings(self, settings: dict) -> None:
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)

    def save_report(self, report_type: str, period: str, data: dict) -> None:
        filename = f"{report_type}_{period}.json"
        path = self.reports_dir / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_report(self, report_type: str, period: str) -> dict | None:
        filename = f"{report_type}_{period}.json"
        path = self.reports_dir / filename
        if not path.exists():
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
