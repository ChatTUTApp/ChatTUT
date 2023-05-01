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

def main():
    pageconfig()    # ページ設定
    load_dotenv("variable.env") # 変数読み込み
    # color:背景色, on_color:文字色     color(key)の上にon_color(key)で対応
    color = ast.literal_eval(os.environ["COLOR_DICT"])  # color: list(key: 色の名前, value: カラーコード)
    on_color = ast.literal_eval(os.environ["ON_COLOR_DICT"])  # on_color: list(key: 色の名前, value: カラーコード)
    # answer = machine_learning()
    begin()
    page = sidebar(color, on_color)
    if page == "ホーム":
        application(color, on_color)
    elif page == "バージョン":
        app_varsion(color, on_color)

# ページ更新時に読み込まない
@st.cache_data
def begin():
    ConsoleLogger()

# ページ設定
def pageconfig():
    icon = Image.open('image/icon.png')
    st.set_page_config(
        page_title="Chat TUT",
        page_icon=icon
        )

# サイドバー
def sidebar(color:list, on_color:list):
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
def application(color:list, on_color:list, answer:str=""):
    communicate_logger = CommunicateLogger("data/prompt_log.csv", "data/prompt_log.jsonl")

    st.title("Chat TUT")

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
            answer = machine_learning(prompt)
        with col2:
            st.write("")
            st.write("")
            submitted = st.form_submit_button("質問する")

        if submitted:
            with answer_location:
                with st.spinner("回答を考え中..."):
                    time.sleep(3)
                answer_location.text(answer)
                communicate_logger.logger_csv(prompt, answer)
                communicate_logger.logger_json(prompt, answer)

def app_varsion(color:list, on_color:list):
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
    model_type = {"is_bert":MyBERT(), "is_openai_api": OpenAI_API(api_key)}
    chattut = Chattut(model_type["is_bert"]) # TODO アプリ画面上でモードを切り替えられるようになったらいいなぁ
    answer = chattut.create_response(prompt)
    return answer

if __name__ == "__main__":
    main()