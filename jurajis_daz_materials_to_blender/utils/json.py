from dataclasses import is_dataclass, asdict, fields
from json import JSONEncoder


class DataclassJSONEncoder(JSONEncoder):
    def default(self, dmc):
        if is_dataclass(dmc):
            return self.as_dict(dmc)
        else:
            return super().default(dmc)

    @classmethod
    def as_dict(cls, obj):
        if hasattr(obj, "__as_dict__"):
            return obj.__as_dict__()
        elif is_dataclass(obj):
            return {f.name: cls.as_dict(getattr(obj, f.name)) for f in fields(obj)}
        elif isinstance(obj, (list, tuple)):
            return [cls.as_dict(v) for v in obj]
        elif isinstance(obj, dict):
            return {k: cls.as_dict(v) for k, v in obj.items()}
        else:
            return obj


def serializable(*include_props: str):
    def decorator(cls):
        if not is_dataclass(cls):
            raise TypeError("@serializable can only be applied to dataclasses")

        def __as_dict__(self):
            base = asdict(self)
            for name in include_props:
                attr = getattr(self, name)
                base[name] = attr() if callable(attr) else attr
            return base

        cls.__as_dict__ = __as_dict__
        return cls

    return decorator
