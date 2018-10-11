from PyQt5.QtGui import QPainter

class Painter(QPainter):
    
    def __init__(self, parent):
        super().__init__(parent)