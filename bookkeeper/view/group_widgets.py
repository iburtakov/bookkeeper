from PySide6 import QtWidgets
from PySide6.QtCore import Qt

class LabeledLineInput(QtWidgets.QWidget):
    def __init__(self, text, placeholder, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder = placeholder
        self.layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(text)
        self.layout.addWidget(self.label, stretch=1)
        self.input = QtWidgets.QLineEdit(self.placeholder)
        self.layout.addWidget(self.input, stretch=4)
        self.setLayout(self.layout)

    def clear(self):
        self.input.setText(self.placeholder)
    
    def set_text(self, text: str) -> None:
        self.input.setText(text)

    def text(self):
        return self.input.text()

class LabeledComboBoxInput(QtWidgets.QWidget):
    def __init__(self, text: str, items: list[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(text)
        self.layout.addWidget(self.label, stretch=1)
        self.combo_box = QtWidgets.QComboBox()
        #self.combo_box.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.combo_box.setEditable(True)
        self.combo_box.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.combo_box.setMaxVisibleItems(16)
        self.set_items(items)
        self.layout.addWidget(self.combo_box, stretch=4)
        self.setLayout(self.layout)

    def clear(self):
        self.combo_box.setCurrentText(self.combo_box.placeholderText())

    def text(self):
        return self.combo_box.currentText()

    def set_text(self, text: str) -> None:
        self.combo_box.setCurrentText(text)

    def set_items(self, items: list[str]):
        self.items = items
        self.combo_box.clear()
        self.combo_box.addItems(items)
        if len(items) != 0:
            self.combo_box.setPlaceholderText(items[0])
        else:
            self.combo_box.setPlaceholderText("")
        self.clear()

class GroupLabel(QtWidgets.QLabel):
    def __init__(self, text, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        #self.setFrameStyle(QtWidgets.QFrame.Plain | QtWidgets.QFrame.Box)
        self.setAlignment(Qt.AlignCenter)
        #self.setLineWidth(1)

class LabeledCheckBox(QtWidgets.QWidget):
    def __init__(self, text, chstate_func=None, init_state=Qt.Unchecked, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(text)
        self.layout.addWidget(self.label, stretch=1)
        self.check_box = QtWidgets.QCheckBox()
        self.check_box.setCheckState(Qt.Checked)
        if chstate_func is not None:
            self.check_box.stateChanged.connect(chstate_func)
        self.layout.addWidget(self.check_box, stretch=1)
        self.setLayout(self.layout)