import openai
import argparse
import os
from dotenv import load_dotenv

class OpenAI_API:
  def __init__(self, api_key):
    self.api_key = api_key
    openai.api_key = self.api_key

  def fine_tuning(self, file_name):
    # 訓練用ファイルをアップロード
    upload_response = openai.File.create(
    file=open(file_name, "rb"),
    purpose='fine-tune'
    )
    file_id = upload_response.id

    # ファインチューニングの実行
    print(file_id)
    fine_tune_response = openai.FineTune.create(training_file=file_id, model="davinci")
    print(fine_tune_response)

  # ファインチューニングタスクの進行状況確認
  def get_fine_tune_status(self, fine_tune_id):
    fine_tune = openai.FineTune.retrieve(fine_tune_id)

    if 'status' not in fine_tune:
        print(f"Error: {fine_tune}")
        return None

    return fine_tune['status'], fine_tune.get('fine_tuned_model', None)

  # 回答を生成
  def create_response(self, prompt):
      model = os.getenv("MODEL")
      self.response = openai.Completion.create(
          model=model,
          prompt = prompt,
          temperature=0,
          max_tokens=100
      )
      self.response = self.response['choices'][0]['text']
      return self.response

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', '--prompt', type=str,
                          default="",
                          help='Talk with ChatTUT')
  parser.add_argument('-f', '--finetuning', type=bool,
                          default=False,
                          help='Execute finetuning')
  parser.add_argument('-c', '--checkstatus', type=bool,
                          default=False,
                          help='Check tuning status')
  args = parser.parse_args()

  ### 各種設定 ############################################
  load_dotenv("variable.env")  # .envファイルを読み込む
  api_key = os.getenv("OPENAI_API_KEY")
  fine_tune_id = os.getenv("FINE_TUNE_ID")
  fine_tune_file_name = "data/train_data.jsonl"
  #########################################################

  chattut = OpenAI_API(api_key)

  if args.finetuning: # ファインチューニングの開始
    chattut.fine_tuning(fine_tune_file_name)
    print("fine tuning started.")
  elif args.checkstatus: # ファインチューニングの状況確認
    status, fine_tuned_model_id = chattut.get_fine_tune_status(fine_tune_id)
    print(f"Fine-tune status: {status}") # pending→running→succeeded
    print(f"Fine-tuned model ID: {fine_tuned_model_id}")
  elif args.prompt: # 会話
    answer = chattut.create_response(args.prompt)
    print("質問：{}\n".format(args.prompt))
    print("答え：{}".format(answer['choices'][0]['text']))
  else:
    print("Please add option")

if __name__ == "__main__":
  main()
