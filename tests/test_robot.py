import unittest
from typing import List, Any
from dataclasses import dataclass
from minimake import *

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
def all() -> List[Ontology]:
    onts = ['cl', 'go']
    return [build(Ontology(name=o)) for o in onts]

@action
def all_go() -> List[Ontology]:
    return annotate(reason(Ontology(name='go'), reasoner='elk'))
    #return build(Ontology(name='cl'))

class BasicTestCase(unittest.TestCase):
    ## TODO: this runs in dry-run mode for now, we don't actually check the commands execute

    def test_workflow(self):
        print('##ALL_GO')
        a = Runner()
        a.engine.dry_run = True
        out = a.make(all_go())
        print(out)
        assert out.output == 'go.elk.ann'

    def test_all(self):
        print('## ALL')
        a = Runner()
        a.engine.dry_run = True
        out = a.make(all())
        print(out)
        paths = [o.output for o in out]
        print(f'Paths={paths}')
        assert paths == ['cl.ELK.ann', 'go.ELK.ann']



if __name__ == '__main__':
    unittest.main()
