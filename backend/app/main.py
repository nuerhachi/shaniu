from __future__ import annotations

from datetime import date, timedelta

from fastapi import FastAPI, HTTPException, Query

from app.repository import repo
from app.schemas import (
    DailyAssessment,
    DailyAssessmentRequest,
    MealRecord,
    MealRecordCreate,
    UserProfile,
    UserProfileCreate,
    WeeklyReport,
)
from app.service import build_daily_assessment

app = FastAPI(title="ShanYu API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/users", response_model=UserProfile)
def create_user(payload: UserProfileCreate) -> UserProfile:
    user = UserProfile(id=0, **payload.model_dump())
    return repo.create_user(user)


@app.post("/api/v1/meals", response_model=MealRecord)
def create_meal(payload: MealRecordCreate) -> MealRecord:
    if payload.user_id not in repo.users:
        raise HTTPException(status_code=404, detail="user not found")
    meal = MealRecord(id=0, **payload.model_dump())
    return repo.create_meal(meal)


@app.get("/api/v1/meals", response_model=list[MealRecord])
def list_meals(user_id: int = Query(...), date_value: date = Query(..., alias="date")) -> list[MealRecord]:
    return repo.list_meals_by_date(user_id, date_value)


@app.post("/api/v1/assessments/daily", response_model=DailyAssessment)
def calculate_daily_assessment(payload: DailyAssessmentRequest) -> DailyAssessment:
    user = repo.users.get(payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    meals = repo.list_meals_by_date(payload.user_id, payload.date)
    assessment = build_daily_assessment(user, payload.date, meals)
    return repo.save_assessment(assessment)


@app.get("/api/v1/assessments/daily", response_model=DailyAssessment)
def get_daily_assessment(user_id: int, date_value: date = Query(..., alias="date")) -> DailyAssessment:
    assessment = repo.get_assessment(user_id, date_value)
    if not assessment:
        raise HTTPException(status_code=404, detail="assessment not found")
    return assessment


@app.get("/api/v1/reports/weekly", response_model=WeeklyReport)
def get_weekly_report(user_id: int, end_date: date = Query(...)) -> WeeklyReport:
    start_date = end_date - timedelta(days=6)
    scores: list[int] = []
    for i in range(7):
        d = start_date + timedelta(days=i)
        assessment = repo.get_assessment(user_id, d)
        if assessment:
            scores.append(assessment.score)

    average_score = round(sum(scores) / len(scores), 2) if scores else 0.0
    return WeeklyReport(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        average_score=average_score,
        completed_days=len(scores),
    )
