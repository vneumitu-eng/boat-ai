import streamlit as st
import datetime
import pandas as pd

st.title("競艇AI：意思決定エンジン v7.0")

# 入力項目
balance = st.number_input("現在の軍資金", value=20000)
grade = st.selectbox("レースグレード", ["G1/SG", "一般/G2/G3"])
display_odds = st.number_input("3連単本線オッズ", value=5.0)

# 特例ロジック：峰竜太チェック
mine_pos = st.selectbox("峰竜太の出走枠", ["不在", "1枠", "4-6枠"])
collapse_2course = st.checkbox("【トリガー】2コースが潰れる展開")

if st.button("AI判定を開始"):
    # ロジック判定
    if mine_pos == "4-6枠":
        st.error("【警告】峰竜太が外枠のため、大勝負から除外します")
    
    margin = 0.3 if grade == "G1/SG" else 0.8
    virtual_odds = max(1.0, display_odds - margin)
    
    st.write(f"計算用仮想オッズ: {virtual_odds:.2f}")
    
    if display_odds < 5.0:
        st.error("【判定】見送り：オッズ不足")
    else:
        st.success(f"【判定】勝負レース")
        bet_amount = balance * 0.1
        
        st.subheader("推奨買い目 (3連単6点)")
        
        # 買い目の切り替え
        if collapse_2course:
            st.warning("【展開スイッチON】2コース潰れ")
            bets = ["1-3-2", "1-3-4", "1-3-5", "1-4-2", "1-4-3", "1-4-5"]
        else:
            st.info("【通常展開】2コース壁")
            bets = ["1-2-3", "1-2-4", "1-2-5", "1-3-2", "1-3-4", "1-3-5"]
        
        # 表形式で見やすく表示
        df = pd.DataFrame(bets, columns=["推奨買い目"])
        st.table(df)
        
        st.info(f"合計投資: {bet_amount:.0f}円 (軍資金の {int((bet_amount/balance)*100)}%)")

        if st.button("このレースを履歴に保存"):
            timestamp = datetime.datetime.now().strftime("%H:%M")
            history = f"{timestamp} | 投資: {bet_amount:.0f}円 | 買い目: {bets}"
            st.session_state.history = st.session_state.get("history", []) + [history]
            st.success("履歴保存完了")

if "history" in st.session_state:
    st.subheader("勝負履歴")
    st.write(st.session_state.history)
