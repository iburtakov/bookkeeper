"""
Тесты GUI для модуля с добавлением новой траты
"""

from pytestqt.qt_compat import qt_api

from bookkeeper.view.new_expense import NewExpenseGroup
from bookkeeper.models.category import Category

cats_edit_show = lambda: None
exp_adder = lambda amount, cat_name, comment: None

def test_create_group(qtbot):
    widget = NewExpenseGroup([], 
                             cats_edit_show, 
                             exp_adder,)
    qtbot.addWidget(widget)
    assert widget.cats_edit_show == cats_edit_show
    assert widget.exp_adder == exp_adder

def test_set_categories(qtbot):
    widget = NewExpenseGroup([], 
                             cats_edit_show, 
                             exp_adder,)
    qtbot.addWidget(widget)
    cats = [Category("cat1"), Category("cat2"),]
    widget.set_categories(cats)
    assert widget.categories == cats
    assert widget.cat_names == [c.name for c in cats]

def test_add_expense(qtbot):
    def exp_adder(amount, cat_name, comment):
        exp_adder.was_called = True
        assert amount == "100"
        assert cat_name == "cat1"
        assert comment == "test"
    exp_adder.was_called = False
    cats = [Category("cat1"), Category("cat2"),]
    widget = NewExpenseGroup(cats, 
                             cats_edit_show, 
                             exp_adder,)
    qtbot.addWidget(widget)
    widget.amount_input.set_text("100")
    widget.category_input.set_text("cat1")
    widget.comment_input.set_text("test")
    qtbot.mouseClick(
                widget.submit_button,
                qt_api.QtCore.Qt.MouseButton.LeftButton
            )
    assert exp_adder.was_called == True