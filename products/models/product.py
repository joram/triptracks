import dataclasses
import re
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
            if "fabric" in spec.key.lower():
                continue
            if "weight" in spec.key.lower():
                value = spec.value.lower()
                #convert a-b to the average
                if "-" in value:
                    regex = re.compile(r"(\d+)-(\d+)")
                    match = regex.search(value)
                    if match:
                        a = float(match.group(1))
                        b = float(match.group(2))
                        v = (a+b)/2
                        value = regex.sub(value, f"{v}")

                if " " in value:
                    value = value.split(" ")[0]
                if value.endswith("kg"):
                    value = value.replace("kg", "")
                    return float(value) * 1000
                if value.endswith("g"):
                    value = value.replace("g", "")
                    return float(value)
                if value.endswith("lb"):
                    value = value.replace("lb", "")
                    return float(value) * 453.592
                if value.endswith("oz"):
                    value = value.replace("oz", "")
                    return float(value) * 28.3495
                try:
                    return float(value)
                except ValueError:
                    pass
                print(f"Could not parse weight: {spec.value}")
        return None