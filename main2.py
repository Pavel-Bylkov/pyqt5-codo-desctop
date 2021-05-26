
from PyQt5.QtWidgets import (QApplication, QWidget)

from interface import Ui_Form


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Заметки")
        self.show()



app = QApplication([])  # Создаем приложение
win = MainWindow()  # Создаем главный виджет - окно


app.exec()
