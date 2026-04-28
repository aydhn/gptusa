import pytest
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from usa_signal_bot.core.serialization import (
    dataclass_to_dict,
    dataclass_to_json,
    enum_to_value,
    serialize_value
)

class DummyEnum(str, Enum):
    A = "VALUE_A"

@dataclass
class NestedDataclass:
    inner_val: int = 42

@dataclass
class OuterDataclass:
    text: str = "hello"
    enum_val: DummyEnum = DummyEnum.A
    nested: NestedDataclass = field(default_factory=NestedDataclass)
    path_val: Path = field(default_factory=lambda: Path("/tmp/test"))
    a_list: list = None

    def __post_init__(self):
        if self.a_list is None:
            self.a_list = [1, DummyEnum.A, NestedDataclass()]

def test_enum_to_value():
    assert enum_to_value(DummyEnum.A) == "VALUE_A"
    assert enum_to_value("string") == "string"

def test_dataclass_to_dict():
    obj = OuterDataclass()
    d = dataclass_to_dict(obj)

    assert d["text"] == "hello"
    assert d["enum_val"] == "VALUE_A"
    assert d["nested"] == {"inner_val": 42}
    assert d["path_val"] == "/tmp/test"
    assert d["a_list"] == [1, "VALUE_A", {"inner_val": 42}]

def test_dataclass_to_json():
    obj = OuterDataclass()
    j = dataclass_to_json(obj)
    assert '"text": "hello"' in j
    assert '"enum_val": "VALUE_A"' in j
    assert '"inner_val": 42' in j
