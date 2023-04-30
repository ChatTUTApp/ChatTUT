"""
Chattutクラスがappにて選択されたモデルから
回答を受取りappへ送りかえす構造
もうちょいセンスのある構造があったら即採用
"""

class Chattut:
  def __init__(self, responser):
    self.responser = responser

  def record(self):
    print("voice recoding")

  def speak(self):
    print("chattut speak")

  # 回答を生成
  def create_response(self, prompt):
    response = self.responser.create_response(prompt)
    return response

def main():
  print("設計中")

if __name__ == "__main__":
  main()
