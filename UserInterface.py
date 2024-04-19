import sys
from tkinter import CURRENT
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "Milestone3App.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Milestone3(QMainWindow):
    def __init__(self):
        super(Milestone3, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.enterPW.clicked.connect(self.connectUI)
        

    def connectUI(self):
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipcodeList.itemSelectionChanged.connect(self.zipcodeChanged)
        self.ui.categoryList.itemSelectionChanged.connect(self.categoryChanged)
        self.ui.bName.textChanged.connect(self.getBusinessNames)
        self.ui.businesses.itemSelectionChanged.connect(self.displayBusinessCity)

    def executeQuery(self, sql_str):
        try:
            password = self.ui.databasePW.text()
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='" + password + "'")
            self.ui.enterPW.hide()
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "SELECT distinct state FROM business ORDER BY state;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print('Failed To Load State List!')
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()
        
    def stateChanged(self):
        self.ui.cityList.clear()
        self.ui.zipcodeList.clear()
        self.ui.categoryList.clear()
        self.ui.zipcodeMedianIncomeLabel.clear()
        self.ui.zipcodeAvgIncomeLabel.clear()
        self.ui.zipcodePopulationLabel.clear()
        self.ui.zipcodeNumBusinessesLabel.clear()
        self.ui.topCategories.clear()
        state = self.ui.stateList.currentText()
        if (self.ui.stateList.currentIndex() >= 0):
            sql_str = "SELECT distinct city FROM business WHERE state ='" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print('Failed To Load City List!')
              
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            sql_str = "SELECT name,address,city,stars,review_count,reviewrating,numcheckins,state FROM business WHERE state = '" + state + "' ORDER BY name;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0])-1)
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', '# of Checkins'])
                self.ui.businessTable.setColumnWidth(0,300)
                self.ui.businessTable.setColumnWidth(1,300)
                self.ui.businessTable.setColumnWidth(2,100)
                self.ui.businessTable.setColumnWidth(3,50)
                self.ui.businessTable.setColumnWidth(4,125)
                self.ui.businessTable.setColumnWidth(5,125)
                self.ui.businessTable.setColumnWidth(6,75)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0,len(results[0])-1):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print('Failed To Load Business Table on State Change!')
                
    def cityChanged(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            city = self.ui.cityList.selectedItems()[0].text()
            state = self.ui.stateList.currentText()
            self.ui.zipcodeList.clear()
            self.ui.categoryList.clear()
            self.ui.zipcodeMedianIncomeLabel.clear()
            self.ui.zipcodeAvgIncomeLabel.clear()
            self.ui.zipcodePopulationLabel.clear()
            self.ui.zipcodeNumBusinessesLabel.clear()
            self.ui.topCategories.clear()
            sql_str = "SELECT distinct zipcode FROM business WHERE state = '" + state + "' AND city = '" + city + "' ORDER BY  zipcode;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.zipcodeList.addItem(row[0])
            except:
                print('Failed To Load Zipcode Table on City Change!')
                
            sql_str = "SELECT name,address,city,stars,review_count,reviewrating,numcheckins,state FROM business WHERE state = '" + state + "' AND city = '" + city + "' ORDER BY  name;"
            try:
                results = self.executeQuery(sql_str)
                self.ui.businessTable.setRowCount(len(results))
                currentRowCount = 0
                for row in results:
                    for colCount in range(0,len(results[0])-1):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print('Failed To Load Business Table on City Change!')
                
    def zipcodeChanged(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (len(self.ui.zipcodeList.selectedItems()) > 0):
            city = self.ui.cityList.selectedItems()[0].text()
            state = self.ui.stateList.currentText()
            zipcode = self.ui.zipcodeList.selectedItems()[0].text()
            self.ui.categoryList.clear()
            self.ui.zipcodeMedianIncomeLabel.clear()
            self.ui.zipcodeAvgIncomeLabel.clear()
            self.ui.zipcodePopulationLabel.clear()
            self.ui.zipcodeNumBusinessesLabel.clear()
            self.ui.topCategories.clear()
            sql_str = "SELECT distinct category FROM businesscategory WHERE businessid IN (SELECT businessid FROM business WHERE state = '" + state + "' AND city = '" + city + "' AND zipcode = '" + zipcode + "') ORDER BY category;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.categoryList.addItem(row[0])
            except:
                print('Failed To Load Category Table on Zipcode Change!')
                
            sql_str = "SELECT name,address,city,stars,review_count,reviewrating,numcheckins,state FROM business WHERE state = '" + state + "' AND city = '" + city + "' AND zipcode = '" + zipcode + "' ORDER BY  name;"
            try:
                results = self.executeQuery(sql_str)
                self.ui.businessTable.setRowCount(len(results))
                currentRowCount = 0
                for row in results:
                    for colCount in range(0,len(results[0])-1):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print('Failed To Load Business Table on Zipcode Change!')
            
            sql_str = "SELECT medianincome, meanincome, population FROM zipcodedata WHERE zipcode = '" + zipcode + "';"
            try:
                results = self.executeQuery(sql_str)
                self.ui.zipcodeMedianIncomeLabel.setText(str(results[0][0]))
                self.ui.zipcodeAvgIncomeLabel.setText(str(results[0][1]))
                self.ui.zipcodePopulationLabel.setText(str(results[0][2]))
            except:
                print('Failed To Load Zipicode Stats on Zipcode Change!')
                
            sql_str = "SELECT COUNT(businessid) FROM business WHERE zipcode = '" + zipcode + "';"
            try:
                results = self.executeQuery(sql_str)
                self.ui.zipcodeNumBusinessesLabel.setText(str(results[0][0]))
            except:
                print('Failed To Load Zipicode Stats on Zipcode Change!')

            sql_str = "SELECT COUNT(DISTINCT b.businessid) AS num_businesses, c.category FROM business b JOIN businesscategory c ON b.businessid = c.businessid WHERE b.zipcode = '" + zipcode + "' GROUP BY c.category ORDER BY num_businesses DESC;"
            try:
                results = self.executeQuery(sql_str)
                self.ui.topCategories.setColumnCount(len(results[0]))
                self.ui.topCategories.setRowCount(len(results))
                self.ui.topCategories.setHorizontalHeaderLabels(['#', 'Category'])
                self.ui.topCategories.setColumnWidth(0,50)
                self.ui.topCategories.setColumnWidth(1,200)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0,len(results[0])):
                        self.ui.topCategories.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print('Failed To Load Top Category Table on Zipcode Change!')
    
    def categoryChanged(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (len(self.ui.zipcodeList.selectedItems()) > 0) and (len(self.ui.categoryList.selectedItems()) > 0):
            city = self.ui.cityList.selectedItems()[0].text()
            state = self.ui.stateList.currentText()
            zipcode = self.ui.zipcodeList.selectedItems()[0].text()
            category = self.ui.categoryList.selectedItems()[0].text()                
            sql_str = "SELECT name,address,city,stars,review_count,reviewrating,numcheckins,state FROM business WHERE state = '" + state + "' AND city = '" + city + "' AND zipcode = '" + zipcode + "' AND businessid IN (SELECT businessID FROM businesscategory WHERE category = '" + category + "') ORDER BY name;"
            try:
                results = self.executeQuery(sql_str)
                self.ui.businessTable.setRowCount(len(results))
                currentRowCount = 0
                for row in results:
                    for colCount in range(0,len(results[0])-1):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print('Failed To Load Business Table on Category Change!')
        
    def getBusinessNames(self):
        self.ui.businesses.clear()
        businessname = self.ui.bName.text()
        sql_str = "SELECT name FROM business WHERE name LIKE '%" + businessname + "%' ORDER BY name;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.businesses.addItem(row[0])
        except:
            print('Query Failed!')
            
    def displayBusinessCity(self):
        businessname = self.ui.businesses.selectedItems()[0].text()
        sql_str = "SELECT city FROM business WHERE name = '" + businessname + "';"
        try:
            results = self.executeQuery(sql_str)
            self.ui.bCity.setText(results[0][0])
        except:
            print('Query Failed!')
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Milestone3()
    window.show()
    sys.exit(app.exec_())