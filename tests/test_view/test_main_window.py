"""
Тесты GUI для главного окна
"""

from pytestqt.qt_compat import qt_api

from bookkeeper.view.main_window import MainWindow
from bookkeeper.view.palette_mode import PaletteMode
from bookkeeper.view.budget import BudgetTableGroup
from bookkeeper.view.new_expense import NewExpenseGroup
from bookkeeper.view.expenses import ExpensesTableGroup

modifier = lambda pk, val1, val2: None
pk_to_name = lambda pk: ""
deleter = lambda pks: None
cats_edit_show = lambda: None
adder = lambda amount, name, comment: None
    

def test_create_window(qtbot):
    budget_table = BudgetTableGroup(modifier)
    new_expense = NewExpenseGroup([], cats_edit_show, adder)
    expenses_table = ExpensesTableGroup(pk_to_name, modifier, deleter)
    window = MainWindow(budget_table, new_expense, expenses_table)
    qtbot.addWidget(window)
    assert window.budget_table == budget_table
    assert window.new_expense == new_expense
    assert window.expenses_table == expenses_table

# def test_change_theme(qtbot):
#     budget_table = BudgetTableGroup(modifier)
#     new_expense = NewExpenseGroup([], cats_edit_show, adder)
#     expenses_table = ExpensesTableGroup(pk_to_name, modifier, deleter)
#     window = MainWindow(budget_table, new_expense, expenses_table)
#     qtbot.addWidget(window)
#     assert window.is_dark_mode == True
#     window.theme.check_box.setCheckState(qt_api.QtCore.Qt.Unchecked)
#     assert window.is_dark_mode == False
#     window.theme.check_box.setCheckState(qt_api.QtCore.Qt.Checked)
#     assert window.is_dark_mode == True

def test_close_event(qtbot, monkeypatch):
    for result, msg in zip(
                [True, False], 
                [qt_api.QtWidgets.QMessageBox.Yes, qt_api.QtWidgets.QMessageBox.No]
                    ):
        budget_table = BudgetTableGroup(modifier)
        new_expense = NewExpenseGroup([], cats_edit_show, adder)
        expenses_table = ExpensesTableGroup(pk_to_name, modifier, deleter)
        window = MainWindow(budget_table, new_expense, expenses_table)
        qtbot.addWidget(window)
        monkeypatch.setattr(qt_api.QtWidgets.QMessageBox,
            "question", lambda *args: msg)
        assert window.close() == result