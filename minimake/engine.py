from typing import List, Any
from dataclasses import dataclass
import logging
import os

@dataclass
class Engine:
    dry_run: bool = False

    def execute(self, command: str, depth: int = 0) -> int:
        None

@dataclass
class ShellEngine(Engine):
    def execute(self, command: str, depth: int = 0) -> int:
        indent = '    ' * depth
        print(f'{indent}RUN: {command}')
        if self.dry_run:
            return 0
        else:
            exit_code = os.system(command)
            if exit_code != 0:
                logging.error(f'Error {exit_code} running: {command}')
            return exit_code
