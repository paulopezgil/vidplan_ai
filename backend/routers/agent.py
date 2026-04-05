from fastapi import APIRouter

router = APIRouter(prefix="/agent", tags=["agent"])

@router.post("/")
async def run_agent():
    return {"message": "Agent endpoint not implemented yet"}
