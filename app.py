import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# APIキーの設定
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# モデルのインスタンス化（プレフィックスなし）
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("競艇解析エンジン v7.0")

uploaded_file = st.file_uploader("出走表のスクショをアップロード", type=["png", "jpg", "jpeg"])

if uploaded_file and st.button("AI解析実行"):
    image = Image.open(uploaded_file)
    with st.spinner('解析中...'):
        try:
            # 画像解析リクエスト
            response = model.generate_content(['競艇出走表からgrade, wind_speed, wave_height, exhibition_timesをJSONで抽出', image])
            st.json(response.text)
        except Exception as e:
            st.error(f"エラー: {e}")
