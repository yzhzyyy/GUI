# table_view_window.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QListWidget, QListWidgetItem, \
    QCheckBox, QMessageBox
from table_content_window import TableContentWindow
from PyQt5.QtCore import Qt


class TableViewWindow(QWidget):
    def __init__(self, connection, database, previous_window):
        super().__init__()
        self.connection = connection
        self.database = database
        self.previous_window = previous_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'Select Table in {self.database}')
        self.layout = QVBoxLayout()

        self.combo_layout = QHBoxLayout()

        self.table_combobox = QComboBox(self)
        self.table_combobox.currentTextChanged.connect(self.on_table_selected)
        self.combo_layout.addWidget(self.table_combobox)

        self.view_button = QPushButton('View Table', self)
        self.view_button.clicked.connect(self.view_table)
        self.combo_layout.addWidget(self.view_button)

        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(self.go_back)
        self.combo_layout.addWidget(self.back_button)

        self.layout.addLayout(self.combo_layout)

        self.attributes_list = QListWidget(self)
        self.layout.addWidget(self.attributes_list)

        self.setLayout(self.layout)
        self.populate_tables()

    def populate_tables(self):
        cursor = self.connection.cursor()
        cursor.execute(f"USE {self.database}")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        self.table_combobox.addItems([table[0] for table in tables])
        cursor.close()

    def on_table_selected(self, table_name):
        self.attributes_list.clear()
        if not table_name:
            return
        cursor = self.connection.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        for column in columns:
            item = QListWidgetItem(column[0])
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.attributes_list.addItem(item)
        cursor.close()

    def view_table(self):
        selected_table = self.table_combobox.currentText()
        selected_columns = [item.text() for item in self.attributes_list.findItems("*", Qt.MatchWildcard) if
                            item.checkState() == Qt.Checked]

        if len(selected_columns) == 0 or len(selected_columns) > 10:
            QMessageBox.warning(self, "Invalid Selection", "Please select between 1 and 10 attributes.")
            return

        self.table_content_window = TableContentWindow(self.connection, self.database, selected_table, selected_columns,
                                                       self)
        self.table_content_window.show()
        self.hide()

    def go_back(self):
        self.previous_window.show()
        self.close()
