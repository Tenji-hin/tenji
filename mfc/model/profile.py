from typing import Optional
from pydantic import BaseModel


class About(BaseModel):
    level: int
    gender: Optional[str] = None
    age: Optional[str] = None
    location: Optional[str] = None
    occupation: Optional[str] = None
    homepage: Optional[str] = None
    shows: Optional[list[str]] = None
    games: Optional[list[str]] = None
    moe_points: Optional[list[str]] = None


class Profile(BaseModel):
    username: str

    subtitle: Optional[str] = None
    status: Optional[str] = None
    banner: Optional[str] = None
    avatar: Optional[str] = None
    last_visit: Optional[str] = None
    joined: Optional[str] = None
    hits: Optional[int] = None
    placement: Optional[int] = None

    about: About
