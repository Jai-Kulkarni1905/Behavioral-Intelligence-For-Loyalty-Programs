import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Loyalty Intelligence",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── COLOUR PALETTE ────────────────────────────────────────────────────────────
# Approachable slate-blue theme — readable, professional, not pitch-black
BG          = "#f0f4f8"   # page background: cool light grey
CARD        = "#ffffff"   # card surface: clean white
CARD_ALT    = "#f8fafc"   # slightly off-white for alternating use
BORDER      = "#dde3ec"   # subtle border
PRIMARY     = "#4f6ef7"   # indigo-blue primary
SUCCESS     = "#16a34a"   # green
WARNING     = "#d97706"   # amber
CRITICAL    = "#dc2626"   # red
HIGH        = "#ea580c"   # orange
TEXT        = "#1e293b"   # near-black for body text
TEXT_SEC    = "#475569"   # slate-600 for secondary text
TEXT_MUTED  = "#94a3b8"   # slate-400 for labels/captions
SIDEBAR_BG  = "#1e293b"   # deep slate sidebar — premium contrast
SIDEBAR_TXT = "#e2e8f0"

PLOT_BG     = "#ffffff"
PLOT_PAPER  = "#f8fafc"
PLOT_FONT   = "#1e293b"
GRID_COLOR  = "#e2e8f0"

# ── STYLING ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    color: {TEXT};
}}

/* ── PAGE BACKGROUND ── */
.stApp {{
    background-color: {BG};
}}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {{
    background: {SIDEBAR_BG} !important;
    border-right: 1px solid #2d3f5a;
}}
section[data-testid="stSidebar"] * {{
    color: {SIDEBAR_TXT} !important;
}}
section[data-testid="stSidebar"] .stMarkdown h3 {{
    color: #ffffff !important;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.02em;
}}
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] {{
    background: #2d3f5a !important;
    border-color: #3d5275 !important;
    color: {SIDEBAR_TXT} !important;
}}
section[data-testid="stSidebar"] .stMultiSelect span {{
    color: {SIDEBAR_TXT} !important;
}}
section[data-testid="stSidebar"] label {{
    color: #94a3b8 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}}
section[data-testid="stSidebar"] hr {{
    border-color: #2d3f5a;
}}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {{
    background: {CARD};
    border-radius: 12px;
    padding: 6px;
    gap: 4px;
    border: 1px solid {BORDER};
    margin-bottom: 8px;
}}
.stTabs [data-baseweb="tab"] {{
    height: 38px;
    padding: 0 20px;
    font-size: 14px;
    font-weight: 500;
    border-radius: 8px;
    color: {TEXT_SEC} !important;
    background: transparent !important;
}}
.stTabs [aria-selected="true"] {{
    background: {PRIMARY} !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}}

/* ── METRIC CARDS ── */
.kpi-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 20px 22px 16px 22px;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    position: relative;
    overflow: hidden;
}}
.kpi-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    border-radius: 4px 0 0 4px;
}}
.kpi-card.critical::before {{ background: {CRITICAL}; }}
.kpi-card.high::before     {{ background: {HIGH}; }}
.kpi-card.warning::before  {{ background: {WARNING}; }}
.kpi-card.primary::before  {{ background: {PRIMARY}; }}
.kpi-card.success::before  {{ background: {SUCCESS}; }}

.kpi-label {{
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: {TEXT_MUTED};
    margin: 0 0 8px 0;
}}
.kpi-value {{
    font-size: 30px;
    font-weight: 700;
    color: {TEXT};
    margin: 0 0 4px 0;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1;
}}
.kpi-sub {{
    font-size: 12px;
    color: {TEXT_SEC};
    margin: 0;
}}

/* ── SECTION HEADERS ── */
.section-header {{
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: {TEXT_MUTED};
    margin: 20px 0 10px 0;
    padding-bottom: 6px;
    border-bottom: 1px solid {BORDER};
}}

/* ── PLAYBOOK CARDS ── */
.playbook-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}}
.playbook-row {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 14px;
}}
.playbook-item {{
    background: {CARD_ALT};
    border-radius: 10px;
    padding: 12px 14px;
    border: 1px solid {BORDER};
}}
.playbook-item-label {{
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: {TEXT_MUTED};
    margin-bottom: 5px;
}}
.playbook-item-value {{
    font-size: 13px;
    color: {TEXT};
    line-height: 1.5;
}}

/* ── RISK BADGES ── */
.badge {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.03em;
}}
.badge-critical {{ background: #fee2e2; color: #b91c1c; }}
.badge-high     {{ background: #ffedd5; color: #c2410c; }}
.badge-medium   {{ background: #fef3c7; color: #92400e; }}
.badge-low      {{ background: #dcfce7; color: #15803d; }}

/* ── INFO CARD ── */
.info-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}

/* ── DEFAULT STREAMLIT METRIC FIX ── */
div[data-testid="stMetric"] {{
    background: {CARD};
    border-radius: 12px;
    padding: 14px 16px;
    border: 1px solid {BORDER};
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}
div[data-testid="stMetric"] label {{
    color: {TEXT_MUTED} !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
    color: {TEXT} !important;
    font-size: 22px !important;
    font-weight: 700 !important;
}}
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {{
    color: {TEXT_SEC} !important;
}}

/* ── DATAFRAME ── */
.stDataFrame {{
    border-radius: 10px;
    border: 1px solid {BORDER};
    overflow: hidden;
}}

/* ── INPUTS ── */
.stTextInput input, .stSelectbox [data-baseweb="select"] {{
    background: {CARD} !important;
    border-color: {BORDER} !important;
    color: {TEXT} !important;
    border-radius: 8px !important;
}}

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton button {{
    background: {PRIMARY} !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 14px 20px !important;
}}
.stDownloadButton button:hover {{
    background: #3b55d4 !important;
}}

/* ── SUCCESS / INFO BOXES ── */
.stSuccess {{
    background: #f0fdf4 !important;
    border: 1px solid #bbf7d0 !important;
    border-radius: 10px !important;
    color: #166534 !important;
}}
.stInfo {{
    background: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 10px !important;
    color: #1e40af !important;
}}

/* ── PAGE HEADINGS ── */
h1, h2, h3, h4 {{
    color: {TEXT} !important;
}}
.stMarkdown h2 {{
    font-size: 20px;
    font-weight: 700;
    color: {TEXT};
    margin-bottom: 2px;
}}
.stMarkdown p {{ color: {TEXT_SEC}; }}
.stCaption {{ color: {TEXT_MUTED} !important; }}

/* ── SLIDER ── */
.stSlider [data-baseweb="slider"] {{
    color: {PRIMARY};
}}
</style>
""", unsafe_allow_html=True)

# ── REUSABLE COMPONENTS ───────────────────────────────────────────────────────
def kpi_card(title, value, subtitle, accent="primary"):
    st.markdown(f"""
    <div class="kpi-card {accent}">
        <p class="kpi-label">{title}</p>
        <p class="kpi-value">{value}</p>
        <p class="kpi-sub">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def section_header(text):
    st.markdown(f'<p class="section-header">{text}</p>', unsafe_allow_html=True)

def risk_badge(tier):
    cls = {"Critical":"badge-critical","High":"badge-high",
           "Medium":"badge-medium","Low":"badge-low"}.get(tier, "badge-low")
    return f'<span class="badge {cls}">{tier}</span>'

def info_card(content_html):
    st.markdown(f'<div class="info-card">{content_html}</div>', unsafe_allow_html=True)

def playbook_item(label, value):
    return f"""
    <div class="playbook-item">
        <div class="playbook-item-label">{label}</div>
        <div class="playbook-item-value">{value}</div>
    </div>
    """

# ── CHART DEFAULTS ────────────────────────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor=PLOT_PAPER,
    plot_bgcolor=PLOT_BG,
    font=dict(color=PLOT_FONT, family="Inter, sans-serif", size=12),
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis=dict(gridcolor=GRID_COLOR, linecolor=BORDER, tickcolor=BORDER),
    yaxis=dict(gridcolor=GRID_COLOR, linecolor=BORDER, tickcolor=BORDER),
)

# ── DATA LOADING ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    customers = pd.read_csv("customers_final.csv")
    clh = pd.read_csv("clh_cleaned.csv")
    df = customers.merge(
        clh[["Loyalty Number", "Gender", "Province", "City",
             "Loyalty Card", "Education", "Marital Status", "Enrollment Type"]],
        on="Loyalty Number", how="left"
    )
    priority_map = {
        'Silent Enrollees':       'Urgent — Onboarding failure',
        'Reward Maximizers':      'Urgent — High engagement, at risk',
        'Rising Seasonal Flyers': 'High — Convert before next off-season',
        'Occasional Travelers':   'Medium — Frequency building',
        'Loyal Regulars':         'Maintain — Unlock redemption behavior'
    }
    if 'Retention_Priority' not in df.columns:
        df['Retention_Priority'] = df['Segment_Name'].map(priority_map)
    df["Churn_Risk_Tier"] = pd.Categorical(
        df["Churn_Risk_Tier"], categories=["Low", "Medium", "High", "Critical"], ordered=True
    )
    df["Churn_Pct"] = (df["Churn_Probability"] * 100).round(1)
    return df

df = load_data()

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
SEG_COLORS = {
    "Loyal Regulars":         "#16a34a",
    "Occasional Travelers":   "#4f6ef7",
    "Rising Seasonal Flyers": "#d97706",
    "Silent Enrollees":       "#dc2626",
    "Reward Maximizers":      "#7c3aed"
}
RISK_COLORS = {"Low": "#16a34a", "Medium": "#d97706", "High": "#ea580c", "Critical": "#dc2626"}

PLAYBOOKS = {
    "Loyal Regulars": {
        "headline": "Unlock redemption behaviour — your best flyers aren't using their points",
        "who": "6,241 members • 2.7% churn rate • fly 8/12 months on average",
        "trigger": "Points balance exceeds 15,000 with no redemption in 3+ months",
        "action": "Personalised email showing exact redemption options for their top 3 routes with a one-click booking link. Subject line: 'You have enough points for a free flight to [CITY]'",
        "timing": "Automated trigger — fires when 3 consecutive months pass without redemption",
        "goal": "15% first-redemption activation rate"
    },
    "Silent Enrollees": {
        "headline": "Activate before permanent disengagement — 71% flew in 2018 with no push at all",
        "who": "2,418 members • 29% churn rate • enrolled ~12 months ago, zero 2017 flights",
        "trigger": "Member enrolled 90+ days ago with zero flights booked",
        "action": "5× points on first flight, offer valid 60 days. Add hard deadline for urgency. For members enrolled 12+ months with still-zero flights: deeper offer or accept as lost.",
        "timing": "Month 3 post-enrollment if no flight booked",
        "goal": "Convert 20% to first-flight activation"
    },
    "Rising Seasonal Flyers": {
        "headline": "Bridge the off-season gap before H1 activity collapses",
        "who": "1,350 members • 18.9% churn • 6.5× activity increase in H2 2017 but near-zero H1",
        "trigger": "February — 6 weeks before typical H1 silence begins",
        "action": "Double miles on any route January–May. Show their H2 2017 flight history and calculate what they could redeem if they fly 2 off-season trips.",
        "timing": "Proactive in February — do NOT wait for inactivity to trigger this",
        "goal": "1 additional off-season flight per member"
    },
    "Occasional Travelers": {
        "headline": "Nudge casual flyers toward frequency with status progression",
        "who": "4,708 members • 10.3% churn • fly ~6 months per year, moderate tenure",
        "trigger": "2 consecutive months without a flight",
        "action": "'Fly 2 more times before June and reach Silver status.' Show their progress bar. Route-specific bonus on destinations they've flown before.",
        "timing": "Reactive — only trigger after 2-month gap, not proactively",
        "goal": "Increase active months from 5.8 to 7+ per year"
    },
    "Reward Maximizers": {
        "headline": "Retain your highest programme-engaged members — they understand loyalty better than anyone",
        "who": "133 members • 24.8% churn • 19% redemption rate (10× others), growing activity",
        "trigger": "Churn probability > 25%",
        "action": "Personal phone outreach — not email. Exclusive early redemption access. Status upgrade offer: 4 flights in the next 6 months locks in Gold tier for 12 months.",
        "timing": "Quarterly review — small segment, manual outreach is feasible",
        "goal": "Reduce 24.8% churn rate below 15%"
    }
}

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✈  Loyalty Intelligence")
    st.markdown("<p style='font-size:12px;color:#64748b;margin-top:-8px;'>Retention Analytics Platform</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("<p style='font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#64748b;margin-bottom:8px;'>Filters</p>", unsafe_allow_html=True)

    seg_filter = st.multiselect(
        "Segment",
        options=df["Segment_Name"].unique().tolist(),
        default=df["Segment_Name"].unique().tolist()
    )
    risk_filter = st.multiselect(
        "Churn Risk Tier",
        options=["Critical", "High", "Medium", "Low"],
        default=["Critical", "High", "Medium", "Low"]
    )
    tier_filter = st.multiselect(
        "Loyalty Card",
        options=sorted(df["Loyalty Card"].dropna().unique().tolist()),
        default=sorted(df["Loyalty Card"].dropna().unique().tolist())
    )
    province_filter = st.multiselect(
        "Province",
        options=sorted(df["Province"].dropna().unique().tolist()),
        default=sorted(df["Province"].dropna().unique().tolist())
    )

    st.markdown("---")
    st.markdown("<p style='font-size:11px;color:#64748b;'>Dataset: 14,850 customers · 2017–2018</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px;color:#64748b;'>Model: XGBoost · AUC = 0.91</p>", unsafe_allow_html=True)

# Apply filters
filtered = df[
    df["Segment_Name"].isin(seg_filter) &
    df["Churn_Risk_Tier"].isin(risk_filter) &
    df["Loyalty Card"].isin(tier_filter) &
    df["Province"].isin(province_filter)
].copy()

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊  Command Center", "🎯  Segment Playbooks", "🔍  Customer Lookup", "📥  Export List"]
)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — COMMAND CENTER
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("## Command Center")
    st.caption("Real-time view of retention risk across the loyalty base.")

    total      = len(filtered)
    critical   = (filtered["Churn_Risk_Tier"] == "Critical").sum()
    high_risk  = (filtered["Churn_Risk_Tier"] == "High").sum()
    urgent_now = (filtered["Churn_Probability"] >= 0.45).sum()
    avg_prob   = filtered["Churn_Probability"].mean()

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        kpi_card("Total Customers", f"{total:,}", "Filtered loyalty base", "primary")
    with c2:
        kpi_card("Critical Risk", f"{critical:,}", f"{critical/total*100:.1f}% of loyalty base", "critical")
    with c3:
        kpi_card("High Risk", f"{high_risk:,}", f"{high_risk/total*100:.1f}% of loyalty base", "high")
    with c4:
        kpi_card("Action Needed Now", f"{urgent_now:,}", "Churn probability > 45%", "warning")
    with c5:
        kpi_card("Avg Churn Probability", f"{avg_prob:.1%}", "Across filtered base", "success")

    st.markdown("---")
    left, right = st.columns([1.4, 1])

    with left:
        section_header("Customers Needing Immediate Attention")
        priority_df = (filtered[filtered["Churn_Risk_Tier"].isin(["Critical", "High"])]
                       .sort_values("Churn_Probability", ascending=False)
                       [["Loyalty Number", "Segment_Name", "Loyalty Card",
                         "Province", "Churn_Pct", "Churn_Risk_Tier",
                         "Active_Months_2017", "Recency_Last_Flight",
                         "Retention_Priority"]]
                       .rename(columns={
                           "Loyalty Number":      "ID",
                           "Segment_Name":        "Segment",
                           "Loyalty Card":        "Card",
                           "Churn_Pct":           "Churn Risk %",
                           "Churn_Risk_Tier":     "Tier",
                           "Active_Months_2017":  "Active Months",
                           "Recency_Last_Flight": "Months Since Last Flight",
                           "Retention_Priority":  "Priority"
                       })
                       .head(200))

        def color_tier(val):
            colors = {"Critical": "background-color:#fee2e2;color:#b91c1c;font-weight:600",
                      "High":     "background-color:#ffedd5;color:#c2410c;font-weight:600"}
            return colors.get(val, "")

        st.dataframe(
            priority_df.style.map(color_tier, subset=["Tier"]),
            height=380, use_container_width=True
        )

    with right:
        section_header("Risk Distribution by Segment")
        risk_seg = (filtered.groupby(["Segment_Name", "Churn_Risk_Tier"])
                            .size().reset_index(name="Count"))
        fig_risk = px.bar(
            risk_seg, x="Count", y="Segment_Name",
            color="Churn_Risk_Tier", orientation="h",
            color_discrete_map=RISK_COLORS,
            category_orders={"Churn_Risk_Tier": ["Critical","High","Medium","Low"]},
            height=380
        )
        fig_risk.update_layout(
            **CHART_LAYOUT,
            legend_title="Risk Tier",
            xaxis_title="Customers",
            yaxis_title="",
            legend=dict(orientation="h", y=-0.18, font=dict(size=11))
        )
        fig_risk.update_traces(marker_line_width=0)
        st.plotly_chart(fig_risk, use_container_width=True)

    st.markdown("---")
    l2, r2 = st.columns(2)

    with l2:
        section_header("Churn Probability Distribution")
        fig_hist = px.histogram(
            filtered, x="Churn_Probability", nbins=50,
            color="Segment_Name", color_discrete_map=SEG_COLORS,
            opacity=0.80, height=300
        )
        fig_hist.add_vline(x=0.45, line_dash="dash", line_color=CRITICAL,
                           annotation_text="Action threshold (45%)",
                           annotation_font_color=CRITICAL)
        fig_hist.update_layout(
            **CHART_LAYOUT,
            xaxis_title="Churn Probability",
            yaxis_title="Customers",
            showlegend=False
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with r2:
        section_header("Segment Overview")
        seg_summary = (filtered.groupby("Segment_Name").agg(
            Customers    = ("Loyalty Number",    "count"),
            Churn_Rate   = ("Churned",           "mean"),
            Avg_Flights  = ("Total_Flights_2017","mean"),
            Avg_Recency  = ("Recency_Last_Flight","mean"),
            Avg_CLV      = ("CLV",               "mean")
        ).reset_index().sort_values("Churn_Rate", ascending=False))
        seg_summary["Churn Rate"] = (seg_summary["Churn_Rate"]*100).round(1).astype(str) + "%"
        seg_summary["Avg Flights"] = seg_summary["Avg_Flights"].round(1)
        seg_summary["Avg CLV"]     = "$" + seg_summary["Avg_CLV"].round(0).astype(int).astype(str)
        st.dataframe(
            seg_summary[["Segment_Name","Customers","Churn Rate","Avg Flights","Avg CLV"]]
            .rename(columns={"Segment_Name":"Segment"}),
            height=300, use_container_width=True, hide_index=True
        )

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — SEGMENT PLAYBOOKS
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("## Segment Playbooks")
    st.caption("Select a segment to see the behavioural profile and recommended retention action.")

    selected_seg = st.selectbox(
        "Select segment", options=list(SEG_COLORS.keys()), label_visibility="collapsed"
    )

    seg_data = filtered[filtered["Segment_Name"] == selected_seg]
    pb       = PLAYBOOKS[selected_seg]
    seg_col  = SEG_COLORS[selected_seg]

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        kpi_card("Customers", f"{len(seg_data):,}", "In this segment", "primary")
    with m2:
        kpi_card("Churn Rate", f"{seg_data['Churned'].mean()*100:.1f}%", "Historical churn", "critical")
    with m3:
        kpi_card("Avg Churn Probability", f"{seg_data['Churn_Probability'].mean():.1%}", "Model score", "warning")
    with m4:
        kpi_card("Avg Active Months", f"{seg_data['Active_Months_2017'].mean():.1f} / 12", "Engagement level", "success")

    # Headline banner
    st.markdown(f"""
    <div style="background:{seg_col}12;border:1px solid {seg_col}40;border-left:4px solid {seg_col};
                border-radius:12px;padding:14px 18px;margin:12px 0 16px 0;">
        <p style="font-size:15px;font-weight:600;color:{seg_col};margin:0 0 2px 0;">{selected_seg}</p>
        <p style="font-size:13px;color:{TEXT_SEC};margin:0;">{pb['headline']}</p>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        section_header("Playbook Details")
        st.markdown(f"""
        <div class="playbook-card">
            <div class="playbook-row">
                {playbook_item("Who this covers", pb['who'])}
                {playbook_item("Trigger condition", pb['trigger'])}
            </div>
            <div class="playbook-row">
                {playbook_item("Timing", pb['timing'])}
                {playbook_item("Target outcome", pb['goal'])}
            </div>
        </div>
        """, unsafe_allow_html=True)

        section_header("Recommended Action")
        st.markdown(f"""
        <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-left:4px solid {SUCCESS};
                    border-radius:12px;padding:14px 18px;">
            <p style="font-size:13px;color:#166534;margin:0;line-height:1.6;">{pb['action']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        section_header("Behavioural Profile vs Rest of Base")
        compare_cols   = ["Active_Months_2017","Recency_Last_Flight",
                          "Redemption_Rate_2017","Flight_Trend_Pct","Tenure_Months"]
        compare_labels = ["Active Months","Recency","Redemption Rate","Flight Trend","Tenure"]

        seg_means  = seg_data[compare_cols].mean().values
        base_means = filtered[compare_cols].mean().values

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=seg_means / (base_means + 1e-9),
            theta=compare_labels, fill="toself",
            name=selected_seg, line_color=seg_col,
            fillcolor=seg_col 
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[1]*len(compare_labels), theta=compare_labels,
            fill="toself", name="Base average",
            line_color=TEXT_MUTED, line_dash="dash",
            fillcolor=TEXT_MUTED 
        ))
        fig_radar.update_layout(
            paper_bgcolor=PLOT_PAPER,
            plot_bgcolor=PLOT_BG,
            font=dict(color=PLOT_FONT, family="Inter, sans-serif", size=11),
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 3], gridcolor=GRID_COLOR, tickfont=dict(size=10)),
                angularaxis=dict(gridcolor=GRID_COLOR),
                bgcolor=PLOT_BG
            ),
            showlegend=True,
            height=320,
            margin=dict(l=30, r=30, t=30, b=30),
            legend=dict(font=dict(size=11))
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")
    section_header(f"Member List — {selected_seg}  ({len(seg_data):,} customers)")
    display_seg = (seg_data.sort_values("Churn_Probability", ascending=False)
                   [["Loyalty Number","Loyalty Card","Province","Gender",
                     "Churn_Pct","Churn_Risk_Tier","Active_Months_2017",
                     "Recency_Last_Flight","Redemption_Rate_2017","Total_Flights_2017"]]
                   .rename(columns={
                       "Loyalty Number":      "ID",
                       "Loyalty Card":        "Card",
                       "Churn_Pct":           "Churn %",
                       "Churn_Risk_Tier":     "Risk",
                       "Active_Months_2017":  "Active Mo.",
                       "Recency_Last_Flight": "Recency",
                       "Redemption_Rate_2017":"Redeem Rate",
                       "Total_Flights_2017":  "Flights 2017"
                   }))
    st.dataframe(display_seg, height=350, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CUSTOMER LOOKUP
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("## Customer Lookup")
    st.caption("Search any member to see their behavioural profile and recommended action.")

    search_id = st.text_input("Enter Loyalty Number", placeholder="e.g. 482922")

    if search_id:
        try:
            cid  = int(search_id.strip())
            row  = df[df["Loyalty Number"] == cid]
            if row.empty:
                st.error("Loyalty Number not found.")
            else:
                r = row.iloc[0]
                seg_avg = df[df["Segment_Name"] == r["Segment_Name"]]
                risk_col = RISK_COLORS.get(r["Churn_Risk_Tier"], "#6b7280")
                badge_cls = {"Critical":"badge-critical","High":"badge-high",
                             "Medium":"badge-medium","Low":"badge-low"}.get(r["Churn_Risk_Tier"],"badge-low")
                seg_col_c = SEG_COLORS.get(r["Segment_Name"], PRIMARY)

                # Customer profile header card
                st.markdown(f"""
                <div style="background:{CARD};border:1px solid {BORDER};border-radius:16px;
                            padding:20px 24px;margin-bottom:16px;
                            box-shadow:0 2px 8px rgba(0,0,0,0.06);
                            border-top:4px solid {risk_col};">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                        <div>
                            <p style="font-size:13px;color:{TEXT_MUTED};font-weight:600;
                                      text-transform:uppercase;letter-spacing:0.07em;margin:0 0 4px 0;">
                                Loyalty Member #{cid}
                            </p>
                            <p style="font-size:22px;font-weight:700;color:{TEXT};margin:0 0 8px 0;">
                                {r.get('Loyalty Card','—')} Card · {r.get('Province','—')}
                            </p>
                            <span class="badge {badge_cls}">{r['Churn_Risk_Tier']} Risk</span>
                            &nbsp;
                            <span style="display:inline-block;padding:3px 10px;border-radius:20px;
                                         font-size:12px;font-weight:600;
                                         background:{seg_col_c}18;color:{seg_col_c};">
                                {r['Segment_Name']}
                            </span>
                        </div>
                        <div style="text-align:right;">
                            <p style="font-size:13px;color:{TEXT_MUTED};margin:0 0 4px 0;">Churn Probability</p>
                            <p style="font-size:32px;font-weight:700;color:{risk_col};
                                      font-family:'JetBrains Mono',monospace;margin:0;">
                                {r['Churn_Pct']:.1f}%
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)
                with col1:
                    section_header("Behavioural Signals")
                    st.metric("Flights in 2017",         int(r["Total_Flights_2017"]))
                    st.metric("Active months",            int(r["Active_Months_2017"]))
                    st.metric("Months since last flight", int(r["Recency_Last_Flight"]))
                with col2:
                    section_header("Loyalty Engagement")
                    st.metric("Points earned 2017",  f"{int(r['Points_Earned_2017']):,}")
                    st.metric("Redemption rate",      f"{r['Redemption_Rate_2017']:.1%}")
                    st.metric("Flight trend (H1→H2)", f"{r['Flight_Trend_Pct']:+.2f}")
                with col3:
                    section_header("Profile")
                    st.metric("Tenure",           f"{int(r['Tenure_Months'])} months")
                    st.metric("CLV",              f"${r['CLV']:,.0f}")
                    st.metric("Seasonality Index", f"{r['Seasonality_Index']:.2f}")

                st.markdown("---")
                pb_cust = PLAYBOOKS[r["Segment_Name"]]
                section_header("Recommended Action")
                st.markdown(f"""
                <div style="background:#f0fdf4;border:1px solid #bbf7d0;
                            border-left:4px solid {SUCCESS};border-radius:12px;
                            padding:14px 18px;margin-bottom:8px;">
                    <p style="font-size:14px;color:#166534;margin:0;line-height:1.6;">
                        {pb_cust['action']}
                    </p>
                </div>
                <p style="font-size:12px;color:{TEXT_MUTED};margin:4px 0 0 4px;">
                    Trigger: {pb_cust['trigger']} &nbsp;|&nbsp; Timing: {pb_cust['timing']}
                </p>
                """, unsafe_allow_html=True)

                st.markdown("---")
                section_header("Comparison vs Segment Average")
                compare_metrics = {
                    "Active Months":   ("Active_Months_2017",   int(r["Active_Months_2017"]),  int(seg_avg["Active_Months_2017"].mean())),
                    "Recency":         ("Recency_Last_Flight",  int(r["Recency_Last_Flight"]),  int(seg_avg["Recency_Last_Flight"].mean())),
                    "Redemption Rate": ("Redemption_Rate_2017", f"{r['Redemption_Rate_2017']:.1%}", f"{seg_avg['Redemption_Rate_2017'].mean():.1%}"),
                    "Flights":         ("Total_Flights_2017",   int(r["Total_Flights_2017"]),   int(seg_avg["Total_Flights_2017"].mean()))
                }
                cc = st.columns(len(compare_metrics))
                for i, (label, (_, cval, savg)) in enumerate(compare_metrics.items()):
                    cc[i].metric(label, cval, f"Seg avg: {savg}")

        except ValueError:
            st.error("Please enter a valid numeric Loyalty Number.")
    else:
        st.info("Enter a Loyalty Number above to look up any customer.")
        st.markdown("#### Quick-access: top 10 highest-risk customers")
        top10 = (df.sort_values("Churn_Probability", ascending=False)
                   .head(10)
                   [["Loyalty Number","Segment_Name","Loyalty Card",
                     "Province","Churn_Pct","Churn_Risk_Tier","Retention_Priority"]]
                   .rename(columns={
                       "Loyalty Number":   "ID",
                       "Segment_Name":     "Segment",
                       "Loyalty Card":     "Card",
                       "Churn_Pct":        "Churn %",
                       "Churn_Risk_Tier":  "Risk",
                       "Retention_Priority":"Priority"
                   }))
        st.dataframe(top10, hide_index=True, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("## Export Campaign List")
    st.caption("Download a filtered list of customers for your CRM or email platform.")

    e1, e2 = st.columns(2)
    with e1:
        export_seg  = st.multiselect("Segments to include",
                        options=list(SEG_COLORS.keys()),
                        default=["Silent Enrollees","Reward Maximizers"])
        export_risk = st.multiselect("Minimum risk tier",
                        options=["Critical","High","Medium","Low"],
                        default=["Critical","High"])
    with e2:
        min_prob = st.slider("Minimum churn probability", 0.0, 1.0, 0.20, 0.05)
        card_sel = st.multiselect("Loyalty card filter",
                    options=sorted(df["Loyalty Card"].dropna().unique()),
                    default=sorted(df["Loyalty Card"].dropna().unique()))

    export_df = df[
        df["Segment_Name"].isin(export_seg) &
        df["Churn_Risk_Tier"].isin(export_risk) &
        (df["Churn_Probability"] >= min_prob) &
        df["Loyalty Card"].isin(card_sel)
    ].sort_values("Churn_Probability", ascending=False)

    # Campaign summary row
    st.markdown("---")
    section_header("Campaign Summary")
    s1, s2, s3 = st.columns(3)
    with s1:
        kpi_card("Customers Matched", f"{len(export_df):,}", "Ready for export", "primary")
    with s2:
        clv_at_risk = export_df["CLV"].sum()
        kpi_card("CLV at Risk", f"${clv_at_risk:,.0f}", "Total customer lifetime value", "critical")
    with s3:
        if len(export_df):
            top_risk_pct = (export_df["Churn_Risk_Tier"].isin(["Critical","High"])).mean() * 100
            kpi_card("High/Critical Mix", f"{top_risk_pct:.0f}%", "Of matched customers", "warning")
        else:
            kpi_card("High/Critical Mix", "—", "No customers matched", "warning")

    st.markdown("---")

    export_cols = ["Loyalty Number","Segment_Name","Retention_Priority",
                   "Churn_Pct","Churn_Risk_Tier","Loyalty Card","Province",
                   "Active_Months_2017","Recency_Last_Flight",
                   "Redemption_Rate_2017","Total_Flights_2017","CLV"]
    out = export_df[export_cols].rename(columns={
        "Loyalty Number":      "loyalty_number",
        "Segment_Name":        "segment",
        "Retention_Priority":  "retention_priority",
        "Churn_Pct":           "churn_probability_pct",
        "Churn_Risk_Tier":     "risk_tier",
        "Loyalty Card":        "loyalty_card",
        "Active_Months_2017":  "active_months_2017",
        "Recency_Last_Flight": "months_since_last_flight",
        "Redemption_Rate_2017":"redemption_rate",
        "Total_Flights_2017":  "total_flights_2017"
    })

    st.dataframe(out.head(50), hide_index=True, use_container_width=True)
    if len(out) > 50:
        st.caption(f"Showing first 50 of {len(out):,}. Full list included in download.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        label=f"⬇  Download full list  ({len(out):,} customers)",
        data=out.to_csv(index=False),
        file_name="retention_campaign_list.csv",
        mime="text/csv",
        use_container_width=True
    )
