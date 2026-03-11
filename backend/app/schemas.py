from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field

MealType = Literal["breakfast", "lunch", "dinner", "snack"]
GoalType = Literal["fat_loss", "muscle_gain", "glycemic_control", "balanced"]


class UserProfileCreate(BaseModel):
    age: int = Field(ge=1, le=120)
    sex: Literal["male", "female", "other"]
    height_cm: float = Field(gt=0)
    weight_kg: float = Field(gt=0)
    goal: GoalType = "balanced"
    avoid_spicy: bool = False
    lactose_intolerant: bool = False


class UserProfile(UserProfileCreate):
    id: int


class MealItemInput(BaseModel):
    food_name: str
    amount: str
    calories: float = Field(ge=0)
    protein: float = Field(ge=0)
    fat: float = Field(ge=0)
    carbs: float = Field(ge=0)
    sodium: float = Field(ge=0)
    fiber: float = Field(ge=0)
    sugar: float = Field(ge=0)


class MealRecordCreate(BaseModel):
    user_id: int
    meal_type: MealType
    occurred_at: datetime
    note: str = ""
    image_url: str | None = None
    items: list[MealItemInput]


class MealRecord(MealRecordCreate):
    id: int


class DailyAssessmentRequest(BaseModel):
    user_id: int
    date: date


class NutritionTotals(BaseModel):
    calories: float
    protein: float
    fat: float
    carbs: float
    sodium: float
    fiber: float
    sugar: float


class DailyAssessment(BaseModel):
    user_id: int
    date: date
    score: int
    totals: NutritionTotals
    risk_tags: list[str]
    suggestions: list[str]


class WeeklyReport(BaseModel):
    user_id: int
    start_date: date
    end_date: date
    average_score: float
    completed_days: int
