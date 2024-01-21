import dataclasses
from typing import Optional


@dataclasses.dataclass
class Spec:
    key: str
    value: str


@dataclasses.dataclass
class Product:
    name: str
    description: str
    url: str
    price_cents: int
    img_hrefs: [str]
    specs: list[Spec]

    @property
    def slug(self):
        name = self.name
        name = name.lower()
        for c in [" ", "/", "(", ")", ",", "'", '"', "&", "’", "”", "“", "‘", "–", "—", "®", "™", "®", "™"]:
            name = name.replace(c, "-")
        while "--" in name:
            name = name.replace("--", "-")
        return name

    @property
    def weight(self) -> Optional[float]:
        for spec in self.specs:
            if "weight" in spec.key.lower():
                # 16g (description)
                # 1.16kg
                value = spec.value.lower()
                if " " in value:
                    value = value.split(" ")[0]
                if value.endswith("kg"):
                    value = value.replace("kg", "")
                    return float(value) * 1000
                if value.endswith("g"):
                    value = value.replace("g", "")
                    return float(value)
        return None