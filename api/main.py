from fastapi import FastAPI
from pydantic import BaseModel, Field
import pandas as pd
import joblib
import sys
from pathlib import Path


# =====================================================
# PROJECT PATH CONFIGURATION
# =====================================================

PROJECT_ROOT = next(
    (
        p
        for p in [Path.cwd(), *Path.cwd().parents]
        if (p / "utils" / "paths.py").exists()
    ),
    None
)

if PROJECT_ROOT is None:
    raise RuntimeError(
        "Project root not found. "
        "Could not locate utils/paths.py."
    )

sys.path.insert(0, str(PROJECT_ROOT))

from utils.paths import MODEL_PATH


# =====================================================
# CREATE FASTAPI APP
# =====================================================

app = FastAPI(
    title="Predictive Maintenance API",
    description="AI-powered machine failure prediction API",
    version="1.1.0"
)


# =====================================================
# LOAD TRAINED MODEL
# =====================================================

model = joblib.load(MODEL_PATH)


# =====================================================
# INPUT VALIDATION
# =====================================================

class MachineData(BaseModel):

    machine_type: str = Field(
        ...,
        pattern="^[LMH]$",
        description="Machine type: L, M or H"
    )

    air_temperature: float = Field(
        ..., ge=250, le=350
    )

    process_temperature: float = Field(
        ..., ge=250, le=400
    )

    rotational_speed: float = Field(
        ..., ge=500, le=3000
    )

    torque: float = Field(
        ..., ge=0, le=100
    )

    tool_wear: float = Field(
        ..., ge=0, le=300
    )


# =====================================================
# ROOT ENDPOINT
# =====================================================

@app.get("/")
def home():

    return {
        "message": "Predictive Maintenance API is running",
        "status": "healthy",
        "docs": "/docs"
    }


# =====================================================
# HEALTH CHECK ENDPOINT
# =====================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "message": "Predictive Maintenance API is running",
        "model_loaded": model is not None
    }


# =====================================================
# PREDICTION ENDPOINT
# =====================================================

@app.post("/predict")
def predict(data: MachineData):

    # -----------------------------------------------
    # FEATURE ENGINEERING
    # -----------------------------------------------

    temperature_difference = (
        data.process_temperature
        - data.air_temperature
    )

    power = (
        data.torque
        * data.rotational_speed
    )

    torque_toolwear = (
        data.torque
        * data.tool_wear
    )


    # -----------------------------------------------
    # MACHINE TYPE ENCODING
    # -----------------------------------------------

    type_h = 1 if data.machine_type == "H" else 0
    type_l = 1 if data.machine_type == "L" else 0
    type_m = 1 if data.machine_type == "M" else 0


    # -----------------------------------------------
    # CREATE INPUT DATAFRAME
    # -----------------------------------------------

    input_data = pd.DataFrame([{

        "Air_temperature_K": data.air_temperature,

        "Process_temperature_K": data.process_temperature,

        "Rotational_speed_rpm": data.rotational_speed,

        "Torque_Nm": data.torque,

        "Tool_wear_min": data.tool_wear,

        "Type_H": type_h,

        "Type_L": type_l,

        "Type_M": type_m,

        "Temperature_Difference": temperature_difference,

        "Power": power,

        "Torque_ToolWear": torque_toolwear

    }])


    # -----------------------------------------------
    # MODEL PREDICTION
    # -----------------------------------------------

    probability = float(
        model.predict_proba(input_data)[0][1]
    )

    prediction = 1 if probability >= 0.5 else 0


    # -----------------------------------------------
    # RISK CLASSIFICATION
    # -----------------------------------------------

    if probability >= 0.70:

        risk = "HIGH"

        recommendation = (
            "Maintenance required immediately."
        )

    elif probability >= 0.40:

        risk = "MEDIUM"

        recommendation = (
            "Schedule maintenance soon."
        )

    else:

        risk = "LOW"

        recommendation = (
            "Machine condition looks normal."
        )


    # -----------------------------------------------
    # API RESPONSE
    # -----------------------------------------------

    return {

        "machine_failure": prediction,

        "failure_probability": round(
            probability * 100, 2
        ),

        "risk_level": risk,

        "recommendation": recommendation

    }

