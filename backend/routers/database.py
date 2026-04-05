from fastapi import APIRouter

router = APIRouter(prefix="/database", tags=["database"])

@router.get("/")
async def get_records():
    return {"message": "Database endpoint not implemented yet"}
