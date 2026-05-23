import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import json

# --- 設定 ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

st.title("競艇勝負ロジック：完全統合エンジン v7.0")

# --- OCR Engine: スクショ解析 ---
uploaded_file = st.file_uploader("出走表のスクショをアップロード", type=["png", "jpg", "jpeg"])
data = None

if uploaded_file:
    image = Image.open(uploaded_file)
    if st.button("AI解析実行"):
        with st.spinner('解析中...'):
            prompt = "この競艇出走表から、grade, wind_speed(m), wave_height(cm), exhibition_times(6個のリスト)をJSONで抽出。"
            response = model.generate_content([prompt, image])
            data = json.loads(response.text.replace('```json', '').replace('```', '').strip())
            st.session_state.data = data
            st.success("解析完了")

# データ保持
if "data" in st.session_state:
    data = st.session_state.data
    st.write(f"解析済み: {data['grade']} / 風速:{data['wind_speed']}m / 波高:{data['wave_height']}cm")

# --- Rule & Risk Engine: 勝負判定 ---
st.divider()
balance = st.number_input("軍資金総額", value=20000)
odds = st.number_input("3連単本線オッズ", value=5.0)
is_collapse = st.checkbox("【トリガー】2コース潰れ展開")

if st.button("最終判定 (GO/NO-GO)"):
    # Risk Engine: 悪魔の代弁者（悪天候チェック）
    if data and data['wave_height'] and int(data['wave_height']) >= 5:
        st.error("【Risk】波高5cm以上：運ゲー水面のためケン（見送り）を推奨")
    
    # Rule Engine: 勝負分類
    margin = 0.3 if data and data['grade'] == "SG/G1" else 0.8
    virtual_odds = odds - margin
    
    if virtual_odds < 4.0:
        st.error("【NO-GO】オッズ不足：見送り")
    else:
        st.success("【GO】勝負レース")
        # Odds Engine: 傾斜配分
        bet_amount = balance * 0.1
        st.write(f"推奨投資: {bet_amount:.0f}円")
        
        # フォーメーション提示
        bets = ["1-3-2", "1-3-4", "1-3-5", "1-4-2", "1-4-3", "1-4-5"] if is_collapse else ["1-2-3", "1-2-4", "1-2-5", "1-3-2", "1-3-4", "1-3-5"]
        st.table(pd.DataFrame(bets, columns=["推奨買い目"]))
        
        # Risk Engine: 損失警告
        st.warning(f"全損リスク: 投資額の {int((bet_amount/balance)*100)}% が消失する可能性があります。")
