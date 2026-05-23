import streamlit as st
import datetime

st.title("競艇AI：意思決定エンジン v7.0")

# 入力項目
balance = st.number_input("現在の軍資金", value=20000)
grade = st.selectbox("レースグレード", ["G1/SG", "一般/G2/G3"])
display_odds = st.number_input("3連単本線オッズ", value=5.0)

# スイッチ機能の追加
collapse_2course = st.checkbox("【トリガー発動】2コースが潰れる展開")

if st.button("AI判定を開始"):
    margin = 0.3 if grade == "G1/SG" else 0.8
    virtual_odds = max(1.0, display_odds - margin)
    
    st.write(f"計算用仮想オッズ: {virtual_odds:.2f}")
    
    if display_odds < 5.0:
        st.error("【判定】見送り：オッズ不足")
    else:
        st.success(f"【判定】勝負レース")
        bet_amount = balance * 0.1
        each_bet = bet_amount / 6
        
        st.subheader("推奨買い目 (3連単6点)")
        # スイッチによる買い目の切り替え
        if collapse_2course:
            st.warning("【展開スイッチON】2コース潰れ：1-34-2345")
            bets = ["1-3-2", "1-3-4", "1-3-5", "1-4-2", "1-4-3", "1-4-5"]
        else:
            st.info("【通常展開】2コース壁：1-23-2345")
            bets = ["1-2-3", "1-2-4", "1-2-5", "1-3-2", "1-3-4", "1-3-5"]
        
        st.write(bets)
        st.info(f"1点あたりの投資: {each_bet:.0f}円")

        # 履歴保存用の簡易ロジック
        if st.button("このレースを履歴に保存"):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            history = f"{timestamp} | 投資: {bet_amount:.0f}円 | 買い目: {bets}"
            st.session_state.history = st.session_state.get("history", []) + [history]
            st.success("履歴に保存しました！")

# 履歴表示
if "history" in st.session_state:
    st.subheader("勝負履歴")
    for item in st.session_state.history:
        st.text(item)
