from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu

# Force every Plotly chart in the dashboard to use the dark theme.
px.defaults.template = "plotly_dark"


def apply_dark_plotly(fig):
    """Force Plotly figures to remain dark regardless of the browser/Streamlit theme."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#020617",
        plot_bgcolor="#0f172a",
        font=dict(color="#f8fafc"),
        title_font=dict(color="#f8fafc"),
        legend=dict(font=dict(color="#f8fafc")),
        xaxis=dict(
            color="#cbd5e1",
            gridcolor="#334155",
            zerolinecolor="#475569",
            title_font=dict(color="#e2e8f0"),
            tickfont=dict(color="#cbd5e1"),
        ),
        yaxis=dict(
            color="#cbd5e1",
            gridcolor="#334155",
            zerolinecolor="#475569",
            title_font=dict(color="#e2e8f0"),
            tickfont=dict(color="#cbd5e1"),
        ),
        coloraxis_colorbar=dict(
            title_font=dict(color="#f8fafc"),
            tickfont=dict(color="#cbd5e1"),
        ),
    )
    return fig

# ==========================================
# 1. PAGE CONFIGURATION & DARK THEME CSS
# ==========================================
st.set_page_config(
    page_title="⚽ FIFA WORLD CUP | Analytics Hub",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Dark Navy & Aesthetic Neon Blue Theme
CUSTOM_CSS = """
<style>
    /* FORCE DARK MODE ACROSS THE ENTIRE STREAMLIT APP */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #020617 !important;
        color: #f8fafc !important;
    }

    /* Dark theme for Streamlit inputs, tabs and expanders */
    [data-baseweb="select"], [data-baseweb="input"], [data-baseweb="textarea"],
    [data-testid="stExpander"], [data-testid="stTabs"] {
        background-color: #0f172a !important;
        color: #f8fafc !important;
    }

    [data-baseweb="select"] *, [data-baseweb="input"] *,
    [data-baseweb="textarea"] *, [data-testid="stExpander"] * {
        color: #f8fafc !important;
    }

    /* Dark dataframe container */
    [data-testid="stDataFrame"] {
        background-color: #0f172a !important;
        border-radius: 12px;
    }
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .emoji {
        font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif !important;
    }

    /* Main App Background */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }

    /* DARK SIDEBAR STYLING */
    section[data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 1px solid #1e293b;
    }
    
    div[data-testid="stSidebarUserContent"] {
        background-color: #020617 !important;
    }

    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span {
        color: #94a3b8 !important;
    }

    /* UNIFORM DASHBOARD CARD STYLING */
    .dashboard-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }

    /* UNIFORM KPI METRIC CARD STYLING */
    .kpi-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.8) 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 16px;
        padding: 20px 16px;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
    }

    .kpi-card:hover {
        transform: translateY(-3px);
        border-color: rgba(56, 189, 248, 0.5);
        box-shadow: 0 12px 25px -5px rgba(56, 189, 248, 0.25);
    }

    .kpi-icon {
        font-size: 1.8rem;
        margin-bottom: 4px;
    }

    .kpi-title {
        color: #94a3b8;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 6px;
    }

    .kpi-value {
        color: #f8fafc;
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
    }

    .kpi-subtitle {
        color: #38bdf8;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 4px;
    }

    /* Hero Banner Header */
    .hero-banner {
        text-align: center;
        padding: 25px 20px;
        background: radial-gradient(ellipse at top, rgba(56, 189, 248, 0.15), transparent 70%);
        border-radius: 20px;
        margin-bottom: 25px;
        border: 1px solid rgba(56, 189, 248, 0.1);
    }

    h1, h2, h3, h4 {
        color: #f8fafc !important;
        letter-spacing: -0.01em;
    }

    p, li {
        color: #94a3b8;
        font-size: 0.95rem;
        line-height: 1.7;
    }

    /* CLEAR & VISIBLE SELECTBOX / DROPDOWN STYLING */
    div[data-testid="stSelectbox"] label {
        color: #38bdf8 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }

    div[data-testid="stSelectbox"] > div > div {
        background-color: #0f172a !important;
        color: #38bdf8 !important;
        border: 1.5px solid #38bdf8 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] span {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }

    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="menu"],
    ul[role="listbox"] {
        background-color: #0f172a !important;
        border: 1.5px solid #38bdf8 !important;
        border-radius: 12px !important;
    }

    li[role="option"],
    div[data-baseweb="option"],
    ul[role="listbox"] li {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        padding: 12px 16px !important;
        font-weight: 500 !important;
    }

    li[role="option"]:hover,
    div[data-baseweb="option"]:hover,
    li[aria-selected="true"] {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }

    /* Download CSV Button Styling */
    div[data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(56, 189, 248, 0.5) !important;
        border-radius: 12px !important;
        padding: 10px 24px !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 20px rgba(2, 132, 199, 0.3) !important;
    }

    div[data-testid="stDownloadButton"] > button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%) !important;
        color: #020617 !important;
        border-color: #38bdf8 !important;
    }

    /* Dataframe Deep Blue Override */
    div[data-testid="stDataFrame"] {
        background-color: #0f172a !important;
        border: 1.5px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 14px !important;
        padding: 6px !important;
    }

    div[data-testid="stDataFrame"] canvas {
        filter: invert(0.92) hue-rotate(195deg) brightness(1.1) contrast(1.15) !important;
    }

    .section-title {
        color: #f8fafc;
        font-size: 1.25rem;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 12px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# HIGHLY POLISHED & GLOWING DARK PLOTLY THEME
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0", family="Plus Jakarta Sans, sans-serif", size=12),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.12)",
        title_font=dict(size=13, color="#38bdf8", family="Plus Jakarta Sans"),
        tickfont=dict(color="#cbd5e1")
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.12)",
        title_font=dict(size=13, color="#38bdf8", family="Plus Jakarta Sans"),
        tickfont=dict(color="#cbd5e1")
    ),
    margin=dict(l=30, r=30, t=50, b=30),
    colorway=["#38bdf8", "#818cf8", "#c084fc", "#f472b6", "#34d399", "#fbbf24"]
)

# ==========================================
# 2. DATA LOADING & CACHING
# ==========================================
BASE_DIR = Path(__file__).resolve().parent

MATCHES_FILENAME = "Cleaned_WorldCupMatches(4).csv"
PLAYERS_FILENAME = "Cleaned_WorldCupPlayers(3).csv"
CUPS_FILENAME = "Cleaned_WorldCups(3).csv"

@st.cache_data
def load_data():
    matches_path = BASE_DIR / MATCHES_FILENAME
    players_path = BASE_DIR / PLAYERS_FILENAME
    cups_path = BASE_DIR / CUPS_FILENAME

    if not matches_path.exists(): matches_path = BASE_DIR / "WorldCupMatches.csv"
    if not players_path.exists(): players_path = BASE_DIR / "WorldCupPlayers.csv"
    if not cups_path.exists(): cups_path = BASE_DIR / "WorldCups.csv"

    matches, players, cups = None, None, None
    errors = []

    if matches_path.exists():
        try: matches = pd.read_csv(matches_path)
        except Exception as e: errors.append(f"{matches_path.name}: {e}")
    else: errors.append(f"{MATCHES_FILENAME} not found.")

    if players_path.exists():
        try: players = pd.read_csv(players_path)
        except Exception as e: errors.append(f"{PLAYERS_FILENAME}: {e}")
    else: errors.append(f"{PLAYERS_FILENAME} not found.")

    if cups_path.exists():
        try: cups = pd.read_csv(cups_path)
        except Exception as e: errors.append(f"{CUPS_FILENAME}: {e}")
    else: errors.append(f"{CUPS_FILENAME} not found.")

    return matches, players, cups, errors

matches_raw, players_raw, cups_raw, load_errors = load_data()

if load_errors:
    st.error("⚠️ Data File Loading Error:")
    for err in load_errors: st.write(f"- {err}")
    st.stop()

# ==========================================
# 3. PRE-PROCESSING FUNCTION
# ==========================================
@st.cache_data
def preprocess_data(df_matches, df_players, df_cups):
    df_m = df_matches.dropna(how="all").copy() if df_matches is not None else pd.DataFrame()
    num_cols = ["Home Team Goals", "Away Team Goals", "Half-time Home Goals", "Half-time Away Goals", "Year"]
    for col in num_cols:
        if col in df_m.columns:
            df_m[col] = pd.to_numeric(df_m[col], errors="coerce").fillna(0)

    if "Home Team Goals" in df_m.columns and "Away Team Goals" in df_m.columns:
        df_m["Total Goals"] = df_m["Home Team Goals"] + df_m["Away Team Goals"]
        df_m["Full-time Goal Difference"] = df_m["Home Team Goals"] - df_m["Away Team Goals"]

    if "Half-time Home Goals" in df_m.columns and "Half-time Away Goals" in df_m.columns:
        df_m["Half-time Goal Difference"] = df_m["Half-time Home Goals"] - df_m["Half-time Away Goals"]

    str_cols = ["Home Team Name", "Away Team Name", "Stage", "Win conditions"]
    for col in str_cols:
        if col in df_m.columns:
            df_m[col] = df_m[col].astype(str).str.strip()

    df_p = df_players.dropna(how="all").copy() if df_players is not None else pd.DataFrame()
    df_c = df_cups.dropna(how="all").copy() if df_cups is not None else pd.DataFrame()

    if "GoalsScored" in df_c.columns:
        df_c["GoalsScored"] = pd.to_numeric(df_c["GoalsScored"], errors="coerce").fillna(0)

    return df_m, df_p, df_c

matches_df, players_df, cups_df = preprocess_data(matches_raw, players_raw, cups_raw)

def get_unique_countries(df):
    if df.empty: return 0
    country_cols = ["Home Team Name", "Away Team Name", "Team", "Team Name", "Country", "Winner", "Runners-Up", "Third", "Fourth"]
    found_cols = [col for col in country_cols if col in df.columns]
    if not found_cols: return 0
    return int(pd.concat([df[col].dropna().astype(str) for col in found_cols]).nunique())

def get_unique_continents(df):
    if df.empty: return None
    continent_cols = ["Continent", "Continents", "Confederation", "Region"]
    found_cols = [col for col in continent_cols if col in df.columns]
    if found_cols:
        return int(pd.concat([df[col].dropna().astype(str) for col in found_cols]).nunique())
    return None

# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown(
        """
        <div style='text-align: center; padding: 10px 0;'>
            <h2 style='color: #38bdf8; margin:0; font-size: 1.5rem;'>⚽ FIFA WORLD CUP</h2>
            <p style='font-size: 0.75rem; color: #64748b; margin-top: 2px;'>Historical Analytics Hub</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    selected_page = option_menu(
        menu_title=None,
        options=["Home", "Data Explorer", "Pre-Processing", "Visualization", "About"],
        icons=["house-fill", "table", "sliders", "bar-chart-fill", "info-circle-fill"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#020617"},
            "icon": {"color": "#38bdf8", "font-size": "16px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "4px 0px",
                "color": "#94a3b8",
                "border-radius": "10px",
                "padding": "10px 14px",
                "background-color": "#020617",
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg, rgba(56, 189, 248, 0.2) 0%, rgba(30, 41, 59, 0.8) 100%)",
                "color": "#38bdf8",
                "font-weight": "700",
                "border-left": "3px solid #38bdf8",
            },
        },
    )

    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.8rem; font-weight:700; color: #94a3b8;'>🎛️ ERA FILTER</p>", unsafe_allow_html=True)

    min_year = int(matches_df["Year"].min()) if not matches_df.empty and "Year" in matches_df.columns else 1930
    max_year = int(matches_df["Year"].max()) if not matches_df.empty and "Year" in matches_df.columns else 2014

    selected_years = st.slider(
        "Tournament Era Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
    )

filtered_matches = matches_df[
    (matches_df["Year"] >= selected_years[0]) & (matches_df["Year"] <= selected_years[1])
] if not matches_df.empty and "Year" in matches_df.columns else matches_df

# ==========================================
# 5. HOME PAGE
# ==========================================
if selected_page == "Home":
    st.markdown(
        """
        <div class='hero-banner'>
            <h1 style='font-size: 2.2rem; margin:0;'><span class='emoji'>⚽</span> FIFA WORLD CUP</h1>
            <p style='color: #38bdf8; font-size: 1rem; font-weight: 600; margin-top: 4px;'>
                Historical Data Analytics Dashboard
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    total_matches = len(filtered_matches)
    total_goals = int(filtered_matches["Total Goals"].sum()) if "Total Goals" in filtered_matches.columns else 0
    total_cups = len(cups_df[(cups_df["Year"] >= selected_years[0]) & (cups_df["Year"] <= selected_years[1])]) if not cups_df.empty and "Year" in cups_df.columns else len(cups_df)
    total_players = len(players_df)
    avg_goals = round(filtered_matches["Total Goals"].mean(), 2) if total_matches > 0 and "Total Goals" in filtered_matches.columns else 0

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(f"<div class='kpi-card'><div class='kpi-icon'>🏟️</div><div class='kpi-title'>Total Matches</div><div class='kpi-value'>{total_matches:,}</div><div class='kpi-subtitle'>{selected_years[0]}-{selected_years[1]}</div></div>", unsafe_allow_html=True)
    with k2:
        st.markdown(f"<div class='kpi-card'><div class='kpi-icon'>⚽</div><div class='kpi-title'>Total Goals</div><div class='kpi-value'>{total_goals:,}</div><div class='kpi-subtitle'>Scored</div></div>", unsafe_allow_html=True)
    with k3:
        st.markdown(f"<div class='kpi-card'><div class='kpi-icon'>🏆</div><div class='kpi-title'>Tournaments</div><div class='kpi-value'>{total_cups}</div><div class='kpi-subtitle'>World Cups</div></div>", unsafe_allow_html=True)
    with k4:
        st.markdown(f"<div class='kpi-card'><div class='kpi-icon'>👤</div><div class='kpi-title'>Player Records</div><div class='kpi-value'>{total_players:,}</div><div class='kpi-subtitle'>Roster</div></div>", unsafe_allow_html=True)
    with k5:
        st.markdown(f"<div class='kpi-card'><div class='kpi-icon'>📊</div><div class='kpi-title'>Avg Goals/Match</div><div class='kpi-value'>{avg_goals}</div><div class='kpi-subtitle'>Rate</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
    <div class='dashboard-card'>
        <h3 style='margin-top:0;'>🌟 Project Executive Overview</h3>
        <p>This analytics application transforms raw historical FIFA World Cup datasets into intuitive visual insights and metrics.</p>
        <ul>
            <li><b>Match Decision Dynamics:</b> Extra time, penalty shootouts, and golden goals.</li>
            <li><b>Scoring Explosiveness:</b> Top high-scoring encounters.</li>
            <li><b>Half-time Lead Impact:</b> Correlation between half-time lead and victory.</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ==========================================
# 6. DATA EXPLORER PAGE
# ==========================================
elif selected_page == "Data Explorer":
    st.markdown(
        """
        <div class='hero-banner'>
            <h1 style='font-size: 2.2rem; margin:0;'><span class='emoji'>📊</span> Data Explorer</h1>
            <p style='color: #38bdf8; font-size: 0.95rem; font-weight: 600; margin-top: 4px;'>
                Inspect & Analyze World Cup Raw Datasets
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    ds_choice = st.selectbox(
        "🗂️ Select Dataset to Explore:",
        ["World Cup Matches", "World Cup Players", "World Cups"],
        index=0,
        key="ds_explorer_selection"
    )

    if ds_choice == "World Cup Matches":
        active_df = matches_df.copy() if matches_df is not None else pd.DataFrame()
    elif ds_choice == "World Cup Players":
        active_df = players_df.copy() if players_df is not None else pd.DataFrame()
    else:
        active_df = cups_df.copy() if cups_df is not None else pd.DataFrame()

    filtered_df = active_df.copy()
    if "Year" in filtered_df.columns and not filtered_df.empty:
        filtered_df = filtered_df[
            (filtered_df["Year"] >= selected_years[0]) & 
            (filtered_df["Year"] <= selected_years[1])
        ]

    curr_rows = len(filtered_df)
    curr_cols = len(filtered_df.columns)
    curr_countries = get_unique_countries(filtered_df)
    curr_continents = get_unique_continents(filtered_df)

    if curr_continents is not None:
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f"<div class='kpi-card'><div class='kpi-icon'>📋</div><div class='kpi-title'>Total Rows</div><div class='kpi-value'>{curr_rows:,}</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='kpi-card'><div class='kpi-icon'>📐</div><div class='kpi-title'>Total Columns</div><div class='kpi-value'>{curr_cols}</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='kpi-card'><div class='kpi-icon'>🌍</div><div class='kpi-title'>Continents</div><div class='kpi-value'>{curr_continents}</div></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='kpi-card'><div class='kpi-icon'>🏳️</div><div class='kpi-title'>Countries</div><div class='kpi-value'>{curr_countries:,}</div></div>", unsafe_allow_html=True)
    else:
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='kpi-card'><div class='kpi-icon'>📋</div><div class='kpi-title'>Total Rows</div><div class='kpi-value'>{curr_rows:,}</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='kpi-card'><div class='kpi-icon'>📐</div><div class='kpi-title'>Total Columns</div><div class='kpi-value'>{curr_cols}</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='kpi-card'><div class='kpi-icon'>🏳️</div><div class='kpi-title'>Countries</div><div class='kpi-value'>{curr_countries:,}</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab_preview, tab_columns, tab_summary = st.tabs([
        "📄 Data Preview",
        "🔍 Column Details",
        "☑️ Summary Statistics"
    ])

    with tab_preview:
        st.markdown("#### Preview Filtered Dataset")
        max_rows_limit = max(curr_rows, 1)
        rows_to_show = st.slider("Rows to Display", 1, max_rows_limit, min(20, max_rows_limit), key="ds_rows_slider")
        show_last = st.checkbox("Show Last Rows", value=False, key="ds_show_last")

        preview_display_df = filtered_df.tail(rows_to_show) if show_last else filtered_df.head(rows_to_show)
        
        st.dataframe(preview_display_df, use_container_width=True)

        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Dataset (CSV)",
            data=csv_data,
            file_name=f"{ds_choice.lower().replace(' ', '_')}.csv",
            mime="text/csv",
            key="ds_download_btn"
        )

    with tab_columns:
        st.markdown("#### Schema & Column Structure")
        if not filtered_df.empty:
            col_info_data = []
            for col in filtered_df.columns:
                col_info_data.append({
                    "Column Name": col,
                    "Data Type": str(filtered_df[col].dtype),
                    "Non-Null Values": int(filtered_df[col].notnull().sum()),
                    "Missing Values": int(filtered_df[col].isnull().sum()),
                    "Unique Values": int(filtered_df[col].nunique())
                })
            st.dataframe(pd.DataFrame(col_info_data), use_container_width=True)

    with tab_summary:
        st.markdown("#### Statistical & Null Metrics Summary")
        s1, s2 = st.columns(2)
        with s1:
            tot_missing = int(filtered_df.isnull().sum().sum())
            tot_duplicates = int(filtered_df.duplicated().sum())
            st.dataframe(pd.DataFrame({
                "Metric": ["Total Rows", "Total Columns", "Missing Cells", "Duplicate Rows"],
                "Value": [f"{curr_rows:,}", f"{curr_cols}", f"{tot_missing:,}", f"{tot_duplicates:,}"]
            }), use_container_width=True)

        with s2:
            numeric_df = filtered_df.select_dtypes(include=["number"])
            if not numeric_df.empty:
                st.dataframe(numeric_df.describe().T.reset_index().rename(columns={"index": "Column Name"}), use_container_width=True)

# ==========================================
# 7. PRE-PROCESSING PAGE (DYNAMIC PIPELINE)
# ==========================================
elif selected_page == "Pre-Processing":
    st.markdown(
        """
        <div class='hero-banner'>
            <h1 style='font-size: 2.2rem; margin:0;'><span class='emoji'>⚙️</span> Data Processing Pipeline</h1>
            <p style='color: #38bdf8; font-size: 0.95rem; font-weight: 600; margin-top: 4px;'>
                Dynamic Data Cleaning & Quality Analysis
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    proc_dataset_choice = st.selectbox(
        "🗂️ Select Dataset for Pipeline Processing:",
        ["World Cup Matches", "World Cup Players", "World Cups"],
        index=0,
        key="pipeline_ds_selection"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if proc_dataset_choice == "World Cup Matches":
        raw_target_df = matches_raw.copy() if matches_raw is not None else pd.DataFrame()
    elif proc_dataset_choice == "World Cup Players":
        raw_target_df = players_raw.copy() if players_raw is not None else pd.DataFrame()
    else:
        raw_target_df = cups_raw.copy() if cups_raw is not None else pd.DataFrame()

    if raw_target_df.empty:
        st.warning("⚠️ Selected dataset is empty or not loaded properly.")
    else:
        # BEFORE PROCESSING METRICS
        rows_before = len(raw_target_df)
        cols_before = len(raw_target_df.columns)
        total_missing_before = int(raw_target_df.isnull().sum().sum())
        rows_with_missing_before = int(raw_target_df.isnull().any(axis=1).sum())

        st.markdown("<div class='section-title'>1. Before Processing Analysis</div>", unsafe_allow_html=True)
        
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Rows Before</div><div class='kpi-value'>{rows_before:,}</div></div>", unsafe_allow_html=True)
        with m2: st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Columns</div><div class='kpi-value'>{cols_before}</div></div>", unsafe_allow_html=True)
        with m3: st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total Missing Values</div><div class='kpi-value'>{total_missing_before:,}</div></div>", unsafe_allow_html=True)
        with m4: st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Rows with Missing</div><div class='kpi-value'>{rows_with_missing_before:,}</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>Columns with Missing Values</div>", unsafe_allow_html=True)
        missing_per_col = raw_target_df.isnull().sum()
        missing_cols_df = pd.DataFrame({
            'Column Name': missing_per_col.index,
            'Missing Values': missing_per_col.values,
            'Percentage (%)': (missing_per_col.values / rows_before * 100).round(2)
        })
        missing_cols_df = missing_cols_df[missing_cols_df['Missing Values'] > 0]

        if not missing_cols_df.empty:
            st.dataframe(missing_cols_df, use_container_width=True)
            
            fig_missing = px.bar(
                missing_cols_df, 
                x='Column Name', 
                y='Missing Values', 
                text='Missing Values',
                title="Missing Values Count per Column",
                color='Missing Values',
                color_continuous_scale=['#00f2fe', '#4facfe', '#7f00ff']
            )
            fig_missing.update_traces(
                texttemplate='%{text}', 
                textposition='outside',
                marker=dict(line=dict(color='rgba(255, 255, 255, 0.2)', width=1.5))
            )
            fig_missing.update_layout(**PLOTLY_THEME)
            apply_dark_plotly(fig_missing)

            st.plotly_chart(fig_missing, width="stretch")
        else:
            st.success("✅ No missing values found in this dataset.")

        # DYNAMIC CLEANING EXECUTED
        cleaned_target_df = raw_target_df.dropna(how="all").copy()
        if proc_dataset_choice == "World Cup Matches":
            cleaned_target_df, _, _ = preprocess_data(raw_target_df, pd.DataFrame(), pd.DataFrame())
        
        rows_after = len(cleaned_target_df)
        cols_after = len(cleaned_target_df.columns)
        rows_removed = rows_before - rows_after
        total_missing_after = int(cleaned_target_df.isnull().sum().sum())
        rows_with_missing_after = int(cleaned_target_df.isnull().any(axis=1).sum())

        # AFTER PROCESSING METRICS
        st.markdown("<div class='section-title'>2. After Processing Summary</div>", unsafe_allow_html=True)

        a1, a2, a3, a4, a5 = st.columns(5)
        with a1: st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Rows Remaining</div><div class='kpi-value'>{rows_after:,}</div></div>", unsafe_allow_html=True)
        with a2: st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Rows Removed</div><div class='kpi-value'>{rows_removed:,}</div></div>", unsafe_allow_html=True)
        with a3: st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Columns Remaining</div><div class='kpi-value'>{cols_after}</div></div>", unsafe_allow_html=True)
        with a4: st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Missing Remaining</div><div class='kpi-value'>{total_missing_after:,}</div></div>", unsafe_allow_html=True)
        with a5: st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Rows w/ Missing</div><div class='kpi-value'>{rows_with_missing_after:,}</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>Before vs After Comparison Table</div>", unsafe_allow_html=True)
        comparison_data = {
            "Metric": ["Total Rows", "Total Columns", "Total Missing Values", "Rows Containing Missing Values"],
            "Before Processing": [f"{rows_before:,}", f"{cols_before}", f"{total_missing_before:,}", f"{rows_with_missing_before:,}"],
            "After Processing": [f"{rows_after:,}", f"{cols_after}", f"{total_missing_after:,}", f"{rows_with_missing_after:,}"]
        }
        st.dataframe(pd.DataFrame(comparison_data), use_container_width=True)

        # PREVIEW & DOWNLOAD CLEANED DATA
        st.markdown("<div class='section-title'>3. Preview of Cleaned Data</div>", unsafe_allow_html=True)
        st.dataframe(cleaned_target_df.head(20), use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        csv_cleaned = cleaned_target_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Cleaned Data CSV",
            data=csv_cleaned,
            file_name="cleaned_data.csv",
            mime="text/csv",
            key="download_cleaned_csv_btn"
        )

# ==========================================
# ==========================================
# 8. VISUALIZATION PAGE (ALL EXISTING PLOTLY GRAPHS)
# ==========================================
elif selected_page == "Visualization":
    st.markdown(
        """
        <div class='hero-banner'>
            <h1 style='font-size: 2.2rem; margin:0;'>
                <span class='emoji'>📈</span> Interactive Visual Analytics
            </h1>
            <p style='color: #38bdf8; font-size: 0.95rem; font-weight: 600; margin-top: 4px;'>
                FIFA WORLD CUP — Matches, Players & World Cup Analysis
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------
    # THREE DATASET TABS
    # --------------------------------------------------
    match_tab, player_tab, cups_tab = st.tabs(
        ["⚽ World Cup Matches", "👤 World Cup Players", "🏆 World Cups"]
    )

    # ==================================================
    # 1. WORLD CUP MATCHES — 6 EXISTING GRAPHS
    # ==================================================
    with match_tab:
        st.markdown(
            "<div class='section-title'>⚽ World Cup Matches Analysis</div>",
            unsafe_allow_html=True
        )

        match_data = filtered_matches.copy()

        # ---------- GRAPH 1 ----------
        st.markdown(
            "<div class='dashboard-card'><h3>🏆 Number of Matches in Each Stage</h3></div>",
            unsafe_allow_html=True
        )

        stage_count = match_data["Stage"].value_counts().reset_index()
        stage_count.columns = ["Stage", "Count"]

        fig1 = px.bar(
            stage_count,
            x="Stage",
            y="Count",
            color="Count",
            color_continuous_scale="Viridis",
            title="🏆 Number of Matches in Each Stage",
            template="plotly_dark",
            text="Count",
        )

        fig1.update_layout(
            title_x=0.5,
            xaxis_tickangle=-45,
        )

        apply_dark_plotly(fig1)


        st.plotly_chart(fig1, width="stretch")

        # ---------- GRAPH 2 ----------
        st.markdown(
            "<div class='dashboard-card'><h3>⚽ Home Team Goals vs Away Team Goals</h3></div>",
            unsafe_allow_html=True
        )

        fig2 = px.scatter(
            match_data,
            x="Home Team Goals",
            y="Away Team Goals",
            title="⚽ Home Team Goals vs Away Team Goals",
            color_discrete_sequence=["#331fb4"],
        )

        fig2.update_traces(
            marker=dict(
                size=12,
                opacity=0.8,
                line=dict(width=1.5, color="black"),
            )
        )

        fig2.update_layout(
            template="plotly_dark",
            title_font_size=24,
            title_x=0.5,
            xaxis_title="Home Team Goals",
            yaxis_title="Away Team Goals",
        )

        apply_dark_plotly(fig2)


        st.plotly_chart(fig2, width="stretch")

        # ---------- GRAPH 3 ----------
        st.markdown(
            "<div class='dashboard-card'><h3>📈 Average Home Goals vs Away Goals by Year</h3></div>",
            unsafe_allow_html=True
        )

        yearly_average = (
            match_data.groupby("Year")[["Home Team Goals", "Away Team Goals"]]
            .mean()
            .reset_index()
        )

        fig3 = px.line(
            yearly_average,
            x="Year",
            y=["Home Team Goals", "Away Team Goals"],
            title="⚽ Average Home Team Goals vs Away Team Goals by Year",
        )

        fig3.update_traces(line=dict(width=4))

        if len(fig3.data) >= 2:
            fig3.data[0].line.color = "#90EE90"
            fig3.data[1].line.color = "#FFD700"

        fig3.update_layout(
            template="plotly_dark",
            title_x=0.5,
            xaxis_title="Year",
            yaxis_title="Average Goals",
        )

        apply_dark_plotly(fig3)


        st.plotly_chart(fig3, width="stretch")

        # ---------- GRAPH 4 ----------
        st.markdown(
            "<div class='dashboard-card'><h3>🥅 Distribution of Match Outcomes</h3></div>",
            unsafe_allow_html=True
        )

        outcome_data = match_data.copy()

        outcome_data["Match Outcome"] = np.where(
            outcome_data["Home Team Goals"] > outcome_data["Away Team Goals"],
            "Home Win",
            np.where(
                outcome_data["Home Team Goals"] < outcome_data["Away Team Goals"],
                "Away Win",
                "Draw",
            ),
        )

        outcome_counts = (
            outcome_data.groupby("Match Outcome", as_index=False)
            .size()
            .rename(columns={"size": "Match Count"})
        )

        fig4 = px.pie(
            outcome_counts,
            names="Match Outcome",
            values="Match Count",
            hole=0.45,
            title="Distribution of Match Outcomes",
            color="Match Outcome",
            color_discrete_map={
                "Home Win": "#e74096",
                "Away Win": "#27c4d6",
                "Draw": "#f0e570",
            },
        )

        fig4.update_traces(
            textposition="inside",
            textinfo="percent+label",
        )

        fig4.update_layout(
            template="plotly_dark",
            title_x=0.5,
            legend_title="Match Outcome",
        )

        apply_dark_plotly(fig4)


        st.plotly_chart(fig4, width="stretch")

        # ---------- GRAPH 5 ----------
        st.markdown(
            "<div class='dashboard-card'><h3>🔥 Top 10 Highest Scoring FIFA World Cup Matches</h3></div>",
            unsafe_allow_html=True
        )

        top_match_data = match_data.copy()

        top_match_data["Total Goals"] = (
            top_match_data["Home Team Goals"]
            + top_match_data["Away Team Goals"]
        )

        top_match_data["Match Description"] = (
            top_match_data["Year"].astype(str)
            + " - "
            + top_match_data["Home Team Name"]
            + " vs "
            + top_match_data["Away Team Name"]
        )

        top_matches = (
            top_match_data
            .sort_values(by="Total Goals", ascending=False)
            .head(10)
        )

        fig5 = px.bar(
            top_matches,
            x="Total Goals",
            y="Match Description",
            color="Year",
            orientation="h",
            text="Total Goals",
            title="Top 10 Highest Scoring FIFA World Cup Matches",
            color_continuous_scale="Blues",
        )

        fig5.update_traces(textposition="outside")

        fig5.update_layout(
            xaxis_title="Total Goals",
            yaxis_title="Match (Year - Home vs Away)",
            template="plotly_dark",
            title_x=0.5,
            yaxis=dict(categoryorder="total ascending"),
        )

        apply_dark_plotly(fig5)


        st.plotly_chart(fig5, width="stretch")

        # ---------- GRAPH 6 ----------
        st.markdown(
            "<div class='dashboard-card'><h3>📦 Distribution of Total Goals by Match Stage</h3></div>",
            unsafe_allow_html=True
        )

        fig6 = px.box(
            top_match_data,
            x="Stage",
            y="Total Goals",
            color="Stage",
            title="Distribution of Total Goals by Match Stage",
            points="all",
        )

        fig6.update_layout(
            xaxis_title="Match Stage",
            yaxis_title="Total Goals",
            template="plotly_dark",
            title_x=0.5,
            showlegend=False,
        )

        apply_dark_plotly(fig6)


        st.plotly_chart(fig6, width="stretch")

    # ==================================================
    # 2. WORLD CUP PLAYERS — 5 EXISTING GRAPHS
    # ==================================================
    with player_tab:
        st.markdown(
            "<div class='section-title'>👤 World Cup Players Analysis</div>",
            unsafe_allow_html=True
        )

        player_data = players_df.copy()

        # ---------- GRAPH 7 ----------
        st.markdown(
            "<div class='dashboard-card'><h3>🌍 Players by Team</h3></div>",
            unsafe_allow_html=True
        )

        team_count = (
            player_data.groupby("Team Initials")
            .size()
            .reset_index(name="Player Count")
        )

        fig7 = px.bar(
            team_count,
            x="Team Initials",
            y="Player Count",
            color="Player Count",
            text="Player Count",
            title="🌍 Players by Team",
            template="plotly_dark",
        )

        fig7.update_layout(
            title_x=0.5,
            xaxis_title="Team Initials",
            yaxis_title="Player Count",
        )

        apply_dark_plotly(fig7)


        st.plotly_chart(fig7, width="stretch")

        # ---------- GRAPH 8 ----------
        st.markdown(
            "<div class='dashboard-card'><h3>⚽ Player Distribution by Team and Position</h3></div>",
            unsafe_allow_html=True
        )

        treemap_data = (
            player_data.groupby(["Team Initials", "Position"])
            .size()
            .reset_index(name="Count")
        )

        fig8 = px.treemap(
            treemap_data,
            path=["Team Initials", "Position"],
            values="Count",
            color="Count",
            color_continuous_scale="Turbo",
            title="⚽ Player Distribution by Team and Position",
        )

        fig8.update_layout(
            template="plotly_dark",
            title_x=0.5,
        )

        apply_dark_plotly(fig8)


        st.plotly_chart(fig8, width="stretch")

        # ---------- GRAPH 9 ----------
        st.markdown(
            "<div class='dashboard-card'><h3>👕 Shirt Numbers Used for Each Player Position</h3></div>",
            unsafe_allow_html=True
        )

        shirt_position_data = (
            player_data.groupby(["Position", "Shirt Number"])
            .size()
            .reset_index(name="Count")
        )

        fig9 = px.density_heatmap(
            shirt_position_data,
            x="Shirt Number",
            y="Position",
            z="Count",
            color_continuous_scale="Turbo",
            text_auto=True,
            title="👕 Shirt Numbers Used for Each Player Position",
        )

        fig9.update_layout(
            template="plotly_dark",
            title={
                "text": "👕 Shirt Numbers Used for Each Player Position",
                "x": 0.5,
                "font": dict(size=24),
            },
            xaxis_title="Shirt Number",
            yaxis_title="Player Position",
            font=dict(size=14),
            coloraxis_colorbar=dict(title="Players"),
        )

        fig9.update_traces(
            hovertemplate="<b>Position:</b> %{y}<br>"
                          "<b>Shirt Number:</b> %{x}<br>"
                          "<b>Players:</b> %{z}<extra></extra>"
        )

        apply_dark_plotly(fig9)


        st.plotly_chart(fig9, width="stretch")

        # ---------- GRAPH 10 ----------
        st.markdown(
            "<div class='dashboard-card'><h3>⚽ Number of Players Representing Each Team</h3></div>",
            unsafe_allow_html=True
        )

        team_players = (
            player_data.groupby("Team Initials")
            .size()
            .reset_index(name="Player Count")
            .sort_values("Player Count", ascending=True)
        )

        fig10 = px.bar(
            team_players,
            x="Player Count",
            y="Team Initials",
            orientation="h",
            color="Player Count",
            color_continuous_scale="Viridis",
            text="Player Count",
            title="⚽ Number of Players Representing Each Team",
        )

        fig10.update_layout(
            template="plotly_dark",
            title={
                "text": "⚽ Number of Players Representing Each Team",
                "x": 0.5,
                "font": dict(size=24),
            },
            xaxis_title="Number of Players",
            yaxis_title="Team Initials",
            font=dict(size=14),
            height=700,
        )

        fig10.update_traces(
            textposition="outside",
            hovertemplate="<b>Team:</b> %{y}<br>"
                          "<b>Players:</b> %{x}<extra></extra>",
        )

        apply_dark_plotly(fig10)


        st.plotly_chart(fig10, width="stretch")

        # ---------- GRAPH 11 ----------
        st.markdown(
            "<div class='dashboard-card'><h3>👕 Most Commonly Used Shirt Numbers</h3></div>",
            unsafe_allow_html=True
        )

        shirt_count = (
            player_data.groupby("Shirt Number")
            .size()
            .reset_index(name="Player Count")
            .sort_values("Shirt Number")
        )

        fig11 = px.bar(
            shirt_count,
            x="Shirt Number",
            y="Player Count",
            color="Player Count",
            text="Player Count",
            color_continuous_scale="Inferno",
            title="👕 Most Commonly Used Shirt Numbers",
        )

        fig11.update_traces(
            textposition="outside",
            marker_line_color="white",
            marker_line_width=1.5,
            hovertemplate="<b>Shirt Number:</b> %{x}<br>"
                          "<b>Players:</b> %{y}<extra></extra>",
        )

        fig11.update_layout(
            template="plotly_dark",
            title={
                "text": "👕 Most Commonly Used Shirt Numbers",
                "x": 0.5,
                "font": dict(size=26),
            },
            xaxis_title="Shirt Number",
            yaxis_title="Number of Players",
            font=dict(size=14),
            coloraxis_colorbar=dict(title="Players"),
        )

        apply_dark_plotly(fig11)


        st.plotly_chart(fig11, width="stretch")

    # ==================================================
    # 3. WORLD CUPS — 5 EXISTING GRAPHS
    # ==================================================
    with cups_tab:
        st.markdown(
            "<div class='section-title'>🏆 World Cups Analysis</div>",
            unsafe_allow_html=True
        )

        cups_data = cups_df.copy()

        # ---------- GRAPH 12 ----------
        st.markdown(
            "<div class='dashboard-card'><h3>🏆 FIFA World Cup Titles by Country</h3></div>",
            unsafe_allow_html=True
        )

        winner_count = (
            cups_data.groupby("Winner")
            .size()
            .reset_index(name="Titles")
            .sort_values("Titles", ascending=False)
        )

        fig12 = px.bar(
            winner_count,
            x="Winner",
            y="Titles",
            color="Titles",
            text="Titles",
            title="🏆 FIFA World Cup Titles by Country",
            template="plotly_dark",
        )

        fig12.update_layout(
            title_x=0.5,
            xaxis_title="Winner",
            yaxis_title="World Cup Titles",
        )

        apply_dark_plotly(fig12)


        st.plotly_chart(fig12, width="stretch")

        # ---------- GRAPH 13 ----------
        st.markdown(
            "<div class='dashboard-card'><h3>⚽ Goals Scored and Matches Played Over the Years</h3></div>",
            unsafe_allow_html=True
        )

        df_new = cups_data[
            ["Year", "GoalsScored", "MatchesPlayed"]
        ].melt(
            id_vars="Year",
            value_vars=["GoalsScored", "MatchesPlayed"],
            var_name="Metric",
            value_name="Value",
        )

        fig13 = px.line(
            df_new,
            x="Year",
            y="Value",
            color="Metric",
            markers=True,
            color_discrete_map={
                "GoalsScored": "#EAEF40",
                "MatchesPlayed": "#A7E98B",
            },
            title="Goals Scored and Matches Played Over the Years",
        )

        fig13.update_layout(
            template="plotly_dark",
            xaxis_title="Year",
            yaxis_title="Count",
            title_x=0.5,
        )

        apply_dark_plotly(fig13)


        st.plotly_chart(fig13, width="stretch")

        # ---------- GRAPH 14 ----------
        st.markdown(
            "<div class='dashboard-card'><h3>🌍 Qualified Teams in FIFA World Cup</h3></div>",
            unsafe_allow_html=True
        )

        fig14 = go.Figure()

        fig14.add_trace(
            go.Scatter(
                x=cups_data["Year"],
                y=cups_data["QualifiedTeams"],
                mode="markers+text",
                marker=dict(
                    size=14,
                    color="#FF00C3",
                    line=dict(color="white", width=2),
                ),
                text=cups_data["QualifiedTeams"],
                textposition="top center",
            )
        )

        for x, y in zip(cups_data["Year"], cups_data["QualifiedTeams"]):
            fig14.add_shape(
                type="line",
                x0=x,
                x1=x,
                y0=0,
                y1=y,
                line=dict(color="#00E5FF", width=3),
            )

        fig14.update_layout(
            template="plotly_dark",
            title="Qualified Teams in FIFA World Cup",
            title_x=0.5,
            xaxis_title="Year",
            yaxis_title="Qualified Teams",
        )

        apply_dark_plotly(fig14)


        st.plotly_chart(fig14, width="stretch")

        # ---------- GRAPH 15 ----------
        st.markdown(
            "<div class='dashboard-card'><h3>🏟️ Which Country Hosted the Most World Cup Matches?</h3></div>",
            unsafe_allow_html=True
        )

        country_matches = (
            cups_data.groupby("Country")
            .size()
            .reset_index(name="Matches")
            .sort_values(by="Matches", ascending=False)
        )

        fig15 = px.bar(
            country_matches,
            x="Country",
            y="Matches",
            color="Matches",
            color_continuous_scale="Tealgrn",
            title="Which Country Hosted the Most World Cup Matches?",
            template="plotly_dark",
            text="Matches",
        )

        fig15.update_traces(textposition="outside")

        fig15.update_layout(
            xaxis_title="Host Country",
            yaxis_title="Number of Matches",
            showlegend=False,
            xaxis_tickangle=-45,
            title_x=0.5,
        )

        apply_dark_plotly(fig15)


        st.plotly_chart(fig15, width="stretch")

        # ---------- GRAPH 16 ----------
        st.markdown(
            "<div class='dashboard-card'><h3>🥇 Countries with the Most FIFA World Cup Titles</h3></div>",
            unsafe_allow_html=True
        )

        winner_count2 = (
            cups_data.groupby("Winner")
            .size()
            .reset_index(name="World Cup Titles")
            .sort_values(by="World Cup Titles", ascending=False)
        )

        fig16 = px.bar(
            winner_count2,
            x="World Cup Titles",
            y="Winner",
            orientation="h",
            color="World Cup Titles",
            color_continuous_scale="YlOrBr",
            template="plotly_dark",
            text="World Cup Titles",
            title="Countries with the Most FIFA World Cup Titles",
        )

        fig16.update_traces(textposition="outside")

        fig16.update_layout(
            title_x=0.5,
            xaxis_title="Number of World Cup Titles",
            yaxis_title="Country",
            showlegend=False,
            font=dict(size=15),
        )

        apply_dark_plotly(fig16)


        st.plotly_chart(fig16, width="stretch")

# ==========================================
# 9. ABOUT PAGE
# ==========================================
elif selected_page == "About":

    st.markdown(
        "<div class='hero-card'>"
        "<h1 style='margin-bottom:6px;'>🏆 FIFA WORLD CUP</h1>"
        "<p style='font-size:1.05rem;'>An interactive historical FIFA World Cup data analytics dashboard</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='dashboard-card'>"
        "<h3>🌍 About the Project</h3>"
        "<p>FIFA WORLD CUP is an interactive data analytics project built to explore historical World Cup tournaments through matches, players, teams, goals, hosts and tournament statistics.</p>"
        "<p>The dashboard uses cleaned FIFA World Cup datasets and presents the information through interactive tables, preprocessing insights and Plotly visualizations.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "<div class='dashboard-card'>"
            "<h3>📊 Datasets Used</h3>"
            "<ul>"
            "<li><b>World Cup Matches</b> — match results, teams, goals, stages and match details.</li>"
            "<li><b>World Cup Players</b> — player teams, positions and shirt numbers.</li>"
            "<li><b>World Cups</b> — tournament years, winners, hosts, goals, matches and qualified teams.</li>"
            "</ul>"
            "</div>",
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            "<div class='dashboard-card'>"
            "<h3>🔎 What You Can Explore</h3>"
            "<ul>"
            "<li>🏟️ Matches across tournament stages</li>"
            "<li>⚽ Home and away goal patterns</li>"
            "<li>🔥 Highest-scoring World Cup matches</li>"
            "<li>👤 Player and team distributions</li>"
            "<li>🏆 World Cup winners and titles</li>"
            "<li>🌍 Host countries and qualified teams</li>"
            "</ul>"
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div class='dashboard-card'>"
        "<h3>📈 Dashboard Sections</h3>"
        "<p><b>Home</b> gives a quick overview. <b>Data Explorer</b> provides access to the cleaned datasets. "
        "<b>Pre-Processing</b> presents data preparation and cleaning information. <b>Visualization</b> contains the 16 interactive Plotly charts covering matches, players and World Cup tournaments. "
        "<b>About</b> describes the purpose, datasets and technologies used in the project.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    col3, col4, col5 = st.columns(3)

    with col3:
        st.markdown(
            "<div class='dashboard-card' style='text-align:center;'>"
            "<div style='font-size:2rem;'>🐍</div>"
            "<h4>Python</h4>"
            "<p>Data processing and analysis</p>"
            "</div>",
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            "<div class='dashboard-card' style='text-align:center;'>"
            "<div style='font-size:2rem;'>🎈</div>"
            "<h4>Streamlit</h4>"
            "<p>Interactive dashboard interface</p>"
            "</div>",
            unsafe_allow_html=True,
        )

    with col5:
        st.markdown(
            "<div class='dashboard-card' style='text-align:center;'>"
            "<div style='font-size:2rem;'>📊</div>"
            "<h4>Plotly</h4>"
            "<p>Interactive data visualizations</p>"
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div class='hero-card' style='margin-top:20px;'>"
        "<h3>⚽ Explore. Analyze. Discover.</h3>"
        "<p>Use the sidebar to navigate through the FIFA WORLD CUP dashboard and explore the story hidden inside historical tournament data.</p>"
        "</div>",
        unsafe_allow_html=True,
    )