import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ページ設定
st.set_page_config(page_title="感情の計測 (PANAS)", layout="centered")

# ヘッダー画像
st.image("header.png", width='stretch')

# フォームのタイトルと説明
st.title("感情の計測")
st.markdown("""
ポジティブ感情・ネガティブ感情測定尺度(PANAS)によって、今日１日のあなたの感情を総合的に判断します。\n
過去24時間に、各質問にあることがどの程度の頻度で感じたのかを答えてください。
""")

# 質問リスト
questions = [
    "1. 面白かったこと、愉快だったこと",
    "2. いらだったこと、不愉快だったこと",
    "3. 屈辱だったこと、不祥事を起こしたこと",
    "4. 畏敬の念を感じたこと、驚きを感じたこと",
    "5. 軽蔑したこと、見下す気持ちだったこと",
    "6. 嫌悪感を感じたこと、不快だったこと",
    "7. 恥ずかしかったこと、人目が気になったこと",
    "8. 感謝したこと、ありがたかったこと",
    "9. 後悔したこと、自責の念にかられたこと",
    "10. 憎しみを感じたこと、不信感をもったこと",
    "11. 希望を感じたこと、勇気が出たこと",
    "12. 高揚感を感じたこと、元気づけられたこと",
    "13. 好奇心を持ったこと、強い関心をもったこと",
    "14. うれしかったこと、幸せだったこと",
    "15. 親しみを感じたこと、信頼できたこと",
    "16. 自信を持ったこと、自分を信頼できたこと",
    "17. 悲しかったこと、がっかりしたこと",
    "18. 怖かったこと、不安だったこと",
    "19. 安心したこと、平穏を感じたこと",
    "20. ストレスを感じたこと、緊張したこと"
]

# 選択肢とスコアの対応
options = {
    "まったくなかった": 1,
    "若干あった": 2,
    "普通にあった": 3,
    "かなりあった": 4,
    "非常に多かった": 5
}

# ポジティブ・ネガティブの判定インデックス
pos_indices = [0, 3, 7, 10, 11, 12, 13, 14, 15, 18]  # case 1, 4, 8, 11, 12, 13, 14, 15, 16, 19
neg_indices = [1, 2, 4, 5, 6, 8, 9, 16, 17, 19]     # case 2, 3, 5, 6, 7, 9, 10, 17, 18, 20

# UI構築
st.divider()
# st.write("過去 24 時間に、質問にあることがどのくらいの頻度であったのかを答えてください。")

# 回答を格納する辞書
user_responses = []

# 質問の表示
for i, q in enumerate(questions):
    st.markdown(f"**{q}**")
    res = st.selectbox(q, list(options.keys()), index=0, key=f"q_{i}", label_visibility="collapsed")
    user_responses.append(options[res])

st.divider()

# 「結果を表示する」ボタン
if st.button("結果を表示する", type="primary"):
    # スコア計算
    positive_score = sum(user_responses[i] for i in pos_indices)
    negative_score = sum(user_responses[i] for i in neg_indices)
    
    # 比率計算
    ratio = round((positive_score / negative_score) * 10) / 10 if negative_score > 0 else 0

    # 結果表示セクション
    st.header("測定結果")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("ポジティブ感情", f"{positive_score} 点")
    col2.metric("ネガティブ感情", f"{negative_score} 点")
    col3.metric("ポジティビティ比率", f"{ratio}")

    st.info("ポジティビティ比率を１以上にすることがウェル・ビーイングにつながります。")

    # グラフ表示
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        plot_data = pd.DataFrame({
            "感情タイプ": ["ネガティブ感情", "ポジティブ感情"],
            "点数": [negative_score, positive_score]
        })
        fig = px.bar(
            plot_data,
            x="感情タイプ",
            y="点数",
            color="感情タイプ",
            range_y=[0, 50],
            color_discrete_map={"ネガティブ感情": "#4169E1", "ポジティブ感情": "#FFA500"}
        )
        fig.update_layout(showlegend=False, title=dict(text="ポジティブ感情とネガティブ感情"))
        st.plotly_chart(fig, width='stretch')

    with chart_col2:
        fig2 = go.Figure(data=[go.Pie(
            values=[positive_score, negative_score],
            labels=["ポジティブ感情", "ネガティブ感情"],
            hole=0.6,
            marker_colors=["#FFA500", "#4169E1"],
            textinfo="label+percent",
        )])
        fig2.update_layout(
            showlegend=False,
            annotations=[
                dict(
                    text="ポジティビティ比率",
                    x=0.5, y=0.6,
                    font_size=16,
                    showarrow=False,
                ),
                dict(
                    text=f"{ratio:.1f}",
                    x=0.5, y=0.45,
                    font_size=36,
                    showarrow=False,
                ),
            ],
        )
        st.plotly_chart(fig2, width='stretch')
    
    # 比率に応じた演出
    if ratio >= 1.0:
        st.balloons()