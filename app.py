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
from responser.openai_api import OpenAI_API
from responser.mybert import MyBERT

def main():
    app = APP()
    app.pageconfig()    # ページ設定
    load_dotenv("variable.env") # 変数読み込み
    # color:背景色, on_color:文字色     color(key)の上にon_color(key)で対応
    color = ast.literal_eval(os.environ["COLOR_DICT"])  # color: list(key: 色の名前, value: カラーコード)
    on_color = ast.literal_eval(os.environ["ON_COLOR_DICT"])  # on_color: list(key: 色の名前, value: カラーコード)
    # answer = machine_learning()
    page = app.sidebar(color, on_color)
    if page == "ホーム":
        app.application(color, on_color)
    elif page == "バージョン":
        app.app_varsion(color, on_color)


class APP:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_type = {"is_bert": MyBERT(), "is_openai_api": OpenAI_API(self.api_key)}
        self.responser = self.model_type["is_bert"]
        self.chattut = Chattut()

    # ページ設定
    def pageconfig(self):
        icon = Image.open('image/icon.png')
        st.set_page_config(
            page_title="Chat TUT",
            page_icon=icon
        )

    # サイドバー
    def sidebar(self, color:list, on_color:list):
        with st.sidebar:
            selected_options = streamlit_option_menu.option_menu(menu_title=None,
                options=["ホーム", "お問い合わせ", "バージョン", "利用規約", "Chat TUTについて"],
                icons=["house", "envelope", "ticket", "shield-exclamation", "info-circle"],
                default_index=0,
                styles={
                    "container": {"background-color": f"{color['secondary100']}"},
                    "icon": {"color": f"{color['secondary500']}", "font-size": "20px"},
                    "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": f"{color['secondary300']}"},
                    "nav-link-selected": {"background-color": f"{color['secondary300']}"},
                }
            )
            return selected_options

    # メインアプリ画面
    def application(self, color:list, on_color:list, answer:str=""):
        communicate_logger = CommunicateLogger("data/prompt_log.csv", "data/prompt_log.jsonl")

        title_col1, title_col2 = st.columns(2)
        with title_col1:
            st.title("Chat TUT")
        with title_col2:
            st.write("")
            st.write("")
            st.write("")
            st.write("version 1.0.0")

        model_option = st.selectbox(
        'モデルを選択してください',
        ('BERT', 'GPT-3.5'))
        if model_option == "BERT":
            self.select_responser("BERT")
        elif model_option == "GPT-3.5":
            self.select_responser("GPT-3.5")

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
                answer = self.machine_learning(prompt)
                with answer_location:
                    with st.spinner("回答を考え中..."):
                        time.sleep(3)
                    answer_location.text(answer)
                    # communicate_logger.logger_csv(prompt, answer)
                    # communicate_logger.logger_json(prompt, answer)
                    communicate_logger.logging2gspread(prompt, answer)

    def app_varsion(self, color:list, on_color:list):
        st.title("設定")

        # UIカラーパレットテスト
        st.header('UIカラーパレットテスト')

        with open("./templates/html/color_pallet.html") as html:
            with open("./static/css/color_pallet.css") as css:
                stc.html(html.read().format(style=css.read()), width=640, height=640)

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

if __name__ == "__main__":
    main()
