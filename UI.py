import sys
import os
import pdb
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import recombine


filenames = []
filepaths = []

class Pdfitwindown(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def initUI(self):
    
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.setWindowTitle("pdfit")
        self.setWindowIcon(QIcon('./images/logo.jpg'))

        self.createFileGroupBox()
        self.createCommandGroupBox()
        self.createStartLayout()

        mainLayout = QVBoxLayout()
        self.centralwidget.setLayout(mainLayout)
        #菜单栏
        menubar = self.menuBar()
        menu_file = menubar.addMenu('File')
        act_addfile = menu_file.addAction(QIcon('./images/addfile.png'),'add files')
        act_addfile.setShortcut('Ctrl+O')
        act_addfile.triggered.connect(self.addfile)
        act_quit = menu_file.addAction('Quit')
        act_quit.setShortcut('Ctrl+Q')
        act_quit.triggered.connect(qApp.quit)
        menu_help = menubar.addMenu('Help')
        act_command_example = menu_help.addAction('command example')
        act_command_example.triggered.connect(self.command_example)
        menu_about = menubar.addMenu('About')
        act_about = menu_about.addAction('About')
        act_about.triggered.connect(self.about)
        
        #工具栏
        self.tool_RemoveEmpty = self.addToolBar('removeempty')
        self.tool_RemoveEmpty.setEnabled(False)
        act_RemoveEmpty = self.tool_RemoveEmpty.addAction(QIcon('./images/removeempty.png'),'Remove empty')
        act_RemoveEmpty.triggered.connect(self.removeEmpty)
        
        self.tool_MoveUp = self.addToolBar('moveup')
        self.tool_MoveUp.setEnabled(False)
        act_MoveUp = self.tool_MoveUp.addAction(QIcon('./images/moveup.png'),'Move up')
        act_MoveUp.triggered.connect(self.moveup)
        
        self.tool_MoveDown = self.addToolBar('movedown')
        self.tool_MoveDown.setEnabled(False)
        act_MoveDown = self.tool_MoveDown.addAction(QIcon('./images/movedown.png'),'Move down')
        act_MoveDown.triggered.connect(self.movedown)
        
        mainLayout.addWidget(self.FileGroupBox)
        mainLayout.addWidget(self.commandGroupBox)
        mainLayout.addLayout(self.starthbox)
                
        self.show()

    def createFileGroupBox(self):
        
        self.FileGroupBox = QGroupBox('files')
        layout = QGridLayout()
   
        # 创建表格
        self.tableWidger = QTableWidget(self)
        col = 1 #列
        row = 0 #行
        self.tableWidger.setRowCount(row)
        self.tableWidger.setColumnCount(col)
        self.tableWidger.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#宽度设置
        self.tableWidger.setEditTriggers(QTableWidget.NoEditTriggers)#不可编辑
        self.tableWidger.setHorizontalHeaderLabels(['filename'])
        self.tableWidger.verticalHeader().setVisible(False)#隐藏列表头
        self.tableWidger.setSelectionMode(QAbstractItemView.SingleSelection)#单选
        self.tableWidger.clicked.connect(self.tableClicked)
        
        # add file button
        self.btn_addfile = QPushButton('Add Files',self)
        self.btn_addfile.clicked.connect(self.addfile)
        
        # remove file button
        self.btn_removefile = QPushButton('Remove Files',self)
        self.btn_removefile.clicked.connect(self.removefile)
        self.btn_removefile.setEnabled(False)
        
        layout.addWidget(self.tableWidger,0,0,3,3)
        layout.addWidget(self.btn_removefile,3,1)
        layout.addWidget(self.btn_addfile,3,2)
        
        self.FileGroupBox.setLayout(layout)
        
    def createCommandGroupBox(self):
        self.commandGroupBox = QGroupBox('Input')
        layout = QFormLayout()
        
        label = QLabel("Command:",self)
        label.setFont(QFont("Roman times",10))
        
        self.text = QLineEdit(self)
        self.text.textChanged[str].connect(self.judgeStartBut)
        layout.addWidget(label)
        layout.addWidget(self.text)
        
        self.commandGroupBox.setLayout(layout)
    
    def createStartLayout(self):
        self.starthbox = QHBoxLayout()
        self.starthbox.addStretch(1)
        self.btn_start = QPushButton('Start processing')
        self.btn_start.setEnabled(False)
        self.starthbox.addWidget(self.btn_start)
        self.btn_start.clicked.connect(self.startProcess)

    def changefilenameToTable(self):
        row = len(filenames)
        self.tableWidger.setRowCount(row)
        for i in range(len(filenames)):
            item_filename = QTableWidgetItem(filenames[i])
            item_filename.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled) #设置物件的状态为只可被选择
            self.tableWidger.setItem(i,0,item_filename)
        self.judgeRemoveBut()
        self.judgeStartBut()
        self.judgeRemoveEmptyTool()
        self.judgeMoveUpAndDownTool()

    def judgeRemoveEmptyTool(self):
        if len(filenames)==0:
            self.tool_RemoveEmpty.setEnabled(False)
        else:
            self.tool_RemoveEmpty.setEnabled(True)
            
    def tableClicked(self):
        self.tool_MoveDown.setEnabled(True)
        self.tool_MoveUp.setEnabled(True)
            
    def judgeMoveUpAndDownTool(self):
        if len(filenames)==0 or self.tableWidger.currentIndex().row() == -1:
            self.tool_MoveDown.setEnabled(False)
            self.tool_MoveUp.setEnabled(False)
        else:
            self.tool_MoveDown.setEnabled(True)
            self.tool_MoveUp.setEnabled(True)
            
    def judgeRemoveBut(self):
        if len(filenames)==0:
            self.btn_removefile.setEnabled(False)
        else:
            self.btn_removefile.setEnabled(True)

    def judgeStartBut(self):
        if len(filenames)!=0 and self.text.text()!="":
            self.btn_start.setEnabled(True)
        else:
            self.btn_start.setEnabled(False)

    def removeEmpty(self):
        filenames.clear()
        filepaths.clear()
        self.changefilenameToTable()

    def movedown(self):
        row = len(filenames)
        select_row = self.tableWidger.currentIndex().row()
        # pdb.set_trace()
        if select_row < row-1:
            filenames[select_row],filenames[select_row+1]=filenames[select_row+1],filenames[select_row]
            filepaths[select_row],filepaths[select_row+1]=filepaths[select_row+1],filepaths[select_row]
            self.changefilenameToTable()
            self.tableWidger.setCurrentCell(select_row+1,0)
            
    def moveup(self):
        row = len(filenames)
        select_row = self.tableWidger.currentIndex().row()
        if select_row > 0:
            filenames[select_row],filenames[select_row-1]=filenames[select_row-1],filenames[select_row]
            filepaths[select_row],filepaths[select_row-1]=filepaths[select_row-1],filepaths[select_row]
            self.changefilenameToTable()
            self.tableWidger.setCurrentCell(select_row-1,0)

    def command_example(self):
        QMessageBox.information(self,"command example","0#3 选定第一个pdf的第四页\n0#3 选定第一个pdf的第三页。\n0#0=r90 选定第一个pdf的第一页，并把第一页顺时针旋转90度。\n0#0:10=r-90 选定第一个pdf的第一页到第十一页，并把这些页面逆时针旋转90度。\n0#0,1#1,2#2 选定第一个pdf的第一页、第二个pdf的第二页、第三个pdf的第三页，并将其组合起来。",QMessageBox.Yes)

    def addfile(self):
        files = QFileDialog.getOpenFileNames(self,'选取文件','C:/','*.pdf')[0]
        for i in range(len(files)):
            filepath = files[i]
            if filepath != "":
                filepaths.append(filepath)
                filename = os.path.basename(filepath).split('.')[0]
                filenames.append(filename)
                self.changefilenameToTable()

    def removefile(self):
        r = self.tableWidger.currentIndex().row()
        filepaths.pop(r)
        filenames.pop(r)
        self.changefilenameToTable()

    def about(self):
        QMessageBox.information(self,"about","测试版本0.5，用于pdf重组\nQQ:1072505283、1345472228",QMessageBox.Yes)
    
    def startProcess(self):
        savepath = QFileDialog.getSaveFileName(self,'文件保存','C:/','*.pdf')[0]
        os.startfile(os.path.dirname(savepath))
        command = self.text.text()
        recombine.start(command,filepaths,savepath)
        QMessageBox.information(self,"重组成功","成功！",QMessageBox.Yes)


if __name__=='__main__':
    #创建应用程序和对象
    app = QApplication(sys.argv)
    win = Pdfitwindown()
    sys.exit(app.exec_())