# table_content_window.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton

class TableContentWindow(QWidget):
    def __init__(self, connection, database, table, previous_window):
        super().__init__()
        self.connection = connection
        self.database = database
        self.table = table
        self.previous_window = previous_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'Contents of {self.table}')
        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)
        self.populate_table_contents()

    def populate_table_contents(self):
        cursor = self.connection.cursor()
        cursor.execute(f"USE {self.database}")
        cursor.execute(f"SELECT * FROM {self.table}")
        rows = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        display_text = f"Table: {self.table}\n\n" + "\t".join(column_names) + "\n"
        for row in rows:
            display_text += "\t".join(map(str, row)) + "\n"
        self.text_edit.setPlainText(display_text)
        cursor.close()

    def go_back(self):
        self.previous_window.show()
        self.close()
