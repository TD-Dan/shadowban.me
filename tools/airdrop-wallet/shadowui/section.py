
class Section:
    name = None
    sub_sections:dict = {}
    
    def __init__(self,name:str,sub_sections:list = None ) -> None:
        self.name=name
        if sub_sections:
            self.sub_sections=sub_sections

    def __iadd__(self, val2):
        try:
            for obj in val2:
                self.sub_sections[obj.name] = obj
        except TypeError:
            try:
                self.sub_sections[val2.name] = val2
            except AttributeError:
                raise TypeError("Only adding a Section or Iterable of Sections is supported")
        return self

    def __getattr__(self,attr):
        return self.sub_sections[attr]