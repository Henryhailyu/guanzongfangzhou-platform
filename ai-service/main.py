from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Guanlian AI Service")


class WritingRequest(BaseModel):
    essay: str
    material: str
    essay_type: str = "critique"


@app.get("/ai/health")
def health():
    return {"success": True, "service": "ai-service"}


@app.post("/ai/writing/critique")
def critique(req: WritingRequest):
    # MVP：混元 API 接入前返回占位批改结果
    return {
        "success": True,
        "data": {
            "total_score": 0,
            "feedback": "混元 API 密钥配置后将启用真实批改。请在 .env 中设置 HUNYUAN_SECRET_ID。",
            "dimension_scores": {
                "accuracy": 0,
                "depth": 0,
                "language": 0,
                "structure": 0,
            },
        },
    }
