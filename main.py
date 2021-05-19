import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QListWidget, QTextEdit,
                             QHBoxLayout, QInputDialog, QMessageBox)

# ToDo Добавить возможность добавлять теги и делать быстрый поиск по тегам
# ToDo Добавить поле для редактирования названия заметки

WIN_X, WIN_Y = 1200, 800
filename = "data.json"

def default_note():
    note = {"Заметка по умолчанию": {
                        'текст': 'Это самое лучшее приложение для заметок в мире!',
                        'теги': ['добро', 'инструкция']}
            }
    return note


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.data = self.read_data()
        self.setWindowTitle("Заметки")
        self.resize(WIN_X, WIN_Y)
        self.create_widgets()
        self.layout_widgets()
        self.start_load_data()
        self.connects()
        self.show()

    def start_load_data(self):
        self.lw_notebooks.addItems(self.data)  # загрузили список блокнотов
        self.lw_notebooks.setCurrentRow(0)
        self.show_notes()

    def read_data(self):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            data = {"Блокнот по умолчанию": default_note()}
            return data

    def write_data(self):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.data, file, sort_keys=True, ensure_ascii=False)

    def create_widgets(self):
        self.lb_notebooks = QLabel("Список блокнотов")
        self.lw_notebooks = QListWidget()
        self.btn_add_notebooks = QPushButton("Создать блокнот")
        self.btn_del_notebooks = QPushButton("Удалить блокнот")
        self.lb_notes = QLabel("Список заметок")
        self.lw_notes = QListWidget()
        self.btn_add_notes = QPushButton("Добавить заметку")
        self.btn_del_note = QPushButton("Удалить заметку")
        self.btn_save = QPushButton("Сохранить")
        self.te_note_text = QTextEdit()

    def layout_widgets(self):
        main_row = QHBoxLayout()
        colum1 = QVBoxLayout()  # Создаем невидимый виджет для привязки других виджетов
        colum1.addWidget(self.lb_notebooks, alignment=Qt.AlignLeft)
        colum1.addWidget(self.lw_notebooks, 80, alignment=Qt.AlignCenter)
        row1 = QHBoxLayout()
        row1.addWidget(self.btn_add_notebooks, alignment=Qt.AlignCenter)
        row1.addWidget(self.btn_del_notebooks, alignment=Qt.AlignCenter)
        colum1.addLayout(row1)

        colum2 = QVBoxLayout()  # Создаем невидимый виджет для привязки других виджетов
        colum2.addWidget(self.lb_notes, alignment=Qt.AlignLeft)
        colum2.addWidget(self.lw_notes, 80, alignment=Qt.AlignCenter)
        row2 = QHBoxLayout()
        row2.addWidget(self.btn_add_notes, alignment=Qt.AlignCenter)
        row2.addWidget(self.btn_del_note, alignment=Qt.AlignCenter)
        colum2.addLayout(row2)

        colum3 = QVBoxLayout()  # Создаем невидимый виджет для привязки других виджетов
        row = QHBoxLayout()
        row.addWidget(self.btn_save, alignment=Qt.AlignRight)
        colum3.addLayout(row)
        colum3.addWidget(self.te_note_text, alignment=Qt.AlignCenter)

        main_row.addLayout(colum1, stretch=1)
        main_row.addLayout(colum2, stretch=1)
        main_row.addLayout(colum3, stretch=3)

        self.setLayout(main_row)  # Привязываем линию к окну

    def connects(self):
        self.btn_save.clicked.connect(self.note_save)
        self.btn_add_notebooks.clicked.connect(self.add_notebooks)
        self.btn_add_notes.clicked.connect(self.add_notes)
        self.lw_notebooks.itemClicked.connect(self.show_notes)
        self.lw_notes.itemClicked.connect(self.show_note)

    def note_save(self):
        if self.lw_notebooks.selectedItems():
            notebook = self.lw_notebooks.selectedItems()[0].text()
            if self.lw_notes.selectedItems():
                note = self.lw_notes.selectedItems()[0].text()
                self.data[notebook][note]["текст"] = self.te_note_text.toPlainText()
                self.write_data()
            else:
                QMessageBox.warning(self, "Уведомление", "Не выбрана заметка")
        else:
            QMessageBox.warning(self, "Уведомление", "Не выбран блокнот для заметки")

    def show_notes(self):
        """Получаем список заметок и отображаем его"""
        if self.lw_notebooks.selectedItems():
            notebook = self.lw_notebooks.selectedItems()[0].text()
            self.lw_notes.clear()
            self.lw_notes.addItems(self.data[notebook])
            self.lw_notes.setCurrentRow(0)
            self.show_note()
        else:
            QMessageBox.warning(self, "Уведомление", "Не выбран блокнот")

    def show_note(self):
        """Получаем текст из заметки с выделенным названием и отображаем его в поле редактирования"""
        if self.lw_notebooks.selectedItems():
            notebook = self.lw_notebooks.selectedItems()[0].text()
            if self.lw_notes.selectedItems():
                note = self.lw_notes.selectedItems()[0].text()
                self.te_note_text.setText(self.data[notebook][note]["текст"])
        else:
            QMessageBox.warning(self, "Уведомление", "Не выбран блокнот для заметки")

    def add_notebooks(self):
        name_notebooks, ok = QInputDialog.getText(self, "Создать блокнот", "Название блокнота: ")
        if ok and name_notebooks != "":
            if name_notebooks not in self.data:
                self.data[name_notebooks] = default_note()
                self.lw_notebooks.addItem(name_notebooks)
                self.write_data()
            else:
                QMessageBox.warning(self, "Уведомление", "Блокнот уже существует!")
        elif ok:
            QMessageBox.warning(self, "Уведомление", "Название не должно быть пустым!")

    def add_notes(self):
        if self.lw_notebooks.selectedItems():
            key = self.lw_notebooks.selectedItems()[0].text()
            name_note, ok = QInputDialog.getText(self, "Добавить заметку", "Название заметки: ")
            if ok and name_note != "":
                if name_note not in self.data[key]:
                    self.data[key][name_note] = {
                            'текст': '',
                            'теги': []
                        }
                    self.lw_notes.addItem(name_note)
                    self.write_data()
                else:
                    QMessageBox.warning(self, "Уведомление", "Заметка уже существует!")
            elif ok:
                QMessageBox.warning(self, "Уведомление", "Название не должно быть пустым!")
        else:
            QMessageBox.warning(self, "Уведомление", "Не выбран блокнот для заметки")


app = QApplication([])  # Создаем приложение
win = MainWindow()  # Создаем главный виджет - окно


app.exec()
