#
# PySide Text Editor Example
#
# Based on
# https://www.binpress.com/tutorial/building-a-text-editor-with-pyqt-part-one/143
#

from PySide import QtCore, QtGui
from PySide.QtCore import Qt

import sys
import codecs

class Main(QtGui.QMainWindow):

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self,parent)

        self.filename = ""

        self.initUI()

    def initAction(self):

        self.newAction = QtGui.QAction(QtGui.QIcon("icons/new.png"),"New",self)
        self.newAction.setStatusTip("Create a new document from scratch.")
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.triggered.connect(self.new)

        self.openAction = QtGui.QAction(QtGui.QIcon("icons/open.png"),"Open file",self)
        self.openAction.setStatusTip("Open existing document")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)

        self.saveAction = QtGui.QAction(QtGui.QIcon("icons/save.png"),"Save",self)
        self.saveAction.setStatusTip("Save document")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)

        self.quitAction = QtGui.QAction(QtGui.QIcon("icons/quit.png"), "Quit", self)
        self.quitAction.setShortcut("Ctrl+Shift+W")
        self.quitAction.triggered.connect(QtCore.QCoreApplication.instance().quit)

        # Copy & Paste
        self.cutAction = QtGui.QAction(QtGui.QIcon("icons/cut.png"),"Cut to clipboard",self)
        self.cutAction.setStatusTip("Delete and copy text to clipboard")
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self.getActiveText().cut)

        self.copyAction = QtGui.QAction(QtGui.QIcon("icons/copy.png"),"Copy to clipboard",self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.getActiveText().copy)

        self.pasteAction = QtGui.QAction(QtGui.QIcon("icons/paste.png"),"Paste from clipboard",self)
        self.pasteAction.setStatusTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self.getActiveText().paste)

        self.undoAction = QtGui.QAction(QtGui.QIcon("icons/undo.png"),"Undo last action",self)
        self.undoAction.setStatusTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.getActiveText().undo)

        self.redoAction = QtGui.QAction(QtGui.QIcon("icons/redo.png"),"Redo last undone thing",self)
        self.redoAction.setStatusTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.getActiveText().redo)

        # Font
        self.fontLargerAction = QtGui.QAction(QtGui.QIcon("icons/font_larger.png"), "Use larger font",self)
        self.fontLargerAction.setStatusTip("Use larger font")
        self.fontLargerAction.setShortcut("Ctrl+=")
        self.fontLargerAction.triggered.connect(self.font_larger)

        self.fontSmallerAction = QtGui.QAction(QtGui.QIcon("icons/font_smaller.png"), "Use smaller font",self)
        self.fontSmallerAction.setStatusTip("Use smaller font")
        self.fontSmallerAction.setShortcut("Ctrl+-")
        self.fontSmallerAction.triggered.connect(self.font_smaller)

        # printing
        self.printAction = QtGui.QAction(QtGui.QIcon("icons/print.png"),"Print document",self)
        self.printAction.setStatusTip("Print document")
        self.printAction.setShortcut("Ctrl+P")
        self.printAction.triggered.connect(self.print_it)

        self.previewAction = QtGui.QAction(QtGui.QIcon("icons/preview.png"),"Page view",self)
        self.previewAction.setStatusTip("Preview page before printing")
        self.previewAction.setShortcut("Ctrl+Shift+P")
        self.previewAction.triggered.connect(self.preview)


    def initToolbar(self):

        self.toolbar = self.addToolBar("Options")

        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)

        self.toolbar.addSeparator()

        # Copy & Paste
        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)

        self.toolbar.addSeparator()

        # printing
        self.toolbar.addAction(self.printAction)
        self.toolbar.addAction(self.previewAction)

        self.toolbar.addSeparator()

        # Makes the next toolbar appear underneath this one
        #self.addToolBarBreak()

    def initFormatbar(self):

        self.formatbar = self.addToolBar("Format")

    def initMenubar(self):

        menubar = self.menuBar()

        file = menubar.addMenu("File")
        file.addAction(self.newAction)
        file.addAction(self.openAction)
        file.addAction(self.saveAction)
        file.addAction(self.printAction)
        file.addAction(self.previewAction)
        file.addAction(self.quitAction)

        edit = menubar.addMenu("Edit")

        edit.addAction(self.undoAction)
        edit.addAction(self.redoAction)
        edit.addAction(self.cutAction)
        edit.addAction(self.copyAction)
        edit.addAction(self.pasteAction)

        view = menubar.addMenu("View")
        view.addAction(self.fontLargerAction)

    # https://srinikom.github.io/pyside-docs/PySide/QtGui/QTabWidget.html
    def initTab(self):
        tabWidget = QtGui.QTabWidget(self);
        tabWidget.setDocumentMode(True)
        tabWidget.setTabsClosable(True)
        tabWidget.tabCloseRequested.connect(self.closeTab)

        self.tabWidget = tabWidget

    def initUI(self):

        self.initTab()
        self.addTextTab()

        self.initAction()

        self.initToolbar()
        self.initFormatbar()
        self.initMenubar()

        self.setCentralWidget(self.tabWidget)

        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()

        # x and y coordinates on the screen, width, height
        self.setGeometry(100,100,1030,800)

        self.setWindowTitle("Writer")
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

    # action
    def addTextTab(self, title = None):
        if title is None:
            title = "NEW1"

        # QTextEdit
        # http://doc.qt.io/qt-4.8/qtextedit.html
        text = QtGui.QTextEdit(self)

        # Tab stop
        text.acceptRichText = False
        text.setTabStopWidth(33)

        # cursor position
        text.cursorPositionChanged.connect(self.cursorPosition)

        tab = self.tabWidget.addTab(text, title)
        return text

    def getActiveText(self):
        return self.tabWidget.currentWidget()

    # Edit commands

    def new(self):
        self.addTextTab()

    def open(self):
        # Get filename and show only .txt files
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', ".", "(*.txt;*.py)")

        if self.filename and self.filename[0]:
            self.filename = self.filename[0]
            tab = self.addTextTab(self.filename)
            with codecs.open(self.filename, "r", "utf-8") as file:
                tab.setText(file.read())
            self.tabWidget.setCurrentWidget(tab)

    def save(self):

        # Only open dialog if there is no filename yet
        if not self.filename:
            self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        print(self.filename)

        # Append extension if not there yet
        if not self.filename.endswith(".txt"):
            self.filename += ".txt"

        # We just store the contents of the text file along with the
        # format in html, which Qt does in a very nice way for us
        with codecs.open(self.filename, "w", "utf-8") as file:
            file.write(self.getActiveText().toPlainText())

    def preview(self):

        # Open preview dialog
        preview = QtGui.QPrintPreviewDialog()

        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.getActiveText().print_(p))

        preview.exec_()

    def print_it(self):

        # Open printing dialog
        dialog = QtGui.QPrintDialog()

        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.getActiveText().document().print_(dialog.printer())

    # signal handler

    def cursorPosition(self):

        cursor = self.getActiveText().textCursor()

        # Mortals like 1-indexed things
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        self.statusbar.showMessage("Line: {} | Column: {}".format(line,col))

    def closeTab(self, index):
        self.tabWidget.removeTab(index);

    def font_larger(self):
        cursor = self.getActiveText().textCursor()
        self.getActiveText().selectAll()
        self.getActiveText().setFontPointSize(32)
        self.getActiveText().setTextCursor(cursor)

    def font_smaller(self):
        cursor = self.getActiveText().textCursor()
        self.getActiveText().selectAll()
        self.getActiveText().setFontPointSize(8)
        self.getActiveText().setTextCursor(cursor)

def main():

    app = QtGui.QApplication(sys.argv)

    main = Main()
    main.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
