import streamlit as st

st.title("競艇AI：意思決定エンジン v7.0")

# 1. データ入力フォーム
st.subheader("レース状況を入力")
balance = st.number_input("現在の軍資金", value=20000)
grade = st.selectbox("レースグレード", ["G1/SG", "一般/G2/G3"])
display_odds = st.number_input("3連単本線オッズ", value=5.0)

# ロジック判定
if st.button("AI判定を開始"):
    margin = 0.3 if grade == "G1/SG" else 0.8
    virtual_odds = max(1.0, display_odds - margin)
    
    st.write(f"---")
    st.write(f"計算用仮想オッズ: {virtual_odds:.2f}")
    
    # ここに判定ロジックが組み込まれます
    if display_odds < 5.0:
        st.error("【判定】見送り：オッズ不足")
    else:
        st.success(f"【判定】勝負レース")
        st.write(f"推奨投資額: {balance * 0.5:.0f}円")
        st.warning("悪魔の代弁者：本命が飛んだ場合、資金を失います。覚悟はいいですか？")
