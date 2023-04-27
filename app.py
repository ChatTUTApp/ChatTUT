import streamlit as st
import time
import os
import ast
import torch
import openai
import base64
from dotenv import load_dotenv
from PIL import Image

from chattut import Chattut
from prompt import PromptLogger


def main():
    load_dotenv("variable.env")
    color = ast.literal_eval(os.environ["COLOR_DICT"])

    answer = machine_learning()
    application(color, answer)


def application(color:list, answer:str):
    ##################
    ### アプリ画面 ###
    ##################
    icon = Image.open('image/icon.png')
    # ページ設定
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

    promptlogger = PromptLogger("data/prompt_log.csv", "data/prompt_log.jsonl")

    st.title("Chat TUT")

    with st.form("main_form", clear_on_submit=False):
        file_ = open("image/img.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="cat gif" width="80%" height="80%">',
                    unsafe_allow_html=True
                    )

        answerlocation = st.empty()

        col1, col2 = st.columns((3, 1))
        with col1:
            prompt = st.text_input("質問を入力してください")
        with col2:
            st.write("")
            st.write("")
            submitted = st.form_submit_button("質問する")

        if submitted:
            answerlocation.text("回答を考え中...")
            time.sleep(3)
            answerlocation.text(answer)
            promptlogger.logger_csv(prompt, answer)
            promptlogger.logger_json(prompt, answer)

    # UIカラーパレットテスト
    st.write(f'<p><font color={color["neutrals900"]}>neutrals900</font></p>', unsafe_allow_html=True)
    st.write(f'<p><font color={color["neutrals700"]}>neutrals700</font></p>', unsafe_allow_html=True)
    st.write(f'<p><font color={color["neutrals500"]}>neutrals500</font></p>', unsafe_allow_html=True)
    st.write(f'<p><font color={color["neutrals300"]}>neutrals300</font></p>', unsafe_allow_html=True)
    st.write(f'<p><font color={color["primary700"]}>primary700</font></p>', unsafe_allow_html=True)
    st.write(f'<p><font color={color["primary400"]}>primary400</font></p>', unsafe_allow_html=True)
    st.write(f'<p><font color={color["primary200"]}>primary200</font></p>', unsafe_allow_html=True)
    st.write(f'<p><font color={color["primary100"]}>primary100</font></p>', unsafe_allow_html=True)
    st.write(f'<p><font color={color["secondary700"]}>secondary700</font></p>', unsafe_allow_html=True)
    st.write(f'<p><font color={color["secondary400"]}>secondary400</font></p>', unsafe_allow_html=True)
    st.write(f'<p><font color={color["secondary200"]}>secondary200</font></p>', unsafe_allow_html=True)
    st.write(f'<p><font color={color["secondary100"]}>secondary100</font></p>', unsafe_allow_html=True)
    st.write(f'<p><font color={color["error"]}>error</font></p>', unsafe_allow_html=True)
    st.write(f'<p><font color={color["success"]}>success</font></p>', unsafe_allow_html=True)


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