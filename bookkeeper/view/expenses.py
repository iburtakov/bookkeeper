from PySide6 import QtWidgets

from bookkeeper.view.group_widgets import GroupLabel
from bookkeeper.models.expense import Expense


class ExpensesTableWidget(QtWidgets.QTableWidget):
    def __init__(self, exp_modifier, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exp_modifier = exp_modifier
        self.setColumnCount(4)
        self.setRowCount(50)
        self.headers = "Дата Сумма Категория Комментарий".split()
        self.col_to_attr = {0:"expense_date", 1:"amount", 2:"category", 3:"comment"}
        self.setHorizontalHeaderLabels(self.headers)
        header = self.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.Stretch)
        self.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked)
        self.cellDoubleClicked.connect(self.double_click)
        #self.verticalHeader().hide()

    def double_click(self, row: int, columns: int) -> None:
        self.cellChanged.connect(self.cell_changed)

    def cell_changed(self, row, column):
        self.cellChanged.disconnect(self.cell_changed)
        pk = self.data[row][-1]
        new_val = self.item(row, column).text()
        attr = self.col_to_attr[column]
        self.exp_modifier(pk, attr, new_val)

    def add_data(self, data: list[list[str]]):
        self.data = data
        for i, row in enumerate(data):
            for j, x in enumerate(row[:-1]):
                self.setItem(
                    i, j,
                    QtWidgets.QTableWidgetItem(x.capitalize())
                )

class ExpensesTableGroup(QtWidgets.QGroupBox):
    def __init__(self, catpk_to_name, exp_modifier, 
                       exp_deleter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.catpk_to_name = catpk_to_name
        self.exp_deleter = exp_deleter
        self.vbox = QtWidgets.QVBoxLayout()
        self.label = GroupLabel("<b>Последние траты</b>")
        self.vbox.addWidget(self.label)
        self.table = ExpensesTableWidget(exp_modifier)
        self.vbox.addWidget(self.table)
        self.del_button = QtWidgets.QPushButton('Удалить выбранные траты')
        self.del_button.clicked.connect(self.delete_expenses)
        self.vbox.addWidget(self.del_button)
        self.setLayout(self.vbox)

    def set_expenses(self, exps: list[Expense]):
        self.expenses = exps
        self.data = self.exps_to_data(self.expenses)
        self.table.clearContents()
        self.table.add_data(self.data)

    def exps_to_data(self, exps: list[Expense]):
        data = []
        for exp in exps:
            item = ["","","","",exp.pk]
            if exp.expense_date:
                item[0] = str(exp.expense_date)
            if exp.amount:
                item[1] = str(exp.amount)
            if exp.category:
                item[2] = str(
                    self.catpk_to_name(exp.category))
            if exp.comment:
                item[3] = str(exp.comment)
            data.append(item)
        return data

    def delete_expenses(self):
        pks_to_del = []
        chosen_ranges = self.table.selectedRanges()
        for ch_range in chosen_ranges:
            start = ch_range.topRow()
            end = min(ch_range.bottomRow(), len(self.data))
            pks_to_del += [i[-1] for i in self.data[start:end+1]]
        self.exp_deleter(set(pks_to_del))