from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
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
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #574740;")
        main_layout.addWidget(title_label)

        self.table_widget = QTableWidget(self)
        self.load_table_data()
        main_layout.addWidget(self.table_widget)

    def load_table_data(self):
        cursor = self.connection.cursor()
        cursor.execute(f"USE {self.database}")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        self.table_widget.setRowCount(len(tables))
        self.table_widget.setColumnCount(1)
        self.table_widget.setHorizontalHeaderLabels(["Tables"])

        for i, table in enumerate(tables):
            self.table_widget.setItem(i, 0, QTableWidgetItem(table[0]))

        cursor.close()
