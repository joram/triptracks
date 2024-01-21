import dataclasses


@dataclasses.dataclass
class Spec:
    key: str
    value: str


@dataclasses.dataclass
class Product:
    name: str
    url: str
    price_cents: int
    img_hrefs: [str]
    specs: list[Spec]
