from typing import Optional
from pydantic import BaseModel


# Entidad user
class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: str