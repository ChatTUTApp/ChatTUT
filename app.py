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

# ページ設定
def pageconfig():
    icon = Image.open('image/icon.png')
    st.set_page_config(
        page_title="Chat TUT",
        page_icon=icon
    )

def main():
    # ロード時に更新されない変数の初期化
    if 'model_type' not in st.session_state:
        st.session_state.model_type = 'is_bert'
    if 'color' not in st.session_state:     # color: list(key: 色の名前, value: カラーコード)
        load_dotenv("variable.env")
        st.session_state.color = ast.literal_eval(os.environ["COLOR_DICT"])
    if 'on_color' not in st.session_state:     # on_color: list(key: 色の名前, value: カラーコード)
        load_dotenv("variable.env")
        st.session_state.on_color = ast.literal_eval(os.environ["ON_COLOR_DICT"])

    page = sidebar()
    if page == "ホーム":
        application()
    elif page == "お問い合わせ":
        app_varsion()
    elif page == "バージョン":
        app_varsion()
    elif page == "利用規約":
        app_varsion()
    elif page == "Chat TUTについて":
        app_varsion()

# モデル読み込み(入出力をkey, valueとし，キャッシュに保存)
@st.cache_resource
def load_models():
    api_key = os.getenv("OPENAI_API_KEY")
    models = {"is_bert": MyBERT(), "is_openai_api": OpenAI_API(api_key)}
    return models

# サイドバー
def sidebar():
    with st.sidebar:
        selected_options = streamlit_option_menu.option_menu(menu_title=None,
            options=["ホーム", "お問い合わせ", "バージョン", "利用規約", "Chat TUTについて"],
            icons=["house", "envelope", "ticket", "shield-exclamation", "info-circle"],
            default_index=0,
            styles={
                "container": {"background-color": f"{st.session_state.color['secondary100']}"},
                "icon": {"color": f"{st.session_state.color['secondary500']}", "font-size": "20px"},
                "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "color": f"{st.session_state.on_color['secondary100']}", "--hover-color": f"{st.session_state.color['secondary300']}"},
                "nav-link-selected": {"background-color": f"{st.session_state.color['secondary300']}", "color": f"{st.session_state.color['secondary900']}"},
            }
        )
        return selected_options

# メインアプリ画面
def application():
    communicate_logger = CommunicateLogger("data/prompt_log.csv", "data/prompt_log.jsonl")
    models = load_models()
    responser = models[st.session_state.model_type]

    title_col1, title_col2 = st.columns(2)
    with title_col1:
        with open("./templates/html/title.html") as html:
            with open("./static/css/title.css") as css:
                stc.html(html.read().format(style=css.read(), text="Chat TUT"), width=250, height=80)
    with title_col2:
        with open("./templates/html/version.html") as html:
            with open("./static/css/version.css") as css:
                stc.html(html.read().format(style=css.read(), text="version 1.0.0"), width=250, height=80)

    model_option = st.selectbox('モデルを選択してください', ('BERT', 'GPT-3.5'))
    if model_option == "BERT":
        st.session_state.model_type = 'is_bert'
    elif model_option == "GPT-3.5":
        st.session_state.model_type = 'is_openai_api'

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
            with answer_location:
                with st.spinner("回答を考え中..."):
                    answer = responser.create_response(prompt)
                with open("./templates/html/answer.html") as html:
                    with open("./static/css/answer.css") as css:
                        stc.html(html.read().format(style=css.read(), text=answer))
                # communicate_logger.logger_csv(prompt, answer)
                # communicate_logger.logger_json(prompt, answer)
                communicate_logger.logging2gspread(prompt, answer)

def app_varsion():
    st.title("今はテストページ")

    # UIカラーパレットテスト
    st.header('UIカラーパレットテスト')

    with open("./templates/html/color_pallet.html") as html:
        with open("./static/css/color_pallet.css") as css:
            stc.html(html.read().format(style=css.read()), width=640, height=640)

if __name__ == "__main__":
    pageconfig()    # ページ設定
    main()
