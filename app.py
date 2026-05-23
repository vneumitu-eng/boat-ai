import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import json

# --- 1. APIキーの設定 (Secretsから読み込み) ---
# ※設定したGEMINI_API_KEYを安全に呼び出します
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-1.5-flash')

st.title("競艇AI：スクショ解析データ入力エンジン")

# --- 2. データの入力方法 ---
# 画像アップロード
uploaded_file = st.file_uploader("出走表のスクリーンショットをアップロード", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='解析中の出走表', use_column_width=True)
    
    if st.button("AI解析開始"):
        with st.spinner('Geminiが画像を解析中...'):
            prompt = """
            この競艇の出走表から、以下のデータを抽出し、JSON形式で出力してください。
            {
              "grade": "SG/G1/一般",
              "wind_speed": "風速",
              "wave_height": "波高",
              "exhibition_times": [1号艇の展示タイム, 2, 3, 4, 5, 6]
            }
            """
            response = model.generate_content([prompt, image])
            data = json.loads(response.text.replace('```json', '').replace('```', '').strip())
            
            st.success("データ取得完了！")
            
            # --- 3. 判定ロジック (統合版) ---
            st.subheader("解析結果とAI判定")
            df = pd.DataFrame({"艇番": [1,2,3,4,5,6], "展示タイム": data["exhibition_times"]})
            st.table(df)
            
            # 悪天候チェック
            if data["wave_height"] and int(data["wave_height"]) >= 5:
                st.error("【警告】波高が5cm以上のため見送り推奨")
            
            # 爆弾足チェック (1号艇との比較)
            times = [float(t) for t in data["exhibition_times"] if t is not None]
            if times and (min(times) < float(data["exhibition_times"][0]) - 0.05):
                st.warning("【警告】1号艇より速い艇が存在します。内枠の壁に注意！")

# --- 4. 手動入力の補助 ---
st.divider()
st.subheader("手動調整")
balance = st.number_input("現在の軍資金", value=20000)
display_odds = st.number_input("3連単本線オッズ", value=5.0)
if st.button("最終判定"):
    st.info(f"勝負レース判定：オッズ {display_odds} 倍に対し、仮想オッズで判定を行います。")
    
