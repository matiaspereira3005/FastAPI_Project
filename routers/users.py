from fastapi import APIRouter, HTTPException 
from pydantic import BaseModel 

router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={404: {"message": "No encontrado"}})


# Inicia el serve: uvicorn users:app --reload
#Swagger: 

#Entidad user
class User(BaseModel):

    id: int
    name: str
    surname: str
    url: str
    age: int 

users_list = [User(id=1, name="Brais"  , surname="Smith", url="https://morpheussdev.cl", age=24),
              User(id=2, name="Bob"    , surname="Dev"  , url="https://morpheussdev.cl", age=25),
              User(id=3, name="Charlie", surname="Stone", url="https://morpheussdev.cl", age=26)]

"""
GET METHOD
"""
@router.get("/json")
async def usersjson(): # type: ignore
    return [{"name": "Alice", "surname": "Smith", "url": "https://example.com/alice", "age": 35},
            {"name": "Bob", "surname": "Johnson", "url": "https://example.com/bob", "age": 34},
            {"name": "Charlie", "surname": "Brown", "url": "https://example.com/charlie", "age": 33}]

@router.get("/usersclass")
async def usersclass():
    return User(name = "Brais", surname="Smith", url="https://morpheussdev.cl", age=24)

@router.get("/")
async def users():
    return users_list

#User_path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)

#User_query
@router.get("/user/")
async def user(id: int):
    return search_user(id)

"""
Trabajar en el path es poder trabajar con los datos sobre la misma URL
Trabajar con la query permite poder llamar con el método que querramos
"""


"""
POST METHOD
"""
@router.post("/user/", response_model= User,  status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
       #Error con raise, no return, así propaga, no retorna contenido, lanza excepción
       raise HTTPException(status_code=404, detail="El usuario ya existe")
    users_list.append(user)
    return user


"""
PUT METHOD
"""
@router.put("/user/")
async def user(user: User):
    
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            print("Flag true")
            users_list[index] = user
            found = True

    if not found:
        raise HTTPException(status_code=404, detail="no se ha actualizado el usuario")

    return user


"""
DELETE METHOD
"""
@router.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    
    if not found:
        raise HTTPException(status_code=404, detail="no se ha eliminado el usuario")
    else:
        raise HTTPException(status_code=200, detail="usuario eliminado")



"""
FUNCTIONS
"""
def search_user(id: int):
        #filter(lambda x: x.n == 5, myList)
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return{"error":"no se ha encontrado el usuario"}



"""
CODIGOS STATUS
100 - 199: Informational responses
200 - 299: Successful responses
300 - 399: Redirection messages
400 - 499: Client error responses
500 - 599: Server error responses
"""
