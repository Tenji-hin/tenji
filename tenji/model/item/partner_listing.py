from pydantic import BaseModel

from tenji.model.category import ItemCategory



class PartnerListing(BaseModel):
    jan: int
    shop_name: str
    shop_icon: str
    status: str
    url: str