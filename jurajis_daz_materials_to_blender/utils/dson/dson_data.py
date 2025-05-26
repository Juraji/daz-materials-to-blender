from dataclasses import dataclass, field
from typing import TypeVar, Generic, Protocol

_DMC_V = TypeVar('_DMC_V')
DsonCoordinate = tuple[float, float, float]
DsonRGBA = tuple[float, float, float, float]


@dataclass
class DsonChannel(Generic[_DMC_V]):
    value: _DMC_V
    default_value: _DMC_V
    image_file: str | None

    def has_image(self) -> bool: return self.image_file is not None

    def is_set(self):
        return self.value != self.default_value or self.has_image()


@dataclass
class DsonColorChannel(DsonChannel[DsonCoordinate]):
    alpha: float = 1.0

    def as_rgba(self) -> DsonRGBA:
        return self.value[0], self.value[1], self.value[2], self.alpha

    def as_float(self) -> float:
        return (sum(self.value) / 3) * self.alpha


@dataclass
class DsonFloatChannel(DsonChannel[float]):
    pass


@dataclass
class DsonBoolChannel(DsonChannel[bool]):
    pass


@dataclass
class DsonStringChannel(DsonChannel[str]):
    pass


@dataclass
class DsonImageChannel(DsonChannel[None]):
    def is_set(self):
        return self.has_image()


@dataclass
class DsonChannels:
    name: str
    type_id: str
    channels: dict[str, DsonChannel] = field(default_factory=dict)


class DsonTransforms(Protocol):
    origin: DsonCoordinate
    rotation: DsonCoordinate
    translation: DsonCoordinate
    scale: DsonCoordinate


@dataclass
class DsonObjectInstance(DsonTransforms):
    id: str
    label: str
    origin: DsonCoordinate
    rotation: DsonCoordinate
    translation: DsonCoordinate
    scale: DsonCoordinate


@dataclass
class DsonObject(DsonTransforms):
    id: str
    label: str
    origin: DsonCoordinate
    rotation: DsonCoordinate
    translation: DsonCoordinate
    scale: DsonCoordinate
    parent_id: str | None
    materials: list[DsonChannels] = field(default_factory=list)
    instances: list[DsonObjectInstance] = field(default_factory=list)


@dataclass
class DsonData:
    objects: list[DsonObject]
    dson_to_blender: dict[str, str]
    blender_to_dson: dict[str, str]

    def to_blender_name(self, dson_id: str) -> str:
        if dson_id in self.dson_to_blender:
            return self.dson_to_blender[dson_id]
        else:
            return dson_id

    def to_dson_id(self, blender_name: str) -> str:
        if blender_name in self.blender_to_dson:
            return self.blender_to_dson[blender_name]
        else:
            return blender_name
