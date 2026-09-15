# Stack: Python 3.12 | FastAPI 0.115 + httpx | File: main.py
# The container is stateless: every Task lives in a Back4app backend, reached over REST.
import os
from typing import Optional
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

APP_ID = os.environ["PARSE_APP_ID"]
REST_KEY = os.environ["PARSE_REST_KEY"]
BASE = os.environ.get("PARSE_SERVER_URL", "https://parseapi.back4app.com")
HEADERS = {"X-Parse-Application-Id": APP_ID, "X-Parse-REST-API-Key": REST_KEY, "Content-Type": "application/json"}
VERSION = "1.0.0"

app = FastAPI(title="tasks")
backend = httpx.AsyncClient(base_url=BASE, headers=HEADERS, timeout=10)


class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    done: bool = False


class TaskPatch(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    done: Optional[bool] = None


def parse_error(r: httpx.Response):
    """Map a Parse error onto an HTTP status the client understands."""
    body = r.json() if r.headers.get("content-type", "").startswith("application/json") else {"error": r.text}
    status = {101: 404, 142: 422, 209: 401}.get(body.get("code"), 502)
    raise HTTPException(status_code=status, detail=body)


@app.get("/healthz")
async def healthz():
    return {"ok": True, "version": VERSION}


@app.post("/tasks", status_code=201)
async def create_task(task: TaskIn):
    r = await backend.post("/classes/Task", json=task.model_dump())
    if r.status_code != 201:
        parse_error(r)
    return {**task.model_dump(), **r.json()}


@app.get("/tasks")
async def list_tasks(done: Optional[bool] = None):
    params = {"order": "-createdAt"}
    if done is not None:
        params["where"] = '{"done": %s}' % ("true" if done else "false")
    r = await backend.get("/classes/Task", params=params)
    if r.status_code != 200:
        parse_error(r)
    return r.json()["results"]


@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    r = await backend.get(f"/classes/Task/{task_id}")
    if r.status_code != 200:
        parse_error(r)
    return r.json()


@app.patch("/tasks/{task_id}")
async def update_task(task_id: str, patch: TaskPatch):
    r = await backend.put(f"/classes/Task/{task_id}", json=patch.model_dump(exclude_none=True))
    if r.status_code != 200:
        parse_error(r)
    return r.json()


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str):
    r = await backend.delete(f"/classes/Task/{task_id}")
    if r.status_code != 200:
        parse_error(r)
