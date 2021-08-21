from typing import List, Any
from dataclasses import dataclass
from minimake.runner import *

@dataclass
class Ontology(Product):
    id: str = None


@action
def annotate(input: Ontology, id: str = 'DEFAULT') -> Ontology:
    return Ontology('robot annotate -i {input} --ontology-id {id} -o {output}', output=f'{input}.ann')

@action
def reason(input: Ontology, reasoner: str = 'ELK') -> Ontology:
    return Ontology('robot reason -i {input} -r {reasoner} -o {output}', output=f'{input.name}.{reasoner}')

@action
def convert(input: Ontology, fmt: str = 'owl') -> Ontology:
    return Ontology('robot convert -i {input} -f {fmt} -o {output}', output=f'{input}.{fmt}')

@action
def multiconvert(input: Ontology, fmts = ['obo', 'owl', 'json']) -> List[Ontology]:
    return [convert(input, fmt) for fmt in fmts]


@action
def mbuild(input: Ontology) -> List[Ontology]:
    return multiconvert(annotate(reason(input), id='fooz'))

@action
def build(input: Ontology) -> Ontology:
    return annotate(reason(input), id='my_ont')
#    return multiconvert(annotate(reason(input), id='fooz'))

@action
def xall() -> List[Ontology]:
    onts = ['cl', 'go']
    return [build(Ontology(name=o)) for o in onts]

@action
def all() -> List[Ontology]:
    onts = ['cl', 'go']
    return annotate(reason(Ontology(name='cl'), reasoner='elk'))
    #return build(Ontology(name='cl'))
                          


a = Runner()
a.make(all())
