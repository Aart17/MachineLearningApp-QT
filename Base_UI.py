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

        self.form = QFormLayout(self)
        self.hbox = QHBoxLayout(self)
        self.path_form = QFormLayout(self)

        self.type_qlb = QLabel('Выберите тип задачи: ', self)
        self.path_qlb = QLabel('Введите путь к дата сету: : ', self)

        self.type_rb_reg = QRadioButton('Регрессия')
        self.type_rb_cl = QRadioButton('Классификация')
        self.type_rb_vis = QRadioButton('Компьютерное зрение')
        self.path_qle = QLineEdit(self)
        self.path_btn = QPushButton(icon=QIcon('images/choose_path.png'))

        self.path_qle.setPlaceholderText('Your dataset path')
        self.path_btn.setFixedSize(15, 15)

        self.hbox.setSpacing(10)
        self.hbox.addWidget(self.type_rb_reg)
        self.hbox.addWidget(self.type_rb_cl)
        self.hbox.addWidget(self.type_rb_vis)

        self.path_form.addRow(self.path_qle, self.path_btn)

        self.form.addRow(self.type_qlb, self.hbox)
        self.form.addRow(self.path_qlb, self.path_form)
        self.setLayout(self.form)

    def align(self):
        win = self.MainWindow
        desk = QApplication.desktop()
        x = (desk.width() - win.width()) // 2
        y = (desk.height() - win.height()) // 2
        self.MainWindow.move((x, y), filter=True)


if __name__ == "__main__":
    from sys import argv, exit
    from PyQt5.QtWidgets import QApplication, QWidget

    app = QApplication(argv)
    w = FramelessWindow()  # Модуль для создания окон без рамок
    w.setWidget(BaseUI(w))  # Добавить свое окно
    w.show()
    exit(app.exec_())
