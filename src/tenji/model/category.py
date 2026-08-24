from enum import IntEnum


class ItemCategory(IntEnum):
    Prepainted = 1
    ActionDolls = 2
    Trading = 3
    GarageKits = 4
    Plushes = 5
    Accessories = 6
    ModelKits = 10
    Linens = 13
    Dishes = 14
    HangedUp = 15
    Apparel = 17
    OnWalls = 18
    Stationeries = 20
    Misc = 16
    Books = 21
    Music = 22
    Video = 26
    Games = 28
    Software = 29


ITEM_CATEGORY_LABELS = {
    "Prepainted": ItemCategory.Prepainted,
    "Action/Dolls": ItemCategory.ActionDolls,
    "Trading": ItemCategory.Trading,
    "Garage Kits": ItemCategory.GarageKits,
    "Model Kits": ItemCategory.ModelKits,
    "Plushes": ItemCategory.Plushes,
    "Accessories": ItemCategory.Accessories,
    "Linens": ItemCategory.Linens,
    "Dishes": ItemCategory.Dishes,
    "Hanged up": ItemCategory.HangedUp,
    "Apparel": ItemCategory.Apparel,
    "On Walls": ItemCategory.OnWalls,
    "Stationeries": ItemCategory.Stationeries,
    "Misc": ItemCategory.Misc,
    "Books": ItemCategory.Books,
    "Music": ItemCategory.Music,
    "Video": ItemCategory.Video,
    "Games": ItemCategory.Games,
    "Software": ItemCategory.Software,
}


def get_item_category_from_str(category: str) -> ItemCategory:
    """Maps an MFC category label onto its ItemCategory.

    Raises ValueError for an unrecognised label. Returning None instead would
    only defer the failure to the model, where category is required, and lose
    the offending label along the way.
    """
    try:
        return ITEM_CATEGORY_LABELS[category.strip()]
    except AttributeError:
        raise ValueError(f"Item category must be a string, got {category!r}") from None
    except KeyError:
        raise ValueError(f"Unknown MFC item category: {category!r}") from None
