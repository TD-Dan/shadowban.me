
from .section import Section

"""Interface base class for all os level windows."""
class WindowBase(Section):
    name = 'Unnamed Program'
    
    def open(self): raise NotImplementedError('open method not implemented by subclass.')
    def add_tool(self,page): raise NotImplementedError('add_tool method not implemented by subclass.')