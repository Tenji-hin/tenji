from typing import Optional
from pydantic import BaseModel


class Meta(BaseModel):
    is_guest: bool
    username: Optional[str] = None
    avatar: Optional[str] = None
