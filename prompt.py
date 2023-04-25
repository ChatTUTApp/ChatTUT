import csv
import json
import datetime

class PromptLogger:
    def __init__(self, csv, json):
        self.filename_csv = csv
        self.filename_json = json

    def logger_csv(self, prompt, answer):
        self.consele_log("INFO", "START", "self.filename_csv")
        answer = answer.replace("\n", "")   # 改行を削除
        answer = answer.replace(" ", "")    # 空白を削除
        data = [[prompt, answer]]
        with open(self.filename_csv, "a", encoding="utf_8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)
            self.consele_log("INFO", "Write", target_data=data)
        self.consele_log("INFO", "END", target_file=self.filename_csv)

    def logger_json(self, prompt, answer):
        self.consele_log("INFO", "START", target_file=self.filename_json)
        answer = answer.replace("\n", "")   # 改行を削除
        answer = answer.replace(" ", "")    # 空白を削除
        data = {"prompt": prompt, "answer": answer}
        with open(self.filename_json, "a", encoding="utf_8") as f:
            f.writelines([json.dumps(data, ensure_ascii=False)])
            f.write("\n")
            self.consele_log("INFO", "Write", target_data=data)
        self.consele_log("INFO", "END", target_file=self.filename_json)

    def time(self):
        self.dt_now = datetime.datetime.now()

    def consele_log(self, log_level, event_detail, target_file=None, target_data=None):
        self.time()
        if(event_detail == "START" or event_detail == "END"):
            print(log_level, self.dt_now, event_detail, "-", target_file)
        if(event_detail == "Write"):
            print(log_level, self.dt_now, event_detail, target_data)