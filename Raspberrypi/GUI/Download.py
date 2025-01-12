# PySide2のモジュールを読み込む
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# from tusin import post
from shadow_effect import ShadowEffect



class uploadWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__()

        #ウィンドウ
        self.setObjectName('uploadWindow')
        self.setFixedSize(800,480)

        #タイトル
        self.label = QLabel(self) 
        self.label.setText("ダウンロード")  
        #タイトルの装飾
        self.label.setFont(QFont('メイリオ',25))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName('title')
        self.label.setGraphicsEffect(ShadowEffect(self))

        # コンボボックスの生成+装飾
        self.kougi_combobox = QComboBox(self)
        self.kougi_combobox.setFont(QFont('メイリオ',20))
        self.kougi_combobox.setFixedSize(200,130)
        self.kougi_combobox.setObjectName('kougi_combobox')
        self.kougi_combobox.setGraphicsEffect(ShadowEffect(self))
        self.kougi_combobox.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)

        
        # 講義のコンボボックスの選択肢を追加
        self.kougi_combobox.addItems(['F1','F2','F3','F4','F5','M1','M2','M3','M4','M5'])
        
        #ダウンロードボタンを追加
        self.btn = QPushButton("ダウンロード")
        #ファイル選択のダイアログが表示される
        #self.btn.clicked.connect(self.getfile)

        #コンボボックスから参照してファイルをダウンロードする
        self.btn.clicked.connect(lambda: self.download_risyusya_list(self.kougi_combobox.currentText()))

        #アップロードボタンの装飾
        self.btn.setFixedSize(230,80)
        self.btn.setFont(QFont("メイリオ",20))
        self.btn.setObjectName('btn')
        self.btn.setGraphicsEffect(ShadowEffect(self))
        self.btn.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)

        #self.le = QLabel("Hello")

        #レイアウト
        self.main_layout = QVBoxLayout()
        self.main_layout = QGridLayout()
        self.top_layout = QGridLayout()
        self.middle_layout = QGridLayout()
        self.bottom_layout = QGridLayout()
        # self.main_layout.setMargin(50)
        self.main_layout.setSpacing(50)
        self.top_layout.addWidget(QWidget(),0,0)
        self.top_layout.addWidget(self.label,0,1,1,3)
        self.top_layout.addWidget(QWidget(),0,4)
        self.middle_layout.addWidget(self.kougi_combobox,0,0,1,1)
        
        self.bottom_layout.addWidget(QWidget(),0,0)
        self.bottom_layout.addWidget(self.btn,0,1,1,2)
        self.bottom_layout.addWidget(QWidget(),0,3)
        self.main_layout.addLayout(self.top_layout,0,0)
        self.main_layout.addLayout(self.middle_layout,1,0,2,1)
        self.main_layout.addLayout(self.bottom_layout,3,0)
        self.setLayout(self.main_layout)
        self.setWindowTitle("出席管理＿ダウンロード")



    """#ファイル選択ダイアログを表示
    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"CSV files (*.csv)")
        self.le.setPixmap(QPixmap(fname))
    """

    #コンボボックスから参照してファイルをダウンロードする
    def download_risyusya_list(self, kamoku):
        flag = True
        # flag = get_risyudata(kamoku)
        print(kamoku)
        
        # ダウンロード成功時の処理
        if flag:
            res = QMessageBox.information(self, 'ダウンロード完了', '履修者データのダウンロードが成功しました',QMessageBox.Ok)

        # ダウンロード失敗時の処理
        elif not flag:
            res = QMessageBox.information(self, 'ダウンロード失敗', '履修者データのダウンロードができませんでした',QMessageBox.Ok)

# アプリの実行と終了
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = uploadWindow()
    
    #cssの読み込み
    with open('download.css','r') as f:
        css = f.read()
        app.setStyleSheet(css)

    ex.show()
    sys.exit(app.exec_())