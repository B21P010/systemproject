from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

# 集計結果表示用ウィジェット
class TotalizationWidget(QLabel):
    def __init__(self):
        super(TotalizationWidget, self).__init__()
        self.font = QFont("メイリオ",15)
        self.attend = 99 # 出席者数
        self.late = 20 # 遅刻者数
        self.absence = 10 # 欠席者数
        self.initUI()

    def test(self,attend):
        self.attend = attend

    def initUI(self):
        self.setText('出席者数:{:4}\n遅刻者数:{:4}\n欠席者数:{:4}'.format(self.attend,self.late,self.absence))
        self.setFont(self.font)
        # self.setMargin(10)
        self.setStyleSheet("border-radius:40%;color:black;background-color: white;padding:10%")
        self.setAlignment(Qt.AlignCenter)

    def update_text(self):
        self.setText('出席者数:{:4}\n遅刻者数:{:4}\n欠席者数:{:4}'.format(self.attend,self.late,self.absence))
