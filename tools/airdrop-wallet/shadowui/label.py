
from .section import Section

class Label(Section):
    content = None
    def __init__(self, name: str, sub_sections: list = [], on_input_changed:callable = None) -> None:
        super().__init__(name, sub_sections)