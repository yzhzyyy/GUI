from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt


class TableViewPage(QWidget):
    def __init__(self, connection, parent=None, database=None):
        super().__init__(parent)
        self.connection = connection
        self.database = database
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        title_label = QLabel(f"Tables in Database: {self.database}", self)
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setStyleSheet("""
            font-size: 34px;
            font-weight: bold;
            color: #A58978;
            padding: 0px 10px;
        """)
        title_label.setFixedHeight(40)
        main_layout.addWidget(title_label)

        body_widget = QWidget()
        body_layout = QHBoxLayout(body_widget)

        # Left side: Table names list
        self.table_list = QListWidget(self)
        self.table_list.setStyleSheet("""
            QListWidget {
                border: none;
            }
            QListWidget::item {
                height: 40px;
                padding-left: 10px;
                outline: none;
            }
            QListWidget::item:hover {
                background-color: #a58978;
                color: #ffffff;
            }
            QListWidget::item:selected {
                background-color: #a58978;
                color: #ffffff;
            }
        """)
        self.table_list.itemClicked.connect(self.on_table_item_clicked)
        self.load_table_names()
        body_layout.addWidget(self.table_list, 1)

        # Right side: Table data view
        self.table_data_widget = QTableWidget(self)
        body_layout.addWidget(self.table_data_widget, 3)

        main_layout.addWidget(body_widget)

    def load_table_names(self):
        cursor = self.connection.cursor()
        cursor.execute(f"USE {self.database}")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        self.table_list.clear()
        for table in tables:
            item = QListWidgetItem(table[0])
            self.table_list.addItem(item)

        cursor.close()

    def on_table_item_clicked(self, item):
        selected_table = item.text()
        self.load_table_data(selected_table)

    def load_table_data(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute(f"USE {self.database}")
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        self.table_data_widget.setRowCount(len(rows))
        self.table_data_widget.setColumnCount(len(columns))
        self.table_data_widget.setHorizontalHeaderLabels(columns)

        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                self.table_data_widget.setItem(i, j, QTableWidgetItem(str(col)))

        cursor.close()
