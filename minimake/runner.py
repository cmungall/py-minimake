import os
from pathlib import Path
from typing import List, Any
from dataclasses import dataclass
from minimake.product import Product
from minimake.engine import Engine, ShellEngine

@dataclass
class Activity:
    generated: Product = None
    used: List[Product] = None
    started_at_time: int = None
    ended_at_time: int = None
    command: str = None


@dataclass
class Runner:
    engine: Engine = None
    activities: List[Activity] = None

    def __post_init__(self):
        if self.activities is None:
            self.activities = []
        if self.engine is None:
            self.engine = ShellEngine()

    def make(self, product, depth=0, parent=None) -> Product:
        def info(msg):
            indent = '    ' * depth
            print(f'{indent}{msg}')
        info(f'MAKING = {product} // {type(product)}')
        if isinstance(product, tuple) and callable(product[0]):
            f, dependencies = product[0], product[1:]
            for d in dependencies:
                self.make(d, depth+1, product)
            return self.make(f(), depth+1)
        if isinstance(product, str):
            return product
        if isinstance(product, list):
            return [self.make(p, depth+1, product) for p in product]
        dependencies = self._get_dependencies(product)
        info(f' - Making Dependencies = {dependencies}')
        for d in dependencies.values():
            self.make(d, depth+1, product)
        command = product.command
        product.set_output()
        params = {k: getattr(product,k) for k in dir(product)}
        if command is None:
            info(f'NO ACTION for {product.__repr__()}')
        else:
            if self._exists_and_not_stale(product, dependencies=dependencies.values()):
                info(f'PRODUCT IS UP TO DATE: {product}')
            else:
                command_inst = command.format(**params)
                self.engine.execute(command_inst)
                product.materialized = True
                self.add_activity(command=command_inst, generated=product, used=dependencies.values())
            #info(f'RUN: {command_inst}')
        if depth == 0:
            info(f'COMPLETE: out={product.output}')
            info(f'SESSION ACTIVITIES: {len(self.activities)}')
        return product

    def add_activity(self, **kwargs):
        a = Activity(**kwargs)
        self.activities.append(a)

    def _get_dependencies(self, product):
        d = {}
        for k in dir(product):
            # currently assumes all attributes are potentially dependencies
            v = getattr(product, k)
            if isinstance(v, Product) or k == 'input':
                if v is not None:
                    d[k] = v
        return d

    def _exists_and_not_stale(self, product: Product, dependencies: List=[]):
        if (not product.materialized) and (not product.exists()):
            print(f'*** NOT MATERIALIZED: {product}')
            return False
        else:
            t = product.timestamp()
            print(f'*** T={t}: {product}')
            for d in dependencies:
                dpath = Path(str(d))
                if dpath.exists():
                    td = os.path.getmtime(dpath)
                    print(f'*** COMPARE {td}>{t} for {dpath}>{product}')
                    if td > t:
                        return False
            return True





        
