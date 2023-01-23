
from .section import Section

"""Interface base class for all os level windows."""
class WindowBase(Section):    
    def open(self): raise NotImplementedError('open method not implemented by subclass.')
    def add_tool(self,page): raise NotImplementedError('add_tool method not implemented by subclass.')

    def __init__(self, name: str, sub_sections: list = []) -> None:
        super().__init__(name, sub_sections)