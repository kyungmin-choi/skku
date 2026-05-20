import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# 페이지 기본 설정
# =====================================================
st.set_page_config(
    page_title="한국 글로벌 무역 포지션 대시보드",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CSS 디자인 설정
# =====================================================
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top left, #10284f 0%, #07111f 35%, #020617 100%);
        color: #e5eefc;
    }

    section[data-testid="stSidebar"] {
        background: rgba(5, 15, 30, 0.92);
        border-right: 1px solid rgba(100, 180, 255, 0.25);
    }

    .main-title {
        font-size: 44px;
        font-weight: 800;
        background: linear-gradient(90deg, #7dd3fc, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }

    .sub-title {
        color: #b8c7e0;
        font-size: 18px;
        margin-bottom: 28px;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(125, 211, 252, 0.18);
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.22);
        backdrop-filter: blur(10px);
        margin-bottom: 18px;
    }

    .metric-card {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.2), rgba(79, 70, 229, 0.18));
        border: 1px solid rgba(125, 211, 252, 0.25);
        border-radius: 18px;
        padding: 18px;
        text-align: center;
    }

    .metric-label {
        color: #b8c7e0;
        font-size: 14px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 28px;
        font-weight: 800;
    }

    .keyword-pill {
        display: inline-block;
        padding: 7px 13px;
        margin: 5px;
        border-radius: 100px;
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(125, 211, 252, 0.3);
        color: #dbeafe;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# 샘플 데이터
# 실제 제출 전에는 OECD, World Bank, KITA 데이터로 교체 가능
# =====================================================

trade_partners = pd.DataFrame({
    "국가": ["중국", "미국", "베트남", "일본", "대만", "독일", "싱가포르", "인도", "멕시코", "호주"],
    "영문국가명": ["China", "United States", "Vietnam", "Japan", "Taiwan", "Germany", "Singapore", "India", "Mexico", "Australia"],
    "iso_alpha": ["CHN", "USA", "VNM", "JPN", "TWN", "DEU", "SGP", "IND", "MEX", "AUS"],
    "수출액_십억달러": [124.8, 115.7, 53.5, 29.0, 28.4, 11.2, 18.7, 18.0, 12.3, 17.8],
    "수입액_십억달러": [142.9, 71.3, 26.7, 47.6, 23.1, 23.7, 12.4, 8.9, 7.1, 33.2],
    "지역": ["아시아", "북미", "아시아", "아시아", "아시아", "유럽", "아시아", "아시아", "북미", "오세아니아"]
})
trade_partners["총교역액_십억달러"] = trade_partners["수출액_십억달러"] + trade_partners["수입액_십억달러"]
trade_partners["무역수지_십억달러"] = trade_partners["수출액_십억달러"] - trade_partners["수입액_십억달러"]

trade_timeline = pd.DataFrame({
    "연도": list(range(2014, 2025)),
    "수출": [573, 527, 495, 573, 605, 542, 512, 644, 683, 632, 683],
    "수입": [526, 436, 406, 478, 535, 503, 467, 615, 731, 642, 632],
})
trade_timeline["무역수지"] = trade_timeline["수출"] - trade_timeline["수입"]
trade_timeline["총교역액"] = trade_timeline["수출"] + trade_timeline["수입"]

industries = pd.DataFrame({
    "산업": ["반도체", "자동차", "석유화학", "배터리", "조선", "철강", "디스플레이", "기계", "IT 기기"],
    "수출액": [129, 71, 54, 38, 22, 31, 20, 53, 46],
    "공급망_의존도": ["높음", "중간", "중간", "높음", "중간", "중간", "높음", "중간", "높음"],
    "주요_연결국가": ["중국 / 대만 / 미국", "미국 / 유럽", "중국 / ASEAN", "미국 / 유럽 / 중국", "유럽 / 중동", "중국 / 일본", "중국 / 베트남", "미국 / 중국", "중국 / 베트남"]
})

oecd_sample = pd.DataFrame({
    "국가": ["한국", "독일", "일본", "미국", "네덜란드", "프랑스", "멕시코", "캐나다"],
    "무역의존도": [85, 89, 45, 27, 156, 66, 83, 68],
    "GVC참여도": [56, 52, 41, 38, 61, 45, 49, 46],
    "서비스무역비중": [18, 24, 21, 31, 33, 29, 15, 20],
    "FDI연결성": [62, 68, 48, 76, 85, 64, 59, 66],
    "제조업비중": [27, 19, 20, 11, 10, 10, 18, 10]
})

supply_chain = pd.DataFrame({
    "출발": ["한국", "한국", "한국", "일본", "대만", "중국", "베트남", "한국", "미국"],
    "도착": ["중국", "미국", "베트남", "한국", "한국", "미국", "미국", "유럽", "한국"],
    "값": [35, 28, 20, 14, 12, 26, 18, 21, 16],
    "분야": ["반도체", "자동차", "전자제품", "소재", "칩", "최종재", "조립", "배터리", "기술"]
})

fdi_data = pd.DataFrame({
    "연도": list(range(2016, 2025)),
    "외국인직접투자_유입": [10, 12, 17, 13, 11, 19, 18, 15, 16],
    "해외직접투자_유출": [27, 31, 38, 35, 32, 44, 52, 48, 50]
})

service_trade = pd.DataFrame({
    "분야": ["운송", "IT 서비스", "여행", "금융", "지식재산권", "기타 비즈니스 서비스"],
    "비중": [28, 22, 14, 11, 9, 16]
})

# =====================================================
# 사이드바
# =====================================================
st.sidebar.title("🌐 대시보드 컨트롤")
st.sidebar.caption("한국 글로벌 무역 포지션 대시보드")

selected_year = st.sidebar.slider("연도 선택", 2014, 2024, 2024)
selected_region = st.sidebar.multiselect(
    "지역 선택",
    options=trade_partners["지역"].unique(),
    default=list(trade_partners["지역"].unique())
)
selected_industries = st.sidebar.multiselect(
    "수출 산업 선택",
    options=industries["산업"].tolist(),
    default=industries["산업"].tolist()[:5]
)
selected_country = st.sidebar.selectbox(
    "OECD 비교 국가 선택",
    options=[c for c in oecd_sample["국가"] if c != "한국"]
)

filtered_trade = trade_partners[trade_partners["지역"].isin(selected_region)]
filtered_industries = industries[industries["산업"].isin(selected_industries)]

# =====================================================
# 헤더
# =====================================================
st.markdown('<h1 class="main-title">한국 글로벌 무역 포지션 대시보드</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">데이터 시각화를 통해 세계 경제 속 한국의 역할을 이해하는 인터랙티브 웹사이트</p>', unsafe_allow_html=True)

# =====================================================
# 상단 핵심 지표 카드
# =====================================================
metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">총 교역액</div>
        <div class="metric-value">${filtered_trade['총교역액_십억달러'].sum():.1f}B</div>
    </div>
    """, unsafe_allow_html=True)
with metric2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">총 수출액</div>
        <div class="metric-value">${filtered_trade['수출액_십억달러'].sum():.1f}B</div>
    </div>
    """, unsafe_allow_html=True)
with metric3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">총 수입액</div>
        <div class="metric-value">${filtered_trade['수입액_십억달러'].sum():.1f}B</div>
    </div>
    """, unsafe_allow_html=True)
with metric4:
    korea_gvc = oecd_sample.loc[oecd_sample["국가"] == "한국", "GVC참여도"].iloc[0]
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">한국 GVC 참여도</div>
        <div class="metric-value">{korea_gvc}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# 탭 구성
# =====================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📌 개요",
    "🗺️ 무역 네트워크",
    "📈 무역 타임라인",
    "🏭 산업 분석",
    "🔗 GVC & 공급망",
    "🌍 OECD 비교",
    "💰 FDI & 서비스"
])

# =====================================================
# 탭 1: 개요
# =====================================================
with tab1:
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("""
        <div class="glass-card">
        <h3>프로젝트 방향성</h3>
        <p>
        이 대시보드는 한국이 세계 경제와 국제 공급망 안에서 어떤 위치에 있는지를 시각화합니다.
        단순히 수출입 통계를 나열하는 것이 아니라, 한국의 경제적 연결 관계, 무역 의존도,
        글로벌 가치사슬 참여도, 산업 구조를 함께 보여주는 것이 목표입니다.
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
        <h3>핵심 질문</h3>
        <ul>
            <li>한국은 어떤 국가들과 가장 강하게 경제적으로 연결되어 있는가?</li>
            <li>한국 경제는 세계 무역에 얼마나 의존하고 있는가?</li>
            <li>한국은 글로벌 가치사슬에서 어떤 역할을 하는가?</li>
            <li>한국의 무역 구조는 시간에 따라 어떻게 변화해왔는가?</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'><h3>핵심 키워드</h3>", unsafe_allow_html=True)
        keywords = [
            "글로벌 무역", "한국 경제", "GVC", "OECD 비교",
            "공급망", "무역 의존도", "데이터 시각화", "인터랙티브 대시보드"
        ]
        keyword_html = "".join([f"<span class='keyword-pill'>{k}</span>" for k in keywords])
        st.markdown(keyword_html + "</div>", unsafe_allow_html=True)

        fig_overview = px.bar(
            trade_partners.sort_values("총교역액_십억달러", ascending=False),
            x="국가",
            y="총교역액_십억달러",
            title="한국의 주요 교역국",
            labels={"총교역액_십억달러": "총 교역액, 십억 달러", "국가": "국가"}
        )
        fig_overview.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_overview, use_container_width=True)

# =====================================================
# 탭 2: 무역 네트워크
# =====================================================
with tab2:
    st.subheader("글로벌 무역 네트워크 지도")
    st.caption("한국의 주요 교역국을 세계 지도 위에 시각화합니다. 색이 진할수록 교역 규모가 큽니다.")

    fig_map = px.choropleth(
        filtered_trade,
        locations="iso_alpha",
        color="총교역액_십억달러",
        hover_name="국가",
        hover_data={"수출액_십억달러": True, "수입액_십억달러": True, "무역수지_십억달러": True, "iso_alpha": False},
        color_continuous_scale="Blues",
        title="한국의 글로벌 무역 연결 구조"
    )
    fig_map.update_layout(template="plotly_dark", geo=dict(bgcolor="rgba(0,0,0,0)"), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_map, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_export = px.bar(filtered_trade.sort_values("수출액_십억달러", ascending=True), x="수출액_십억달러", y="국가", orientation="h", title="국가별 수출액")
        fig_export.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_export, use_container_width=True)
    with col2:
        fig_import = px.bar(filtered_trade.sort_values("수입액_십억달러", ascending=True), x="수입액_십억달러", y="국가", orientation="h", title="국가별 수입액")
        fig_import.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_import, use_container_width=True)

# =====================================================
# 탭 3: 무역 타임라인
# =====================================================
with tab3:
    st.subheader("무역 변화 타임라인")

    chart_option = st.radio("보고 싶은 차트 선택", ["수출 & 수입", "무역수지", "총 교역액"], horizontal=True)

    if chart_option == "수출 & 수입":
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=trade_timeline["연도"], y=trade_timeline["수출"], mode="lines+markers", name="수출"))
        fig_line.add_trace(go.Scatter(x=trade_timeline["연도"], y=trade_timeline["수입"], mode="lines+markers", name="수입"))
        fig_line.update_layout(title="한국의 수출입 변화", template="plotly_dark", yaxis_title="십억 달러")
    elif chart_option == "무역수지":
        fig_line = px.bar(trade_timeline, x="연도", y="무역수지", title="한국의 무역수지 변화")
        fig_line.update_layout(template="plotly_dark", yaxis_title="십억 달러")
    else:
        fig_line = px.area(trade_timeline, x="연도", y="총교역액", title="한국의 총 교역액 변화")
        fig_line.update_layout(template="plotly_dark", yaxis_title="십억 달러")

    fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("""
    <div class="glass-card">
    <h3>경제 이벤트 해석</h3>
    <p><b>코로나19:</b> 글로벌 수요 감소와 물류 차질이 한국 수출 산업에 영향을 주었습니다.</p>
    <p><b>반도체 호황:</b> 한국의 수출 성과는 반도체 경기 사이클에 크게 좌우됩니다.</p>
    <p><b>미중 무역 갈등:</b> 한국은 두 거대 경제권 사이에 위치해 공급망 불확실성에 영향을 받습니다.</p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# 탭 4: 산업 분석
# =====================================================
with tab4:
    st.subheader("수출 산업 및 산업 구조 분석")

    col1, col2 = st.columns([1.2, 1])
    with col1:
        fig_tree = px.treemap(
            filtered_industries,
            path=["공급망_의존도", "산업"],
            values="수출액",
            title="한국의 주요 수출 산업 구조"
        )
        fig_tree.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_tree, use_container_width=True)

    with col2:
        fig_industry_bar = px.bar(
            filtered_industries.sort_values("수출액", ascending=True),
            x="수출액",
            y="산업",
            orientation="h",
            title="산업별 수출액"
        )
        fig_industry_bar.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_industry_bar, use_container_width=True)

    st.dataframe(filtered_industries, use_container_width=True)

# =====================================================
# 탭 5: GVC & 공급망
# =====================================================
with tab5:
    st.subheader("글로벌 가치사슬과 공급망 흐름")

    labels = list(pd.unique(supply_chain[["출발", "도착"]].values.ravel("K")))
    label_index = {label: i for i, label in enumerate(labels)}

    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(
            pad=18,
            thickness=18,
            line=dict(color="rgba(255,255,255,0.3)", width=0.5),
            label=labels,
        ),
        link=dict(
            source=supply_chain["출발"].map(label_index),
            target=supply_chain["도착"].map(label_index),
            value=supply_chain["값"],
            label=supply_chain["분야"]
        )
    )])
    fig_sankey.update_layout(title_text="단순화한 글로벌 공급망 흐름", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_sankey, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="glass-card">
        <h3>전방 참여 Forward Participation</h3>
        <p>한국에서 만들어진 부품이나 중간재가 다른 나라의 생산 과정에 사용되는 정도입니다.</p>
        <p><b>예시:</b> 한국 반도체 → 중국 조립 → 미국 소비시장 판매</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="glass-card">
        <h3>후방 참여 Backward Participation</h3>
        <p>한국이 수출품을 생산할 때 해외 중간재나 부품에 의존하는 정도입니다.</p>
        <p><b>예시:</b> 일본 소재 → 한국 생산 → 세계 시장 수출</p>
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# 탭 6: OECD 비교
# =====================================================
with tab6:
    st.subheader("한국과 OECD 국가 비교")

    comparison_df = oecd_sample[oecd_sample["국가"].isin(["한국", selected_country])]

    categories = ["무역의존도", "GVC참여도", "서비스무역비중", "FDI연결성", "제조업비중"]

    fig_radar = go.Figure()
    for _, row in comparison_df.iterrows():
        fig_radar.add_trace(go.Scatterpolar(
            r=[row[c] for c in categories],
            theta=categories,
            fill="toself",
            name=row["국가"]
        ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        template="plotly_dark",
        title=f"한국 vs {selected_country}: 경제 구조 비교",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    fig_oecd_bar = px.bar(
        oecd_sample.sort_values("무역의존도", ascending=False),
        x="국가",
        y="무역의존도",
        title="OECD 주요 국가의 무역 의존도 비교"
    )
    fig_oecd_bar.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_oecd_bar, use_container_width=True)

# =====================================================
# 탭 7: FDI & 서비스
# =====================================================
with tab7:
    st.subheader("해외직접투자와 서비스 무역")

    col1, col2 = st.columns(2)
    with col1:
        fig_fdi = go.Figure()
        fig_fdi.add_trace(go.Scatter(x=fdi_data["연도"], y=fdi_data["외국인직접투자_유입"], mode="lines+markers", name="FDI 유입"))
        fig_fdi.add_trace(go.Scatter(x=fdi_data["연도"], y=fdi_data["해외직접투자_유출"], mode="lines+markers", name="FDI 유출"))
        fig_fdi.update_layout(title="한국의 FDI 유입 / 유출 변화", template="plotly_dark", yaxis_title="십억 달러", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_fdi, use_container_width=True)

    with col2:
        fig_service = px.pie(service_trade, names="분야", values="비중", title="서비스 무역 구성")
        fig_service.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_service, use_container_width=True)

    st.markdown("""
    <div class="glass-card">
    <h3>최종 인사이트</h3>
    <p>
    한국은 단순한 수출 중심 국가가 아니라 글로벌 가치사슬 속에서 중요한 연결 지점 역할을 합니다.
    앞으로의 전략은 교역국 다변화, 고부가가치 산업 강화, 공급망 취약성 완화에 달려 있습니다.
    </p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# 푸터
# =====================================================
st.markdown("---")
st.caption("데이터 안내: 현재 버전은 프로토타입용 샘플 데이터를 사용합니다. 최종 제출 시 OECD, World Bank, KITA, UN Comtrade 등의 실제 데이터로 교체할 수 있습니다.")
st.caption("제작 도구: Python, Streamlit, Pandas, Plotly")
