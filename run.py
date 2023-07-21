import logging
import asyncio

from mfc.client import MfcClient
from mfc.request.collection import CollectionStatus

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("mfc.log"), logging.StreamHandler()],
)

logging.getLogger("asyncio").setLevel(logging.CRITICAL)


async def get_profile(client: MfcClient, username: str):
    profile = await client.get_profile(username)

    print("--Profile--")
    print(f"Username: {profile.username}")
    print(f"Subtitle: {profile.subtitle}")
    print(f"Status: {profile.status}")
    print(f"Banner: {profile.banner}")
    print(f"Avatar: {profile.avatar}")

    print("Last Visit:", profile.last_visit)
    print("Joined:", profile.joined)
    print("Hits:", profile.hits)
    print("Placement:", profile.placement)

    print()
    print("--About--")
    print(f"Level: {profile.about.level}")
    print(f"Gender: {profile.about.gender}")
    print(f"Age: {profile.about.age}")
    print(f"Location: {profile.about.location}")
    print(f"Occupation: {profile.about.occupation}")
    print(f"Homepage: {profile.about.homepage}")
    print(f"Shows: {profile.about.shows}")
    print(f"Games: {profile.about.games}")
    print(f"Moe Points: {profile.about.moe_points}")


async def get_item(client: MfcClient, id: int):
    item = await client.get_item(id)

    print("--Item--")

    print(f"Id: {item.id}")
    print(f"Name: {item.name}")
    print(f"Thumbnail: {item.thumbnail}")


async def get_collection(client: MfcClient, username: str, status: CollectionStatus):
    collection = await client.get_collection(username, status)

    print("--Collection--")

    print(f"Username: {username}")
    print(f"Status: {status}")

    for item in collection.items:
        print(f"Id: {item.id}")
        print(f"Name: {item.name}")
        print(f"Thumbnail: {item.thumbnail}")


async def main():
    client = MfcClient()

    # await get_profile(client, "syntack")
    # await get_item(client, 218050)
    await get_collection(client, "syntack", CollectionStatus.Ordered)


if __name__ == "__main__":
    import os

    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
