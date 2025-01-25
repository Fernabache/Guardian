"""
GUARDIAN API Layer
"""
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="GUARDIAN API")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
guardian = None  # GUARDIAN instance

class PatientData(BaseModel):
    nhs_number: str
    data: Dict

class AppointmentData(BaseModel):
    appointments: List[Dict]

@app.post("/api/v1/diagnose")
async def diagnose_case(
    patient: PatientData,
    token: str = Security(oauth2_scheme)
):
    """Analyze patient case"""
    try:
        return await guardian.modules['diagnostics'].analyze_case(
            patient.data
        )
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/api/v1/optimize/appointments")
async def optimize_appointments(
    data: AppointmentData,
    token: str = Security(oauth2_scheme)
):
    """Optimize appointment schedule"""
    try:
        return await guardian.modules['scheduling'].optimize_appointments(
            data.appointments
        )
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/v1/resources/status")
async def get_resource_status(
    token: str = Security(oauth2_scheme)
):
    """Get current resource status"""
    try:
        return await guardian.modules['resources'].get_status()
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/api/v1/preventive/analyze")
async def analyze_population(
    data: List[Dict],
    token: str = Security(oauth2_scheme)
):
    """Run population health analysis"""
    try:
        return await guardian.modules['preventive'].analyze_population(
            data
        )
    except Exception as e:
        raise HTTPException(500, str(e))
