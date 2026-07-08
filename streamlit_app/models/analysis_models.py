from pydantic import BaseModel
from typing import List


class BloodValue(BaseModel):
    parameter: str
    value: str
    reference_range: str
    status: str


class BloodAnalysis(BaseModel):
    patient_summary: str
    health_score: int
    risk_level: str
    blood_values: List[BloodValue]