from pydantic import BaseModel

from tenji.model.category import ItemCategory

class Character(BaseModel):
    id: int
    name: str
    avatar: str

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
    characters: list[Character] = []
    companies: list[Company] = []
