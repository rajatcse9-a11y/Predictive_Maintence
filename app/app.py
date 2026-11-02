from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


# =====================================================
# CONFIGURATION
# =====================================================

# Project root (app.py agar app/ folder ke andar hai toh ek level upar)
# Agar app.py project root mein hi hai, toh .parent.parent ko .parent kar do.
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "model.pkl"

# Fallback: agar app.py root mein rakhi ho
if not MODEL_PATH.exists():
    MODEL_PATH = Path(__file__).resolve().parent / "models" / "model.pkl"

# Model jo 11 features expect karta hai (naam + order EXACT yahi hona chahiye)
FEATURE_COLUMNS = [
    "Air_temperature_K",
    "Process_temperature_K",
    "Rotational_speed_rpm",
    "Torque_Nm",
    "Tool_wear_min",
    "Type_H",
    "Type_L",
    "Type_M",
    "Temperature_Difference",
    "Power",
    "Torque_ToolWear",
]

# ⚠️ Engineered features ke formulas training notebook wale hi hone chahiye.
# Default assumptions:
#   Temperature_Difference = Process_temperature_K - Air_temperature_K
#   Power                  = Torque_Nm * Rotational_speed_rpm
#   Torque_ToolWear        = Torque_Nm * Tool_wear_min
# Agar notebook mein Power rad/s (2*pi*rpm/60) mein bana tha, toh True kar do.
POWER_IN_RAD_PER_SEC = False

# ⚠️ api/main.py wale thresholds yahan copy kar do
MEDIUM_RISK_THRESHOLD = 30.0   # % se upar = MEDIUM
HIGH_RISK_THRESHOLD = 60.0     # % se upar = HIGH

st.set_page_config(
    page_title="Predictive Maintenance | AI Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# MODEL LOADING & PREDICTION
# =====================================================

@st.cache_resource(show_spinner="Model load ho raha hai...")
def load_model(path: str):
    """Model sirf ek baar load hota hai, har click pe nahi."""
    return joblib.load(path)


def get_risk_level(probability: float) -> str:
    if probability >= HIGH_RISK_THRESHOLD:
        return "HIGH"
    if probability >= MEDIUM_RISK_THRESHOLD:
        return "MEDIUM"
    return "LOW"


def get_recommendation(prediction: int, risk: str) -> str:
    # ⚠️ Apne api/main.py ke text se replace kar sakte ho
    if prediction == 1 or risk == "HIGH":
        return (
            "Immediate inspection recommended. Check tool wear, "
            "torque load and cooling before continuing operation."
        )
    if risk == "MEDIUM":
        return (
            "Schedule a preventive inspection soon and monitor "
            "temperature and torque readings closely."
        )
    return "Machine is operating normally. Continue routine monitoring."


def predict_failure(model, inputs: dict):
    air = float(inputs["air_temperature"])
    proc = float(inputs["process_temperature"])
    rpm = float(inputs["rotational_speed"])
    torque = float(inputs["torque"])
    wear = float(inputs["tool_wear"])
    mtype = inputs["machine_type"]

    # Engineered features
    temp_diff = proc - air
    if POWER_IN_RAD_PER_SEC:
        power = torque * (rpm * 2 * 3.141592653589793 / 60)
    else:
        power = torque * rpm
    torque_toolwear = torque * wear

    row = {
        "Air_temperature_K": air,
        "Process_temperature_K": proc,
        "Rotational_speed_rpm": rpm,
        "Torque_Nm": torque,
        "Tool_wear_min": wear,
        "Type_H": int(mtype == "H"),
        "Type_L": int(mtype == "L"),
        "Type_M": int(mtype == "M"),
        "Temperature_Difference": temp_diff,
        "Power": power,
        "Torque_ToolWear": torque_toolwear,
    }

    # Column order model ke hisaab se
    X = pd.DataFrame([row])[FEATURE_COLUMNS]

    prediction = int(model.predict(X)[0])

    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(X)[0][1]) * 100
    else:
        probability = 100.0 if prediction == 1 else 0.0

    risk = get_risk_level(probability)
    recommendation = get_recommendation(prediction, risk)

    return prediction, probability, risk, recommendation


# =====================================================
# PROFESSIONAL UI STYLING
# =====================================================

st.markdown("""
<style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #0b1120;
        color: #e5e7eb;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #263449;
    }

    [data-testid="stHeader"] {
        background: rgba(11, 17, 32, 0.95);
    }

    .hero {
        background: linear-gradient(
            120deg,
            #172554 0%,
            #111827 55%,
            #164e63 100%
        );
        padding: 30px;
        border-radius: 18px;
        border: 1px solid #334155;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: #f8fafc;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .hero p {
        color: #cbd5e1;
        font-size: 14px;
        margin-bottom: 0;
    }

    .section-title {
        color: #f1f5f9;
        font-size: 20px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 5px;
    }

    .section-description {
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 18px;
    }

    .info-card {
        background: #111c30;
        border: 1px solid #263449;
        padding: 20px;
        border-radius: 14px;
        min-height: 110px;
        margin-bottom: 12px;
    }

    .info-label {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .info-value {
        color: #f8fafc;
        font-size: 25px;
        font-weight: 800;
        margin-top: 8px;
    }

    .info-caption {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 5px;
    }

    .result-panel {
        background: #111c30;
        border: 1px solid #263449;
        padding: 25px;
        border-radius: 16px;
        margin-top: 15px;
        margin-bottom: 20px;
    }

    .status-normal {
        color: #4ade80;
        font-size: 25px;
        font-weight: 800;
    }

    .status-danger {
        color: #f87171;
        font-size: 25px;
        font-weight: 800;
    }

    .status-warning {
        color: #fbbf24;
        font-size: 25px;
        font-weight: 800;
    }

    .small-muted {
        color: #94a3b8;
        font-size: 12px;
    }

    div.stButton > button {
        width: 100%;
        background: linear-gradient(
            90deg,
            #2563eb,
            #0891b2
        );
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        min-height: 48px;
        transition: 0.2s ease;
    }

    div.stButton > button:hover {
        background: linear-gradient(
            90deg,
            #1d4ed8,
            #0e7490
        );
        color: white;
        border: none;
    }

    div[data-testid="stMetric"] {
        background: #111c30;
        border: 1px solid #263449;
        padding: 16px;
        border-radius: 12px;
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc;
    }

    hr {
        border-color: #263449;
    }

    .footer {
        color: #64748b;
        text-align: center;
        font-size: 12px;
        padding: 20px 0;
    }
</style>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("## ⚙️ MachineAI")

    st.caption("PREDICTIVE INTELLIGENCE")

    st.divider()

    st.markdown("### Dashboard")

    st.markdown("🖥️ Machine Monitoring")
    st.markdown("🧠 AI Failure Prediction")
    st.markdown("🛠️ Maintenance Insights")

    st.divider()

    st.markdown("### System Information")

    st.caption("Model: Predictive Maintenance")
    st.caption("Inference: Local model")
    st.caption("Frontend: Streamlit")

    st.divider()

    st.markdown("### Model File")

    st.code(MODEL_PATH.name, language="text")

    if st.button("🔌 Check Model Status"):
        if not MODEL_PATH.exists():
            st.error("model.pkl nahi mila. Path check karo.")
        else:
            try:
                load_model(str(MODEL_PATH))
                st.success("Model loaded successfully.")
            except Exception as e:
                st.error(f"Model load nahi hua: {e}")


# =====================================================
# HERO SECTION
# =====================================================

st.markdown("""
<div class="hero">
    <h1>⚙️ Predictive Maintenance Dashboard</h1>
    <p>
        AI-powered machine health monitoring and failure risk
        assessment using industrial sensor data.
    </p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# DASHBOARD OVERVIEW
# =====================================================

st.markdown("### 📊 Monitoring Overview")

top1, top2, top3 = st.columns(3)

with top1:
    st.markdown("""
    <div class="info-card">
        <div class="info-label">System</div>
        <div class="info-value">AI Enabled</div>
        <div class="info-caption">
            Machine failure prediction
        </div>
    </div>
    """, unsafe_allow_html=True)

with top2:
    st.markdown("""
    <div class="info-card">
        <div class="info-label">Input Features</div>
        <div class="info-value">06 Sensors</div>
        <div class="info-caption">
            Machine and operational parameters
        </div>
    </div>
    """, unsafe_allow_html=True)

with top3:
    st.markdown("""
    <div class="info-card">
        <div class="info-label">Inference Engine</div>
        <div class="info-value">Local Model</div>
        <div class="info-caption">
            Loaded directly from model.pkl
        </div>
    </div>
    """, unsafe_allow_html=True)


st.divider()


# =====================================================
# MACHINE INPUT FORM
# =====================================================

st.markdown(
    '<div class="section-title">🛠️ Machine Configuration</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Enter the current operating parameters of the machine. '
    'The model will evaluate these readings after submission.'
    '</div>',
    unsafe_allow_html=True
)


with st.form("machine_prediction_form"):

    st.markdown("#### 🏭 Machine Identification")

    machine_type = st.selectbox(
        "Machine Type",
        options=["L", "M", "H"],
        format_func=lambda x: {
            "L": "L — Low",
            "M": "M — Medium",
            "H": "H — High"
        }[x],
        help="Select the machine type used by your trained model."
    )

    st.divider()

    st.markdown("#### 🌡️ Temperature Monitoring")

    temp1, temp2 = st.columns(2)

    with temp1:

        air_temperature = st.number_input(
            "Air Temperature (K)",
            min_value=250.0,
            max_value=350.0,
            value=300.0,
            step=0.1,
            help="Operating air temperature in Kelvin."
        )

    with temp2:

        process_temperature = st.number_input(
            "Process Temperature (K)",
            min_value=250.0,
            max_value=400.0,
            value=310.0,
            step=0.1,
            help="Operating process temperature in Kelvin."
        )

    st.divider()

    st.markdown("#### ⚡ Mechanical Parameters")

    mech1, mech2, mech3 = st.columns(3)

    with mech1:

        rotational_speed = st.number_input(
            "Rotational Speed (RPM)",
            min_value=500,
            max_value=3000,
            value=1500,
            step=10
        )

    with mech2:

        torque = st.number_input(
            "Torque (Nm)",
            min_value=0.0,
            max_value=100.0,
            value=40.0,
            step=0.5
        )

    with mech3:

        tool_wear = st.number_input(
            "Tool Wear (Minutes)",
            min_value=0,
            max_value=300,
            value=100,
            step=1
        )

    st.divider()

    submitted = st.form_submit_button(
        "🔍 ANALYZE MACHINE HEALTH",
        use_container_width=True
    )


# =====================================================
# SENSOR VISUALIZATION
# =====================================================

st.divider()

st.markdown("### 📈 Current Sensor Readings")

sensor_df = pd.DataFrame({
    "Parameter": [
        "Air Temperature",
        "Process Temperature",
        "Rotational Speed",
        "Torque",
        "Tool Wear"
    ],
    "Reading": [
        air_temperature,
        process_temperature,
        rotational_speed,
        torque,
        tool_wear
    ],
    "Unit": [
        "K",
        "K",
        "RPM",
        "Nm",
        "Minutes"
    ]
})

st.dataframe(
    sensor_df,
    use_container_width=True,
    hide_index=True
)


# =====================================================
# PREDICTION
# =====================================================

if submitted:

    inputs = {
        "machine_type": machine_type,
        "air_temperature": air_temperature,
        "process_temperature": process_temperature,
        "rotational_speed": rotational_speed,
        "torque": torque,
        "tool_wear": tool_wear,
    }

    if not MODEL_PATH.exists():
        st.error(f"Model file nahi mili: {MODEL_PATH}")
        st.stop()

    try:
        model = load_model(str(MODEL_PATH))

        # Agar model ko feature names yaad hain, toh match check kar lo
        expected = getattr(model, "feature_names_in_", None)
        if expected is not None and list(expected) != FEATURE_COLUMNS:
            st.error("FEATURE_COLUMNS model ke columns se match nahi karte.")
            st.write("Model expects:", list(expected))
            st.write("App ne diye:", FEATURE_COLUMNS)
            st.stop()

        with st.spinner("Analyzing sensor readings..."):
            prediction, probability, risk, recommendation = predict_failure(
                model, inputs
            )

    except Exception as e:
        st.error("Prediction fail hui. Neeche error details dekho.")
        with st.expander("View Error Details"):
            st.code(repr(e))
        st.stop()

    st.divider()

    st.markdown(
        '<div class="section-title">🧠 AI Prediction Results</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Results generated by the trained model.'
        '</div>',
        unsafe_allow_html=True
    )

    # ---------------------------------
    # RESULT METRICS
    # ---------------------------------

    res1, res2, res3 = st.columns(3)

    with res1:
        st.metric("Failure Probability", f"{probability:.2f}%")

    with res2:
        st.metric("Risk Level", risk)

    with res3:
        st.metric(
            "Machine Failure Prediction",
            "Failure" if prediction == 1 else "Normal"
        )

    # ---------------------------------
    # PROBABILITY VISUALIZATION
    # ---------------------------------

    st.markdown("#### Failure Risk Indicator")

    st.progress(
        int(round(min(max(probability, 0), 100))),
        text=f"Estimated failure probability: {probability:.2f}%"
    )

    # ---------------------------------
    # MACHINE STATUS
    # ---------------------------------

    st.markdown("#### 🏭 Machine Health Assessment")

    if prediction == 1 or risk == "HIGH":

        st.error(
            "🚨 HIGH ATTENTION REQUIRED\n\n"
            "The model indicates a potential machine failure risk. "
            "Review the maintenance recommendation and inspect "
            "the machine."
        )

    elif risk == "MEDIUM":

        st.warning(
            "⚠️ MODERATE RISK\n\n"
            "The model indicates an elevated risk level. "
            "Monitor the machine and plan an inspection "
            "according to your maintenance procedure."
        )

    else:

        st.success(
            "✅ NORMAL STATUS\n\n"
            "The model currently indicates a lower failure risk. "
            "Continue routine monitoring and follow the scheduled "
            "maintenance plan."
        )

    # ---------------------------------
    # RECOMMENDATION PANEL
    # ---------------------------------

    st.markdown("#### 🛠️ Maintenance Recommendation")

    st.markdown(
        f"""
        <div class="result-panel">
            <div class="info-label">
                MODEL-GENERATED RECOMMENDATION
            </div>
            <div style="
                color:#e2e8f0;
                font-size:16px;
                line-height:1.8;
                margin-top:12px;
            ">
                {recommendation}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------------------------
    # RESULT DETAILS
    # ---------------------------------

    with st.expander("📋 View Prediction Details"):

        st.json({
            "machine_type": machine_type,
            "machine_failure": prediction,
            "failure_probability": round(probability, 4),
            "risk_level": risk,
            "recommendation": recommendation
        })

    # ---------------------------------
    # DOWNLOAD RESULT
    # ---------------------------------

    report = pd.DataFrame([{
        **inputs,
        "machine_failure": prediction,
        "failure_probability": probability,
        "risk_level": risk,
        "recommendation": recommendation
    }])

    st.download_button(
        label="📥 Download Prediction Report (CSV)",
        data=report.to_csv(index=False).encode("utf-8"),
        file_name="machine_prediction_report.csv",
        mime="text/csv",
        use_container_width=True
    )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown("""
<div class="footer">
    Predictive Maintenance System | AI & Machine Learning
    <br>
    Built with Python, Streamlit and scikit-learn
    <br>
    Model predictions are estimates and should be reviewed
    alongside real machine inspections and maintenance procedures.
</div>
""", unsafe_allow_html=True)