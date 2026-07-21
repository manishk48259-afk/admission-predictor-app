# ============================================================
#  🎓 ADMISSION PREDICTOR PRO - FINAL CLEAN EDITION
#  Developed by: Manish Kumar
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import shap
import warnings
import time

warnings.filterwarnings('ignore')

# ============================================================
#  PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Admission Predictor Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
#  ULTIMATE CLEAN CSS
# ============================================================
st.markdown("""
<style>
    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main app background */
    .stApp {
        background: #f8fafc;
    }
    
    /* ==========================================
       WHITE SIDEBAR
       ========================================== */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e5e7eb;
        box-shadow: 2px 0 8px rgba(0,0,0,0.03);
    }
    
    section[data-testid="stSidebar"] * {
        color: #1f2937 !important;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #111827 !important;
        font-weight: 700 !important;
        border-bottom: 2px solid #f3f4f6;
        padding-bottom: 10px;
        margin-top: 20px;
        font-size: 1.05rem !important;
    }
    
    /* ==========================================
       SLIDER - CLEAN
       ========================================== */
    section[data-testid="stSidebar"] [data-baseweb="slider"] [role="slider"] {
        background-color: #4f46e5 !important;
        border: 3px solid white !important;
        box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3) !important;
    }
    
    section[data-testid="stSidebar"] [data-baseweb="slider"] div[role="slider"] > div {
        background: #4f46e5 !important;
        color: white !important;
        padding: 4px 8px !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    
    section[data-testid="stSidebar"] [data-baseweb="slider"] > div > div {
        background: #e5e7eb !important;
    }
    
    section[data-testid="stSidebar"] [data-baseweb="slider"] > div > div > div {
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%) !important;
    }
    
    section[data-testid="stSidebar"] .stSlider [data-testid] {
        background: transparent !important;
    }
    
    section[data-testid="stSidebar"] .stSlider label {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }
    
    /* ==========================================
       PREMIUM HEADER
       ========================================== */
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(30, 41, 59, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(79, 70, 229, 0.15) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        color: #cbd5e1;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    .header-badges {
        margin-top: 1rem;
        position: relative;
        z-index: 1;
    }
    
    .header-badge {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        padding: 0.4rem 1rem;
        border-radius: 20px;
        margin: 0.2rem 0.3rem;
        font-size: 0.85rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* ==========================================
       CARDS
       ========================================== */
    .feature-card {
        background: white;
        padding: 2rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
        height: 100%;
        border: 1px solid #f1f5f9;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        box-shadow: 0 4px 16px rgba(79, 70, 229, 0.1);
        border-color: #c7d2fe;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* ==========================================
       RESULT BOXES
       ========================================== */
    .success-box {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #d1fae5;
        border-left: 6px solid #16a34a;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        margin: 1rem 0;
    }
    
    .info-box {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #dbeafe;
        border-left: 6px solid #2563eb;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        margin: 1rem 0;
    }
    
    .warning-box {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #fef3c7;
        border-left: 6px solid #d97706;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        margin: 1rem 0;
    }
    
    /* ==========================================
       BUTTONS - OUTLINE STYLE (No Background)
       ========================================== */
    .stButton>button {
        background: transparent !important;
        color: #4f46e5 !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 8px !important;
        border: 2px solid #4f46e5 !important;
        width: 100% !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton>button:hover {
        background: #4f46e5 !important;
        color: white !important;
    }
    
    .stDownloadButton>button {
        background: transparent !important;
        color: #059669 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: 2px solid #059669 !important;
        padding: 0.75rem 1.5rem !important;
        width: 100% !important;
    }
    
    .stDownloadButton>button:hover {
        background: #059669 !important;
        color: white !important;
    }
    
    /* ==========================================
       TABS - CLEAN UNDERLINE STYLE
       ========================================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background: transparent;
        padding: 0;
        border-bottom: 2px solid #e5e7eb;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 0 !important;
        padding: 12px 4px !important;
        color: #64748b !important;
        font-weight: 600 !important;
        border-bottom: 3px solid transparent !important;
        margin-bottom: -2px !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: #4f46e5 !important;
        border-bottom: 3px solid #4f46e5 !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #4f46e5 !important;
    }
    
    /* ==========================================
       SECTION HEADERS
       ========================================== */
    .section-header {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1e293b;
        padding: 0.5rem 0;
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid #4f46e5;
        display: inline-block;
    }
    
    /* ==========================================
       METRIC STYLING
       ========================================== */
    div[data-testid="stMetricValue"] {
        color: #1e293b !important;
        font-weight: 700 !important;
        font-size: 1.75rem !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    div[data-testid="stMetricDelta"] {
        font-size: 0.85rem !important;
    }
    
    /* ==========================================
       DIVIDER
       ========================================== */
    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e5e7eb, transparent);
        margin: 2rem 0;
    }
    
    /* ==========================================
       FOOTER
       ========================================== */
    .footer {
        text-align: center;
        padding: 1.5rem;
        background: #1e293b;
        color: white;
        border-radius: 12px;
        margin-top: 3rem;
    }
    
    .footer-title {
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .footer-text {
        font-size: 0.85rem;
        color: #cbd5e1;
        margin: 0.3rem 0;
    }
    
    .developer-tag {
        color: #fbbf24 !important;
        font-weight: 700;
        font-size: 0.95rem;
    }
    
    /* ==========================================
       SIDEBAR STUDENT PROFILE
       ========================================== */
    .student-profile-card {
        background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem 0 1.5rem 0;
        border: 1px solid #e0e7ff;
    }
    
    .avatar-circle {
        width: 85px;
        height: 85px;
        border-radius: 50%;
        margin: 0 auto 1rem auto;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        border: 4px solid white;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
    }
    
    .profile-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e293b !important;
        margin-bottom: 0.2rem;
    }
    
    .profile-subtitle {
        font-size: 0.8rem;
        color: #64748b !important;
    }
    
    /* Caption */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: #6b7280 !important;
        font-size: 0.8rem !important;
    }
    
    /* Alerts */
    .stAlert {
        border-radius: 8px !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 8px !important;
        border: 1px solid #e5e7eb !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
#  LOAD MODEL & DATA
# ============================================================
@st.cache_resource
def load_model():
    project_root = Path(__file__).parent.parent
    model_path = project_root / "models" / "saved_models" / "xgboost_optimized.pkl"
    with open(model_path, 'rb') as f:
        return pickle.load(f)

@st.cache_resource
def load_explainer(_model):
    return shap.TreeExplainer(_model)

@st.cache_data
def load_feature_names():
    project_root = Path(__file__).parent.parent
    df = pd.read_csv(project_root / "data" / "processed" / "admission_engineered.csv")
    df.columns = df.columns.str.strip()
    target = [col for col in df.columns if 'Admit' in col][0]
    return df.drop(target, axis=1).columns.tolist()

@st.cache_data
def load_original_dataset():
    project_root = Path(__file__).parent.parent
    df = pd.read_csv(project_root / "data" / "processed" / "admission_engineered.csv")
    df.columns = df.columns.str.strip()
    return df

# ============================================================
#  FEATURE ENGINEERING
# ============================================================
def engineer_features(gre, toefl, univ_rating, sop, lor, cgpa, research):
    features = {
        'GRE Score': gre, 'TOEFL Score': toefl, 'University Rating': univ_rating,
        'SOP': sop, 'LOR': lor, 'CGPA': cgpa, 'Research': research,
        'GRE_x_CGPA': gre * cgpa, 'TOEFL_x_CGPA': toefl * cgpa,
        'GRE_x_TOEFL': gre * toefl, 'Research_x_CGPA': research * cgpa,
        'SOP_x_LOR': sop * lor, 'UnivRating_x_CGPA': univ_rating * cgpa,
        'GRE_squared': gre ** 2, 'CGPA_squared': cgpa ** 2,
        'TOEFL_squared': toefl ** 2, 'CGPA_cubed': cgpa ** 3,
        'GRE_sqrt': np.sqrt(gre),
        'Academic_Score': ((gre/340)*0.35 + (toefl/120)*0.25 + (cgpa/10)*0.40) * 100,
        'Application_Strength': ((sop/5)*0.40 + (lor/5)*0.40 + (univ_rating/5)*0.20) * 100,
        'Profile_Strength': 0,
        'Test_Score_Avg': ((gre/340) + (toefl/120)) / 2 * 100,
        'SOP_to_LOR_ratio': sop / lor if lor > 0 else 0,
        'GRE_to_TOEFL_ratio': gre / toefl if toefl > 0 else 0,
        'CGPA_Achievement': cgpa / 10,
        'Test_Performance': ((gre-260)/80 + (toefl-80)/40) / 2,
        'CGPA_Category': 3 if cgpa >= 9.0 else 2 if cgpa >= 8.0 else 1 if cgpa >= 7.0 else 0,
        'GRE_Category': 3 if gre >= 325 else 2 if gre >= 315 else 1 if gre >= 305 else 0,
        'TOEFL_Category': 3 if toefl >= 110 else 2 if toefl >= 105 else 1 if toefl >= 100 else 0,
        'High_Achiever': 1 if (cgpa >= 8.5 and gre >= 320 and toefl >= 108) else 0,
        'Mean_All_Scores': ((gre/340) + (toefl/120) + (cgpa/10) + (sop/5) + (lor/5) + (univ_rating/5)) / 6,
        'Score_Consistency': np.std([gre/340, toefl/120, cgpa/10, sop/5, lor/5]),
        'Total_Weighted_Score': (gre*0.20 + toefl*0.15 + cgpa*10*0.35 + sop*5*0.10 + 
                                  lor*5*0.10 + univ_rating*5*0.05 + research*20*0.05),
    }
    features['Profile_Strength'] = (features['Academic_Score']*0.60 + 
                                      features['Application_Strength']*0.30 + research*10)
    return features

# ============================================================
#  LOAD RESOURCES
# ============================================================
try:
    model = load_model()
    explainer = load_explainer(model)
    feature_names = load_feature_names()
    dataset = load_original_dataset()
    model_loaded = True
except Exception as e:
    st.error(f"Error loading model: {e}")
    model_loaded = False

# ============================================================
#  PREMIUM HEADER
# ============================================================
st.markdown("""
<div class="main-header">
    <div class="header-title">🎓 Admission Predictor Pro</div>
    <div class="header-subtitle">AI-Powered Graduate Admission Prediction System</div>
    <div class="header-badges">
        <span class="header-badge">⚡ XGBoost</span>
        <span class="header-badge">🔍 SHAP</span>
        <span class="header-badge">🎯 90%+ Accuracy</span>
        <span class="header-badge">🤖 33 Features</span>
        <span class="header-badge">⚙️ Optuna Tuned</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
#  CLEAN WHITE SIDEBAR
# ============================================================
with st.sidebar:
    # Student Profile Card
    st.markdown("""
    <div class="student-profile-card">
        <div class="avatar-circle">👨‍🎓</div>
        <div class="profile-name">Student Profile</div>
        <div class="profile-subtitle">Enter your details below</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Academic Section
    st.markdown("### 📚 Academic Scores")
    
    gre = st.slider("**GRE Score**", 260, 340, 320, help="Graduate Record Examination Score")
    st.caption(f"Current: **{gre}** | Target: 325+")
    
    toefl = st.slider("**TOEFL Score**", 80, 120, 110, help="Test of English as Foreign Language")
    st.caption(f"Current: **{toefl}** | Target: 110+")
    
    cgpa = st.slider("**CGPA (out of 10)**", 6.0, 10.0, 8.5, 0.1, help="Undergraduate GPA")
    st.caption(f"Current: **{cgpa}** | Target: 8.5+")
    
    # Application Section
    st.markdown("### 🎯 Application Details")
    
    univ_rating = st.slider("**University Rating**", 1, 5, 3, help="Target university rating")
    st.caption(f"Rating: {'⭐' * univ_rating} ({univ_rating}/5)")
    
    sop = st.slider("**SOP Strength**", 1.0, 5.0, 3.5, 0.5, help="Statement of Purpose quality")
    st.caption(f"Quality: {sop}/5")
    
    lor = st.slider("**LOR Strength**", 1.0, 5.0, 3.5, 0.5, help="Letter of Recommendation")
    st.caption(f"Quality: {lor}/5")
    
    # Research
    st.markdown("### 🔬 Research")
    research = st.radio("**Research Experience?**", 
                         options=[0, 1], 
                         format_func=lambda x: "No" if x == 0 else "Yes",
                         horizontal=True)
    
    # Profile Status (No Box)
    st.markdown("### 📌 Profile Status")
    
    total_score = (gre/340 + toefl/120 + cgpa/10) / 3 * 100
    if total_score >= 90:
        tier = "Elite"
        tier_icon = "🏆"
        tier_color = "#059669"
    elif total_score >= 75:
        tier = "Strong"
        tier_icon = "⭐"
        tier_color = "#4f46e5"
    elif total_score >= 60:
        tier = "Good"
        tier_icon = "✓"
        tier_color = "#0891b2"
    else:
        tier = "Developing"
        tier_icon = "📚"
        tier_color = "#d97706"
    
    st.markdown(f"""
    <div style='padding: 0.5rem 0;'>
        <div style='font-size: 1.3rem; font-weight: 700; color: {tier_color} !important; margin-bottom: 0.3rem;'>
            {tier_icon} <span style="color:{tier_color} !important;">{tier} Profile</span>
        </div>
        <div style='font-size: 0.9rem; color: #6b7280 !important;'>
            Overall Score: <b style='color: #1e293b !important;'>{total_score:.1f}/100</b>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Predict Button (Clean Outline)
    predict_button = st.button("🚀 PREDICT MY CHANCES", use_container_width=True)

# ============================================================
#  MAIN CONTENT
# ============================================================
if predict_button and model_loaded:
    
    # Loading
    with st.spinner('🔮 Analyzing your profile...'):
        time.sleep(0.5)
        features_dict = engineer_features(gre, toefl, univ_rating, sop, lor, cgpa, research)
        input_df = pd.DataFrame([features_dict])
        input_df = input_df[feature_names]
        prediction = model.predict(input_df)[0]
        prediction_pct = prediction * 100
        shap_values = explainer.shap_values(input_df)
    
    # TABS
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Prediction", "🔍 Explanation", "📈 Analytics", "💡 Recommendations"])
    
    # ============================================================
    # TAB 1: PREDICTION
    # ============================================================
    with tab1:
        st.markdown('<div class="section-header">📊 Prediction Result</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prediction_pct,
                title={'text': "<b>Your Admission Chance</b>", 
                       'font': {'size': 20, 'color': '#1e293b'}},
                number={'font': {'size': 55, 'color': '#1e293b'}, 'suffix': '%'},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "#64748b",
                             'tickfont': {'size': 12}},
                    'bar': {'color': "#4f46e5", 'thickness': 0.35},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "#e2e8f0",
                    'steps': [
                        {'range': [0, 40], 'color': "#fee2e2"},
                        {'range': [40, 70], 'color': "#fef3c7"},
                        {'range': [70, 100], 'color': "#d1fae5"}
                    ],
                }
            ))
            fig_gauge.update_layout(
                height=380, 
                margin=dict(l=20, r=20, t=60, b=20),
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            if prediction_pct >= 75:
                st.markdown(f'''<div class="success-box">
                    <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🎉</div>
                    <div style='font-size: 0.9rem; font-weight: 600; letter-spacing: 2px; color: #16a34a;'>EXCELLENT CHANCE</div>
                    <div style='font-size: 3.5rem; font-weight: 800; margin: 0.5rem 0; color: #14532d;'>{prediction_pct:.1f}%</div>
                    <div style='font-size: 1rem; color: #166534; font-weight: 500;'>Strong Application Profile</div>
                    <div style='font-size: 0.9rem; color: #16a34a; margin-top: 0.5rem;'>You have great chances of admission!</div>
                </div>''', unsafe_allow_html=True)
            elif prediction_pct >= 50:
                st.markdown(f'''<div class="info-box">
                    <div style='font-size: 3rem; margin-bottom: 0.5rem;'>👍</div>
                    <div style='font-size: 0.9rem; font-weight: 600; letter-spacing: 2px; color: #2563eb;'>MODERATE CHANCE</div>
                    <div style='font-size: 3.5rem; font-weight: 800; margin: 0.5rem 0; color: #1e3a8a;'>{prediction_pct:.1f}%</div>
                    <div style='font-size: 1rem; color: #1e40af; font-weight: 500;'>Competitive Application</div>
                    <div style='font-size: 0.9rem; color: #2563eb; margin-top: 0.5rem;'>Room for improvement exists</div>
                </div>''', unsafe_allow_html=True)
            else:
                st.markdown(f'''<div class="warning-box">
                    <div style='font-size: 3rem; margin-bottom: 0.5rem;'>⚠️</div>
                    <div style='font-size: 0.9rem; font-weight: 600; letter-spacing: 2px; color: #d97706;'>NEEDS IMPROVEMENT</div>
                    <div style='font-size: 3.5rem; font-weight: 800; margin: 0.5rem 0; color: #78350f;'>{prediction_pct:.1f}%</div>
                    <div style='font-size: 1rem; color: #92400e; font-weight: 500;'>Consider Strengthening Profile</div>
                    <div style='font-size: 0.9rem; color: #d97706; margin-top: 0.5rem;'>Focus on key improvement areas</div>
                </div>''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Metrics
        st.markdown('<div class="section-header">📈 Profile Metrics</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📚 Academic Score", f"{features_dict['Academic_Score']:.1f}/100",
                      delta=f"{features_dict['Academic_Score']-75:.1f} vs avg")
        with col2:
            st.metric("📝 Application", f"{features_dict['Application_Strength']:.1f}/100",
                      delta=f"{features_dict['Application_Strength']-70:.1f} vs avg")
        with col3:
            st.metric("🎯 Profile Strength", f"{features_dict['Profile_Strength']:.1f}",
                      delta=f"{features_dict['Profile_Strength']-72:.1f} vs avg")
        with col4:
            st.metric("⭐ Overall Score", f"{features_dict['Total_Weighted_Score']:.1f}",
                      delta=f"{features_dict['Total_Weighted_Score']-72:.1f}")
        
        st.markdown("---")
        
        # Radar Chart
        st.markdown('<div class="section-header">🎯 Profile Radar Analysis</div>', unsafe_allow_html=True)
        
        categories = ['GRE', 'TOEFL', 'CGPA', 'SOP', 'LOR', 'Research', 'Univ Rating']
        values = [gre/340*100, toefl/120*100, cgpa/10*100, sop/5*100, 
                  lor/5*100, research*100, univ_rating/5*100]
        avg_values = [92, 88, 85, 70, 72, 60, 60]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=avg_values, theta=categories, fill='toself',
            name='Average Student', line_color='#94a3b8',
            fillcolor='rgba(148, 163, 184, 0.2)'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=values, theta=categories, fill='toself',
            name='Your Profile', line_color='#4f46e5',
            fillcolor='rgba(79, 70, 229, 0.3)'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True, height=450,
            paper_bgcolor='rgba(0,0,0,0)',
            title="<b>Your Profile vs Average Student</b>"
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    # ============================================================
    # TAB 2: SHAP EXPLANATION
    # ============================================================
    with tab2:
        st.markdown('<div class="section-header">🔍 Why This Prediction?</div>', unsafe_allow_html=True)
        
        st.info("💡 **SHAP Analysis** explains how each feature contributed to your prediction. Red reduces chance, Blue increases chance.")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        shap.plots.waterfall(
            shap.Explanation(
                values=shap_values[0],
                base_values=explainer.expected_value,
                data=input_df.iloc[0],
                feature_names=input_df.columns.tolist()
            ),
            show=False, max_display=10
        )
        plt.tight_layout()
        st.pyplot(fig)
        
        st.markdown("---")
        
        st.markdown('<div class="section-header">🏆 Top Contributing Factors</div>', unsafe_allow_html=True)
        
        shap_df = pd.DataFrame({
            'Feature': input_df.columns,
            'SHAP_Value': shap_values[0],
            'Feature_Value': input_df.iloc[0].values
        })
        shap_df['Abs_SHAP'] = shap_df['SHAP_Value'].abs()
        shap_df = shap_df.sort_values('Abs_SHAP', ascending=False).head(10)
        shap_df['Impact'] = shap_df['SHAP_Value'].apply(
            lambda x: '🟢 Positive' if x > 0 else '🔴 Negative'
        )
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            colors_list = ['#16a34a' if v > 0 else '#dc2626' for v in shap_df['SHAP_Value']]
            fig = go.Figure(go.Bar(
                x=shap_df['SHAP_Value'], y=shap_df['Feature'],
                orientation='h', marker_color=colors_list,
                text=[f"{v:+.4f}" for v in shap_df['SHAP_Value']],
                textposition='outside'
            ))
            fig.update_layout(
                title="<b>Top 10 Feature Contributions</b>",
                xaxis_title="SHAP Value (Impact)",
                yaxis={'categoryorder': 'total ascending'},
                height=500, showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='#fafafa'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📋 Impact Details")
            display_df = shap_df[['Feature', 'Feature_Value', 'Impact']].head(10)
            display_df['Feature_Value'] = display_df['Feature_Value'].round(3)
            st.dataframe(display_df, use_container_width=True, hide_index=True, height=500)
    
    # ============================================================
    # TAB 3: ANALYTICS
    # ============================================================
    with tab3:
        st.markdown('<div class="section-header">📈 Comparative Analytics</div>', unsafe_allow_html=True)
        
        st.markdown("### Your Percentile Ranking")
        
        target_col = [col for col in dataset.columns if 'Admit' in col][0]
        
        col1, col2, col3 = st.columns(3)
        
        gre_percentile = (dataset['GRE Score'] < gre).sum() / len(dataset) * 100
        toefl_percentile = (dataset['TOEFL Score'] < toefl).sum() / len(dataset) * 100
        cgpa_percentile = (dataset['CGPA'] < cgpa).sum() / len(dataset) * 100
        
        with col1:
            st.metric("📊 GRE Percentile", f"{gre_percentile:.1f}%",
                      f"Better than {gre_percentile:.0f}% students")
        with col2:
            st.metric("📊 TOEFL Percentile", f"{toefl_percentile:.1f}%",
                      f"Better than {toefl_percentile:.0f}% students")
        with col3:
            st.metric("📊 CGPA Percentile", f"{cgpa_percentile:.1f}%",
                      f"Better than {cgpa_percentile:.0f}% students")
        
        st.markdown("---")
        
        st.markdown("### 📊 Where You Stand")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=dataset['CGPA'], nbinsx=30, 
                                        marker_color='#94a3b8', name='All Students', opacity=0.7))
            fig.add_vline(x=cgpa, line_dash="dash", line_color="#4f46e5", 
                          line_width=3, annotation_text=f"You: {cgpa}")
            fig.update_layout(title="<b>CGPA Distribution</b>", height=350,
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#fafafa',
                              showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=dataset['GRE Score'], nbinsx=30,
                                        marker_color='#94a3b8', name='All Students', opacity=0.7))
            fig.add_vline(x=gre, line_dash="dash", line_color="#4f46e5",
                          line_width=3, annotation_text=f"You: {gre}")
            fig.update_layout(title="<b>GRE Score Distribution</b>", height=350,
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#fafafa',
                              showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("### 🎯 CGPA vs Admission Chance")
        
        fig = px.scatter(dataset, x='CGPA', y=target_col, 
                          color='Research', 
                          color_continuous_scale=['#94a3b8', '#4f46e5'])
        fig.add_scatter(x=[cgpa], y=[prediction], mode='markers',
                         marker=dict(size=25, color='#dc2626', symbol='star',
                                     line=dict(color='white', width=2)),
                         name='You', showlegend=True)
        fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='#fafafa')
        st.plotly_chart(fig, use_container_width=True)
    
    # ============================================================
    # TAB 4: RECOMMENDATIONS
    # ============================================================
    with tab4:
        st.markdown('<div class="section-header">💡 Personalized Recommendations</div>', unsafe_allow_html=True)
        
        recommendations = []
        if cgpa < 8.5:
            recommendations.append(("📚 Improve CGPA", 
                                    f"Current: {cgpa} | Target: 8.5+ | Impact: HIGHEST",
                                    "CGPA has the strongest correlation with admission. Even a 0.2 point increase can boost your chances significantly."))
        if gre < 320:
            recommendations.append(("📝 Boost GRE Score", 
                                    f"Current: {gre} | Target: 320+ | Impact: HIGH",
                                    "Focus on Quantitative and Verbal sections. Consider a retake if score is below 315."))
        if toefl < 108:
            recommendations.append(("🗣️ Strengthen TOEFL", 
                                    f"Current: {toefl} | Target: 108+ | Impact: MODERATE",
                                    "Practice speaking and writing sections. Take mock tests regularly."))
        if research == 0:
            recommendations.append(("🔬 Get Research Experience", 
                                    "Current: No | Target: Yes | Impact: SIGNIFICANT",
                                    "Research adds ~10% to your chances. Contact professors for research opportunities."))
        if sop < 4.0:
            recommendations.append(("✍️ Improve SOP", 
                                    f"Current: {sop} | Target: 4.0+ | Impact: MODERATE",
                                    "Get your SOP reviewed by mentors. Focus on unique experiences and clear goals."))
        if lor < 4.0:
            recommendations.append(("📄 Better LORs", 
                                    f"Current: {lor} | Target: 4.0+ | Impact: MODERATE",
                                    "Build strong relationships with professors early. Choose recommenders who know you well."))
        
        if not recommendations:
            st.success("🎉 **Your profile is EXCELLENT!** Focus on:\n\n"
                       "- Strong Statement of Purpose\n"
                       "- Well-crafted essays\n"
                       "- Interview preparation\n"
                       "- Application timing")
        else:
            for idx, (title, meta, desc) in enumerate(recommendations):
                with st.expander(f"{title} - {meta}", expanded=(idx < 2)):
                    st.write(desc)
        
        st.markdown("---")
        
        # What-If Analysis
        st.markdown('<div class="section-header">🔮 What-If Analysis</div>', unsafe_allow_html=True)
        st.info("See how improvements could boost your chances")
        
        col1, col2, col3 = st.columns(3)
        
        scenarios = [
            ("💯 Perfect CGPA", "CGPA = 9.5", {'cgpa': 9.5}),
            ("🏆 Add Research", "Research = Yes", {'research': 1}),
            ("⭐ All Perfect", "Everything Maxed", {'gre': 340, 'toefl': 120, 'cgpa': 9.5, 'research': 1})
        ]
        
        for col, (title, desc, changes) in zip([col1, col2, col3], scenarios):
            with col:
                new_gre = changes.get('gre', gre)
                new_toefl = changes.get('toefl', toefl)
                new_cgpa = changes.get('cgpa', cgpa)
                new_research = changes.get('research', research)
                
                new_features = engineer_features(new_gre, new_toefl, univ_rating, 
                                                    sop, lor, new_cgpa, new_research)
                new_input = pd.DataFrame([new_features])[feature_names]
                new_pred = model.predict(new_input)[0] * 100
                
                improvement = new_pred - prediction_pct
                
                st.metric(title, f"{new_pred:.1f}%", 
                          delta=f"+{improvement:.1f}% improvement")
                st.caption(desc)
        
        st.markdown("---")
        
        # Download Report
        st.markdown('<div class="section-header">📥 Download Full Report</div>', unsafe_allow_html=True)
        
        report_text = f"""
================================================
   ADMISSION PREDICTION REPORT
================================================

Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

------------------------------------------------
STUDENT PROFILE
------------------------------------------------
GRE Score         : {gre}
TOEFL Score       : {toefl}
CGPA              : {cgpa}
University Rating : {univ_rating}
SOP               : {sop}
LOR               : {lor}
Research          : {'Yes' if research else 'No'}

------------------------------------------------
PREDICTION
------------------------------------------------
Admission Chance  : {prediction_pct:.2f}%
Profile Tier      : {tier}
Overall Score     : {total_score:.1f}/100
Confidence        : {'HIGH' if prediction_pct >= 75 else 'MODERATE' if prediction_pct >= 50 else 'LOW'}

------------------------------------------------
PERCENTILE RANKINGS
------------------------------------------------
GRE Percentile    : {gre_percentile:.1f}%
TOEFL Percentile  : {toefl_percentile:.1f}%
CGPA Percentile   : {cgpa_percentile:.1f}%

------------------------------------------------
TOP CONTRIBUTING FACTORS
------------------------------------------------
{chr(10).join([f"{i+1}. {row['Feature']:25s} : {row['Impact']}" for i, (_, row) in enumerate(shap_df.head(5).iterrows())])}

------------------------------------------------
RECOMMENDATIONS
------------------------------------------------
{chr(10).join([f"- {t}: {d}" for t, m, d in recommendations]) if recommendations else 'Excellent Profile!'}

================================================
Developed by Manish Kumar
Powered by XGBoost + SHAP + Optuna
================================================
"""
        
        st.download_button(
            label="📥 Download Complete Report (TXT)",
            data=report_text,
            file_name=f"admission_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )

else:
    # WELCOME SCREEN
    st.markdown('<div class="section-header">✨ Welcome</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Accurate Predictions</div>
            <div class="feature-desc">
                Advanced XGBoost model with 90%+ accuracy trained on real admission data
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">33 Smart Features</div>
            <div class="feature-desc">
                Advanced feature engineering with interactions, ratios, and composite scores
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">SHAP Explainability</div>
            <div class="feature-desc">
                Understand exactly WHY each prediction was made with full transparency
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div class="section-header">📊 Model Performance</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎯 R² Score", "0.90+", "Higher is better")
    col2.metric("📉 RMSE", "0.05", "Lower is better")
    col3.metric("📊 MAPE", "5-7%", "Prediction error")
    col4.metric("🤖 Features", "33", "Engineered from 7")
    
    st.markdown("---")
    
    st.markdown('<div class="section-header">🔬 How It Works</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div style='font-size: 2rem;'>1️⃣</div>
            <div class="feature-title">Enter Details</div>
            <div class="feature-desc">Fill your academic profile in the sidebar</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div style='font-size: 2rem;'>2️⃣</div>
            <div class="feature-title">AI Analysis</div>
            <div class="feature-desc">Model processes 33 engineered features</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div style='font-size: 2rem;'>3️⃣</div>
            <div class="feature-title">Get Prediction</div>
            <div class="feature-desc">Instant admission chance with explanation</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div style='font-size: 2rem;'>4️⃣</div>
            <div class="feature-title">Improve Profile</div>
            <div class="feature-desc">Get personalized recommendations</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div class="section-header">🎓 Sample Profiles</div>', unsafe_allow_html=True)
    
    sample_data = pd.DataFrame({
        'Profile Type': ['🏆 High Achiever', '👍 Average Student', '⭐ Strong Applicant'],
        'GRE': [335, 315, 325],
        'TOEFL': [115, 105, 112],
        'CGPA': [9.5, 8.0, 8.8],
        'Research': ['✅ Yes', '❌ No', '✅ Yes'],
        'Expected Chance': ['~92%', '~68%', '~85%']
    })
    st.dataframe(sample_data, use_container_width=True, hide_index=True)
    
    st.info("👈 **Enter your details in the sidebar** and click **'PREDICT MY CHANCES'** to get your personalized prediction!")

# ============================================================
#  FOOTER
# ============================================================
st.markdown("""
<div class="footer">
    <div class="footer-title">🎓 Admission Predictor Pro</div>
    <div class="footer-text">Powered by XGBoost + SHAP + Optuna</div>
    <div class="footer-text">Developed by <span class="developer-tag">Manish Kumar</span></div>
</div>
""", unsafe_allow_html=True)