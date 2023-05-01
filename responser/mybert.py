from transformers import BertJapaneseTokenizer, AutoModelForQuestionAnswering
import torch
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile 
import streamlit as st

from aws import AWS

class MyBERT:
  def __init__(self):
    # aws = AWS()
    self.model = AutoModelForQuestionAnswering.from_pretrained("chattut/bert-model", use_auth_token=True)
    self.tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking') 

  def fine_tuning(self):
    print("fine tune bert")

  # 回答を生成
  def create_response(self, prompt):
    context  = '私の名前は、Chat TUTです。私は技科生のためのアシスタントとして生まれました。'\
    '技科大の特徴は女子が少ないことです。'\

    inputs = self.tokenizer.encode_plus(prompt, context, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]
    output = self.model(**inputs)

    answer_start = torch.argmax(output.start_logits)  
    answer_end = torch.argmax(output.end_logits) + 1 
    response = self.tokenizer.convert_tokens_to_string(self.tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
    response = response.replace(' ', '')

    return response + "です!"

def main():
  chattut = MyBERT()
  prompt = "あなたの名前は何ですか？"
  answer = chattut.create_response(prompt)

  # 結果出力
  print("質問: "+prompt)
  print("応答: "+answer)

if __name__ == "__main__":
  main()
