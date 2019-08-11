from dataclasses import dataclass, field
from enum import IntEnum

from . import const


@dataclass
class Attribute:
    @dataclass
    class Part:
        text: str
        type: int

    parts: list
    length: int = field(init=False, repr=False)

    def __post_init__(self):
        self.length = sum(len(p.text) for p in self.parts)

    def __len__(self):
        return self.length


class char(str):
    pass
