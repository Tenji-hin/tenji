from pydantic import BaseModel

from tenji.model.category import ItemCategory


class Company(BaseModel):
    id: int
    name: str
    logo: str
    role: str


class Item(BaseModel):
    id: int
    name: str
    thumbnail: str
    category: ItemCategory
    companies: list[Company] = []
