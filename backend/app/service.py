from __future__ import annotations

from app.recommendation import generate_suggestions
from app.schemas import DailyAssessment, MealRecord, NutritionTotals, UserProfile
from app.scoring import build_risk_tags, calc_daily_score


def aggregate_totals(meals: list[MealRecord]) -> NutritionTotals:
    calories = protein = fat = carbs = sodium = fiber = sugar = 0.0
    for meal in meals:
        for item in meal.items:
            calories += item.calories
            protein += item.protein
            fat += item.fat
            carbs += item.carbs
            sodium += item.sodium
            fiber += item.fiber
            sugar += item.sugar
    return NutritionTotals(
        calories=round(calories, 2),
        protein=round(protein, 2),
        fat=round(fat, 2),
        carbs=round(carbs, 2),
        sodium=round(sodium, 2),
        fiber=round(fiber, 2),
        sugar=round(sugar, 2),
    )


def build_daily_assessment(user: UserProfile, d, meals: list[MealRecord]) -> DailyAssessment:
    totals = aggregate_totals(meals)
    score = calc_daily_score(totals, user.goal)
    risk_tags = build_risk_tags(totals)
    suggestions = generate_suggestions(risk_tags, user)
    return DailyAssessment(
        user_id=user.id,
        date=d,
        score=score,
        totals=totals,
        risk_tags=risk_tags,
        suggestions=suggestions,
    )
