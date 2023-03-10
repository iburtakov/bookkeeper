from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from bookkeeper.view.group_widgets import GroupLabel
from bookkeeper.models.budget import Budget


class BudgetTableWidget(QtWidgets.QTableWidget):
    def __init__(self, bdg_modifier, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bdg_modifier = bdg_modifier
        self.setColumnCount(3)
        self.setRowCount(3)
        hheaders = "Бюджет Потрачено Остаток".split()
        self.setHorizontalHeaderLabels(hheaders)
        vheaders = "День Неделя Месяц".split()
        self.setVerticalHeaderLabels(vheaders)
        for h in [self.horizontalHeader(), self.verticalHeader(),]:
            h.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)     
        self.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked)
        self.cellDoubleClicked.connect(self.double_click)
        #self.verticalHeader().hide()

    def double_click(self, row, columns):
        self.cellChanged.connect(self.cell_changed)

    def cell_changed(self, row, column):
        self.cellChanged.disconnect(self.cell_changed)
        pk = self.data[row][-1]
        new_limit = self.item(row, column).text()
        row_to_period = {0:"day", 1:"week", 2:"month"}
        self.bdg_modifier(pk, new_limit, row_to_period[row])

    def add_data(self, data: list[list[str]]):
        self.data = data
        for i, row in enumerate(data):
            for j, x in enumerate(row[:-1]):
                self.setItem(
                    i, j,
                    QtWidgets.QTableWidgetItem(x.capitalize())
                )
                self.item(i, j).setTextAlignment(Qt.AlignCenter)
                if j == 0:
                    self.item(i, j).setFlags(Qt.ItemIsEditable 
                                             | Qt.ItemIsEnabled 
                                             | Qt.ItemIsSelectable)
                else: 
                    self.item(i, j).setFlags(Qt.ItemIsEnabled)


class BudgetTableGroup(QtWidgets.QGroupBox):
    def __init__(self, bdg_modifier, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vbox = QtWidgets.QVBoxLayout()
        self.label = GroupLabel("<b>Бюджет</b>")
        self.vbox.addWidget(self.label)
        self.table = BudgetTableWidget(bdg_modifier)
        #self.table.add_data(self.data)
        self.vbox.addWidget(self.table)
        self.setLayout(self.vbox)

    def set_budgets(self, budgets: list[Budget]):
        self.budgets = budgets
        self.data = self.budgets_to_data(self.budgets)
        self.table.clearContents()
        self.table.add_data(self.data)

    def budgets_to_data(self, budgets: list[Budget]):
        data = []
        for period in ["day", "week", "month"]:
            bdg = [b for b in budgets if b.period == period]
            if len(bdg) == 0:
                data.append(["- Не установлен -", "", "", None])
            else:
                b = bdg[0]
                data.append([str(b.limitation), str(b.spent),
                            str(int(b.limitation) - int(b.spent)), b.pk])
        return data    