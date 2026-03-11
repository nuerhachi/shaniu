from __future__ import annotations

from collections import defaultdict
from datetime import date

from app.schemas import DailyAssessment, MealRecord, UserProfile


class InMemoryRepository:
    def __init__(self) -> None:
        self._user_id = 1
        self._meal_id = 1
        self.users: dict[int, UserProfile] = {}
        self.meals: dict[int, MealRecord] = {}
        self.assessments: dict[tuple[int, date], DailyAssessment] = {}
        self.meals_by_user_date: dict[tuple[int, date], list[int]] = defaultdict(list)

    def create_user(self, user: UserProfile) -> UserProfile:
        user.id = self._user_id
        self.users[user.id] = user
        self._user_id += 1
        return user

    def create_meal(self, meal: MealRecord) -> MealRecord:
        meal.id = self._meal_id
        self.meals[meal.id] = meal
        self._meal_id += 1
        self.meals_by_user_date[(meal.user_id, meal.occurred_at.date())].append(meal.id)
        return meal

    def list_meals_by_date(self, user_id: int, d: date) -> list[MealRecord]:
        ids = self.meals_by_user_date.get((user_id, d), [])
        return [self.meals[i] for i in ids]

    def save_assessment(self, assessment: DailyAssessment) -> DailyAssessment:
        self.assessments[(assessment.user_id, assessment.date)] = assessment
        return assessment

    def get_assessment(self, user_id: int, d: date) -> DailyAssessment | None:
        return self.assessments.get((user_id, d))


repo = InMemoryRepository()
