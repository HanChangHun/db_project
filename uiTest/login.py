# coding=utf8

import sys

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtGui
import urllib.request
import psycopg2 as pg2
from getbarcode import read_barcode

mainLayout = uic.loadUiType("mainWindow.ui")[0]
signinLayout = uic.loadUiType("signIn.ui")[0]
initialLayout = uic.loadUiType("initialLayout.ui")[0]

if sys.platform.lower() == 'darwin':
    conn = pg2.connect(host="localhost", database="projectDB", user="postgres", password="0000", port="5433")
elif sys.platform == 'win32':
    conn = pg2.connect(host="localhost", database="projectDB", user="postgres", password="1234", port="5432")

cur = conn.cursor()

global session # login session
global searcharr
searcharr=[]

global sessionInfo
sessionInfo=[] # allergy, vegiterrian

class initWindow(QMainWindow, initialLayout):
    def __init__(self) :
        super(initWindow, self).__init__(parent=None)
        self.setupUi(self)

        self.setWindowTitle('Initial Window')

        self.show()

        self.inputPS_text.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signinBtn.clicked.connect(self.opensigninFunction)
        self.loginBtn.clicked.connect(self.loginFunction)

    def opensigninFunction(self):
        signinWindow(self)

    def loginmessegeFuntion(self):
        msg = QMessageBox()
        msg.setText("반갑습니다!! ")
        msg.exec_()

    def loginFunction(self):
        global session, sessionInfo
        id = self.inputID_text.text()
        pw = self.inputPS_text.text()

        if id != "" and pw!="": # null check
            # check login info is right
            loginQ = "SELECT * FROM usertable where userid= '"+id+"' AND password= '" +pw +"';"
            cur.execute(loginQ)
            userResult = cur.fetchall()

            print(userResult)

            if(len(userResult)== 0):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("아이디 비밀번호를 확인해주세요!!")
                msg.setWindowTitle("Error")
                msg.exec_()

                self.inputID_text.setText("")
                self.inputPS_text.setText("")
            else:
                self.loginmessegeFuntion()
                session=id
                sessionInfo=[userResult[0][4], userResult[0][5]]
                mainWindow(self)
                self.inputID_text.setText("")
                self.inputPS_text.setText("")

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("아이디 비밀번호를 입력해주세요!! ")
            msg.setWindowTitle("Error")
            msg.exec_()
        # if it's right open main window


class mainWindow(QMainWindow, mainLayout):
    global session, listview
    global searchArr
    global itemAllergy, itemRawmtrl

    def  __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Main Winow')

        self.show()
        self.pushButton_2.clicked.connect(self.read_barcode)

        self.showID.setText(session)
        self.logoutBtn.clicked.connect(self.logoutFunction)

        self.searchBtn.clicked.connect(self.searchFunction)
        self.resultList.itemClicked.connect(self.showResultFunction)

        self.searchBBtn.clicked.connect(self.searchBarcodeFunction)

        # self.alterAlist.currentIndexChanged.connect()
        # self.alterVlist.currentIndexChanged.connect()


    def showResultFunction(self): # 현재 에러
        global searcharr, listview
        global itemAllergy, itemRawmtrl

        if listview.currentItem().text()== "검색 결과가 없습니다. ":
            return
        else:
            index = listview.selectionModel().currentIndex().row()

            url = searcharr[index][3]
            data = urllib.request.urlopen(url).read()
            pixmap = QPixmap()
            pixmap.loadFromData(data)

            pixmap.scaled(self.productImg.width(), self.productImg.height(), QtCore.Qt.KeepAspectRatio)

            self.productImg.setPixmap(pixmap) # url 제품 사진
            self.productImg.setScaledContents(True)
            self.productImg.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

            self.productName.setText("제품명: "+searcharr[index][0])
            self.productAllergy.setText("알러지 유발 물질:" + searcharr[index][2])
            self.productNutrient.setText("영양정보: " + searcharr[index][4])
            self.productmtrl.setText("원재료: "+searcharr[index][1])

            itemAllergy = searcharr[index][2]
            itemRawmtrl = searcharr[index][1]

            self.showpersonalResult()

    def showpersonalResult(self):
        global itemAllergy, itemRawmtrl


        qPixmapVar = QPixmap()
        qPixmapVar.load("yes.png")
        qPixmapVar = qPixmapVar.scaled(81, 71)
        self.resultVImg.setPixmap(qPixmapVar)

        self.resultVText.setText("이 먹을 수 없는 "+"가 들어있어요! ") #

        qPixmapVar = QPixmap()
        qPixmapVar.load("no.png")
        qPixmapVar = qPixmapVar.scaled(81, 71)
        self.resultAImg.setPixmap(qPixmapVar)

        # 대체식품 검색 후 listview 선택하기. ()
        for i in range (0, len(searcharr)):
            self.alterAlist.addItem(searcharr[i][0]);
        # self.showResultFunction()

    def searchBarcodeFunction(self):
        global listview, searcharr

        searchtext = self.searchBTxt.text()

        searchQ = "SELECT prdlstname, rawmtrl, allergy, imgurl1, nutrient FROM foodinfo where barcode like '%" + searchtext + "%';"
        cur.execute(searchQ)
        searchResult = cur.fetchall()

        listview = self.resultList
        listview.clear()
        listview.setIconSize(QSize(60, 60))
        listview.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel);

        if len(searchResult) == 0:
            listview.addItem('검색 결과가 없습니다. ')
        else:
            searcharr.clear()
            for i in range(0, len(searchResult)):
                searcharr.append(searchResult[i])

                listview.addItem(searchResult[i][0])

                url = searchResult[i][3]
                data = urllib.request.urlopen(url).read()
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                icon = QIcon(pixmap)
                listview.item(i).setIcon(icon)

    def searchFunction(self):
        global listview, searcharr

        searchtext=self.searchTxt.text()

        searchQ = "SELECT prdlstname, rawmtrl, allergy, imgurl1, nutrient FROM foodinfo where prdlstname like '%" + searchtext + "%';"
        cur.execute(searchQ)
        searchResult = cur.fetchall()

        listview = self.resultList
        listview.clear()
        listview.setIconSize(QSize(60, 60))
        listview.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel);

        if len(searchResult)== 0:
            listview.addItem('검색 결과가 없습니다. ')
        else:
            searcharr.clear()
            for i in range (0, len(searchResult)):
                searcharr.append(searchResult[i])

                listview.addItem(searchResult[i][0])

                url = searchResult[i][3]
                data = urllib.request.urlopen(url).read()
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                icon = QIcon(pixmap)
                listview.item(i).setIcon(icon)

    def read_barcode(self):
        barcodes = read_barcode()
        self.searchBTxt.setText('{}'.format(barcodes))

    def logoutFunction(self):
        global session
        session = ''
        sessionInfo.clear()
        self.close()

class signinWindow(QMainWindow, signinLayout):
    global ischecked
    ischecked = False # check overlap id

    def __init__(self, parent=None):
        super(signinWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Sign In')

        self.show()

        self.setPass_text.setEchoMode(QtWidgets.QLineEdit.Password)
        self.checkOverlapBtn.clicked.connect(self.checkidFunction)
        self.signinBtnBox.accepted.connect(self.signinFunction)
        self.signinBtnBox.rejected.connect(self.closeFunction)

    def closeFunction(self):
        self.close()

    def signinFunction(self):
        global isfilled
        # check fully filled
        isfilled = False

        id = self.setID_text.text()
        pw = self.setPass_text.text()

        age = self.getAge_box.value()
        veg = self.vegCombo.currentText()

        if id and pw and age!=0:
            isfilled = True
        else:
            isfilled = False

        # get veg
        # 'vegan', 'lactoVeg', 'ovoVeg', 'lactoOvoVeg', 'pescoVeg', 'polloVeg', 'flex'
        if veg == '해당없음':
            veg='nan'
        elif veg == '비건':
            veg='vegan'
        elif veg == "락토 베지테리언":
            veg='lactoVeg'
        elif veg == "오보 베지테리언":
            veg='ovoVeg'
        elif veg == "락토 오보 베지테리언":
            veg='lactoOvoVeg'
        elif veg == "페스코 베지테리언":
            veg='pescoVeg'
        elif veg == "폴로 베지테리언":
            veg='polloVeg'

        # get gender
        if self.femaleBtn.isChecked():
            gender = 'f'
            isfilled = True
        elif self.maleBtn.isChecked():
            gender = 'm'
            isfilled = True
        else:
            self.fillerrormeassage()
            isfilled = False

        # get allergey
        allegy=[]
        if self.none_check.isChecked():
            print('nan')
        else:
            if self.bean_check.isChecked():
                allegy.append(self.bean_check.text())
            if self.beef_check.isChecked():
                allegy.append(self.beef_check.text())
            if self.buckwheat_check.isChecked():
                allegy.append(self.buckwheat_check.text())
            if self.egg_check.isChecked():
                allegy.append(self.egg_check.text())
            if self.milk_check.isChecked():
                allegy.append(self.milk_check.text())
            if self.peanut_check.isChecked():
                allegy.append(self.peanut_check.text())
            if self.wheat_check.isChecked():
                allegy.append(self.wheat_check.text())
            if self.crab_check.isChecked():
                allegy.append(self.crab_check.text())
            if self.mackerel_check.isChecked():
                allegy.append(self.mackerel_check.text())
            if self.peach_check.isChecked():
                allegy.append(self.peach_check.text())
            if self.pork_check.isChecked():
                allegy.append(self.pork_check.text())
            if self.shrimp_check.isChecked():
                allegy.append(self.shrimp_check.text())
            if self.squid_check.isChecked():
                allegy.append(self.squid_check.text())
            if self.tomato_check.isChecked():
                allegy.append(self.tomato_check.text())
            if self.acid_check.isChecked():
                allegy.append(self.acid_check.text())
            if self.calm_check.isChecked():
                allegy.append(self.calm_check.text())
            if self.chicken_check.isChecked():
                allegy.append(self.chicken_check.text())
            if self.kiwi_check.isChecked():
                allegy.append(self.kiwi_check.text())
            if self.pinenut_check.isChecked():
                allegy.append(self.pinenut_check.text())
            if self.sesame_check.isChecked():
                allegy.append(self.sesame_check.text())
            if self.walnut_check.isChecked():
                allegy.append(self.walnut_check.text())

        # parse allegy to string(enum type)
        allstr = str(allegy)
        allstr = allstr.replace("[", "{")
        allstr = allstr.replace("]", "}")
        allstr = allstr.replace("'", "")

        if isfilled and ischecked :

            adduserQ = "INSERT INTO usertable values('" + id + "', '" + pw + "', '" + gender + "', " + str(age) + ", '" + allstr + "', '" + veg + "')"
            print(adduserQ)
            cur.execute(adduserQ)
            conn.commit()
            self.signinmeassage()
            self.close()
        else:
            self.fillerrormeassage()

    def signinmeassage(self):
        msg = QMessageBox()
        msg.setText("회원 가입이 완료되었습니다!")
        msg.exec_()

    def fillerrormeassage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("양식을 전부 작성해 주세요!!")
        msg.exec_()

    def checkidFunction(self):
        global ischecked
        getid = self.setID_text.text()
        # check login info is right

        loginQ = "SELECT * FROM usertable where userid= '" + getid + "';"
        cur.execute(loginQ)
        userResult = cur.fetchall()

        if (len(userResult) == 0):
            msg = QMessageBox()
            msg.setText("사용 가능한 아이디 입니다! ")
            msg.exec_()
            ischecked = True

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("중복된 아이디 입니다! ")
            msg.setWindowTitle("Error")
            msg.exec_()

            self.setID_text.setText("")


class initDB():
    createUserQ="CREATE TABLE IF NOT EXISTS UserTable (userID TEXT, password TEXT, gender gen, age INT, allergies allergy[], vName veg, primary key(userID));"

    cur.execute(createUserQ, createUserQ)
    conn.commit()

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    initDB()
    myWindow = initWindow()
    myWindow.show()
    app.exec_()