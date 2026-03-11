from __future__ import annotations

from app.schemas import NutritionTotals


def _target_calories(goal: str) -> tuple[float, float]:
    if goal == "fat_loss":
        return (1500, 1900)
    if goal == "muscle_gain":
        return (2200, 2900)
    return (1700, 2400)


def calc_daily_score(totals: NutritionTotals, goal: str) -> int:
    low, high = _target_calories(goal)

    calorie_score = 25
    if totals.calories < low:
        calorie_score = max(0, 25 - int((low - totals.calories) / 80))
    elif totals.calories > high:
        calorie_score = max(0, 25 - int((totals.calories - high) / 80))

    protein_ratio = totals.protein * 4 / totals.calories if totals.calories else 0
    fat_ratio = totals.fat * 9 / totals.calories if totals.calories else 0
    carbs_ratio = totals.carbs * 4 / totals.calories if totals.calories else 0

    macro_score = 25
    if not 0.15 <= protein_ratio <= 0.35:
        macro_score -= 8
    if not 0.2 <= fat_ratio <= 0.35:
        macro_score -= 8
    if not 0.4 <= carbs_ratio <= 0.6:
        macro_score -= 9
    macro_score = max(macro_score, 0)

    micro_score = 20
    if totals.fiber < 25:
        micro_score -= min(10, int((25 - totals.fiber) / 2.5))
    if totals.sodium > 2000:
        micro_score -= min(10, int((totals.sodium - 2000) / 200))
    micro_score = max(micro_score, 0)

    risk_penalty_bucket = 20
    if totals.sodium > 2400:
        risk_penalty_bucket -= 7
    if totals.sugar > 50:
        risk_penalty_bucket -= 7
    if totals.protein < 60:
        risk_penalty_bucket -= 6
    risk_penalty_bucket = max(risk_penalty_bucket, 0)

    regularity_bonus = 10 if totals.calories > 0 else 0

    score = calorie_score + macro_score + micro_score + risk_penalty_bucket + regularity_bonus
    return max(0, min(100, score))


def build_risk_tags(totals: NutritionTotals) -> list[str]:
    tags: list[str] = []
    if totals.sodium > 2000:
        tags.append("HIGH_SODIUM")
    if totals.protein < 60:
        tags.append("LOW_PROTEIN")
    if totals.fiber < 25:
        tags.append("LOW_FIBER")
    if totals.sugar > 50:
        tags.append("HIGH_SUGAR")
    return tags
