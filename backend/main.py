
from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

# --------------------------------------------------
# 1. Initialize FastAPI
# --------------------------------------------------

app = FastAPI(
    title="Food Surplus and Spoilage Risk Predictor",
    description="API for predicting food waste using a trained ML model.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:4173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# 2. Load the trained machine learning model
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "food_waste_model.joblib"

model = None

try:
    model = joblib.load(MODEL_PATH)
    print("Food waste prediction model loaded successfully.")

except Exception as error:
    print(f"Model loading failed: {error}")


# --------------------------------------------------
# 3. Define input validation
# --------------------------------------------------

class PredictionInput(BaseModel):

    meals_served: int = Field(gt=0)
    kitchen_staff: int = Field(ge=0)

    temperature_C: float
    humidity_percent: float = Field(ge=0, le=100)

    day_of_week: int = Field(ge=0, le=6)
    special_event: int = Field(ge=0, le=1)

    past_waste_kg: float = Field(ge=0)

    staff_experience: str = Field(min_length=1)
    waste_category: str = Field(min_length=1)

    month: int = Field(ge=1, le=12)
    day_of_month: int = Field(ge=1, le=31)


# --------------------------------------------------
# 4. Root endpoint
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Food Surplus and Spoilage Risk Predictor API",
        "status": "running"
    }


# --------------------------------------------------
# 5. Health check endpoint
# --------------------------------------------------

@app.get("/health")
def health_check():

    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Prediction model is not available."
        )

    return {
        "status": "healthy",
        "model_loaded": True,
        "model_name": "Linear Regression",
        "target": "food_waste_kg"
    }


# --------------------------------------------------
# 6. Food waste prediction endpoint
# --------------------------------------------------

@app.post("/predict")
def predict_food_waste(input_data: PredictionInput):

    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Prediction model is not available."
        )

    try:

        # Convert the input into a DataFrame.
        # The column names match the model's training features.

        input_dict = input_data.model_dump()

        input_dict["staff_experience"] = (
            input_dict["staff_experience"].strip().lower()
        )

        input_dict["waste_category"] = (
            input_dict["waste_category"].strip().lower()
        )

        input_df = pd.DataFrame([input_dict])

        # Generate prediction
        prediction = model.predict(input_df)[0]

        return {
            "predicted_food_waste_kg": round(float(prediction), 2),
            "unit": "kg",
            "model": "Linear Regression"
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )
