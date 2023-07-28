from pydantic import BaseModel


class Pagination(BaseModel):
    current_page: int
    has_next_page: bool
