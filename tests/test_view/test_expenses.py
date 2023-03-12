"""
Тесты GUI для модуля с таблицей расходов
"""

from pytestqt.qt_compat import qt_api

from bookkeeper.view.expenses import ExpensesTableWidget, \
                                     ExpensesTableGroup
from bookkeeper.models.expense import Expense

test_data = [["1_1", "1_2", "1_3", "1_4", 1],
             ["2_1", "2_2", "2_3", "2_4", 2],]

exp_modifier = lambda pk, attr, new_val: None
catpk_to_name = lambda pk: "1_3"
exp_deleter = lambda exp_pks: None

def test_create_widget(qtbot):
    widget = ExpensesTableWidget(exp_modifier)
    qtbot.addWidget(widget)
    assert widget.exp_modifier == exp_modifier

def test_add_data(qtbot):
    widget = ExpensesTableWidget(exp_modifier)
    qtbot.addWidget(widget)
    widget.add_data(test_data)
    assert widget.data == test_data
    for i, row in enumerate(test_data):
        for j, x in enumerate(row[:-1]):
            assert widget.item(i, j).text() == test_data[i][j]

def test_cell_changed(qtbot):
    def exp_modifier(pk, attr, new_val):
        exp_modifier.was_called = True
        assert pk == test_data[0][4]
        assert new_val == test_data[0][0]
    exp_modifier.was_called = False
    widget = ExpensesTableWidget(exp_modifier)
    qtbot.addWidget(widget)
    widget.add_data(test_data)
    widget.cellChanged.emit(0,0)
    assert exp_modifier.was_called == False
    widget.cellDoubleClicked.emit(0,0)
    widget.cellChanged.emit(0,0)
    assert exp_modifier.was_called == True

def test_create_group(qtbot):
    widget = ExpensesTableGroup(catpk_to_name, 
                                exp_modifier, 
                                exp_deleter)
    qtbot.addWidget(widget)
    assert widget.catpk_to_name == catpk_to_name
    assert widget.exp_deleter == exp_deleter

def test_set_expenses(qtbot):
    widget = ExpensesTableGroup(catpk_to_name, 
                                exp_modifier, 
                                exp_deleter)
    qtbot.addWidget(widget)
    exps = [Expense(100, 1, expense_date="12.12.2012 15:30", 
                            comment="test"), 
            Expense(200, 2, expense_date="12.12.2012 15:30")]
    widget.set_expenses(exps)
    assert widget.expenses == exps
    for exp, w_data in zip(exps, widget.data):
        assert str(exp.expense_date) == w_data[0]
        assert str(exp.amount) == w_data[1]
        assert catpk_to_name(exp.category) == w_data[2]
        assert str(exp.comment) == w_data[3]
        assert exp.pk == w_data[4]

def test_delete_expenses(qtbot):
    def exp_deleter(exp_pks):
        exp_deleter.was_called = True
        assert exp_pks == set([2,3])
    exp_deleter.was_called = False
    widget = ExpensesTableGroup(catpk_to_name, 
                                exp_modifier, 
                                exp_deleter)
    qtbot.addWidget(widget)
    exps = [Expense(100, 1, pk=1), Expense(200, 2, pk=2),
            Expense(300, 3, pk=3), Expense(400, 4, pk=4),]
    widget.set_expenses(exps)
    widget.table.setRangeSelected(
                qt_api.QtWidgets.QTableWidgetSelectionRange(1,1,2,2), True)
    widget.table.setRangeSelected(
                qt_api.QtWidgets.QTableWidgetSelectionRange(1,3,3,4), True)
    qtbot.mouseClick(
            widget.del_button,
            qt_api.QtCore.Qt.MouseButton.LeftButton
        )
    assert exp_deleter.was_called == True