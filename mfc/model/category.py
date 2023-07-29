from enum import IntEnum


class ItemCategory(IntEnum):
    Prepainted = 1
    ActionDolls = 2
    Trading = 3
    GarageKits = 4
    Plushes = 5
    Accessories = 6
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


def get_item_category_from_str(category: str) -> ItemCategory:
    if category == "Prepainted":
        return ItemCategory.Prepainted
    elif category == "Action/Dolls":
        return ItemCategory.ActionDolls
    elif category == "Trading":
        return ItemCategory.Trading
    elif category == "Garage Kits":
        return ItemCategory.GarageKits
    elif category == "Plushes":
        return ItemCategory.Plushes
    elif category == "Accessories":
        return ItemCategory.Accessories
    elif category == "Linens":
        return ItemCategory.Linens
    elif category == "Dishes":
        return ItemCategory.Dishes
    elif category == "Hanged up":
        return ItemCategory.HangedUp
    elif category == "Apparel":
        return ItemCategory.Apparel
    elif category == "On Walls":
        return ItemCategory.OnWalls
    elif category == "Stationeries":
        return ItemCategory.Stationeries
    elif category == "Misc":
        return ItemCategory.Misc
    elif category == "Books":
        return ItemCategory.Books
    elif category == "Music":
        return ItemCategory.Music
    elif category == "Video":
        return ItemCategory.Video
    elif category == "Games":
        return ItemCategory.Games
    elif category == "Software":
        return ItemCategory.Software
