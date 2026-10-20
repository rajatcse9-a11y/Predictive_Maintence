import requests
import streamlit as st
import pandas as pd


# =====================================================
# CONFIGURATION
# =====================================================

# API_URL = "http://127.0.0.1:8000/predict"
import os

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/predict"
)

st.set_page_config(
    page_title="Predictive Maintenance | AI Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


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
    st.caption("Backend: FastAPI")
    st.caption("Frontend: Streamlit")

    st.divider()

    st.markdown("### API Endpoint")

    st.code(API_URL, language="text")

    if st.button("🔌 Check API Connection"):

        try:
            health_response = requests.get(
                API_URL.rsplit("/", 1)[0] + "/health",
                timeout=3
            )

            if health_response.status_code == 200:
                st.success("API is reachable.")

            elif health_response.status_code == 404:
                st.warning(
                    "API server is reachable, but /health "
                    "route is not configured."
                )

            else:
                st.warning(
                    f"API returned HTTP "
                    f"{health_response.status_code}."
                )

        except requests.exceptions.RequestException:
            st.error("Cannot connect to the API server.")


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
        <div class="info-value">FastAPI</div>
        <div class="info-caption">
            Connected through REST API
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
# PREDICTION REQUEST
# =====================================================

if submitted:

    data = {
        "machine_type": machine_type,
        "air_temperature": air_temperature,
        "process_temperature": process_temperature,
        "rotational_speed": rotational_speed,
        "torque": torque,
        "tool_wear": tool_wear
    }

    with st.spinner(
        "Analyzing sensor readings and evaluating machine health..."
    ):

        try:

            response = requests.post(
                API_URL,
                json=data,
                timeout=15
            )

            if response.status_code == 200:

                result = response.json()

                # Preserve your existing FastAPI response schema.
                prediction = int(result["machine_failure"])
                probability = float(
                    result["failure_probability"]
                )
                risk = str(result["risk_level"]).upper()
                recommendation = str(
                    result["recommendation"]
                )

                # Avoid displaying an invalid percentage.
                if not 0 <= probability <= 100:
                    st.error(
                        "API returned an invalid failure "
                        "probability. Expected a value from 0 to 100."
                    )
                    st.stop()

                if prediction not in (0, 1):
                    st.error(
                        "API returned an invalid machine_failure value."
                    )
                    st.stop()

                st.divider()

                st.markdown(
                    '<div class="section-title">'
                    '🧠 AI Prediction Results'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="section-description">'
                    'Results returned by your existing FastAPI model.'
                    '</div>',
                    unsafe_allow_html=True
                )

                # ---------------------------------
                # RESULT METRICS
                # ---------------------------------

                res1, res2, res3 = st.columns(3)

                with res1:
                    st.metric(
                        "Failure Probability",
                        f"{probability:.2f}%"
                    )

                with res2:
                    st.metric(
                        "Risk Level",
                        risk
                    )

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
                    int(round(probability)),
                    text=f"Estimated failure probability: "
                         f"{probability:.2f}%"
                )

                # ---------------------------------
                # MACHINE STATUS
                # ---------------------------------

                st.markdown("#### 🏭 Machine Health Assessment")

                if prediction == 1 or risk == "HIGH":

                    st.error(
                        "🚨 HIGH ATTENTION REQUIRED\n\n"
                        "The model indicates a potential machine "
                        "failure risk. Review the maintenance "
                        "recommendation and inspect the machine."
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
                        "The model currently indicates a lower "
                        "failure risk. Continue routine monitoring "
                        "and follow the scheduled maintenance plan."
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
                        "failure_probability": probability,
                        "risk_level": risk,
                        "recommendation": recommendation
                    })

                # ---------------------------------
                # DOWNLOAD RESULT
                # ---------------------------------

                report = pd.DataFrame([{
                    "machine_type": machine_type,
                    "air_temperature": air_temperature,
                    "process_temperature": process_temperature,
                    "rotational_speed": rotational_speed,
                    "torque": torque,
                    "tool_wear": tool_wear,
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

            else:

                st.error(
                    f"API Error: HTTP {response.status_code}"
                )

                with st.expander("View API Error Details"):
                    st.code(response.text)

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to FastAPI. "
                "Check whether the backend server is running "
                "and the API URL is correct."
            )

            st.code(
                "uvicorn api:app --reload",
                language="bash"
            )

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ The API request timed out. "
                "Check the backend and try again."
            )

        except (KeyError, TypeError, ValueError):

            st.error(
                "The API response format is invalid or contains "
                "unexpected values. Verify the response keys "
                "and data types in api.py."
            )

        except requests.exceptions.RequestException as e:

            st.error(f"Request failed: {e}")


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown("""
<div class="footer">
    Predictive Maintenance System | AI & Machine Learning
    <br>
    Built with Python, Streamlit and FastAPI
    <br>
    Model predictions are estimates and should be reviewed
    alongside real machine inspections and maintenance procedures.
</div>
""", unsafe_allow_html=True)
