import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from modules.FramelessWindow import FramelessWindow


class BaseUI(QWidget):
    def __init__(self, *args, **kwargs):
        super(BaseUI, self).__init__(*args, **kwargs)

        self.title_bar = args[0].titleBar
        self.MainWindow = args[0]
        self.MainWindow.setWindowTitle("<b>NeuraMade app</b>")
        self.MainWindow.resize(560, 600)

        # Вспомогательные переменные
        self.datasets_types = {'file': ['*.csv', '*.xls', '*.xml', '*.db', '*.xls', '*.fwf', '*.json'],
                               'dir': ''}
        self.dataset_info = {}
        self.model_context = {}

        # Создание контейнеров выравнивания
        self.main_vbox = QVBoxLayout(self)
        self.base_form = QFormLayout(self)
        self.type_hbox = QHBoxLayout(self)
        self.path_form = QFormLayout(self)
        self.graph_hbox = QHBoxLayout(self)

        # Основной текст и вывод информации
        self.type_qlb = QLabel('Выберите тип задачи: ', self)
        self.path_qlb = QLabel('Введите путь к дата сету: : ', self)
        self.target_qlb = QLabel('Введите название целевой переменной: ', self)
        self.graphs_qlb = QLabel('Выберите виды графиков отображения результата: ', self)

        self.console_qte = ConsoleTextEdit()

        # Варианты выбора и поля для ввода текста
        self.type_rb_reg = QRadioButton('Регрессия')
        self.type_rb_cl = QRadioButton('Классификация')
        self.type_rb_vis = QRadioButton('Компьютерное зрение')
        self.path_qle = QLineEdit(self)
        self.path_btn = QPushButton(icon=QIcon('images/choose_path.png'))
        self.target_qle = QLineEdit(self)
        self.graphs_chb_hist = QCheckBox('Гистограмма')
        self.graphs_chb_sct = QCheckBox('График разброса')
        self.graphs_chb_mtrx = QCheckBox('Матрица соответствий')

        self.create_btn = QPushButton('Создать', self)

        # Настройка полей ввода
        self.path_qle.setPlaceholderText('Your dataset path')
        self.path_qle.setFixedSize(300, 25)
        self.path_btn.setFixedSize(15, 15)
        self.path_btn.clicked.connect(self.choose_path)
        self.target_qle.setPlaceholderText('Пример: "Value"')
        self.path_btn.clicked.connect(self.create_model)
        self.console_qte.setFixedHeight(200)

        # Настройка контейнеров выравнивания
        self.type_hbox.setSpacing(10)
        self.type_hbox.addWidget(self.type_rb_reg)
        self.type_hbox.addWidget(self.type_rb_cl)
        self.type_hbox.addWidget(self.type_rb_vis)

        self.path_form.addRow(self.path_qle, self.path_btn)

        self.graph_hbox.addWidget(self.graphs_chb_hist)
        self.graph_hbox.addWidget(self.graphs_chb_sct)
        self.graph_hbox.addWidget(self.graphs_chb_mtrx)

        self.base_form.addRow(self.type_qlb, self.type_hbox)
        self.base_form.addRow(self.path_qlb, self.path_form)
        self.base_form.addRow(self.target_qlb, self.target_qle)
        self.base_form.addRow(self.graphs_qlb, self.graph_hbox)

        self.main_vbox.addLayout(self.base_form)
        self.main_vbox.addWidget(self.create_btn)
        self.main_vbox.addWidget(self.console_qte)

        self.setLayout(self.main_vbox)

    def choose_path(self):
        if self.type_rb_vis.isChecked():
            self.dataset_info['path'] = QFileDialog.getExistingDirectory(
                self, 'Open file', '')
        elif self.type_rb_vis.isChecked() is False:
            sup_types = ' '.join(self.datasets_types['file'])
            self.dataset_info['path'] = QFileDialog.getOpenFileName(
                self, 'Open file', '', f"Datasets files ({sup_types})"
            )[0]
            self.dataset_info['file_type'] = self.dataset_info['path'].split('.')[-1]
        else:
            raise 'Path error'
        if self.dataset_info['path']:
            self.path_qle.setText(self.dataset_info['path'])

    def create_model(self):
        pass

    def align(self):
        win = self.MainWindow
        desk = QApplication.desktop()
        x = (desk.width() - win.width()) // 2
        y = (desk.height() - win.height()) // 2
        self.MainWindow.move((x, y), filter=True)


# Класс для вывода содержимого консоли сразу в приложение
class ConsoleTextEdit(QTextEdit):
    def __init__(self, *args):
        super(ConsoleTextEdit, self).__init__(*args)

        self.setReadOnly(True)
        self.setPlaceholderText('Результат выполнения')

        self.all_output = []
        sys.stdout = self

    def setText(self, text, p_str=None):
        self.write(text)

    def write(self, text):
        self.all_output.append(text)
        self.setText(''.join(self.all_output))


if __name__ == "__main__":
    from sys import argv, exit
    from PyQt5.QtWidgets import QApplication, QWidget

    output = sys.stdout
    app = QApplication(argv)
    w = FramelessWindow()  # Модуль для создания окон без рамок
    w.setWidget(BaseUI(w))  # Добавить свое окно
    w.show()
    sys.stdout = output
    exit(app.exec_())
