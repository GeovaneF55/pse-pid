from PyQt5.QtWidgets import QDoubleSpinBox

class DoubleTextSpinBox(QDoubleSpinBox):
    def currentText(self):
        return str(self.value())
