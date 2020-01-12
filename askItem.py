import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow


class askItem(QMainWindow):
    def __init__(self, type, item1, item2):
        super().__init__()
        uic.loadUi('askItem.ui', self)
        self.name1.setText(item1.name)
        self.str1.setText("Сила: " + item1.strength)
        self.agl1.setText("Ловкость: " + item1.agility)
        self.int1.setText("Интелект: " + item1.intellegent)
        if type == "weapon":
            self.dora1.setText("Урон: " + item1.dora)
        else:
            self.dora1.setText("Защита: " + item1.dora)
        if item2 != 0:
            self.name2.setText(item1.name)
            self.str2.setText("Сила: " + item2.strength)
            self.agl2.setText("Ловкость: " + item2.agility)
            self.int2.setText("Интелект: " + item2.intellegent)
            if type == "weapon":
                self.dora2.setText("Урон: " + item2.dora)
            else:
                self.dora2.setText("Защита: " + item2.dora)
        else:
            self.name2.setText(item1.name)
            if type == "weapon" or type == "shild":
                self.name2.setText("Кулаки")
            else:
                self.name2.setText("Ничего")
            self.str2.setText("Сила: " + "0")
            self.agl2.setText("Ловкость: " + "0")
            self.int2.setText("Интелект: " + "0")
            if type == "weapon":
                self.dora2.setText("Урон: " + "10")
            else:
                self.dora2.setText("Защита: " + "0")
        self.pushButton1.clicked.connect(self.returnTrue)
        self.pushButton1.clicked.connect(self.returnFasle)
        self.ret = False
        self.clicked = False

    def returnTrue(self):
        self.ret = True
        self.clicked = True
        self.close()

    def returnFasle(self):
        self.ret = False
        self.clicked = True
        self.close()
