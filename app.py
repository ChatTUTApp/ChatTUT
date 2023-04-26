import streamlit as st
import time
import os
import ast
import torch
import openai
import base64
import google_auth_httplib2
import httplib2
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
from dotenv import load_dotenv
from PIL import Image

from chattut import Chattut
from prompt import PromptLogger


SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SHEET_ID = "12CKugl5GSpvy"
SHEET_NAME = "all"

@st.experimental_singleton()
def connect_to_gsheet():
    # Create a connection object
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=[SCOPE]
    )

    # Create a new Http() object for every request
    def build_request(http, *args, **kwargs):
        new_http = google_auth_httplib2.AuthorizedHttp(
            credentials, http=httplib2.Http()
        )

        return HttpRequest(new_http, *args, **kwargs)

    authorized_http = google_auth_httplib2.AuthorizedHttp(
        credentials, http=httplib2.Http()
    )

    service = build("sheets", "v4", requestBuilder=build_request, http=authorized_http)
    gsheet_connector = service.spreadsheets()

    return gsheet_connector


def add_row_to_gsheet(gsheet_connector, row):
    gsheet_connector.values().append(
        spreadsheetId=SHEET_ID,
        range=f"{SHEET_NAME}!A:C",
        body=dict(values=row),
        valueInputOption="USER_ENTERED",
    ).execute()

gsheet_connector = connect_to_gsheet()







load_dotenv("variable.env")
color = ast.literal_eval(os.environ["COLOR_DICT"])
##################
### アプリ画面 ###
##################
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

st.title("Chat TUT")

with st.form("my_form", clear_on_submit=False):
    col1,  col3 = st.columns((1,  1))
    with col1:
        prompt = st.text_input("質問を入力してください")
        submitted = st.form_submit_button("質問する")

    # with col2:
    #     image = Image.open('image/img.png')
    #     st.image(image, use_column_width=True)

    with col3:
        file_ = open("image/img.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="cat gif" width="80%" height="80%">',
                    unsafe_allow_html=True
                    )

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

################
### 機械学習 ###
################
# load_dotenv("variable.env")  # .envファイルを読み込む
api_key = os.getenv("OPENAI_API_KEY")
chattut = Chattut(api_key)
model = os.getenv("MODEL")
# answer = chattut.create_response(prompt, model)
# answer = answer['choices'][0]['text']
answer = "answer"

promptlogger = PromptLogger("data/prompt_log.csv", "data/prompt_log.jsonl")
if submitted:
    with st.spinner("回答を考え中..."):
        time.sleep(3)
    st.text(answer)
    promptlogger.logger_csv(prompt, answer)
    promptlogger.logger_json(prompt, answer)
    add_row_to_gsheet(gsheet_connector, [[prompt, answer]])
