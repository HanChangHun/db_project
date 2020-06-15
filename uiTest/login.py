# -*- coding: euc-kr -*-


from getbarcode import read_barcode

from PyQt5 import uic, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
import urllib.request

import psycopg2 as pg2
import sys

mainLayout = uic.loadUiType("mainWindow.ui")[0]
signinLayout = uic.loadUiType("signIn.ui")[0]
initialLayout = uic.loadUiType("initialLayout.ui")[0]

conn = pg2.connect(host="localhost", database="projectDB", user="postgres", password="0000", port="5433")
cur = conn.cursor()

global session # login session

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
        global session
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

    def  __init__(self, parent=None):
        global listview
        super(mainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Main Winow')

        self.show()
        self.pushButton_2.clicked.connect(self.read_barcode)

        self.showID.setText(session)
        self.logoutBtn.clicked.connect(self.logoutFunction)

        self.searchBtn.clicked.connect(self.searchFunction)

        listview = self.resultList

    def searchFunction(self):
        listview.setTextUp('제품명')
        listview.setTextDown('제품 회사명')



    def read_barcode(self):
        barcodes = read_barcode()
        self.temp_codes.setText('{}'.format(barcodes))

    def logoutFunction(self):
        global session
        session = ''
        self.close()

class signinWindow(QMainWindow, signinLayout):
    global ischecked
    ischecked= False # check overlap id

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
            veg=''
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
            print('no allergy')
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
            if veg=='':
                adduserQ =  "INSERT INTO usertable values('" + id + "', '" + pw + "', '" + gender + "', " + str(
                         age) + ", '" + allstr + "')"
            else:
                adduserQ = "INSERT INTO usertable values('" + id + "', '" + pw + "', '" + gender + "', " + str(
                         age) + ", '" + allstr + "', '" + veg + "')"

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
    createTypeQ = "CREATE TYPE gen AS ENUM ('f', 'm'); "  +\
                  "CREATE TYPE allergy AS ENUM ('난류', '우유', '메밀', '땅콩', '대두', '쇠고기',  '밀', '고등어', '게', '새우', '돼지고기', '복숭아', '오징어', '토마토', '아황산류', '호두', '잣', '키위', '닭고기', '조개류', '참깨'); " + \
                  "CREATE TYPE veg AS ENUM ('vegan', 'lactoVeg', 'ovoVeg', 'lactoOvoVeg', 'pescoVeg', 'polloVeg'); "

    createUserQ="CREATE TABLE IF NOT EXISTS UserTable (userID TEXT, password TEXT, gender gen, age INT, allergies allergy[], vName veg, primary key(userID));"

    # cur.execute(createTypeQ) # 존재하는지 체크하는 함수 생성 필요
    cur.execute(createUserQ)
    conn.commit()

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    initDB()
    myWindow = initWindow()
    myWindow.show()
    app.exec_()