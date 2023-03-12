import sys
from typing import Protocol
from collections.abc import Callable
from PySide6 import QtWidgets

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.view.main_window import MainWindow
from bookkeeper.view.palette_mode import PaletteMode
from bookkeeper.view.budget import BudgetTableGroup
from bookkeeper.view.new_expense import NewExpenseGroup
from bookkeeper.view.expenses import ExpensesTableGroup
from bookkeeper.view.categories_edit import CategoriesEditWindow


class AbstractView(Protocol):

    def show_main_window() -> None:
        pass

    def set_categories(cats : list[Category]) -> None:
        pass

    def set_expenses(cats : list[Expense]) -> None:
        pass

    def set_budgets(cats : list[Budget]) -> None:
        pass
    
    def set_cat_adder(handler: Callable[[str, str], None]) -> None:
        pass

    def set_cat_deleter(handler: Callable[[str], None]) -> None:
        pass

    def set_cat_checker(handler: Callable[[str], None]) -> None:
        pass

    def set_bdg_modifier(handler: Callable[['int | None', str, str], 
                                                        None]) -> None:
        pass

    def set_exp_adder(handler: Callable[[str, str, str], None]) -> None:
        pass

    def set_exp_deleter(handler: Callable[[list[int]], None]) -> None:
        pass

    def set_exp_modifier(handler: Callable[[int, str, str], None]) -> None:
        pass

    def death() -> None:
        pass


        self.view.set_exp_adder(self.add_expense)
        self.view.set_exp_deleter(self.delete_expenses)
        self.view.set_exp_modifier(self.modify_expense)


def handle_error(widget, handler):
    def inner(*args, **kwargs):
        try:
            handler(*args, **kwargs)
        except ValueError as ex:
            QtWidgets.QMessageBox.critical(widget, 'Ошибка', str(ex))
    return inner


class View:

    categories: list[Category] = []
    main_window: MainWindow
    budget_table: BudgetTableGroup
    new_expense: NewExpenseGroup
    expenses_table: ExpensesTableGroup
    cats_edit_window: CategoriesEditWindow

    def __init__(self):
        self.config_app()
        self.config_cats_edit()
        self.budget_table = BudgetTableGroup(self.modify_budget)
        self.new_expense = NewExpenseGroup(self.categories, 
                                           self.cats_edit_show,
                                           self.add_expense)
        self.expenses_table = ExpensesTableGroup(self.catpk_to_name,
                                                 self.modify_expense,
                                                 self.delete_expenses)
        self.config_main_window()
        

    def show_main_window(self):
        self.main_window.show()
        print("run app")
        print(f"Application ends with exit status {self.app.exec()}")
        sys.exit()
    
    def config_app(self):
        self.app = QtWidgets.QApplication(sys.argv)
        #self.app.setQuitOnLastWindowClosed(False)
        self.app.setStyle("Fusion")
        self.app.setPalette(PaletteMode(is_dark_mode=True))

    def config_main_window(self):
        self.main_window = MainWindow(self.budget_table, 
                                      self.new_expense, 
                                      self.expenses_table)
        self.main_window.resize(1000, 800)

    def config_cats_edit(self):
        self.cats_edit_window = CategoriesEditWindow(self.categories, 
                                                     self.add_category,
                                                     self.delete_category)
        self.cats_edit_window.setWindowTitle("Редактирование категорий")
        self.cats_edit_window.resize(600, 600)

    def cats_edit_show(self):
        self.cats_edit_window.show()

    def set_categories(self, cats: list[Category]) -> None:
        self.categories = cats
        self.new_expense.set_categories(self.categories)
        self.cats_edit_window.set_categories(self.categories)

    def catpk_to_name(self, pk: int) -> str:
        name = [c.name for c in self.categories if int(c.pk) == int(pk)]
        if len(name):
            return str(name[0])
        return ""

    # def set_cat_modifier(self, handler: Callable[[Category], None]):
    #     pass

    def set_cat_adder(self, handler):
        """ устанавливает метод добавления категории (из bookkeeper_app)"""
        self.cat_adder = handle_error(self.main_window, handler)

    def set_cat_deleter(self, handler):
        """ устанавливает метод удаления категории (из bookkeeper_app)"""
        self.cat_deleter = handle_error(self.main_window, handler)

    def set_cat_checker(self, handler):
        """ устанавливает метод проверки существования категории (из bookkeeper_app)"""
        self.cat_checker = handle_error(self.main_window, handler)
        self.cats_edit_window.set_cat_checker(self.cat_checker)

    def add_category(self, name, parent):
        self.cat_adder(name, parent)

    def delete_category(self, cat_name: str):
        self.cat_deleter(cat_name)

    def set_expenses(self, exps: list[Expense]) -> None:
        self.expenses = exps
        self.expenses_table.set_expenses(self.expenses)

    def set_exp_adder(self, handler):
        """ устанавливает метод добавления траты (из bookkeeper_app)"""
        self.exp_adder = handle_error(self.main_window, handler)

    def set_exp_deleter(self, handler):
        """ устанавливает метод удаления трат (из bookkeeper_app)"""
        self.exp_deleter = handle_error(self.main_window, handler)

    def set_exp_modifier(self, handler):
        """ устанавливает метод изменения траты (из bookkeeper_app)"""
        self.exp_modifier = handle_error(self.main_window, handler)

    def add_expense(self, amount: str, cat_name: str, comment: str = ""):
        self.exp_adder(amount, cat_name, comment)

    def delete_expenses(self, exp_pks: set[int]) -> None:
        if len(exp_pks) == 0:
            QtWidgets.QMessageBox.critical(self.main_window, 
                            'Ошибка', 
                            'Траты для удаления не выбраны.')
        else:
            reply = QtWidgets.QMessageBox.question(self.main_window, 
                    'Удаление трат',
                    'Вы уверены, что хотите удалить все выбранные траты?')
            if reply == QtWidgets.QMessageBox.Yes:
                self.exp_deleter(exp_pks)
        

    def modify_expense(self, pk, attr, new_val):
        self.exp_modifier(pk, attr, new_val)

    def set_budgets(self, budgets: list[Budget]) -> None:
        self.budgets = budgets
        self.budget_table.set_budgets(self.budgets)

    def set_bdg_modifier(self, handler):
        """ устанавливает метод изменения бюджета (из bookkeeper_app)"""
        self.bdg_modifier = handle_error(self.main_window, handler)

    def modify_budget(self, pk: int, new_limit: str, period: str):
        self.bdg_modifier(pk, new_limit, period)

    def death(self):
        msg = "При добавлении последней траты обнаружен дефицит бюджета " \
            + "Отмените последнюю покупку, чтобы восстановить течение судьбы,"
        QtWidgets.QMessageBox.warning(self.main_window, 'Превышение бюджета', msg)