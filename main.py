#Documentación oficial: https://fastapi.tiangolo.com/es/

#Instala FastAPI: pip install "fastapi[all]"


from fastapi import FastAPI
from routers import products, users, jwt_auth_users, basic_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(users.router)

app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

#URL LOCAL : http://localhost:8000/



@app.get("/")
async def root():
    return "Hola FastAPI!"

#URL LOCAL : http://localhost:8001/url

@app.get("/url")
async def root():
    return { "url_curso" : "https://morpheussdev.cl" }

#Sin contenedor Docker:
#Inicia server con: uvicorn main:app --reload
#Detiene server con: CTRL + C

#Documentacion automatica: http://localhost:8001/docs
#Documentacion alternativa: http://localhost:8001/redoc