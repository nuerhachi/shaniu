# MVP 执行方案

## 1. 用户流程
1. 用户注册并填写基础信息（身高、体重、目标）
2. 上传每餐图片 + 文字描述
3. 系统解析出食物条目与份量
4. 系统计算每日营养总量并打分
5. 用户查看仪表盘和建议

## 2. 技术实现路径
- **后端框架**：FastAPI
- **接口协议**：REST + JSON
- **模型校验**：Pydantic
- **MVP 存储**：内存仓储（代码已实现）
- **生产化迁移**：PostgreSQL + SQLAlchemy + Redis + Celery

## 3. API 草案（已实现核心端点）
- `POST /api/v1/users`：新增用户
- `POST /api/v1/meals`：新增餐次记录
- `GET /api/v1/meals?user_id=1&date=2026-03-10`：查询某日记录
- `POST /api/v1/assessments/daily`：触发某日评估
- `GET /api/v1/assessments/daily?user_id=1&date=2026-03-10`：获取评估结果
- `GET /api/v1/reports/weekly?user_id=1&end_date=2026-03-10`：获取周报

## 4. 风险标签规则（示例）
- `HIGH_SODIUM`: 单日钠 > 2000 mg
- `LOW_PROTEIN`: 单日蛋白质 < 60 g
- `LOW_FIBER`: 单日纤维 < 25 g
- `HIGH_SUGAR`: 添加糖 > 50 g

## 5. 建议模板（示例）
- HIGH_SODIUM: “明天优先选择清蒸/水煮类，减少汤底与蘸料摄入。”
- LOW_PROTEIN: “下一餐增加 1 份优质蛋白（鸡蛋/豆腐/鱼虾）。”
- LOW_FIBER: “增加 1 碗深色蔬菜 + 1 份低糖水果。”

## 6. 埋点建议
- `meal_record_created`
- `daily_score_viewed`
- `suggestion_clicked`
- `suggestion_adopted`
