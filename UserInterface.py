import sys
from tkinter import CURRENT
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

import math

qtCreatorFile = "Milestone3App.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# helper function that rounds x to 2 sig figs
def roundToSigFig(x):
                if (x != 0.0):
                    return round(x, -int(math.floor(math.log10(abs(x))-1)))
                else:
                    return x

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

    def executeQuery(self, sql_str):
        try:
            password = self.ui.databasePW.text()
            conn = psycopg2.connect("dbname='milestone3db' user='postgres' host='localhost' password='" + password + "'")
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

        #clear popular and successful business lists
        self.ui.popularBusinessTable.clear()
        self.ui.successfulBusinessTable.clear()

        state = self.ui.stateList.currentText()
        if (self.ui.stateList.currentIndex() >= 0):
            sql_str = "SELECT distinct city FROM business WHERE state ='" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print('Failed To Load City List!')
                
            sql_str = "SELECT distinct category FROM businesscategory WHERE businessid IN (SELECT businessid FROM business WHERE state = '" + state + "') ORDER BY category;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.categoryList.addItem(row[0])
            except:
                print('Failed To Load Category Table on Zipcode Change!')
              
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
            #clear popular and successful business lists
            self.ui.popularBusinessTable.clear()
            self.ui.successfulBusinessTable.clear()

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
                
            sql_str = "SELECT distinct category FROM businesscategory WHERE businessid IN (SELECT businessid FROM business WHERE state = '" + state + "' AND city = '" + city + "') ORDER BY category;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.categoryList.addItem(row[0])
            except:
                print('Failed To Load Category Table on Zipcode Change!')
                
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

            # update popular business list
            sql_str = """
                SELECT business.name as name, CAST(business.review_count as FLOAT)/ages.businessAge as reviewFrequency, local.localPopularity as localPopularity
                FROM business, (SELECT businessId, MAX(rating.date)-MIN(rating.date) as businessAge
                                FROM rating
                                GROUP BY businessId) ages, (SELECT businessId, business.numCheckins/CAST(zipcodeData.population as FLOAT) as localPopularity
                                                            FROM business, zipcodeData
                                                            WHERE business.zipcode = '""" + zipcode + """' and business.zipcode = zipcodeData.zipcode) local
                WHERE business.businessId = ages.businessId and business.businessId = local.businessId and business.zipcode = '""" + zipcode + """' and ages.businessAge <> 0;
            """

            try:
                results = self.executeQuery(sql_str)
                self.ui.popularBusinessTable.clear()
                self.ui.popularBusinessTable.setColumnCount(len(results[0])+1)
                self.ui.popularBusinessTable.setRowCount(len(results))
                self.ui.popularBusinessTable.setHorizontalHeaderLabels(['Rank', 'Business Name', 'Reviews Per Month', 'Visited by % Pop.'])

                # sort results by popularity score
                results = sorted(results, key = lambda row : row[1]*row[2], reverse = True)

                # populate popular business list
                for rowIndex in range(0, len(results)):
                    row = results[rowIndex]

                    # business rank
                    self.ui.popularBusinessTable.setItem(rowIndex, 0, QTableWidgetItem(str(rowIndex+1)))

                    # business name
                    self.ui.popularBusinessTable.setItem(rowIndex, 1, QTableWidgetItem(str(row[0])))

                    # review frequency
                    self.ui.popularBusinessTable.setItem(rowIndex, 2, QTableWidgetItem(str(roundToSigFig(row[1]*30.0))))

                    # local popularity
                    self.ui.popularBusinessTable.setItem(rowIndex, 3, QTableWidgetItem(str(roundToSigFig(row[2]*100.0))))

                self.ui.popularBusinessTable.setColumnWidth(0,50)
                self.ui.popularBusinessTable.setColumnWidth(1,200)
                self.ui.popularBusinessTable.setColumnWidth(2,150)
                self.ui.popularBusinessTable.setColumnWidth(3,150)
            except Exception as e:
                print('Failed To Load Popular Businesses on Zipcode Change!')
                print(e)

            # update successful business list
            sql_str = """
                SELECT ratingDiff.name as name, ages.businessAge as businessAge, ratingDiff.ratingDifference as ratingDifference
                FROM (SELECT businessId, MAX(rating.date)-MIN(rating.date) as businessAge
                    FROM rating
                    GROUP BY businessId) ages, (SELECT business.businessId as businessId, business.zipcode as zipcode, business.name as name, business.reviewrating - AVG(competetor.reviewrating) as ratingDifference
                                                FROM business as competetor, business, BusinessCategory as competetorCategory, BusinessCategory
                                                WHERE business.businessId <> competetor.businessId and
                                                    BusinessCategory.businessId = business.businessId and
                                                    competetorCategory.businessId = competetor.businessId and
                                                    BusinessCategory.category = competetorCategory.category
                                                GROUP BY business.businessId) ratingDiff
                WHERE ages.businessId = ratingDiff.businessId and ratingDiff.zipcode = '""" + zipcode + """'
            """

            try:
                results = self.executeQuery(sql_str)
                self.ui.successfulBusinessTable.clear()
                self.ui.successfulBusinessTable.setColumnCount(len(results[0])+1)
                self.ui.successfulBusinessTable.setRowCount(len(results))
                self.ui.successfulBusinessTable.setHorizontalHeaderLabels(['Rank', 'Business Name', 'Business Age (days)', 'Stars Above Average'])

                # sort results by success score
                results = sorted(results, key = lambda row : row[1]*(2**(row[2]+5)), reverse = True)

                # populate successful business list
                for rowIndex in range(0, len(results)):
                    row = results[rowIndex]

                    # business rank
                    self.ui.successfulBusinessTable.setItem(rowIndex, 0, QTableWidgetItem(str(rowIndex+1)))

                    # business name
                    self.ui.successfulBusinessTable.setItem(rowIndex, 1, QTableWidgetItem(str(row[0])))

                    # age
                    self.ui.successfulBusinessTable.setItem(rowIndex, 2, QTableWidgetItem(str(row[1])))

                    # rating difference
                    self.ui.successfulBusinessTable.setItem(rowIndex, 3, QTableWidgetItem(str(roundToSigFig(row[2]))))

                self.ui.successfulBusinessTable.setColumnWidth(0,50)
                self.ui.successfulBusinessTable.setColumnWidth(1,200)
                self.ui.successfulBusinessTable.setColumnWidth(2,150)
                self.ui.successfulBusinessTable.setColumnWidth(3,150)
            except Exception as e:
                print('Failed To Load Successful Businesses on Zipcode Change!')
                print(e)

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
        elif (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (len(self.ui.categoryList.selectedItems()) > 0):
            city = self.ui.cityList.selectedItems()[0].text()
            state = self.ui.stateList.currentText()
            category = self.ui.categoryList.selectedItems()[0].text()                
            sql_str = "SELECT name,address,city,stars,review_count,reviewrating,numcheckins,state FROM business WHERE state = '" + state + "' AND city = '" + city + "' AND businessid IN (SELECT businessID FROM businesscategory WHERE category = '" + category + "') ORDER BY name;"
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
        elif (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.categoryList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            category = self.ui.categoryList.selectedItems()[0].text()                
            sql_str = "SELECT name,address,city,stars,review_count,reviewrating,numcheckins,state FROM business WHERE state = '" + state + "' AND businessid IN (SELECT businessID FROM businesscategory WHERE category = '" + category + "') ORDER BY name;"
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
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Milestone3()
    window.show()
    sys.exit(app.exec_())