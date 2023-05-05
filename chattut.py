"""
Chattutクラスがappにて選択されたモデルから
回答を受取りappへ送りかえす構造
もうちょいセンスのある構造があったら即採用
"""

class Chattut:
  def record(self):
    print("voice recoding")

  def speak(self):
    print("chattut speak")

  # 回答を生成
  def create_response(self, prompt, responser):
    response = responser.create_response(prompt)
    return response

def main():
  print("設計中")

if __name__ == "__main__":
  main()
