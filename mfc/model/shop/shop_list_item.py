
from typing import Optional
from pydantic import BaseModel

from mfc.model.shop.shop_category import ShopCategory

class ShopListItem(BaseModel):
    id: int
    name: str
    icon: str
    category: ShopCategory
    location: Optional[str]