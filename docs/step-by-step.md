# 实操记录

## 当前后端能力

- `GET /health`：确认服务运行状态。
- `POST /api/polish`：调用 ModelGate 进行论文润色。
- `GET /api/tasks`：查看最近匿名润色任务。
- `GET /api/tasks/{task_id}`：查看单条任务详情。
- PostgreSQL：保存匿名任务记录、成功结果和失败错误。

## 本地测试

```powershell
conda activate paper-polish-agent
cd E:\python_Demo\paper-polish-agent\backend
python -m pytest -v
```

## 服务器 `.env`

服务器部署时，`backend/.env` 至少需要：

```dotenv
MODELGATE_API_KEY=你的真实ModelGate密钥
MODELGATE_BASE_URL=https://mg.aid.pub/v1
MODELGATE_MODEL=gpt-5.5
DATABASE_URL=postgresql+psycopg://paper_polish:paper_polish_password@postgres:5432/paper_polish
APP_ENV=production
```

## Docker 部署

```bash
cd /opt/paper-polish-agent
git pull
docker compose up -d --build
docker compose ps
```

查看任务记录接口：

```bash
curl http://127.0.0.1/api/tasks
```
