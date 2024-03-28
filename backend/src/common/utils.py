from typing import Callable

from injector import Binder, Module, noscope


class Depends(Module):
    def __init__(self, depends: Callable = None):
        self.depends = depends

    def configure(self, binder: Binder):
        binder.bind(Depends, to=self.depends, scope=noscope)
