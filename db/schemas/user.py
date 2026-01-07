"""
Docstring for db.schemas.user
Es capaz de hacer diferentes operaciones para ayudarnos a transformar datos de db a lo que requerimos
para trabajar
"""

def user_schema(user) -> dict:
    return{
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"]}

def users_schema(users) -> list:
    return [user_schema(user) for user in users]
