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

def main():
    pageconfig()    # ページ設定
    load_dotenv("variable.env") # 変数読み込み
    color = ast.literal_eval(os.environ["COLOR_DICT"])  # color: list(key: 色の名前, value: カラーコード)
    answer = machine_learning()

    begin()
    page = sidebar()
    if page == "ホーム":
        application(color, answer)
    elif page == "設定":    # TODO:以下関数化
        st.title("設定")
    elif page == "Q&A（よくあるご質問）":
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
def application(color:list, answer:str):
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
            answer_location.text("回答を考え中...")
            time.sleep(3)
            answer_location.text(answer)
            communicate_logger.logger_csv(prompt, answer)
            communicate_logger.logger_json(prompt, answer)

    # UIカラーパレットテスト
    st.header('UIカラーパレットテスト')
    st.write(f'<p><font color={color["neutrals900"]}>neutrals900</font>|'
                f'<font color={color["neutrals700"]}>neutrals700</font>|',
                f'<font color={color["neutrals500"]}>neutrals500</font>|',
                f'<font color={color["neutrals300"]}>neutrals300</font></p>',
                unsafe_allow_html=True)
    st.write(f'<p><font color={color["primary700"]}>primary700</font>|'
                f'<font color={color["primary400"]}>primary400</font>|'
                f'<font color={color["primary200"]}>primary200</font>|'
                f'<font color={color["primary100"]}>primary100</font></p>',
                unsafe_allow_html=True)
    st.write(f'<p><font color={color["secondary700"]}>secondary700</font>|'
                f'<font color={color["secondary400"]}>secondary400</font>|'
                f'<font color={color["secondary200"]}>secondary200</font>|'
                f'<font color={color["secondary100"]}>secondary100</font></p>',
                unsafe_allow_html=True)
    st.write(f'<p><font color={color["error"]}>error</font>|'
                f'<font color={color["success"]}>success</font></p>',
                unsafe_allow_html=True)

def machine_learning():
    ################
    ### 機械学習 ###
    ################
    api_key = os.getenv("OPENAI_API_KEY")
    chattut = Chattut(api_key)
    model = os.getenv("MODEL")
    # answer = chattut.create_response(prompt, model)
    # answer = answer['choices'][0]['text']
    answer = "answer\nanswer\nanswer"
    return answer

if __name__ == "__main__":
    main()