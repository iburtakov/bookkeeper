from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

class PaletteMode(QPalette):
    def __init__(self, is_dark_mode=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if is_dark_mode:
            self.setColor(QPalette.Window, QColor(53, 53, 53))
            self.setColor(QPalette.WindowText, Qt.white)
            self.setColor(QPalette.Base, QColor(25, 25, 25))
            self.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            self.setColor(QPalette.ToolTipBase, Qt.black)
            self.setColor(QPalette.ToolTipText, Qt.white)
            self.setColor(QPalette.Text, Qt.white)
            self.setColor(QPalette.Button, QColor(53, 53, 53))
            self.setColor(QPalette.ButtonText, Qt.white)
            self.setColor(QPalette.BrightText, Qt.red)
            self.setColor(QPalette.Link, QColor(42, 130, 218))
            self.setColor(QPalette.Highlight, QColor(42, 130, 218))
            self.setColor(QPalette.HighlightedText, Qt.black)