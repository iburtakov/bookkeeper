"""
Тесты GUI для модуля с таблицей расходов
"""
#import pytest
from pytestqt.qt_compat import qt_api
from PySide6.QtCore import Qt

from bookkeeper.view.expenses import ExpensesTableWidget, ExpensesTableGroup

test_data = [["1_1","1_2","1_3","1_4",1],
                ["2_1","2_2","2_3","2_4",2],]

exp_modifier = lambda pk, attr, new_val: None

def test_create_widget(qtbot):
    widget = ExpensesTableWidget(exp_modifier)
    qtbot.addWidget(widget)


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
    widget.cellDoubleClicked.emit(0,0)
    widget.cellChanged.emit(0,0)
    assert exp_modifier.was_called == True