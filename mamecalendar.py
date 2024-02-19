#--------------------------------------------------------------------------------------------------
# タイトル：カレンダー
# 内容：
#    カレンダーを表示する
#    暦や祝日の機能はまだない
# 作成者：だいちゃまめ
#--------------------------------------------------------------------------------------------------
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.clock import Clock
import sys
import datetime
import calendar

# ウィンドウサイズの指定
Window.size=(480,320)

#--------------------------------------------------------------------------------------------------
# プログラム終了コマンド
#--------------------------------------------------------------------------------------------------
class PopupExitDialog(Popup):
    pass
    # プログラム終了
    def exec_exit(self):
       sys.exit()
#--------------------------------------------------------------------------------------------------
# メインウィジット
#--------------------------------------------------------------------------------------------------
class MameWidget(Widget):
    # 初期処理
    def __init__(self, **kwargs):
        super(MameWidget, self).__init__(**kwargs)
        Clock.schedule_once(self.init_calendar)
    # カレンダー初期化
    def init_calendar(self,dt):
        now_date = datetime.datetime.now()      # 現在の日付取得
        self.year = now_date.year               # 表示用の年に初期値設定
        self.month = now_date.month             # 表示用の月に初期値設定
        self.set_calendar()                     # カレンダー表示
    # カレンダー描画
    def set_calendar(self):
        month_calendar = calendar.monthcalendar(self.year,self.month)            # カレンダー取得
        self.ids.lbl_date.text = str(self.year) + "年" + str(self.month) + "月"   # 日付表示
        self.clear_calendar()   # 表示されているカレンダーをクリア
        for i in range(0,len(month_calendar)):
            self.set_week(i,month_calendar[i]) #　週ごとに表示
    # カレンダー画面の値を消去
    def clear_calendar(self):
        buf=(0,0,0,0,0,0,0)
        for i in range(0,6):
            self.set_week(i,buf)
    # 一週間の表示
    def set_week(self,what_week,days):
        today = datetime.datetime.now()     # 今日の日付取得
        id_week="w" + str(what_week)        # 週のIDを設定
        for i in range(7):
            id_weekday="lbl_weekday" + str(i)   # 曜日のIDを設定
            if(days[i] == 0):       # 0の場合、空で表示
                buf=""
            else:
                buf=str(days[i])    # 数字を文字列に変換
            # 今日の日付の背景を設定
            if((today.year == self.year)*(today.month == self.month)*(today.day == days[i])):
                self.ids[id_week].ids[id_weekday].ids.lbl_day.background_color=(.8,.8,0,1)
            else:
                self.ids[id_week].ids[id_weekday].ids.lbl_day.background_color=(.5,.5,.4,1)
            # 文字色の設定
            if(i==5):   # 土曜日
                self.ids[id_week].ids[id_weekday].ids.lbl_day.color=(0,0,1,1)
            elif(i==6): # 日曜日
                self.ids[id_week].ids[id_weekday].ids.lbl_day.color=(1,0,0,1)
            else:
                self.ids[id_week].ids[id_weekday].ids.lbl_day.color=(1,1,1,1)
            self.ids[id_week].ids[id_weekday].ids.lbl_day.text = buf             

    # 下部メニューボタン押下時の処理
    def menu_sw(self,cmd):
        if cmd == 'prev':               # < ボタン 1月前
            self.month = (self.month > 1)*(self.month - 1) + (self.month == 1)*12
            self.year = (self.month < 12)*self.year + (self.month == 12)*(self.year - 1)
        elif cmd == 'next':             # > ボタン 1月後
            self.month = (self.month < 12)*(self.month + 1) + (self.month == 12)
            self.year = (self.month > 1)*self.year + (self.month == 1)*(self.year + 1)
        elif cmd == 'down':             # - ボタン 1年前
            self.year = self.year - 1
        elif cmd == 'up':               # + ボタン 1年後
            self.year = self.year + 1
        else:
            print("nothing")
        self.set_calendar() # カレンダーを表示

    # 終了ダイアログ
    def exit_dialog(self):
        popup = PopupExitDialog()
        popup.open()

# アプリの定義
class MameCalendarApp(App):  
    def __init__(self, **kwargs):
        super(MameCalendarApp,self).__init__(**kwargs)
        self.title="Mame App"                          # ウィンドウタイトル名

# メインの定義
if __name__ == '__main__':
    MameCalendarApp().run()                                            # クラスを指定

Builder.load_file('mamecalendar.kv')                                   # kvファイル名

