import sys
from PySide2.QtCore import SIGNAL, Slot
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QTextEdit, QStatusBar, QGridLayout, QShortcut, QAction, QMainWindow, QLabel
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QMessageBox, QToolButton, QToolBar,  QCompleter
from PySide2 import QtGui, QtCore

import sqlite3


class HTMLHelper():
    def __init__(self):
        self.word = ""
        self.meanings = ""
        self.meaninglist = []
        self.htmlstring = ""


    def getHTMLword(self, word):
        self.word = "<div><span style='font-weight:bold;font-size:16px;'>"
        self.word = self.word + word
        self.word = self.word + "</span> ~ <span style='color:red; font-style: italic;'>noun</span></div>"
        return self.word

    def setmeaningslist(self, meanings):
        self.meaninglist = meanings.split('; ')

    def getHTMLmeanings(self, mlist): #அக்காரம்
        if((mlist.__sizeof__()) == 1):
            self.htmlstring = "<div>"
            self.htmlstring = self.htmlstring + "<span style='font-weight:bold;color:lightgray'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + 1 + ". " + "</span>"
            self.htmlstring = self.htmlstring + "<span style='font-size:14px;'>" + mlist[0] + "</span><br/>"
            self.htmlstring = self.htmlstring + "</div>"
        else:
            self.htmlstring = "<div>"
            for x in range(len(mlist)):
                self.htmlstring = self.htmlstring + "<span style='font-weight:bold;color:lightgray'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+ str(x+1) +". " +"</span>"
                self.htmlstring = self.htmlstring + "<span style='font-size:14px;'>" + mlist[x] +"</span><br/>"
                self.htmlstring = self.htmlstring + "</div>"

        return self.htmlstring


class DBHelper:
    def __init__(self):
        self.conn = sqlite3.connect("PTTamil.db")
        self.c = self.conn.cursor()
        self.c.execute("PRAGMA encoding='UTF-8'")


    def closeconn(self):
        self.c.close()
        self.conn.close()

    def getconn(self):
        return self.conn


    def getwordMeaning(self, word):
        self.c.execute("SELECT meanings from dictionary where word = ?", (word,))
        trow = self.c.fetchone()
        while trow is not None:
            return trow[0]

    def checkwordpresent(self, word):
        self.c.execute("SELECT count(*) from dictionary where word = ?", (word,))
        trow = self.c.fetchone()
        print(trow)
        while trow is not None:
            return trow[0]

class ClickableLineEdit(QLineEdit):
    clicked = QtCore.Signal()

    def mousePressEvent(self, event):
        super(ClickableLineEdit, self).mousePressEvent(event)
        self.clicked.emit()

class myWindow(QMainWindow):
    def __init__(self, parent=None):
        super(myWindow, self).__init__(parent)
        clicked = QtCore.Signal()
        self.primed = 0
        self.pointer = None
        self.histlist = []
        self.HIST_SIZE = 10


        self.tb = self.addToolBar("File")
        self.tb.setMovable(False)
        self.tb.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.tb.actionTriggered[QAction].connect(self.toolbtnpressed)

        self.previous = QAction(QIcon("./imgs/56.png"), "Previous", self)
        self.tb.addAction(self.previous)
        self.next = QAction(QIcon("./imgs/57.png"), "Next", self)
        self.tb.addAction(self.next)
        self.options = QAction(QIcon("./imgs/46.png"), "Options", self)
        self.tb.addAction(self.options)
        self.about = QAction(QIcon("./imgs/48.png"), "About", self)
        self.about.triggered.connect(self._show_about)
        self.tb.addAction(self.about)

        if(self.pointer is None):
            self.previous.setEnabled(False)
            self.next.setEnabled(False)

        wdg = QWidget(self)
        wdg.setMinimumSize(460, 460)

        glayout = QGridLayout()
        self.setMinimumSize(600, 600)

        self.le = ClickableLineEdit(wdg)
        self.le.setStyleSheet('color:maroon;font-size: 14px;')
        self.le.setObjectName("searchword")
        self.le.setText("Enter word to Search...!")

        self.le.clicked.connect(self.le.clear)

        self.wordlist = []
        self.loadwords()
        completer = QCompleter(self.wordlist, self.le)
        completer.setCompletionMode(completer.PopupCompletion)
        self.le.setCompleter(completer)


        self.pb = QPushButton(wdg)
        self.pb.setObjectName("go")
        self.pb.setText("தேடு")
        self.pb.setStyleSheet('color: #0077CC; font-weight:bold; font-size: 14px;')

        self.te = QTextEdit(wdg)
        self.te.setLineWrapMode(QTextEdit.NoWrap)

        self.sbar = QStatusBar()
        self.sbar.setStyleSheet('color:maroon;')
        self.sbar.showMessage('Ready...!')

        glayout.addWidget(QLabel("Find ", self), 1, 1)
        glayout.addWidget(self.le, 1, 2)
        glayout.addWidget(self.pb, 1, 3)
        glayout.addWidget(self.te, 2, 1, 1, 3)
        glayout.addWidget(self.sbar, 3, 1, 1, 3)

        wdg.setLayout(glayout)

        self.setWindowTitle("Power Tamil Dictionary")
        app_icon = QtGui.QIcon()
        app_icon.addFile('./imgs/PT-Icon.png', QtCore.QSize(16, 16))
        self.setWindowIcon(app_icon)


        self.connect(self.pb, SIGNAL("clicked()"), self.button_click)
        self.le.returnPressed.connect(self.pb.click)

        self.hotkey = {}
        self.hotkey['my_key'] = QShortcut(QtGui.QKeySequence("Ctrl+E"), self)
        self.hotkey['my_key'].activated.connect(self.animate_click)

        self.te.selectionChanged.connect(self.handleSelectionChanged)

        self.setCentralWidget(wdg)
    


    @Slot()
    def button_click(self):
        # sword is a QString object
        dbh = DBHelper()
        sword = self.le.text().strip()
        print(sword)
        if(sword.strip() == ""):
            self.sbar.showMessage("Please type a word to Search!")
        elif(dbh.checkwordpresent(sword) == 0):
            self.sbar.showMessage("Cannot find :: " + sword)
        else:
            self.addtohistory(sword)
            if(self.primed == 0):
                self.primed = 1
            self.enablePN()

            meanings = dbh.getwordMeaning(sword)
            hhelpr = HTMLHelper()
            HTML_word = hhelpr.getHTMLword(sword)
            hhelpr.setmeaningslist(meanings)
            HTML_meanings = hhelpr.getHTMLmeanings(hhelpr.meaninglist)

            print("bcPointer :: " + str(self.pointer))

            self.te.setText(HTML_word + HTML_meanings)
            self.sbar.showMessage("Found :: "+ sword)

    @Slot()
    def animate_click(self, selword):
        print("CALLED.....!!!!!!!!!")
        dbh = DBHelper()
        sword = selword
        print(sword)
        presentflag = dbh.checkwordpresent(sword)

        if(presentflag==0):
            self.sbar.showMessage("Cannot find :: " + sword)
        else:
            self.addtohistory(sword)
            if(self.primed == 0):
                self.primed = 1
                self.pointer = 0
            self.enablePN()

            meanings = dbh.getwordMeaning(sword)
            hhelpr = HTMLHelper()
            HTML_word = hhelpr.getHTMLword(sword)

            hhelpr.setmeaningslist(meanings)
            HTML_meanings = hhelpr.getHTMLmeanings(hhelpr.meaninglist)

            self.le.setText(sword)
            self.te.setText(HTML_word + HTML_meanings)
            self.sbar.showMessage("Found :: "+ sword)

    def histnavigate(self, selword):
        
        dbh = DBHelper()
        sword = selword.title()
        wmdict = dbh.getwordMeaning(sword)
        hhelpr = HTMLHelper()
        HTML_T = ""
        meanings = dbh.getwordMeaning(sword)
        hhelpr = HTMLHelper()
        HTML_word = hhelpr.getHTMLword(sword)
        hhelpr.setmeaningslist(meanings)
        HTML_meanings = hhelpr.getHTMLmeanings(hhelpr.meaninglist)
        HTML_T = HTML_word + HTML_meanings

        self.te.setText(HTML_T)
        self.sbar.showMessage("Found :: " + sword)


    def addtohistory(self, hword):
        if(self.pointer is None):
            if (not hword in self.histlist):
                self.histlist.append(hword)
                self.pointer = 0
        elif(len(self.histlist) == self.HIST_SIZE):
            self.histlist.pop(0)
            if (not hword in self.histlist):
                self.histlist.append(hword)
                self.pointer = self.HIST_SIZE - 1
        else:
            if (not hword in self.histlist):
                self.histlist.append(hword)
                self.pointer = self.pointer + 1
        self.enablePN()
        print(self.histlist)


    def toolbtnpressed(self, action):
        if(action.text()=="Previous"):
            print("PREV :: P::" +str(self.pointer) + " LS::" + str(len(self.histlist)))
            # edge case P0 L1
            if (self.pointer == 0 & len(self.histlist) ==1):
                self.pointer = self.pointer - 1
                self.le.setText(self.histlist[self.pointer])
                self.histnavigate(self.histlist[self.pointer])
                #print("previousR:: " + str(self.pointer))
            elif(self.pointer == 0):
                self.pointer = self.pointer
                self.le.setText(self.histlist[self.pointer])
                self.histnavigate(self.histlist[self.pointer])
                #print("previousL :: " + str(self.pointer))
                #print(self.histlist[self.pointer])
            # majority case
            elif(self.pointer <= len(self.histlist) - 1):
                self.pointer = self.pointer - 1
                self.le.setText(self.histlist[self.pointer])
                self.histnavigate(self.histlist[self.pointer])
                #print("previous:: " + str(self.pointer))

        elif(action.text()=="Next"):
            print("NEXT :: P::" + str(self.pointer) + " LS::" + str(len(self.histlist)))
            # edge case
            if (self.pointer == len(self.histlist) - 1):
                self.pointer = self.pointer
                self.le.setText(self.histlist[self.pointer])
                self.histnavigate(self.histlist[self.pointer])
                #print("nextR:: " + str(self.pointer))
            # edge case
            elif (self.pointer == 0):
                self.pointer = self.pointer + 1
                self.le.setText(self.histlist[self.pointer])
                self.histnavigate(self.histlist[self.pointer])
                #print("nextL:: " + str(self.pointer))
            # majority case
            elif (self.pointer < len(self.histlist) - 1):
                self.pointer = self.pointer + 1
                self.le.setText(self.histlist[self.pointer])
                self.histnavigate(self.histlist[self.pointer])
                #print("next:: " + str(self.pointer))
        self.enablePN()


    def enablePN(self):
        # pointer starts from 0 while len counts from 1
        if (self.pointer is None):
            pass
        elif(self.pointer == len(self.histlist)-1):
            self.previous.setEnabled(True)
            self.next.setEnabled(False)
        elif(self.pointer == 0):
            self.previous.setEnabled(False)
            self.next.setEnabled(True)
        elif(self.pointer < len(self.histlist)-1):
            self.previous.setEnabled(True)
            self.next.setEnabled(True)


    def handleSelectionChanged(self):
        cursor = self.te.textCursor()
        textSelected = cursor.selectedText()
        self.le.setText(textSelected)
        if(textSelected != ""):
            self.animate_click(textSelected)


    def _show_about(self):
        QMessageBox.about(self, 'About', '<p><b>PowerTamil Dictionary V1.0</b></p>'
                                         '<p>Copyright © 2020 Rajkumar Palani</p>'
                                         '<p>Power Tamil dictionary is free to use and distribute. </p>'
                                         '<p><a href="http://www.rajkumarpalani.com/software">www.rajkumarpalani.com/software</a></p>')
    def loadwords(self):
        with open("AllTamilWords.txt", "r", encoding="utf8") as f:
            self.wordlist = f.read().split()

def main():
    app = QApplication(sys.argv)
    ex = myWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()