from dataclasses import dataclass
from uuid import UUID
from models.base_model import BaseModel
from models.note import Note

def test_base_model_repr_uses_class_name_and_fields():
    @dataclass(kw_only=True)
    class DummyModel(BaseModel):
        name: str

        def _validate(self) -> dict[str, bool]:
            return {"name": bool(self.name)}

    instance = DummyModel(name="test")
    text = repr(instance)

    assert "DummyModel" in text
    assert "name='test'" in text

def test_note_transform_form_data_splits_tags_string():
    data = {"text": "hello", "tags": "one, two , three"}

    note = Note.from_dict(data)

    assert note.tags == ["one", "two", "three"]

def test_base_model_transform_form_data_handles_empty_id():
    @dataclass(kw_only=True)
    class DummyModel(BaseModel):
        def _validate(self) -> dict[str, bool]:
            return {}

    data_with_empty_id = {"id": ""}
    instance = DummyModel.from_dict(data_with_empty_id)

    # Має бути створений новий UUID, а не пустий рядок
    assert isinstance(instance.id, UUID)
