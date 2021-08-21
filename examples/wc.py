from typing import List, Any
from dataclasses import dataclass
from minimake.runner import *

@dataclass
class TextFile(Product):
    None


@action
def grep(input: TextFile, keyword: str) -> TextFile:
    return TextFile('grep {keyword} {input} > {output}', output=f'{input}-{keyword}.grep.txt')
@action
def wc(input: TextFile) -> TextFile:
    return TextFile('wc {input}', input)

a = Runner()
a.make(wc(grep('my.txt', keyword='bar')))
