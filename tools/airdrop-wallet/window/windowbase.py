
"""Interface base class for all screen user interfaces."""
class WindowBase:
    program_name: str = 'Unnamed Program'
    program_version: str = 'v.0.0.1'
    def open(self): raise NotImplementedError('open method not implemented by subclass.')
    def add_tool(self,page): raise NotImplementedError('add_tool method not implemented by subclass.')