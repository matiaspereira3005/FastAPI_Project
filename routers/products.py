from fastapi import APIRouter #type: ignore

router = APIRouter(prefix="/products", 
                   tags=["products"],
                   responses={404: {"message": "No encontrado"}})

product_list = ["producto 1", "producto 2", "producto 3", "producto 4"]

@router.get("/")
async def users():
    return ["producto 1", "producto 2", "producto 3", "producto 4"]

@router.get("/{id}")
async def users(id: int):
    return product_list[id]

















