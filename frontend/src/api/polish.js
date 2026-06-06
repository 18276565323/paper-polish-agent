const API_BASE = import.meta.env.VITE_API_BASE || ''

async function readErrorMessage(response) {
  try {
    const payload = await response.json()
    if (typeof payload.detail === 'string') {
      return payload.detail
    }
    if (Array.isArray(payload.detail)) {
      return payload.detail.map((item) => item.msg || JSON.stringify(item)).join('\n')
    }
    return JSON.stringify(payload)
  } catch {
    return response.statusText || '请求失败'
  }
}

export async function polishPaper(payload) {
  let response

  try {
    response = await fetch(`${API_BASE}/api/polish`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
  } catch (error) {
    throw new Error('无法连接后端服务，请确认 FastAPI 已启动。')
  }

  if (!response.ok) {
    const message = await readErrorMessage(response)
    throw new Error(message)
  }

  return response.json()
}

export async function listTasks(limit = 20) {
  const response = await fetch(`${API_BASE}/api/tasks?limit=${limit}`)

  if (!response.ok) {
    const message = await readErrorMessage(response)
    throw new Error(message)
  }

  return response.json()
}

export async function getTaskDetail(taskId) {
  const response = await fetch(`${API_BASE}/api/tasks/${taskId}`)

  if (!response.ok) {
    const message = await readErrorMessage(response)
    throw new Error(message)
  }

  return response.json()
}

export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE}/health`)
    if (!response.ok) {
      return { ok: false, label: '后端异常' }
    }
    const data = await response.json()
    return { ok: true, label: `${data.service} / ${data.env}` }
  } catch {
    return { ok: false, label: '后端未连接' }
  }
}
