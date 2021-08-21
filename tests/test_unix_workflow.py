import os
import csv
from pathlib import Path
import shutil
import unittest
from typing import List, Any, Optional
from dataclasses import dataclass
from minimake import *

ROOT = os.path.abspath(os.path.dirname(__file__))
INPUT_DIR = os.path.join(ROOT, 'input')
WORK_DIR = os.path.join(ROOT, 'work')
FILES = ['WORDS', 'WORDS2']
IRIS = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'


@dataclass
class TextFile(Product):
    None

@dataclass
class CsvFile(TextFile):
    sep = ','
    def rows(self):
        with open(self.output) as stream:
            reader = csv.DictReader(stream)
            for row in rows:
                yield row

@dataclass
class RemoteURL(Product):
    None

@dataclass
class Directory(Product):
    None

@action
def cat(input: List[TextFile]) -> TextFile:
    return TextFile('cat  {input} > {output}')

@action
def grep(input: TextFile, keyword: str) -> TextFile:
    return TextFile('grep {keyword} {input} > {output}', output=f'{input}-{keyword}.grep.txt')

@action
def wc(input: TextFile) -> TextFile:
    return TextFile('wc {input} > {output}', input, output=f'{input}.wc')

@action
def curl(input: RemoteURL, dir='.', name=None) -> TextFile:
    if name is None:
        name=input.split('/')[-1]
    return TextFile('curl -L -s {input} > {output}', input, output=f'{dir}/{name}.download')

@action
def ls(input: Directory) -> TextFile:
    return TextFile('ls {input} > {output}', input, output=f'{input}/.ls')

@action
def lsrel(input: Directory) -> TextFile:
    return TextFile('find {input} -type f > {output}', input, output=f'{input}/.lsrel')

@action
def find(input: Directory, keyword, type='f') -> TextFile:
    return TextFile('find {input} -type {type} {keyword} > {output}', input, output=f'{input}/.find-{keyword}-{type}')

@action
def echo(input: Optional[TextFile], text: str) -> TextFile:
    return TextFile('echo {text} > {output}', input, output='foo')

@action
def wc_all_in_dir(input: Directory) -> ():
    return lambda: [wc(x) for x in input.lines()], input

a = Runner()

class BasicTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dirpath = Path(WORK_DIR)
        if dirpath.exists():
            if dirpath.is_dir():
                shutil.rmtree(dirpath)
            else:
                raise Exception(f'{dirpath} must be a dir')
        dirpath.mkdir(parents=False)
        for f in FILES:
            shutil.copyfile(src=os.path.join(INPUT_DIR, f), dst=(dirpath / f))


    @classmethod
    def tearDownClass(cls):
        None

    def test_simple(self):
        a = Runner()
        MY_TEXT = "hello"
        out = a.make(echo(input=None, text=MY_TEXT))
        print(out)
        print(out.content())
        assert out.content().strip() == MY_TEXT

    def test_combined(self):
        WORDS = os.path.join(WORK_DIR, 'WORDS')
        a = Runner()
        out = a.make(wc(grep(WORDS, keyword='ab')))
        print(out)
        print(out.content())
        #assert out.content().strip() == MY_TEXT

    def test_find(self):
        #out = a.make(find(WORK_DIR, keyword='W', type='f'))
        out = a.make(find(WORK_DIR, keyword='W'))
        print(out)
        print(out.content())

    def test_ls(self):
        out = a.make(ls(WORK_DIR))
        print(out)
        print(out.content())
        #assert out.content().strip() == MY_TEXT

    def test_wc_ls(self):
        out = a.make(wc(ls(WORK_DIR)))
        print(out)
        print(out.content())
        #assert out.content().strip() == MY_TEXT

    def test_curl(self):
        out = a.make(curl(IRIS, dir=WORK_DIR, name='iris'))
        print(out)
        print(out.content_preview())

    def test_lambda(self):
        out = a.make(wc_all_in_dir(lsrel(WORK_DIR)))
        print(out)
        print([x.content() for x in out])
        #assert out.content().strip() == MY_TEXT

    def test_no_rebuild(self):
        WORDS = os.path.join(WORK_DIR, 'WORDS')
        a = Runner()
        out = a.make(wc(grep(WORDS, keyword='ab')))
        n = len(a.activities)
        #assert n > 0
        print(f'Activities={len(a.activities)}')
        out = a.make(wc(grep(WORDS, keyword='ab')))
        print(f'Activities={len(a.activities)}')
        assert n == len(a.activities)  ## no new activities
        Path(WORDS).touch()
        out = a.make(wc(grep(WORDS, keyword='ab')))
        print(f'Activities={len(a.activities)}')
        assert n < len(a.activities)




if __name__ == '__main__':
    unittest.main()
