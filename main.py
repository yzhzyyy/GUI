import sys
from PyQt5.QtWidgets import QApplication
from mysql_connector_app import MySQLConnectorApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MySQLConnectorApp()
    ex.show()
    sys.exit(app.exec_())
