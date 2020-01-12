import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLineEdit
import names


class FormStarting(QMainWindow):
    def __init__(self):
        super().__init__()
        main_window = uic.loadUi('ui_files/first.ui', self)
        self.pushButton.clicked.connect(self.registration)
        self.pushButton_2.clicked.connect(self.vhod)
        self.con = sqlite3.connect('database/database.db')
        self.cur = self.con.cursor()

    def registration(self):
        global form
        form = Registration()
        form.show()

    def vhod(self):
        self.d = [i for i in self.cur.execute("SELECT login, password FROM players")]
        if (self.lineEdit.text(), self.lineEdit_2.text()) in self.d:
            names.menu = False
            names.game = True
            names.player_login = self.lineEdit.text()
            self.close()
        else:
            self.label_3.setText('Такого пользователя не существует.')


class Registration(QMainWindow):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('database/database.db')
        self.cur = self.con.cursor()
        main_window = uic.loadUi('ui_files/reg.ui', self)
        self.pushButton.clicked.connect(self.reg)
        self.comboBox.addItems(i[0] for i in
            list(self.cur.execute(
                'SELECT name FROM heroes'
            ))
        )
        self.comboBox.activated[str].connect(self.infohero)

    def infohero(self):
        self.label_6.setText(list(self.cur.execute(
            'SELECT description FROM heroes WHERE name = "{k}"'.format(k=self.comboBox.currentText())))[0][0])

    def reg(self):
        self.valid = [i[0] for i in list(self.cur.execute('SELECT login FROM players'))]
        if self.lineEdit.text() in self.valid:
            self.label_5.setText('Пользователь с таким логином уже существует')
        elif self.lineEdit.text() == '':
            self.label_5.setText('Логин не может быть пустым')
        elif len(self.lineEdit_2.text()) == '':
            self.label_5.setText('Пароль не может быть пустым')
        elif self.lineEdit_2.text() != self.lineEdit_3.text():
            self.label_5.setText('Пароли не совпадают.')
        else:
            self.cur.execute(
                'INSERT INTO players(login, hero, password, position) VALUES (?,?,?,?)',
                (
                    self.lineEdit.text(),
                    list(self.cur.execute(
                        'SELECT id FROM heroes WHERE name = "{nam}"'.format(nam=self.comboBox.currentText())))[0][0],
                    self.lineEdit_2.text(),
                    '1 1'
                )
            )
            self.con.commit()
            self.close()


app = QApplication(sys.argv)
form_menu = FormStarting()
form_menu.show()
app.exit(app.exec_())
