from PySide6 import QtWidgets
from collections.abc import Callable

from bookkeeper.view.group_widgets import GroupLabel, LabeledComboBoxInput, LabeledLineInput
from bookkeeper.models.category import Category


class CategoriesEditWindow(QtWidgets.QWidget):
    cat_checker: Callable

    def __init__(self, cats: list[Category],
                 cat_adder, cat_deleter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid = QtWidgets.QGridLayout()
        self.label = GroupLabel("<b>Список категорий</b>")
        self.grid.addWidget(self.label, 0, 0, 1, 2)
        self.cats_tree = QtWidgets.QTreeWidget()
        self.cats_tree.setHeaderLabel("")
        self.cats_tree.itemDoubleClicked.connect(self.double_clicked)
        self.grid.addWidget(self.cats_tree, 1, 0, 1, 2)
        self.label = GroupLabel("<b>Удаление категории</b>")
        self.grid.addWidget(self.label, 2, 0, 1, 2)
        self.cat_del = LabeledComboBoxInput("Категория", [])
        self.grid.addWidget(self.cat_del, 3, 0, 1, 1)
        self.cat_del_button = QtWidgets.QPushButton('Удалить')
        self.cat_del_button.clicked.connect(self.delete_category)
        self.grid.addWidget(self.cat_del_button, 3, 1, 1, 1)
        self.label = GroupLabel("<b>Добавление категории</b>")
        self.grid.addWidget(self.label, 4, 0, 1, 2)
        self.cat_add_parent = LabeledComboBoxInput("Родитель", [])
        self.grid.addWidget(self.cat_add_parent, 5, 0, 1, 1)
        self.cat_add_name = LabeledLineInput("Название", "Новая категория")
        self.grid.addWidget(self.cat_add_name, 6, 0, 1, 1)
        self.cat_add_button = QtWidgets.QPushButton('Добавить')
        self.cat_add_button.clicked.connect(self.add_category)
        self.grid.addWidget(self.cat_add_button, 6, 1, 1, 1)
        self.setLayout(self.grid)
        self.cat_adder = cat_adder
        self.cat_deleter = cat_deleter
        self.set_categories(cats)

    def set_categories(self, cats: list[Category]):
        self.categories = cats
        self.cat_names = [c.name for c in cats]
        top_items = self._find_children()
        self.cats_tree.clear()
        self.cats_tree.insertTopLevelItems(0, top_items)
        self.cat_del.set_items(self.cat_names)
        self.cat_add_parent.set_items(["- Без родительской категории -"]
                                                        + self.cat_names)

    def delete_category(self):
        self.cat_deleter(self.cat_del.text())
        self.cat_del.clear()

    def set_cat_checker(self, checker):
        self.cat_checker = checker

    def add_category(self):
        parent_name = self.cat_add_parent.text()
        if parent_name == "- Без родительской категории -":
            self.cat_adder(self.cat_add_name.text(), None)
        else:
            self.cat_checker(parent_name)
            self.cat_adder(self.cat_add_name.text().lower(), self.cat_add_parent.text())
        self.cat_add_name.clear()
        self.cat_add_parent.clear()
    
    def _find_children(self, parent_pk=None):
        items = []
        children = [c for c in self.categories if c.parent == parent_pk]
        for child in children:
            item = QtWidgets.QTreeWidgetItem([child.name])
            item.addChildren(self._find_children(parent_pk=child.pk))
            items.append(item)
        return items
        
    def double_clicked(self, item, column):
        clicked_cat_name = item.text(column)
        self.cat_del.set_text(clicked_cat_name)
        self.cat_add_parent.set_text(clicked_cat_name)