import streamlit as st
import streamlit.components.v1 as stc
import streamlit_option_menu
import time
import os
import ast
import torch
import openai
import base64
from dotenv import load_dotenv
from PIL import Image

from chattut import Chattut
from comlog import CommunicateLogger
from comlog import ConsoleLogger
from responser.openai_api import OpenAI_API
from responser.mybert import MyBERT
##

def main():
    pageconfig()    # ページ設定
    load_dotenv("variable.env") # 変数読み込み
    # color:背景色, on_color:文字色     color(key)の上にon_color(key)で対応
    color = ast.literal_eval(os.environ["COLOR_DICT"])  # color: list(key: 色の名前, value: カラーコード)
    on_color = ast.literal_eval(os.environ["ON_COLOR_DICT"])  # on_color: list(key: 色の名前, value: カラーコード)
    # answer = machine_learning()
    begin()
    page = sidebar()
    if page == "ホーム":
        application(color, on_color)
    elif page == "設定":
        app_settings(color, on_color)
    elif page == "Q&A（よくあるご質問）": # TODO:以下関数化
        st.title("Q&A（よくあるご質問）")
    elif page == "お問い合わせ":
        st.title("お問い合わせ")
    elif page == "ご意見":
        st.title("ご意見")
    elif page == "バージョン":
        st.title("バージョン")
    elif page == "プライバシーポリシー":
        st.title("プライバシーポリシー")
    elif page == "利用規約":
        st.title("利用規約")
        st.write("悪質に運営の課金額を増やすような操作(プログラムによる繰り返し処理等)の規制")
        st.write("個人を誹謗中傷するような内容の規制")
        st.write("ログイン時の個人情報は外部に漏らさず(あくまでユーザー数の把握と技科大生のみが使用できるようにするための機能である)、誰がどの質問をしたのかは運営も分からないこととする")
    elif page == "ヘルプ":
        st.title("ヘルプ")
    elif page == "Chat TUTについて":
        st.title("Chat TUTについて")
        st.header("コンセプト説明")
        st.write("みんなで育てるをテーマにしていること")
        st.write("定期的に情報を運営がクリーニングし学習を行っていることの説明")
        st.write("たくさん覚えるためにたくさん話しかけてほしいこと")

# ページ更新時に読み込まない
@st.cache_data
def begin():
    ConsoleLogger()

# ページ設定
def pageconfig():
    icon = Image.open('image/icon.png')
    st.set_page_config(
        page_title="Chat TUT",
        page_icon=icon,
        layout="centered",
        initial_sidebar_state="auto",
        menu_items={
            'Get Help': 'https://www.google.com',
            'Report a bug': "https://www.google.com",
            'About': """
            # Chat TUT
            アプリの説明
            """
        })

# サイドバー
def sidebar():
    with st.sidebar:
        selected_options = streamlit_option_menu.option_menu(menu_title=None,
            options=["ホーム", "---", "設定", "---", "Q&A（よくあるご質問）", "お問い合わせ", "ご意見", "---", "バージョン", "プライバシーポリシー", "利用規約", "ヘルプ", "Chat TUTについて"],
            icons=["house", "", "gear", "", "question-lg", "envelope", "chat-left", "", "ticket", "person", "shield-exclamation", "question-circle", "info-circle"],
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#f0f5f9"},
                "icon": {"color": "#2589d0", "font-size": "20px"},
                "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#2589d0"},
                "nav-link-selected": {"background-color": "#2589d0"},
            }
        )
        return selected_options

# メインアプリ画面
def application(color:list, on_color:list, answer:str=""):
    communicate_logger = CommunicateLogger("data/prompt_log.csv", "data/prompt_log.jsonl")

    st.title("Chat TUT")

    menu_location = st.empty()

    with st.form("main_form", clear_on_submit=False):
        file_ = open("image/img.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="cat gif" width="100%" height="100%">',
                    unsafe_allow_html=True
                    )

        answer_location = st.empty()

        col1, col2 = st.columns((3, 1))
        with col1:
            prompt = st.text_input("質問を入力してください")
        with col2:
            st.write("")
            st.write("")
            submitted = st.form_submit_button("質問する")

        if submitted:
            answer = machine_learning(prompt)
            with answer_location:
                with st.spinner("回答を考え中..."):
                    time.sleep(3)
                answer_location.text(answer)
                # communicate_logger.logger_csv(prompt, answer)
                # communicate_logger.logger_json(prompt, answer)
                communicate_logger.logging2gspread(prompt, answer)

def app_settings(color:list, on_color:list):
    st.title("設定")

    # UIカラーパレットテスト
    st.header('UIカラーパレットテスト')

    html = Create_html("./templates/html/test.html", "./static/css/test.css", color, on_color)
    html.create_html(mode="p", text="neutrals900", color="neutrals900", font_size=20,
                    width=150, height=50)
    html.create_html(mode="p", text="neutrals700", color="neutrals700", font_size=20,
                    width=150, height=50)
    html.create_html(mode="p", text="neutrals500", color="neutrals500", font_size=20,
                    width=150, height=50)
    html.create_html(mode="p", text="neutrals300", color="neutrals300", font_size=20,
                    width=150, height=50)
    html.create_html(mode="p", text="primary700", color="primary700", font_size=20,
                    width=150, height=50)
    html.create_html(mode="p", text="primary400", color="primary400", font_size=20,
                    width=150, height=50)
    html.create_html(mode="p", text="primary200", color="primary200", font_size=20,
                    width=150, height=50)
    html.create_html(mode="p", text="primary100", color="primary100", font_size=20,
                    width=150, height=50)
    html.create_html(mode="p", text="secondary700", color="secondary700", font_size=20,
                    width=150, height=50)
    html.create_html(mode="p", text="secondary400", color="secondary400", font_size=20,
                    width=150, height=50)
    html.create_html(mode="p", text="secondary200", color="secondary200", font_size=20,
                    width=150, height=50)
    html.create_html(mode="p", text="secondary100", color="secondary100", font_size=20,
                    width=150, height=50)
    html.create_html(mode="p", text="error", color="error", font_size=20,
                    width=150, height=50)
    html.create_html(mode="p", text="success", color="success", font_size=20,
                    width=150, height=50)

def machine_learning(prompt):
    ################
    ### 機械学習 ###
    ################
    api_key = os.getenv("OPENAI_API_KEY")
    responser = select_responser(api_key)
    chattut = Chattut(responser) # TODO アプリ画面上でモードを切り替えられるようになったらいいなぁ
    answer = chattut.create_response(prompt)
    # answer = "answer"
    return answer

# 自然言語モデルの選択
@st.cache_resource
def select_responser(api_key):
    model_type = {"is_bert":MyBERT(), "is_openai_api": OpenAI_API(api_key)}
    return model_type["is_bert"]

class Create_html:
    def __init__(self, html:str, css:str, color:list, on_color:list):
        self.html = html
        self.css = css
        self.color = color
        self.on_color = on_color

    def create_html(self, mode:str, text:str, color:str, font_size:int=10, font_weight:int=None,
                    width:int=None, height:int=None, margin:int=0, padding:int=0):
        with open(self.html, "r") as h:
            with open(self.css, "r") as c:
                stc.html(
                    h.read().format(
                        mode=mode,
                        text=text,
                        style=c.read().format(
                            mode=mode,
                            color=self.on_color[color],
                            background_color=self.color[color],
                            font_size=str(font_size)+"px" if font_size!=None else font_size,
                            font_weight=str(font_weight)+"px" if font_weight!=None else font_weight,
                            width=str(width)+"px" if width!=None else width,
                            height=str(height)+"px" if height!=None else height,
                            margin=str(margin)+"px" if margin!=None else margin,
                            padding=str(padding)+"px" if padding!=None else padding,
                        )
                    ),
                    width=width+15,
                    height=height
                )

if __name__ == "__main__":
    main()
