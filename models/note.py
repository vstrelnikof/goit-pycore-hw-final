from dataclasses import dataclass, field
from typing import final
from models.base_model import BaseModel

@final
@dataclass
class Note(BaseModel):
    text: str
    tags: list[str] = field(default_factory=list)

    @property
    def tags_string(self) -> str:
        return ', '.join(self.tags)
    
    def _validate(self) -> dict[str, bool]:
        return {
            "text": not self.text,
        }
    
    def set_tags_from_string(self, tags_string: str) -> None:
        if tags_string:
            self.tags = [tag.strip() for tag in tags_string.split(',')]
    
    def __str__(self):
        tags_str = ", ".join(self.tags) if self.tags else "без тегів"
        return f"Нотатка: {self.text} | Теги: {tags_str}"
