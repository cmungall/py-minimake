from minimake.decorators import action
from minimake.runner import Runner
from minimake.product import Product
from dataclasses import dataclass
from typing import List, Any, Dict

runner = Runner()
def make(product: Product, **kwargs):
    return runner.make(product, **kwargs)
