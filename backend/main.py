
from pathlib import Path
from datetime import datetime, timezone

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import firestore


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
        "http://localhost:4173",
        "https://food-wise-52yf6k4bi-saniyasawal.vercel.app",
        "https://food-wise-ai-rose.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# --------------------------------------------------
# 2. Initialize Firestore
# --------------------------------------------------

db = None
history_collection = None

try:
    db = firestore.Client()
    history_collection = db.collection("prediction_history")
    print("Firestore connected successfully.")

except Exception as error:
    print(f"Firestore connection failed: {error}")


# --------------------------------------------------
# 3. Load the trained machine learning model
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
# 4. Define input validation
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
# 5. Root endpoint
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Food Surplus and Spoilage Risk Predictor API",
        "status": "running"
    }


# --------------------------------------------------
# 6. Health check endpoint
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
        "target": "food_waste_kg",
        "firestore_connected": db is not None
    }


# --------------------------------------------------
# 7. Food waste prediction endpoint
# --------------------------------------------------

@app.post("/predict")
def predict_food_waste(input_data: PredictionInput):

    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Prediction model is not available."
        )

    try:

        input_dict = input_data.model_dump()

        input_dict["staff_experience"] = (
            input_dict["staff_experience"].strip().lower()
        )

        input_dict["waste_category"] = (
            input_dict["waste_category"].strip().lower()
        )

        input_df = pd.DataFrame([input_dict])

        prediction = float(model.predict(input_df)[0])
        prediction = round(prediction, 2)

        # Save the prediction to Firestore
        history_saved = False
        prediction_id = None

        if history_collection is not None:

            try:
                record = {
                    "input_data": input_dict,
                    "predicted_food_waste_kg": prediction,
                    "unit": "kg",
                    "model": "Linear Regression",
                    "created_at": datetime.now(timezone.utc)
                }

                document_ref = history_collection.add(record)[1]

                prediction_id = document_ref.id
                history_saved = True

                print(f"Prediction saved: {prediction_id}")

            except Exception as error:
                print(f"Firestore save failed: {error}")

        return {
            "prediction_id": prediction_id,
            "predicted_food_waste_kg": prediction,
            "unit": "kg",
            "model": "Linear Regression",
            "history_saved": history_saved
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )


# --------------------------------------------------
# 8. Retrieve prediction history
# --------------------------------------------------

@app.get("/history")
def get_prediction_history():

    if history_collection is None:
        raise HTTPException(
            status_code=503,
            detail="Firestore is not available."
        )

    try:

        records = (
            history_collection
            .order_by("created_at", direction=firestore.Query.DESCENDING)
            .stream()
        )

        history = []

        for document in records:

            record = document.to_dict()

            created_at = record.get("created_at")

            history.append({
                "id": document.id,
                "input_data": record.get("input_data", {}),
                "predicted_food_waste_kg": record.get(
                    "predicted_food_waste_kg"
                ),
                "unit": record.get("unit", "kg"),
                "model": record.get("model", "Linear Regression"),
                "created_at": (
                    created_at.isoformat()
                    if created_at else None
                )
            })

        return {
            "total_records": len(history),
            "history": history
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Could not retrieve history: {str(error)}"
        )


# --------------------------------------------------
# 9. Delete one prediction-history record
# --------------------------------------------------

@app.delete("/history/{prediction_id}")
def delete_prediction(prediction_id: str):

    if history_collection is None:
        raise HTTPException(
            status_code=503,
            detail="Firestore is not available."
        )

    try:

        document_ref = history_collection.document(prediction_id)
        document = document_ref.get()

        if not document.exists:
            raise HTTPException(
                status_code=404,
                detail="Prediction record not found."
            )

        document_ref.delete()

        return {
            "message": "Prediction deleted successfully.",
            "prediction_id": prediction_id
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Could not delete prediction: {str(error)}"
        )


# --------------------------------------------------
# 10. Delete all prediction-history records
# --------------------------------------------------

@app.delete("/history")
def clear_prediction_history():

    if history_collection is None:
        raise HTTPException(
            status_code=503,
            detail="Firestore is not available."
        )

    try:

        records = history_collection.stream()
        deleted_count = 0

        for document in records:
            document.reference.delete()
            deleted_count += 1

        return {
            "message": "Prediction history cleared successfully.",
            "deleted_records": deleted_count
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Could not clear history: {str(error)}"
        )
