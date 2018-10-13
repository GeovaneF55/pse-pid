from PyQt5.QtWidgets import QToolBar

class ToolBar(QToolBar):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
