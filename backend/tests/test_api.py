from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app


def test_meal_assessment_flow() -> None:
    client = TestClient(app)

    user_resp = client.post(
        "/api/v1/users",
        json={
            "age": 28,
            "sex": "female",
            "height_cm": 165,
            "weight_kg": 58,
            "goal": "balanced",
            "avoid_spicy": True,
            "lactose_intolerant": False,
        },
    )
    assert user_resp.status_code == 200
    user_id = user_resp.json()["id"]

    meal_resp = client.post(
        "/api/v1/meals",
        json={
            "user_id": user_id,
            "meal_type": "lunch",
            "occurred_at": datetime(2026, 3, 10, 12, 0, 0).isoformat(),
            "note": "鸡胸肉+米饭+蔬菜",
            "items": [
                {
                    "food_name": "鸡胸肉",
                    "amount": "150g",
                    "calories": 248,
                    "protein": 46,
                    "fat": 5,
                    "carbs": 0,
                    "sodium": 180,
                    "fiber": 0,
                    "sugar": 0,
                },
                {
                    "food_name": "米饭",
                    "amount": "150g",
                    "calories": 174,
                    "protein": 4,
                    "fat": 0.3,
                    "carbs": 38,
                    "sodium": 2,
                    "fiber": 0.4,
                    "sugar": 0,
                },
            ],
        },
    )
    assert meal_resp.status_code == 200

    assessment_resp = client.post(
        "/api/v1/assessments/daily", json={"user_id": user_id, "date": "2026-03-10"}
    )
    assert assessment_resp.status_code == 200
    body = assessment_resp.json()
    assert 0 <= body["score"] <= 100
    assert body["totals"]["calories"] > 0

    weekly = client.get(f"/api/v1/reports/weekly?user_id={user_id}&end_date=2026-03-10")
    assert weekly.status_code == 200
    assert weekly.json()["completed_days"] >= 1


def test_web_client_index() -> None:
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "MVP 客户端" in response.text
