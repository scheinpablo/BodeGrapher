from PyQt5 import QtWidgets

from PycharmProjects.TC1.UIWindow import UIWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = UIWindow()
    window.show()
    app.exec()