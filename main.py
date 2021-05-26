import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QListWidget, QTextEdit,
                             QHBoxLayout, QInputDialog, QMessageBox, QTabWidget, QLineEdit)
from PyQt5.QtGui import QPalette, QColor, QFont
# ToDo Добавить возможность добавлять теги и делать быстрый поиск по тегам
# ToDo Добавить поле для редактирования названия заметки
# Todo Добавить возможность редактировать название блокнота

WIN_X, WIN_Y = 1400, 800
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
        self.tabWidget = QTabWidget(self)
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.lb_notebooks = QLabel("Список блокнотов")
        self.lw_notebooks = QListWidget()
        self.btn_add_notebook = QPushButton("Создать блокнот")
        self.btn_del_notebook = QPushButton("Удалить блокнот")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.lb_notes = QLabel("Список заметок")
        self.lw_notes = QListWidget()
        self.btn_add_note = QPushButton("Добавить заметку")
        self.btn_del_note = QPushButton("Удалить заметку")
        self.tabWidget.addTab(self.tab_2, "")
        self.le_namenote = QLineEdit("Название заметки")
        self.le_namenote.setFont(QFont("Arial", 18, True))
        self.btn_save = QPushButton("Сохранить")
        self.te_note_text = QTextEdit()

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "Блокноты")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "Заметки")
        self.tabWidget.setCurrentIndex(0)

    def layout_widgets(self):
        main_row = QHBoxLayout()

        colum1 = QVBoxLayout()  # Создаем невидимый виджет для привязки других виджетов
        colum1.addWidget(self.lw_notebooks)
        row1 = QHBoxLayout()
        row1.addWidget(self.btn_add_notebook, alignment=Qt.AlignCenter)
        row1.addWidget(self.btn_del_notebook, alignment=Qt.AlignCenter)
        colum1.addLayout(row1)
        self.tab.setLayout(colum1)

        colum2 = QVBoxLayout()  # Создаем невидимый виджет для привязки других виджетов
        colum2.addWidget(self.lw_notes)
        row2 = QHBoxLayout()
        row2.addWidget(self.btn_add_note, alignment=Qt.AlignCenter)
        row2.addWidget(self.btn_del_note, alignment=Qt.AlignCenter)
        colum2.addLayout(row2)
        self.tab_2.setLayout(colum2)

        main_row.addWidget(self.tabWidget, stretch=1)

        colum3 = QVBoxLayout()  # Создаем невидимый виджет для привязки других виджетов
        row = QHBoxLayout()
        row.addWidget(self.le_namenote)
        row.addWidget(self.btn_save, alignment=Qt.AlignRight)
        colum3.addLayout(row)
        colum3.addWidget(self.te_note_text)


        main_row.addLayout(colum3, stretch=3)

        self.setLayout(main_row)  # Привязываем линию к окну

    def connects(self):
        self.btn_save.clicked.connect(self.note_save)
        self.btn_add_notebook.clicked.connect(self.add_notebook)
        self.btn_add_note.clicked.connect(self.add_note)
        self.btn_del_notebook.clicked.connect(self.del_notebook)
        self.btn_del_note.clicked.connect(self.del_note)
        self.lw_notebooks.itemClicked.connect(self.show_notes)
        self.lw_notes.itemClicked.connect(self.show_note)

    def note_save(self):
        if self.lw_notebooks.selectedItems():
            notebook = self.lw_notebooks.selectedItems()[0].text()
            if self.lw_notes.selectedItems():
                note = self.lw_notes.selectedItems()[0].text()
                if note == self.le_namenote.text():
                    self.data[notebook][note]["текст"] = self.te_note_text.toPlainText()
                elif self.le_namenote.text() not in self.data[notebook]:
                    del self.data[notebook][note]
                    self.lw_notes.clear()
                    note = self.le_namenote.text()
                    self.data[notebook][note] = {
                            'текст': self.te_note_text.toPlainText(),
                            'теги': []
                        }
                    self.lw_notes.addItems(self.data[notebook])
                    self.lw_notes.setCurrentRow(0)
                else:
                    QMessageBox.warning(self, "Уведомление", "Заметка уже существует!")
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
                self.le_namenote.setText(note)
                self.te_note_text.setText(self.data[notebook][note]["текст"])
        else:
            QMessageBox.warning(self, "Уведомление", "Не выбран блокнот для заметки")

    def add_notebook(self):
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

    def add_note(self):
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

    def del_notebook(self):
        if self.lw_notebooks.selectedItems():
            if len(self.lw_notebooks) > 1:
                notebook = self.lw_notebooks.selectedItems()[0].text()
                reply = QMessageBox.warning(self, "Предупреждение",
                                            f"Вы уверены, что хотите удалить блокнот {notebook}",
                                            buttons=(QMessageBox.Yes | QMessageBox.Cancel))
                if reply == QMessageBox.Yes:
                    del self.data[notebook]
                    self.lw_notebooks.clear()
                    self.write_data()
                    self.start_load_data()
            else:
                QMessageBox.warning(self, "Уведомление", "Нельзя удалить единственный блокнот")
        else:
            QMessageBox.warning(self, "Уведомление", "Не выбран блокнот для удаления")

    def del_note(self):
        if self.lw_notebooks.selectedItems():
            notebook = self.lw_notebooks.selectedItems()[0].text()
            if self.lw_notes.selectedItems():
                if len(self.lw_notes) > 1:
                    note = self.lw_notes.selectedItems()[0].text()
                    reply = QMessageBox.warning(self, "Предупреждение",
                                                f"Вы уверены, что хотите удалить заметку {note}",
                                                buttons=(QMessageBox.Yes | QMessageBox.Cancel))
                    if reply == QMessageBox.Yes:
                        del self.data[notebook][note]
                        self.lw_notes.clear()
                        self.write_data()
                        self.show_notes()
                else:
                    QMessageBox.warning(self, "Уведомление", "Нельзя удалить единственную заметку")
            else:
                QMessageBox.warning(self, "Уведомление", "Не выбрана заметка для удаления")
        else:
            QMessageBox.warning(self, "Уведомление", "Не выбран блокнот для удаления заметки")


class QApp(QApplication):
    def __init__(self, list_str):
        super().__init__(list_str)
        self.set_fusion_style()

    def set_fusion_style(self):
        self.setStyle("Fusion")

        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)

        self.setPalette(dark_palette)

        self.setStyleSheet("QToolTip { color: #ffffff; "
                           "background-color: #2a82da; "
                           "border: 1px solid white; }")
        font = self.font()
        font.setPointSize(14)
        QApplication.instance().setFont(font)

app = QApp([])  # Создаем приложение
win = MainWindow()  # Создаем главный виджет - окно


app.exec()
