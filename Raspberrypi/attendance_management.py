import csv
import time_compare
from enum import Enum,auto
class AttendIdent(Enum):
    Already = auto()
    Attendance = auto()
    Late = auto()
    Absence = auto()
    NotARisyusya = auto()


class AttendanceManagement():
    def __init__(self,kamoku,kaisu):
        self.kamoku = kamoku
        self.kaisu = kaisu
        self.risyu_number = 0 # 履修者数
        self.last_idm = 0 # 最後に入力されたIDm
        self.idm_list = [] # 入力されたIDmのリスト
        self.reader = 0 # IDmリーダー
        self.timeconmare = time_compare.TimeCompare('9:00',20,100,900) # 時間比較
        self.risyu_list = dict() # 履修者リスト idmをkeyに下辞書型

    # 出席チェック
    def check_attendance(self,idm:str) -> (bool,str):
        syukketu = ''
        if self.is_effective_idm(idm):
            if not self.is_duplication(idm):
                self.idm_list.append(idm)
                if self.timeconmare.is_syusseki():
                    self.write_syusseki(idm,'出席')
                    syukketu = AttendIdent.Attendance
                elif self.timeconmare.is_tikoku():
                    self.write_syusseki(idm,'遅刻')
                    syukketu = AttendIdent.Late
                else:
                    self.write_syusseki(idm,'欠席')
                    syukketu = AttendIdent.Absence
                print(self.idm_list)
            else:syukketu = AttendIdent.Already
        else:syukketu = AttendIdent.NotARisyusya
        return syukketu

    # 重複チェック
    def is_duplication(self,idm:str) -> bool:
        for s in self.idm_list:
            if s == idm:
                return True
        return False

    # 履修者リストの中に存在するidmかチェック
    def is_effective_idm(self,idm:str) -> bool:
        if idm in self.risyu_list:
            return True
        return False

    # 履修者リスト取得
    def get_risyu_list(self,filename):
        self.risyu_list = dict()
        header = ['number','name','kana','seibetu','idm'] # 履修者リストcsvのヘッダ(適宜書き換えて)
        self.risyu_number = 0
        try:
            with open(filename,'r',encoding='utf-8') as f:
                reader = csv.DictReader(f,header)
                next(reader)
                for csvdata in reader:
                    self.risyu_number = self.risyu_number + 1
                    self.risyu_list[csvdata['idm']] = dict()
                    for s in header:
                        self.risyu_list[csvdata['idm']][s] = csvdata[s]
        except:
            import traceback
            traceback.print_exc()
        #print(self.risyu_list)

    # 書き出し
    def write_syusseki(self,idm,syukketu):
        filename = str(self.kamoku)+'_'+str(self.kaisu)+'.csv'
        print(filename)
        print(idm,syukketu)
        pass

