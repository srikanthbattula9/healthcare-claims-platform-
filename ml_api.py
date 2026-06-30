"""
ml_api.py - FastAPI service serving the charges-prediction model.
Run:  uvicorn ml_api:app --reload --port 8000
Docs: http://localhost:8000/docs
"""
from fastapi import FastAPI
from pydantic import BaseModel, Field
from ml_predict import predict_charge

app = FastAPI(title="Healthcare Charges Prediction API", version="1.0.0")


class Person(BaseModel):
    age: int = Field(..., ge=0, le=120)
    sex: str
    bmi: float = Field(..., gt=0)
    children: int = Field(..., ge=0)
    smoker: str
    region: str
    model_config = {"json_schema_extra": {"example": {"age": 45, "sex": "male", "bmi": 28.5, "children": 2, "smoker": "yes", "region": "southwest"}}}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(person: Person):
    charge = predict_charge(person.model_dump())
    return {"predicted_charge": charge, "currency": "USD", "input": person.model_dump()}
