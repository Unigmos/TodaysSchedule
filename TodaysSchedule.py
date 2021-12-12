#-------------------------------------------------------------------------------
# Name:         Today's Schedule
# Purpose:      当日の講義内容の通知
#
# Author:       Shaneron
#
# Created:     2021/12/12
# Copyright:   (c) Shaneron 2021
#-------------------------------------------------------------------------------

# メイン処理
def main():
    try:
        import time
        import sys
        # スタートアップで画面表示前に通知されてしまうためそれ対策
        time.sleep(40)

        # パス指定
        filepath = "./ScheduleData.xlsx"

        # それぞれの関数の処理実行
        schedule_data = read_schedule(filepath)
        title, schedule = make_content(schedule_data)
        notification(title, schedule)

        # 全て終われば処理終了
        sys.exit()

    except ModuleNotFoundError as No_ModuleError:
        print("ModuleNotFoundError:", No_ModuleError, "at read_schedule")

# ファイル読み込み処理
def read_schedule(readfile):
    try:
        import openpyxl
        import datetime
        import pathlib
        import sys

        path = pathlib.Path(readfile)
        weekday = datetime.date.today().weekday()

        # ファイル別に読み込み
        if path.suffix == ".xlsx":
            wb = openpyxl.load_workbook(readfile)
            sheetdata = wb.get_sheet_by_name('Sheet1')

            row_data = []
            # 曜日別に取得
            for data in list(sheetdata.columns)[weekday + 1]:
                row_data.append(data.value)

            # 見出し(曜日)の削除
            row_data.pop(0)

            return row_data

        elif path.suffix == ".csv":
            print("現在編集中")
            sys.exit()
        else:
            print("未対応ファイルです")
            sys.exit()
    except ModuleNotFoundError as No_ModuleError:
        print("ModuleNotFoundError:", No_ModuleError, "at read_schedule")
    except FileNotFoundError as NotFoundError:
        print("FileNotFoundError:", NotFoundError, "at read_schedule")

# 通知内容作成処理(titleとmessage内容作成)
def make_content(row_data):
    try:
        from datetime import datetime
        weekday = datetime.today().strftime('%a')
        title_str = "本日の予定 (" + weekday + ")"

        new_row = []
        for idx, val in enumerate(row_data):
            num_data = f"{idx + 1}限:{val}"
            new_row.append(num_data)

        #Noneの入っている要素の削除、list→str
        del_none = [s for s in new_row if 'None' not in s]
        if del_none == []:
            message = "本日の予定はありません"
        else:
            message ="\n".join(del_none)

        return title_str, message
    except ModuleNotFoundError as No_ModuleError:
        print("ModuleNotFoundError:", No_ModuleError, "at meke_content")

# 通知処理
def notification(title_word, schedule):
    try:
        from plyer import notification
        notification.notify(
        title = title_word,
        message = str(schedule),
        app_name = "Today's Schedule",
        app_icon = "./python.ico",
        timeout = 10
        )
    except ModuleNotFoundError as No_ModuleError:
        print("ModuleNotFoundError:", No_ModuleError, "at notification")

if __name__ == '__main__':
    main()
