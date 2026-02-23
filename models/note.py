from dataclasses import dataclass, field
from typing import final
from uuid import UUID
from models.base_model import BaseModel

@final
@dataclass(kw_only=True)
class Note(BaseModel):
    text: str
    tags: list[str] = field(default_factory=list)

    @property
    def tags_string(self) -> str:
        return ', '.join(self.tags)
    
    def _validate(self) -> dict[str, bool]:
        return {
            "text": bool(self.text),
        }
    
    def __str__(self):
        tags_str = ", ".join(self.tags) if self.tags else "без тегів"
        return f"Нотатка: {self.text} | Теги: {tags_str}"
    
    @classmethod
    def from_dict(cls, data: dict):
        if isinstance(data.get("id"), str):
            data["id"] = UUID(data["id"])
        tags = data.get("tags")
        if isinstance(tags, str):
            data["tags"] = [tag.strip() for tag in tags.split(',')]
        return cls(**data)
