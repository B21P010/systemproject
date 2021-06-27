import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import ctypes
import requests
import time
import threading
from ic_reader import ICReader 
from attendance_management import AttendanceManagement,AttendIdent

# ラズパイ公式7インチタッチパネル 800 x 480 60fps

# メインウィンドウ
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.widgetList = [DownloadWidget(),StartWidget(),WaitWidget()]
        self.start_widget = StartWidget()
        self.common = TestWidget()
        self.ddd = QPushButton()
        #self.ddd.setGeometry(100,100,100,100)
        self.setCentralWidget(self.start_widget)
        #self.setCentralWidget(self.common)
        #self.widgetList[1].changeWidget.connect(lambda :self.change(3))
        self.start_widget.changeWidget.connect(lambda x,y:self.change(x,y))
        #self.setCentralWidget(self.dwnwidget)
        #self.setCentralWidget(self.idmLabel)

    @Slot(str,int)
    # widgetListのnum番目に切り替え
    def change(self,kamoku,kaisu):
        try:
            self.gamelikeWidget = GamelikeWidget(kamoku,kaisu)
            self.gamelikeWidget.returnsignal.connect(self.return_toppage)
            #self.reader = ICReader(self.gamelikeWidget)
            #self.reader.start_read()
            #self.reader.start()
            self.setCentralWidget(self.gamelikeWidget)
        except:
            import traceback
            traceback.print_exc()

    @Slot()
    def return_toppage(self):
        self.gamelikeWidget = ''
        self.start_widget = StartWidget()
        self.start_widget.changeWidget.connect(lambda x,y:self.change(x,y))
        self.setCentralWidget(self.start_widget)


# 共通ウィジェット
class CommonWidget(QWidget):
    def __init__(self):
        super().__init__()
        #self.initUI()

    def initUI(self):
        # 終了ボタン
        self.exitBtn = QPushButton('x')
        self.exitBtn.setFixedSize(200,100)
        self.exitBtn.clicked.connect(self.exitWindow)

        # 共通範囲
        self.commonLayout = QVBoxLayout()

        # ヘッダ？レイアウト
        self.headerLayout = QHBoxLayout()
        self.headerLayout.setAlignment(Qt.AlignRight)
        self.headerLayout.addWidget(self.exitBtn)

        # コンテンツ部分の
        self.layout = QHBoxLayout()

        # メインコンテンツwidget
        self.content = QWidget()
        self.content.setLayout(self.layout)
        self.content.setFixedSize(500,500)

        # レイアウトに追加
        #self.commonLayout.addWidget(self.exitBtn)
        self.commonLayout.addLayout(self.headerLayout)
        self.commonLayout.addWidget(self.content)

        self.setLayout(self.commonLayout)

    @Slot()
    def exitWindow(self):
        res = QMessageBox.question(self, '終了します', '出席管理を終わりまする．')
        if res == QMessageBox.Yes:
            self.close()
            QCoreApplication.quit()


class TestWidget(CommonWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        super().initUI()
        self.btn1 = QPushButton("1")
        self.btn2 = QPushButton("2")
        self.lb = QLabel("これはテストです")
        self.lb.setFont(QFont('メイリオ',30,QFont.Bold))
        self.layout.addWidget(self.lb)
        self.layout.addWidget(self.btn1)
        self.layout.addWidget(self.btn2)

class DownloadWidget(QWidget):
    readidm:Signal = Signal(str)
    def __init__(self):
        super().__init__()
        self.dirpath = './'
        self.initUI()
        
    def initUI(self):
        self.dir = QDir()
        self.dirlist = QListWidget()
        self.dir.setPath(self.dirpath)
        #self.dir.setFilter(QDir.Dirs | QDir.NoSymLinks) # ディレクトリを表示
        self.dir.setFilter(QDir.Files) # ファイルを表示
        self.dir.setSorting(QDir.Name) # 名前ソート
        self.list = self.dir.entryInfoList() # 
        self.layout = QHBoxLayout()

        self.idmLabel = QLabel()
        self.idmLabel.setText("test")
        self.readidm.connect(lambda x: self.update_label(x))
        

        # QListWidgetの中身を作成
        for i in range(len(self.list)):
            fileinfo = self.list[i]
            dir_item = QListWidgetItem(fileinfo.fileName(),self.dirlist)
            #dir_item.setFlags(self.dirlist.flags())
            #dir_item.setCheckState(Qt.Unchecked)
        self.dirlist.itemClicked.connect(self.itemClicked) # シグナルスロット結びつけ

        self.kamokucombo = QComboBox()
        self.kamokucombo.setFixedSize(200,200)
        self.kamokucombo.addItem('1')
        self.kamokucombo.addItem('2')
        self.kamokucombo.addItem('3')
        self.kamokucombo.addItem('4')
        self.kamokucombo.addItem('5')
        self.kamokucombo.addItem('6')
        self.kamokucombo.addItem('7')
        self.kamokucombo.addItem('8')
        self.kamokucombo.addItem('9')
        self.kamokucombo.addItem('10')
        self.kamokucombo.addItem('11')
        self.kamokucombo.addItem('12')
        self.kamokucombo.addItem('13')
        self.kamokucombo.addItem('14')
        self.kamokucombo.addItem('15')

        self.dwnbtn = QPushButton('ダウンロード')
        self.dwnbtn.setFixedSize(300,300)

        self.layout.addWidget(self.kamokucombo)
        self.layout.addWidget(self.dwnbtn)
        self.layout.addWidget(self.idmLabel)
        self.setLayout(self.layout)

    # アイテムをクリックしたときの処理
    @Slot()
    def itemClicked(self):
        print(self.dirlist.currentItem().text(),'の中身を表示')
        with open(self.dirpath+self.dirlist.currentItem().text()) as f:
            text = f.read()
            print(text)

    @Slot()
    def download(self):
        tmp = DownloadRisyu(self.kamokucombo.currentText())

    # ラベルをidmでアップデート
    @Slot(str)
    def update_label(self,idm):
        self.idmLabel.setText(str(idm))
        self.update()
        

# 起動時の画面
class StartWidget(QWidget):
    changeWidget = Signal(str,int)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 
        self.label = QLabel("出席管理システム")
        self.label.setFont(QFont('メイリオ',40))
        self.label.setAlignment(Qt.AlignCenter)
        # スタートボタン
        self.btn = QPushButton("授業開始")
        self.btn.clicked.connect(self.emit_clicked)
        self.btn.setFixedSize(200,200)
        # 科目コンボボックス
        self.kamoku = ['F1','F2','F3','F4','F5','M1','M2','M3','M4','M5']
        self.kamoku_combo = QComboBox()
        self.kamoku_combo.setFixedSize(200,200)
        for s in self.kamoku:
            self.kamoku_combo.addItem(s)
        # 回数コンボボックス
        self.kaisu = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        self.kaisu_combo = QComboBox()
        self.kaisu_combo.setFixedSize(200,200)
        for s in self.kaisu:
            self.kaisu_combo.addItem(str(s))

        # layout
        self.main_layout = QVBoxLayout()
        self.combo_layout = QHBoxLayout()
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(self.combo_layout)
        self.btn_layout = QHBoxLayout()
        self.btn_layout.addStretch()
        self.btn_layout.addWidget(self.btn)
        self.btn_layout.addStretch()
        self.main_layout.addLayout(self.btn_layout)
        self.combo_layout.addWidget(self.kamoku_combo)
        self.combo_layout.addWidget(self.kaisu_combo)
        self.setLayout(self.main_layout)

    @Slot()
    def emit_clicked(self):
        print(self.kaisu_combo.currentText())
        self.changeWidget.emit(str(self.kamoku_combo.currentText()),int(self.kaisu_combo.currentText()))


# カード読み取り待機画面
class WaitWidget(QWidget):
    changeWidget = Signal()
    def __init__(self):
        super().__init__()
        self.titleLabel = QLabel("見出し用")
        self.descLabel = QLabel("説明用")
        self.exitbtn = QPushButton("x")
        self.exitbtn.clicked.connect(self.emit_clicked)

    def emit_clicked(self):
        self.changeWidget.emit()


class DownloadRisyu:
    def __init__(self,kamoku):
        self.url = 'http://localhost/csv'
        self.param = {'kamoku':kamoku}
        self.recieved_json = requests.get(self.url,self.param).json()
        print(self.recieved_json)
        self.risyusya_csv = self.recieved_json['csv']
        self.kamoku = self.recieved_json['kamoku']
        self.start_syusseki = self.recieved_json['start_syusseki']
        self.start_tikoku = self.recieved_json['start_tikoku']
        self.end_uketuke = self.recieved_json['end_uketuke']
        print(kamoku,self.start_syusseki,self.start_tikoku,self.end_uketuke)


class GamelikeWidget(QWidget):
    readidm:Signal = Signal(str)
    returnsignal:Signal = Signal()
    def __init__(self,kamoku,kaisu,parent=None):
        super(GamelikeWidget,self).__init__(parent)
        self._height = 600
        self._width = 1000
        self.reader = ICReader(self)
        self.reader.on_connect(self.readidm.emit)
        self.reader.start()
        self.attendance_management = AttendanceManagement(kamoku,kaisu)
        self.attendance_management.get_risyu_list('test.csv')
        self.risyusya_number = self.attendance_management.risyu_number
        self.enemyHP = self.attendance_management.risyu_number
        self.myHP = self.attendance_management.risyu_number
        self.initUI()

    def initUI(self):
        self.setFixedSize(self._width,self._height)
        # バックグラウンド(ポケモン風画像)
        self.background = QLabel(self)
        self.background.setFixedSize(self._width,self._height)
        self.background.setPixmap(QPixmap('./UI.png'))
        # 敵HP
        self.enemyHPbar = QProgressBar(self)
        self.enemyHPbar.setFixedSize(240,20)
        self.enemyHPbar.setMaximum(self.risyusya_number)
        self.enemyHPbar.setValue(self.enemyHP)
        self.enemyHPbar.setFormat('%v/'+str(self.risyusya_number))
        self.enemyHPinfo = QLabel(self)
        self.enemyHPinfo.setText(str(self.enemyHP)+'  /  '+str(self.risyusya_number))
        self.enemyHPinfo.setFont(QFont("メイリオ",25))
        self.enemyHPinfo.setFixedSize(140,30)
        # 自分HP
        self.myHPbar = QProgressBar(self)
        self.myHPbar.setFixedSize(240,20)
        self.myHPbar.setMaximum(self.risyusya_number)
        self.myHPbar.setValue(self.myHP)
        self.myHPbar.setFormat('%v/'+str(self.risyusya_number))
        self.myHPinfo = QLabel(self)
        self.myHPinfo.setFont(QFont("メイリオ",25))
        self.myHPinfo.setText(str(self.myHP)+'  /  '+str(self.risyusya_number))
        # テキスト欄
        self.text = QLabel(self)
        self.text.setFixedSize(900,200)
        self.text.setStyleSheet('background-color: red;')
        self.text.setFont(QFont("メイリオ",40))
        self.init_text()

        #終了，戻るボタン
        self.exitBtn = QPushButton(self)
        self.exitBtn.setText("終了")
        self.exitBtn.setFixedSize(100,50)
        self.exitBtn.clicked.connect(self.exitWindow)
        self.exitBtn.setShortcut('q')
        self.returnBtn = QPushButton(self)
        self.returnBtn.setText("戻る")
        self.returnBtn.setFixedSize(100,50)
        self.returnBtn.clicked.connect(self.returnWindow)
        self.returnBtn.setShortcut('r')

        # 配置
        self.background.move(0,0)
        self.enemyHPbar.move(150,110)
        self.enemyHPinfo.move(180,130)
        self.myHPbar.move(620,330)
        self.myHPinfo.move(640,340)
        self.text.move(50,450)
        self.exitBtn.move(800,450)
        self.returnBtn.move(800,500)
        self.readidm.connect(lambda idm: self.update_text(idm))

    # 待機画面のラベルに遷移
    def init_text(self):
        self.text.setText("ICカードをかざすがよい")
        self.update()
        QCoreApplication.processEvents()

    # テキストの内容を割り当てる
    def assign_text(self,syukketu,idm):
        # 出席時には敵のHPが減る
        if syukketu == AttendIdent.Attendance:
            self.enemyHP = self.enemyHP-1
            if self.enemyHP < 0:
                self.enemyHP = 0
            self.enemyHPbar.setValue(self.enemyHP)
            self.enemyHPinfo.setText(str(self.enemyHP)+'  /  '+str(self.risyusya_number))
            #syukketu_table = ['出席','遅刻','欠席']
            self.text.setText(idm+'は出席することができました')
        # 欠席，遅刻時には自分のHPが減る
        elif syukketu == AttendIdent.Late or syukketu == AttendIdent.Absence:
            self.myHP = self.myHP-1
            if self.myHP < 0:
                self.myHP = 0
            self.myHPbar.setValue(self.myHP)
            self.myHPinfo.setText(str(self.myHP)+'  /  '+str(self.risyusya_number))
            #syukketu_table = ['出席','遅刻','欠席']
            if syukketu == AttendIdent.Late:
                self.text.setText(idm+'は遅刻することができました')
            else:
                self.text.setText(idm+'は欠席することができました')
        elif syukketu == AttendIdent.Already:
            self.text.setText(idm+'はすでにかざしてらっしゃる')
        else:
            self.text.setText(idm+'は履修者ではありません')
        self.update()
        QCoreApplication.processEvents()

    # ラベルとかその他とかをアップデート
    @Slot(str)
    def update_text(self,idm):
        syukketu = self.attendance_management.check_attendance(idm)
        self.assign_text(syukketu,idm)
        # 2秒間だけ表示して元のテキストに戻す
        time.sleep(2)
        self.init_text()
        print("setしました")
        self.reader.event.set()

    @Slot()
    def exitWindow(self):
        res = QMessageBox.question(self, '終了します', '出席管理を終わりまする．')
        if res == QMessageBox.Yes:
            self.close()
            QCoreApplication.quit()

    @Slot()
    def returnWindow(self):
        res = QMessageBox.question(self, '終了します', '出席管理を終わりまする．')
        if res == QMessageBox.Yes:
            self.returnsignal.emit()
        self.reader.raise_exception()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #ex = DownloadWidget()
    ex = MainWindow()
    #ex = GamelikeWidget()
    ex.show()
    #reader = ICReader(ex)
    #reader.start_read()
    sys.exit(app.exec_())

