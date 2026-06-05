# 实操记录

## 第 1 步：确认项目目录

目标：确认项目已创建在 `E:\python_Demo\paper-polish-agent`。

命令：

```powershell
Get-ChildItem E:\python_Demo\paper-polish-agent
```

看到 `backend`、`docs`、`README.md` 说明目录创建成功。

## 第 2 步：使用 Conda 项目环境

目标：后续所有 Python 命令都使用独立环境 `paper-polish-agent`，避免和 `base` 或 `.venv` 混用。

```powershell
conda activate paper-polish-agent
cd E:\python_Demo\paper-polish-agent\backend
python -c "import sys; print(sys.executable)"
```

预期路径包含：

```text
D:\miniconda\envs\paper-polish-agent\python.exe
```

## 第 3 步：运行接口自动化测试

目标：不用启动浏览器，也能确认后端接口逻辑正确。测试不会调用真实 ModelGate，不消耗额度。

```powershell
python -m pytest -v
```

预期结果：

```text
5 passed
```

## 第 4 步：配置 ModelGate

目标：把敏感配置放在本机 `.env`，不要写进 Python 代码。

配置文件：

```text
E:\python_Demo\paper-polish-agent\backend\.env
```

示例：

```dotenv
MODELGATE_API_KEY=你的真实ModelGate密钥
MODELGATE_BASE_URL=https://mg.aid.pub/v1
MODELGATE_MODEL=gpt-5.5
APP_ENV=local
```

不要把 `.env` 内容发给别人，也不要截图暴露 API Key。

## 第 5 步：启动 FastAPI 后端

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

浏览器访问：

```text
http://127.0.0.1:8000/health
```

预期返回：

```json
{"status":"ok","service":"paper-polish-agent","env":"local"}
```

## 第 6 步：用 Swagger 调用真实论文润色接口

浏览器访问：

```text
http://127.0.0.1:8000/docs
```

展开 `POST /api/polish`，点击 `Try it out`，输入：

```json
{
  "text": "本文提出了一种方法，该方法可以提高系统性能。",
  "requirement": "学术化润色"
}
```

点击 `Execute`。

当前阶段会通过 `app.providers.modelgate.call_modelgate` 调用 ModelGate，并返回 8 个固定字段。

## 当前后端结构

- `app/main.py`：FastAPI 入口，注册 `/health` 和 `/api/polish`。
- `app/core/config.py`：从 `.env` 读取配置。
- `app/schemas/polish.py`：定义请求和响应 JSON 结构。
- `app/agent/prompt.py`：定义论文润色 Agent Prompt。
- `app/agent/service.py`：Agent 编排入口，调用 provider。
- `app/providers/modelgate.py`：ModelGate/OpenAI 兼容接口调用。
- `tests/`：自动化测试，不读取真实 Key，不调用真实 ModelGate。
