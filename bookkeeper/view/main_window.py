from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from bookkeeper.view.budget import BudgetTableGroup
from bookkeeper.view.new_expense import NewExpenseGroup
from bookkeeper.view.expenses import ExpensesTableGroup
from bookkeeper.view.group_widgets import LabeledCheckBox
from bookkeeper.view.palette_mode import PaletteMode


class MainWindow(QtWidgets.QWidget):
    def __init__(self, budget_table: BudgetTableGroup,
                       new_expense: NewExpenseGroup,
                       expenses_table: ExpensesTableGroup,
                       *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vbox = QtWidgets.QVBoxLayout()
        self.setWindowTitle("Bookkeeper v0.2")
        #self.theme = LabeledCheckBox("Темная тема", 
        #                             init_state=Qt.Checked, 
        #                             chstate_func=self.change_theme)
        #self.vbox.addWidget(self.theme, stretch=0.1, alignment=Qt.AlignRight)
        # Бюджет
        self.budget_table = budget_table
        self.vbox.addWidget(self.budget_table, stretch=3)
        # Новая трата
        self.new_expense = new_expense
        self.vbox.addWidget(self.new_expense, stretch=1)
        # Расходы
        self.expenses_table = expenses_table
        self.vbox.addWidget(self.expenses_table, stretch=6)
        self.setLayout(self.vbox)

    def change_theme(self, status):
        app = QtWidgets.QApplication.instance()
        if(self.theme.check_box.isChecked()):
            app.setPalette(PaletteMode(is_dark_mode=True))
        else:
            app.setPalette(PaletteMode(is_dark_mode=False))

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Закрытие приложение',
        "Вы уверены?\nВсе несохраненные данные будут потеряны.")
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            app = QtWidgets.QApplication.instance()
            app.closeAllWindows()
        else:
            event.ignore()