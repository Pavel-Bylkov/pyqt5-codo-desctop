from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QListWidget, QTextEdit,
                             QHBoxLayout)

WIN_X, WIN_Y = 1200, 800


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Заметки")
        self.resize(WIN_X, WIN_Y)
        self.create_widgets()
        self.layout_widgets()
        self.connects()
        self.show()

    def create_widgets(self):

        self.lb_notebooks = QLabel("Блокноты")
        self.lw_notebooks = QListWidget()
        self.lb_notes = QLabel("Заметки")
        self.lw_notes = QListWidget()
        self.btn_save = QPushButton("Сохранить")
        self.te_note_text = QTextEdit()

    def layout_widgets(self):
        main_row = QHBoxLayout()
        colum1 = QVBoxLayout()  # Создаем невидимый виджет для привязки других виджетов
        colum1.addWidget(self.lb_notebooks, alignment=Qt.AlignLeft, stretch=10)
        colum1.addWidget(self.lw_notebooks, alignment=Qt.AlignCenter, stretch=90)

        colum2 = QVBoxLayout()  # Создаем невидимый виджет для привязки других виджетов
        colum2.addWidget(self.lb_notes, alignment=Qt.AlignLeft, stretch=10)
        colum2.addWidget(self.lw_notes, alignment=Qt.AlignCenter, stretch=90)

        colum3 = QVBoxLayout()  # Создаем невидимый виджет для привязки других виджетов
        row = QHBoxLayout()
        row.addWidget(self.btn_save, alignment=Qt.AlignRight)
        colum3.addLayout(row, stretch=10)
        colum3.addWidget(self.te_note_text, alignment=Qt.AlignCenter, stretch=90)

        main_row.addLayout(colum1, stretch=25)
        main_row.addLayout(colum2, stretch=25)
        main_row.addLayout(colum3, stretch=50)

        self.setLayout(main_row)  # Привязываем линию к окну

    def connects(self):
        self.btn_save.clicked.connect(self.note_save)

    def note_save(self):
        pass


app = QApplication([])  # Создаем приложение
win = MainWindow()  # Создаем главный виджет - окно


app.exec()
