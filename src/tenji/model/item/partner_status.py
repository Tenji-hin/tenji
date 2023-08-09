from enum import Enum

class PartnerListingStatus(Enum):
    MAYBE_AVAILABLE = "Maybe available"
    AVAILABLE = "Available"
    NOT_AVAILABLE = "Not available"
    
    def __str__(self):
        return self.value