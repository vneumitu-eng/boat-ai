import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import json

# --- 設定 ---
# APIキーが空でないか確認
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("APIキーが設定されていません。Secretsを確認してください。")
    st.stop()

genai.configure(api_key=api_key)
# モデル名を明示的に指定
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

st.title("競艇勝負ロジック：完全統合エンジン v7.0")

# --- OCR Engine: スクショ解析 ---
uploaded_file = st.file_uploader("出走表のスクショをアップロード", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた出走表", use_container_width=True)
    
    if st.button("AI解析実行"):
        with st.spinner('解析中...'):
            try:
                prompt = "この競艇出走表から、grade, wind_speed(m), wave_height(cm), exhibition_times(6個のリスト)をJSON形式のみで抽出してください。"
                response = model.generate_content([prompt, image])
                
                # JSONのクリーニング
                text = response.text.replace('```json', '').replace('```', '').strip()
                data = json.loads(text)
                
                st.session_state.data = data
                st.success("解析完了")
            except Exception as e:
                st.error(f"解析エラー: {e}")

# --- データ保持と判定 ---
if "data" in st.session_state:
    data = st.session_state.data
    st.write(f"解析済み: {data.get('grade')} / 風速:{data.get('wind_speed')}m / 波高:{data.get('wave_height')}cm")
    
    st.divider()
    balance = st.number_input("軍資金総額", value=20000)
    odds = st.number_input("3連単本線オッズ", value=5.0)
    is_collapse = st.checkbox("【トリガー】2コース潰れ展開")

    if st.button("最終判定 (GO/NO-GO)"):
        # 悪天候チェック
        if data.get('wave_height') and int(data['wave_height']) >= 5:
            st.error("【Risk】波高5cm以上：運ゲー水面のためケン（見送り）を推奨")
        else:
            # 勝負判定
            margin = 0.3 if data.get('grade') == "SG/G1" else 0.8
            virtual_odds = odds - margin
            
            if virtual_odds < 4.0:
                st.error("【NO-GO】オッズ不足：見送り")
            else:
                st.success("【GO】勝負レース")
                bet_amount = balance * 0.1
                st.write(f"推奨投資: {bet_amount:.0f}円")
                bets = ["1-3-2", "1-3-4", "1-3-5", "1-4-2", "1-4-3", "1-4-5"] if is_collapse else ["1-2-3", "1-2-4", "1-2-5", "1-3-2", "1-3-4", "1-3-5"]
                st.table(pd.DataFrame(bets, columns=["推奨買い目"]))
                st.warning(f"全損リスク: 投資額の {int((bet_amount/balance)*100)}% が消失する可能性があります。")
