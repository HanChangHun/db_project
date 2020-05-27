import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *

detailLayout = uic.loadUiType("detail.ui")[0]
searchlLayout = uic.loadUiType("search.ui")[0]
resultLayout = uic.loadUiType("searchResult.ui")[0]
signinLayout = uic.loadUiType("signIn.ui")[0]

class testWindow(QMainWindow, resultLayout):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Search Result')  # 타이틀바에 나타나는 창의 제목
        # 스크린에 보이기
        self.show()

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = testWindow()
    myWindow.show()
    app.exec_()