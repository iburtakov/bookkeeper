from datetime import datetime

from bookkeeper.view.view import AbstractView, View
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget

class Bookkeeper:
    
    def __init__(self,
                 view: AbstractView,
                 repository_type: type):
        self.view = view
        self.category_rep = repository_type[Category](
                            db_file="database/bookkeeper.db",
                            cls=Category)
        self.categories = self.category_rep.get_all()
        self.view.set_categories(self.categories)
        #self.view.set_cat_modifier(self.modify_cat)
        self.view.set_cat_adder(self.add_category)
        self.view.set_cat_deleter(self.delete_category)
        self.view.set_cat_checker(self.cat_checker)

        self.budget_rep = repository_type[Budget](
                           db_file="database/bookkeeper.db",
                           cls=Budget)
        self.view.set_bdg_modifier(self.modify_budget)

        self.expense_rep = repository_type[Expense](
                           db_file="database/bookkeeper.db",
                           cls=Expense)
        self.update_expenses()
        self.view.set_exp_adder(self.add_expense)
        self.view.set_exp_deleter(self.delete_expenses)
        self.view.set_exp_modifier(self.modify_expense)


    def start_app(self):
        self.view.show_main_window()
        
    # def modify_cat(self, cat: Category) -> None:
    #     self.category_rep.update(cat)
    #     self.view.set_categories(self.categories)

    def cat_checker(self, cat_name: str):
        if cat_name not in [c.name for c in self.categories]:
            raise ValueError(f'Категории "{cat_name}" не существует')

    def add_category(self, name, parent):
        if name in [c.name for c in self.categories]:
            raise ValueError(f'Категория "{name}" уже существует')
        if parent is not None:
            if parent not in [c.name for c in self.categories]:
                raise ValueError(f'Категории "{parent}" не существует')
            parent_pk = self.category_rep.get_all(where={'name':parent})[0].pk
        else:
            parent_pk = None
        cat = Category(name, parent_pk)
        self.category_rep.add(cat)
        self.categories.append(cat)
        self.view.set_categories(self.categories)

    def delete_category(self, cat_name: str):
        cat = self.category_rep.get_all(where={"name":cat_name})
        if len(cat) == 0:
            raise ValueError(f'Категории "{cat_name}" не существует')
        else:
            cat = cat[0]
        self.category_rep.delete(cat.pk)
        # меняет удаленную категорию на родителя (None если родителя нет)
        for child in self.category_rep.get_all(where={'parent':cat.pk}):
            child.parent = cat.parent
            self.category_rep.update(child)
        self.categories = self.category_rep.get_all()
        self.view.set_categories(self.categories)
        # устанавливает None вместо удаленной категории
        for exp in self.expense_rep.get_all(where={'category':cat.pk}):
            exp.category = None
            self.expense_rep.update(exp)
        self.update_expenses()
        
    def update_expenses(self):
        self.expenses = self.expense_rep.get_all()
        self.view.set_expenses(self.expenses)
        self.update_budgets()

    def add_expense(self, amount: str, cat_name: str, comment: str=""):
        try:
            amount = int(amount)
        except:
            raise ValueError('Чем это Вы расплачивались?\n'
                                + 'Введите сумму целым числом.')
        if amount <= 0:
            raise ValueError(f'Удачная покупка! Записывать не буду.')
        cat = self.category_rep.get_all(where={"name":cat_name.lower()})
        if len(cat) == 0:
            raise ValueError(f'Категории "{cat_name}" не существует')
        else:
            cat = cat[0]
        new_exp = Expense(amount, cat.pk, comment=comment)
        self.expense_rep.add(new_exp)
        self.update_expenses()
        if len([b for b in self.budgets if b.spent > b.limitation]):
            self.view.death()

    def modify_expense(self, pk, attr, new_val):
        exp = self.expense_rep.get(pk)
        if attr == "category":
            new_val = new_val.lower()
            if new_val not in [c.name for c in self.categories]:
                self.view.set_expenses(self.expenses)
                raise ValueError(f'Категории "{new_val}" не существует')
            new_val = self.category_rep.get_all(where={'name':new_val})[0].pk
        if attr == "amount":
            try:
                new_val = int(new_val)
            except:
                raise ValueError('Чем это Вы расплачивались?\n'
                                    + 'Введите сумму целым числом.')
            if new_val <= 0:
                self.view.set_expenses(self.expenses)
                raise ValueError(f'Удачная покупка! Записывать не буду.')
        if attr == "expense_date":
            try:
                new_val = datetime.fromisoformat(new_val).isoformat(
                                            sep='\t', timespec='minutes')
            except ValueError:
                self.view.set_expenses(self.expenses)
                raise ValueError(f'Неправильный формат даты.')
        setattr(exp, attr, new_val)
        self.expense_rep.update(exp)
        self.update_expenses()

    def delete_expenses(self, exp_pks: list[int]):
        for pk in exp_pks:
            self.expense_rep.delete(pk)
        self.update_expenses()

    def update_budgets(self):
        for budget in self.budget_rep.get_all():
            budget.update_spent(self.expense_rep)
            self.budget_rep.update(budget)
        self.budgets = self.budget_rep.get_all()
        self.view.set_budgets(self.budgets)


    def modify_budget(self, pk: int | None, new_limit: str, period: str):
        if new_limit == "" and pk is not None:
            self.budget_rep.delete(pk)
            self.update_budgets()
            return
        try:
            new_limit = int(new_limit)
        except ValueError:
            self.update_budgets()
            raise ValueError('Неправильный формат.\n'
                                + 'Введите сумму целым числом.')
        if new_limit < 0:
            self.update_budgets()
            raise ValueError('За этот период придется заработать.')
        if pk is None:
            budget = Budget(limitation=new_limit, period=period)
            self.budget_rep.add(budget)
        else:
            budget = self.budget_rep.get(pk)
            budget.limitation = new_limit
            self.budget_rep.update(budget)
        self.update_budgets()


if __name__ == '__main__':
    view = View()
    bookkeeper_app = Bookkeeper(view, SQLiteRepository)
    bookkeeper_app.start_app()