"""
Тесты GUI для модуля с таблицей бюджетов
"""

from pytestqt.qt_compat import qt_api

from bookkeeper.view.budget import BudgetTableWidget, BudgetTableGroup
from bookkeeper.models.budget import Budget

test_data = [["1_1", "1_2", "1_3", 1],
             ["2_1", "2_2", "2_3", 2],]

bdg_modifier = lambda pk, new_limit, period: None

def test_create_widget(qtbot):
    widget = BudgetTableWidget(bdg_modifier)
    qtbot.addWidget(widget)
    assert widget.bdg_modifier == bdg_modifier

def test_add_data(qtbot):
    widget = BudgetTableWidget(bdg_modifier)
    qtbot.addWidget(widget)
    widget.add_data(test_data)
    assert widget.data == test_data
    for i, row in enumerate(test_data):
        for j, x in enumerate(row[:-1]):
            assert widget.item(i, j).text() == test_data[i][j]
            if j == 0:
                flags = (qt_api.QtCore.Qt.ItemIsEditable 
                        | qt_api.QtCore.Qt.ItemIsEnabled 
                        | qt_api.QtCore.Qt.ItemIsSelectable)
                assert widget.item(i, j).flags() == flags
            else: 
                assert widget.item(i, j).flags() == qt_api.QtCore.Qt.ItemIsEnabled


def test_cell_changed(qtbot):
    def bdg_modifier(pk, new_limit, period):
        bdg_modifier.was_called = True
        assert pk == test_data[1][-1]
        assert new_limit == test_data[1][0]
        assert period == "week"
    bdg_modifier.was_called = False
    widget = BudgetTableWidget(bdg_modifier)
    qtbot.addWidget(widget)
    widget.add_data(test_data)
    widget.cellChanged.emit(1,0)
    assert bdg_modifier.was_called == False
    widget.cellDoubleClicked.emit(1,0)
    widget.cellChanged.emit(1,0)
    assert bdg_modifier.was_called == True

def test_create_group(qtbot):
    widget = BudgetTableGroup(bdg_modifier)
    qtbot.addWidget(widget)

def test_set_budgets(qtbot):
    widget = BudgetTableGroup(bdg_modifier)
    qtbot.addWidget(widget)
    bdgs = [Budget(1000, "day", spent=100),
            Budget(7000, "week"),]
    widget.set_budgets(bdgs)
    assert widget.budgets == bdgs
    for b, w_data in zip(bdgs, widget.data):
        assert str(b.limitation) == w_data[0]
        assert str(b.spent) == w_data[1]
        assert str(int(b.limitation) 
                        - int(b.spent)) == w_data[2]
        assert b.pk == w_data[3]
    assert widget.data[2] == ["- Не установлен -", "", "", None]