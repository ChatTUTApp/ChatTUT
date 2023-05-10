from transformers import BertJapaneseTokenizer, AutoModelForQuestionAnswering
import torch
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile
import streamlit as st
import os

# from aws import AWS

class MyBERT:
  def __init__(self):
    # aws = AWS()
    load_dotenv("variable.env")
    haggingface_token = os.getenv("HAGGINGFACE_TOKEN")
    self.model = AutoModelForQuestionAnswering.from_pretrained("chattut/bert-model", use_auth_token=haggingface_token)
    self.tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')

  def fine_tuning(self):
    print("fine tune bert")

  # 回答を生成
  def create_response(self, prompt):
    context  = open('data/train_data_bert.txt', 'r', encoding='UTF-8') # 回答をテキストファイルから探す
    context_data = context.read()
    context_data=context_data.replace('\n','') # 改行を削除
    inputs = self.tokenizer.encode_plus(prompt, context_data, add_special_tokens=True, return_tensors="pt")
    context.close()
    input_ids = inputs["input_ids"].tolist()[0]
    output = self.model(**inputs)

    answer_start = torch.argmax(output.start_logits)
    answer_end = torch.argmax(output.end_logits) + 1
    response = self.tokenizer.convert_tokens_to_string(self.tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
    response = response.replace(' ', '')

    if response == "":
      return "う～ん、質問の仕方を変えてほしいです！"

    return response + "です!"

def main():
  chattut = MyBERT()
  prompt = "あなたの役目は何ですか？"
  answer = chattut.create_response(prompt)

  # 結果出力
  print("質問: "+prompt)
  print("応答: "+answer)

if __name__ == "__main__":
  main()
