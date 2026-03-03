from dataclasses import dataclass, field
from typing import final
from models.base_model import BaseModel

@final
@dataclass(kw_only=True)
class Note(BaseModel):
    text: str
    tags: list[str] = field(default_factory=list[str])

    @property
    def tags_string(self) -> str:
        return ', '.join(self.tags)

    def _validate(self) -> dict[str, bool]:
        return {
            "text": bool(self.text.strip()),
        }

    def __str__(self) -> str:
        tags_str: str = ", ".join(self.tags) if self.tags else "без тегів"
        return f"Нотатка: {self.text} | Теги: {tags_str}"

    @classmethod
    def _transform_form_data(cls, data: dict) -> dict:
        data = super()._transform_form_data(data)
        tags = data.get("tags")
        if isinstance(tags, str):
            data["tags"] = [tag.strip() for tag in tags.split(',')]
        return data
