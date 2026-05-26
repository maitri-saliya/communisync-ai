from fastapi import APIRouter
from database import *

router=APIRouter()

@router.get("/dashboard")
def dashboard():

    s=Session()

    total=s.query(Need).count()

    return {
        "requests":total,
        "estimated_hours_saved":
        total*0.5
    }