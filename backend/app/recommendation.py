from __future__ import annotations

from app.schemas import UserProfile

RISK_SUGGESTIONS = {
    "HIGH_SODIUM": "明天优先选择清蒸/水煮，减少汤底与蘸料。",
    "LOW_PROTEIN": "下一餐增加 1 份优质蛋白（鸡蛋/豆腐/鱼虾）。",
    "LOW_FIBER": "增加 1 碗深色蔬菜 + 1 份低糖水果。",
    "HIGH_SUGAR": "减少含糖饮料与甜点频次，可替换为无糖茶或气泡水。",
}


def generate_suggestions(risk_tags: list[str], user: UserProfile) -> list[str]:
    suggestions = [RISK_SUGGESTIONS[t] for t in risk_tags if t in RISK_SUGGESTIONS]
    if user.lactose_intolerant:
        suggestions.append("你标记了乳糖不耐，优先选择无乳糖奶或豆制品补蛋白。")
    if user.avoid_spicy:
        suggestions.append("你偏好不辣口味，推荐清炒/炖煮的低刺激菜式。")
    if not suggestions:
        suggestions.append("饮食结构总体良好，请继续保持并稳定记录。")
    return suggestions
