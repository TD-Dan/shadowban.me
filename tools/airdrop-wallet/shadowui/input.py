
from .section import Section

class Input(Section):
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self,value):
        self._value = value
        if self.on_value_changed:
            for listener in self.on_value_changed:
                listener(self.value)

    on_value_changed:list = []

    def __init__(self, name: str, sub_sections: list = [], on_value_changed:callable = None) -> None:
        super().__init__(name, sub_sections)
        self._value = None
        self.on_value_changed.append(on_value_changed)