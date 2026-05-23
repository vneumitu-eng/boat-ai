import streamlit as st

st.title("競艇AI：意思決定エンジン v7.0")

# 入力項目
balance = st.number_input("現在の軍資金", value=20000)
grade = st.selectbox("レースグレード", ["G1/SG", "一般/G2/G3"])
display_odds = st.number_input("3連単本線オッズ", value=5.0)

if st.button("AI判定を開始"):
    # オッズ計算
    margin = 0.3 if grade == "G1/SG" else 0.8
    virtual_odds = max(1.0, display_odds - margin)
    
    st.write(f"計算用仮想オッズ: {virtual_odds:.2f}")
    
    if display_odds < 5.0:
        st.error("【判定】見送り：オッズ不足")
    else:
        st.success(f"【判定】勝負レース")
        
        # 3連単6点の資金配分ロジック（簡易版）
        bet_amount = balance * 0.1
        each_bet = bet_amount / 6
        
        st.subheader("推奨買い目 (3連単6点)")
        col1, col2 = st.columns(2)
        with col1:
            st.write("1-2-3 (厚め)")
            st.write("1-2-4")
            st.write("1-2-5")
        with col2:
            st.write("1-3-2")
            st.write("1-3-4")
            st.write("1-3-5")
        
        st.info(f"1点あたりの投資額: {each_bet:.0f}円 (合計 {bet_amount:.0f}円)")
        
        # 悪魔の代弁者（損切の可視化）
        st.warning(f"【悪魔の代弁者】このレースで本命が飛んだ場合、{bet_amount:.0f}円を失います。")
        st.checkbox("損害額を認識し、リスクを許容します")
