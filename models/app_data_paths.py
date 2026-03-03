from pathlib import Path
from typing import final
from pydantic import BaseModel

@final
class AppDataPaths(BaseModel):
    """Модель шляхів до зберігаємих даних"""
    address_book: Path = Path("data") / "contacts.json"
    notes: Path = Path("data") / "notes.json"
