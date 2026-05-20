import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# Page Config
# =====================================================
st.set_page_config(
    page_title="Korea Global Trade Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# Custom CSS
# =====================================================
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top left, #10284f 0%, #07111f 35%, #020617 100%);
        color: #e5eefc;
    }

    section[data-testid="stSidebar"] {
        background: rgba(5, 15, 30, 0.9);
        border-right: 1px solid rgba(100, 180, 255, 0.25);
    }

    .main-title {
        font-size: 46px;
        font-weight: 800;
        background: linear-gradient(90deg, #7dd3fc, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }

    .sub-title {
        color: #b8c7e0;
        font-size: 18px;
        margin-bottom: 30px;
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
# Sample Data
# Replace these with OECD / World Bank / KITA data later
# =====================================================

trade_partners = pd.DataFrame({
    "country": ["China", "United States", "Vietnam", "Japan", "Taiwan", "Germany", "Singapore", "India", "Mexico", "Australia"],
    "iso_alpha": ["CHN", "USA", "VNM", "JPN", "TWN", "DEU", "SGP", "IND", "MEX", "AUS"],
    "export_usd_billion": [124.8, 115.7, 53.5, 29.0, 28.4, 11.2, 18.7, 18.0, 12.3, 17.8],
    "import_usd_billion": [142.9, 71.3, 26.7, 47.6, 23.1, 23.7, 12.4, 8.9, 7.1, 33.2],
    "region": ["Asia", "North America", "Asia", "Asia", "Asia", "Europe", "Asia", "Asia", "North America", "Oceania"]
})
trade_partners["total_trade"] = trade_partners["export_usd_billion"] + trade_partners["import_usd_billion"]
trade_partners["balance"] = trade_partners["export_usd_billion"] - trade_partners["import_usd_billion"]

trade_timeline = pd.DataFrame({
    "year": list(range(2014, 2025)),
    "exports": [573, 527, 495, 573, 605, 542, 512, 644, 683, 632, 683],
    "imports": [526, 436, 406, 478, 535, 503, 467, 615, 731, 642, 632],
})
trade_timeline["trade_balance"] = trade_timeline["exports"] - trade_timeline["imports"]
trade_timeline["total_trade"] = trade_timeline["exports"] + trade_timeline["imports"]

industries = pd.DataFrame({
    "industry": ["Semiconductors", "Automobiles", "Petrochemicals", "Batteries", "Ships", "Steel", "Displays", "Machinery", "IT Devices"],
    "export_value": [129, 71, 54, 38, 22, 31, 20, 53, 46],
    "dependency_level": ["High", "Medium", "Medium", "High", "Medium", "Medium", "High", "Medium", "High"],
    "main_partners": ["China / Taiwan / USA", "USA / EU", "China / ASEAN", "USA / EU / China", "Europe / Middle East", "China / Japan", "China / Vietnam", "USA / China", "China / Vietnam"]
})

OECD_SAMPLE = pd.DataFrame({
    "country": ["Korea", "Germany", "Japan", "United States", "Netherlands", "France", "Mexico", "Canada"],
    "trade_dependency": [85, 89, 45, 27, 156, 66, 83, 68],
    "gvc_participation": [56, 52, 41, 38, 61, 45, 49, 46],
    "service_trade_ratio": [18, 24, 21, 31, 33, 29, 15, 20],
    "fdi_connectivity": [62, 68, 48, 76, 85, 64, 59, 66],
    "manufacturing_share": [27, 19, 20, 11, 10, 10, 18, 10]
})

supply_chain = pd.DataFrame({
    "source": ["Korea", "Korea", "Korea", "Japan", "Taiwan", "China", "Vietnam", "Korea", "USA"],
    "target": ["China", "USA", "Vietnam", "Korea", "Korea", "USA", "USA", "EU", "Korea"],
    "value": [35, 28, 20, 14, 12, 26, 18, 21, 16],
    "category": ["Semiconductors", "Automobiles", "Electronics", "Materials", "Chips", "Final Goods", "Assembly", "Batteries", "Technology"]
})

fdi_data = pd.DataFrame({
    "year": list(range(2016, 2025)),
    "inflow": [10, 12, 17, 13, 11, 19, 18, 15, 16],
    "outflow": [27, 31, 38, 35, 32, 44, 52, 48, 50]
})

service_trade = pd.DataFrame({
    "category": ["Transport", "IT Services", "Travel", "Finance", "IP Royalties", "Other Business Services"],
    "value": [28, 22, 14, 11, 9, 16]
})

# =====================================================
# Sidebar
# =====================================================
st.sidebar.title("🌐 Dashboard Control")
st.sidebar.caption("Korea Global Trade Position Dashboard")

selected_year = st.sidebar.slider("Select Year", 2014, 2024, 2024)
selected_region = st.sidebar.multiselect(
    "Select Region",
    options=trade_partners["region"].unique(),
    default=list(trade_partners["region"].unique())
)
selected_industries = st.sidebar.multiselect(
    "Select Export Industries",
    options=industries["industry"].tolist(),
    default=industries["industry"].tolist()[:5]
)
selected_country = st.sidebar.selectbox(
    "OECD Country Comparison",
    options=[c for c in OECD_SAMPLE["country"] if c != "Korea"]
)

filtered_trade = trade_partners[trade_partners["region"].isin(selected_region)]
filtered_industries = industries[industries["industry"].isin(selected_industries)]

# =====================================================
# Header
# =====================================================
st.markdown('<h1 class="main-title">Korea Global Trade Position Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Understanding Korea’s Role in the Global Economy Through Data Visualization</p>', unsafe_allow_html=True)

# =====================================================
# Top Metrics
# =====================================================
metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Trade</div>
        <div class="metric-value">${filtered_trade['total_trade'].sum():.1f}B</div>
    </div>
    """, unsafe_allow_html=True)
with metric2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Export Value</div>
        <div class="metric-value">${filtered_trade['export_usd_billion'].sum():.1f}B</div>
    </div>
    """, unsafe_allow_html=True)
with metric3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Import Value</div>
        <div class="metric-value">${filtered_trade['import_usd_billion'].sum():.1f}B</div>
    </div>
    """, unsafe_allow_html=True)
with metric4:
    korea_gvc = OECD_SAMPLE.loc[OECD_SAMPLE["country"] == "Korea", "gvc_participation"].iloc[0]
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Korea GVC Participation</div>
        <div class="metric-value">{korea_gvc}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# Tabs
# =====================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📌 Overview",
    "🗺️ Trade Network",
    "📈 Trade Timeline",
    "🏭 Industry Analysis",
    "🔗 GVC & Supply Chain",
    "🌍 OECD Comparison",
    "💰 FDI & Services"
])

# =====================================================
# Tab 1: Overview
# =====================================================
with tab1:
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("""
        <div class="glass-card">
        <h3>Project Direction</h3>
        <p>
        This dashboard visualizes Korea’s position within the global economy and international supply chains.
        Rather than simply presenting trade statistics, it focuses on Korea’s economic connections,
        trade dependency, GVC participation, and industrial structure.
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
        <h3>Core Questions</h3>
        <ul>
            <li>Which countries is Korea most economically connected to?</li>
            <li>How dependent is Korea on global trade?</li>
            <li>What role does Korea play in global value chains?</li>
            <li>How has Korea’s trade structure evolved over time?</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'><h3>Core Keywords</h3>", unsafe_allow_html=True)
        keywords = [
            "Global Trade", "Korea Economy", "GVC", "OECD Comparison",
            "Supply Chain", "Trade Dependency", "Data Visualization", "Interactive Dashboard"
        ]
        keyword_html = "".join([f"<span class='keyword-pill'>{k}</span>" for k in keywords])
        st.markdown(keyword_html + "</div>", unsafe_allow_html=True)

        fig_overview = px.bar(
            trade_partners.sort_values("total_trade", ascending=False),
            x="country",
            y="total_trade",
            title="Korea's Major Trading Partners",
            labels={"total_trade": "Total Trade, USD Billion", "country": "Country"}
        )
        fig_overview.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_overview, use_container_width=True)

# =====================================================
# Tab 2: Trade Network
# =====================================================
with tab2:
    st.subheader("Global Trade Network Map")
    st.caption("This map shows Korea’s major trade partners. Larger markers indicate larger trade volume.")

    fig_map = px.choropleth(
        filtered_trade,
        locations="iso_alpha",
        color="total_trade",
        hover_name="country",
        hover_data={"export_usd_billion": True, "import_usd_billion": True, "balance": True},
        color_continuous_scale="Blues",
        title="Korea's Global Trade Connections"
    )
    fig_map.update_layout(template="plotly_dark", geo=dict(bgcolor="rgba(0,0,0,0)"), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_map, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_export = px.bar(filtered_trade.sort_values("export_usd_billion", ascending=True), x="export_usd_billion", y="country", orientation="h", title="Exports by Partner")
        fig_export.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_export, use_container_width=True)
    with col2:
        fig_import = px.bar(filtered_trade.sort_values("import_usd_billion", ascending=True), x="import_usd_billion", y="country", orientation="h", title="Imports by Partner")
        fig_import.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_import, use_container_width=True)

# =====================================================
# Tab 3: Timeline
# =====================================================
with tab3:
    st.subheader("Trade Trend Timeline")

    chart_option = st.radio("Select timeline view", ["Exports & Imports", "Trade Balance", "Total Trade"], horizontal=True)

    if chart_option == "Exports & Imports":
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=trade_timeline["year"], y=trade_timeline["exports"], mode="lines+markers", name="Exports"))
        fig_line.add_trace(go.Scatter(x=trade_timeline["year"], y=trade_timeline["imports"], mode="lines+markers", name="Imports"))
        fig_line.update_layout(title="Korea Export and Import Trends", template="plotly_dark", yaxis_title="USD Billion")
    elif chart_option == "Trade Balance":
        fig_line = px.bar(trade_timeline, x="year", y="trade_balance", title="Korea Trade Balance")
        fig_line.update_layout(template="plotly_dark", yaxis_title="USD Billion")
    else:
        fig_line = px.area(trade_timeline, x="year", y="total_trade", title="Total Trade Volume")
        fig_line.update_layout(template="plotly_dark", yaxis_title="USD Billion")

    fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("""
    <div class="glass-card">
    <h3>Historical Context</h3>
    <p><b>COVID-19:</b> Global demand and logistics disruptions affected Korea's export industries.</p>
    <p><b>Semiconductor Boom:</b> Korea’s export performance is highly sensitive to semiconductor cycles.</p>
    <p><b>US-China Conflict:</b> Korea is positioned between major economic blocs, increasing supply chain uncertainty.</p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# Tab 4: Industry Analysis
# =====================================================
with tab4:
    st.subheader("Export Product & Industrial Structure Analysis")

    col1, col2 = st.columns([1.2, 1])
    with col1:
        fig_tree = px.treemap(
            filtered_industries,
            path=["dependency_level", "industry"],
            values="export_value",
            title="Korea Major Export Industries"
        )
        fig_tree.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_tree, use_container_width=True)

    with col2:
        fig_industry_bar = px.bar(
            filtered_industries.sort_values("export_value", ascending=True),
            x="export_value",
            y="industry",
            orientation="h",
            title="Export Value by Industry"
        )
        fig_industry_bar.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_industry_bar, use_container_width=True)

    st.dataframe(filtered_industries, use_container_width=True)

# =====================================================
# Tab 5: GVC & Supply Chain
# =====================================================
with tab5:
    st.subheader("GVC & Supply Chain Flow")

    labels = list(pd.unique(supply_chain[["source", "target"]].values.ravel("K")))
    label_index = {label: i for i, label in enumerate(labels)}

    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(
            pad=18,
            thickness=18,
            line=dict(color="rgba(255,255,255,0.3)", width=0.5),
            label=labels,
        ),
        link=dict(
            source=supply_chain["source"].map(label_index),
            target=supply_chain["target"].map(label_index),
            value=supply_chain["value"],
            label=supply_chain["category"]
        )
    )])
    fig_sankey.update_layout(title_text="Simplified Global Supply Chain Flow", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_sankey, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="glass-card">
        <h3>Forward Participation</h3>
        <p>Korea’s domestic value added is used by other countries to produce final goods.</p>
        <p><b>Example:</b> Korean semiconductor → Chinese assembly → US consumer market.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="glass-card">
        <h3>Backward Participation</h3>
        <p>Korea uses foreign intermediate goods to produce its exports.</p>
        <p><b>Example:</b> Japanese materials → Korean production → global export.</p>
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# Tab 6: OECD Comparison
# =====================================================
with tab6:
    st.subheader("Korea vs OECD Comparison")

    comparison_df = OECD_SAMPLE[OECD_SAMPLE["country"].isin(["Korea", selected_country])]

    categories = ["trade_dependency", "gvc_participation", "service_trade_ratio", "fdi_connectivity", "manufacturing_share"]

    fig_radar = go.Figure()
    for _, row in comparison_df.iterrows():
        fig_radar.add_trace(go.Scatterpolar(
            r=[row[c] for c in categories],
            theta=categories,
            fill="toself",
            name=row["country"]
        ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        template="plotly_dark",
        title=f"Korea vs {selected_country}: Economic Positioning",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    fig_oecd_bar = px.bar(
        OECD_SAMPLE.sort_values("trade_dependency", ascending=False),
        x="country",
        y="trade_dependency",
        title="Trade Dependency by OECD Sample Countries"
    )
    fig_oecd_bar.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_oecd_bar, use_container_width=True)

# =====================================================
# Tab 7: FDI & Services
# =====================================================
with tab7:
    st.subheader("FDI & Service Trade")

    col1, col2 = st.columns(2)
    with col1:
        fig_fdi = go.Figure()
        fig_fdi.add_trace(go.Scatter(x=fdi_data["year"], y=fdi_data["inflow"], mode="lines+markers", name="FDI Inflow"))
        fig_fdi.add_trace(go.Scatter(x=fdi_data["year"], y=fdi_data["outflow"], mode="lines+markers", name="FDI Outflow"))
        fig_fdi.update_layout(title="Korea FDI Inflow / Outflow", template="plotly_dark", yaxis_title="USD Billion", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_fdi, use_container_width=True)

    with col2:
        fig_service = px.pie(service_trade, names="category", values="value", title="Service Trade Composition")
        fig_service.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_service, use_container_width=True)

    st.markdown("""
    <div class="glass-card">
    <h3>Final Insight</h3>
    <p>
    Korea is not only an export-driven economy but also a highly connected node in global value chains.
    Its future strategy depends on diversifying trade partners, strengthening high-value industries,
    and reducing supply chain vulnerability.
    </p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# Footer
# =====================================================
st.markdown("---")
st.caption("Data note: This version uses sample data for prototyping. Replace with OECD, World Bank, KITA, or UN Comtrade data for final submission.")
st.caption("Built with Python, Streamlit, Pandas, and Plotly.")
