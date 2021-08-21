from minimake.product import Product

@dataclass
class TextFile(Product):
    None

@dataclass
class WcFile(TextFile):
    def line_count(self):
        return int(self.lines[0].strip.split(' ')[0])

@dataclass
class DirContents(TextFile):
    def files(self):
        return self.lines()

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
def wc(input: TextFile) -> WcFile:
    return WcFile('wc {input} > {output}', input, output=f'{input}.wc')

@action
def ls(input: Directory) -> TextFile:
    return TextFile('ls {input} > {output}', input, output=f'{input}/.ls')

@action
def dirlist(input: Directory) -> DirContents:
    return DirContents('find {input} -type f > {output}', input, output=f'{input}/.lsrel')