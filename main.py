from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QListWidget, QTextEdit,
                             QHBoxLayout)

# ToDo Добавить возможность добавлять теги и делать быстрый поиск по тегам

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
        self.lb_notebooks = QLabel("Список блокнотов")
        self.lw_notebooks = QListWidget()
        self.btn_add_notebooks = QPushButton("Создать блокнот")
        self.lb_notes = QLabel("Список заметок")
        self.lw_notes = QListWidget()
        self.btn_add_notes = QPushButton("Добавить заметку")
        self.btn_save = QPushButton("Сохранить")
        self.te_note_text = QTextEdit()

    def layout_widgets(self):
        main_row = QHBoxLayout()
        colum1 = QVBoxLayout()  # Создаем невидимый виджет для привязки других виджетов
        colum1.addWidget(self.lb_notebooks, alignment=Qt.AlignLeft)
        colum1.addWidget(self.lw_notebooks, alignment=Qt.AlignCenter, stretch=80)
        colum1.addWidget(self.btn_add_notebooks, alignment=Qt.AlignCenter)

        colum2 = QVBoxLayout()  # Создаем невидимый виджет для привязки других виджетов
        colum2.addWidget(self.lb_notes, alignment=Qt.AlignLeft)
        colum2.addWidget(self.lw_notes, alignment=Qt.AlignCenter, stretch=80)
        colum2.addWidget(self.btn_add_notes, alignment=Qt.AlignCenter)

        colum3 = QVBoxLayout()  # Создаем невидимый виджет для привязки других виджетов
        row = QHBoxLayout()
        row.addWidget(self.btn_save, alignment=Qt.AlignRight)
        colum3.addLayout(row)
        colum3.addWidget(self.te_note_text, alignment=Qt.AlignCenter)

        main_row.addLayout(colum1, stretch=20)
        main_row.addLayout(colum2, stretch=20)
        main_row.addLayout(colum3, stretch=60)

        self.setLayout(main_row)  # Привязываем линию к окну

    def connects(self):
        self.btn_save.clicked.connect(self.note_save)

    def note_save(self):
        pass


app = QApplication([])  # Создаем приложение
win = MainWindow()  # Создаем главный виджет - окно


app.exec()
