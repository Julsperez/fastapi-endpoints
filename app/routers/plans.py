from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from models import Plan, PlanCreate
from db_config import SessionDependency

router = APIRouter()

@router.post("/plans", response_model=Plan, status_code=status.HTTP_201_CREATED, tags=["Plans"])
async def create(plan_data: PlanCreate, session: SessionDependency):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db

@router.get("/plans", tags=["Plans"])
async def get_all(session: SessionDependency):
    plans = session.exec(select(Plan)).all()
    return plans