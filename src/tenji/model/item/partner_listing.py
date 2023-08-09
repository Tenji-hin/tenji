from pydantic import BaseModel

from tenji.model.item.partner_status import PartnerListingStatus



class PartnerListing(BaseModel):
    jan: int
    shop_name: str
    shop_icon: str
    status: PartnerListingStatus
    url: str