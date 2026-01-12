from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.core.task import Task
from app.policy.policy_engine import PolicyEngine
from app.router.model_router import ModelRouter
from app.observability.trace_store import get_traces
from app.observability.metrics import get_metrics

app = FastAPI(title="Enterprise GenAI Router")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve UI
app.mount("/ui", StaticFiles(directory="frontend", html=True), name="ui")

policy_engine = PolicyEngine()
router = ModelRouter()


class ExecuteRequest(BaseModel):
    user_input: str
    task_type: str
    risk_level: str
    sensitivity: str
    budget: float


@app.post("/execute")
def execute_task(req: ExecuteRequest):
    task = Task(
        user_input=req.user_input,
        task_type=req.task_type,
        risk_level=req.risk_level,
        sensitivity=req.sensitivity,
        budget=req.budget
    )

    decision = policy_engine.evaluate(task)
    response = router.execute(task, decision)

    return {
        "model": response.model_used,
        "output": response.content,
        "policy_trace": response.policy_trace
    }


@app.get("/execute")
def execute_get_guard():
    raise HTTPException(
        status_code=405,
        detail="Use POST /execute with JSON body"
    )


@app.get("/metrics")
def metrics():
    return get_metrics()


@app.get("/traces")
def traces():
    return get_traces()
