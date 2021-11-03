from PyQt5.QtWidgets import QApplication
import Layout.Main_Window as layout
import sys


def main():
    app = QApplication(sys.argv)
    mainWindow = layout.MainWindow()

    mainWindow.show()
    app.exec_()

if __name__ == '__main__':
    main()
