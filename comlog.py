import csv
import json
import datetime


class ConsoleLogger:
    def __init__(self):
        print("----------------------------------------------------------------")
        self.console_log("INFO", "BEGIN", "ChatTUT")
        print("----------------------------------------------------------------")

    def console_log(self, log_level, event_detail, processing_contents):
        dt_now = self._time()
        print(f'[{log_level:<5}] {dt_now} {event_detail} - {processing_contents}')

    def _time(self):
        # 現在時刻を取得(マイクロ秒は切り捨て)
        return datetime.datetime.now().replace(microsecond=0)


class CommunicateLogger(ConsoleLogger):
    def __init__(self, csv, json):
        super().__init__()
        self.filename_csv = csv
        self.filename_json = json

    def logger_csv(self, prompt, answer):
        answer = answer.replace("\n", "")   # 改行を削除
        answer = answer.replace(" ", "")    # 空白を削除
        data = [[prompt, answer]]           # csv形式のデータ

        with open(self.filename_csv, "a", encoding="utf_8", newline="") as f:
            try:
                self.console_log("INFO", "START", self.filename_csv)
                csv.writer(f).writerows(data)
            except Exception as e:
                self.console_log("ERROR", "Write", e)
            else:
                self.console_log("INFO", "Write", data)
            finally:
                self.console_log("INFO", "END", self.filename_csv)

    def logger_json(self, prompt, answer):
        answer = answer.replace("\n", "")           # 改行を削除
        answer = answer.replace(" ", "")            # 空白を削除
        data = {"prompt": prompt, "answer": answer} # jsonlines形式のデータ

        with open(self.filename_json, "a", encoding="utf_8") as f:
            try:
                self.console_log("INFO", "START", self.filename_json)
                f.writelines([json.dumps(data, ensure_ascii=False)])
                f.write("\n")
            except Exception as e:
                self.console_log("ERROR", "Write", e)
            else:
                self.console_log("INFO", "Write", data)
            finally:
                self.console_log("INFO", "END", self.filename_json)