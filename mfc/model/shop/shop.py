from typing import Optional
from pydantic import BaseModel


class Shop(BaseModel):
    id: int
    name: str
    homepage: Optional[str]
    contact: Optional[str]
    location: Optional[str]
    shipping: Optional[str]
