import argparse
import os
import torch
from dotenv import load_dotenv

class MyBERT:
  def __init__(self):
    print("bert is init")

  def fine_tuning(self, file_name):
    print("fine tune bert")

  # 回答を生成
  def create_response(self, prompt):
      self.response = prompt + "私はBERTモデルモードのChatTUTです"
      return self.response

