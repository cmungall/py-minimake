import os
from pathlib import Path
from typing import List, Any
from dataclasses import dataclass
import hashlib

@dataclass
class Product:
    """
    base class for "lazy" data products
    """

    command: str = None
    input: Any = None
    name: str = None
    output: str = None
    materialized = False

    def __post_init__(self, *args, **kwargs):
        None

    def __str__(self):
        if self.output is None:
            return super().__str__()
        else:
            return self.output

    def set_output(self):
        if self.output is None:
            self.output = self.name

    def make(self, runner: "Runner"):
        """
        generates the product using a runner
        """
        obj = runner.make(self)
        return obj

    def content(self) -> str:
        return Path(self.output).read_text()

    def content_preview(self, n=200) -> str:
        return self.content()[0:n]

    def lines(self) -> List[str]:
        return self.content().split("\n")

    def md5(self) -> str:
        return hashlib.md5(str(self.content()).encode('utf-8')).digest()

    def path(self) -> Path:
        return Path(self.output)

    def timestamp(self) -> int:
        return os.path.getmtime(self.output)

    def exists(self) -> int:
        return self.path().exists()

@dataclass
class ProductSet:
    products: List[Product]