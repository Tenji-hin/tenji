import logging
import asyncio

from mfc.client import MfcClient

# basic logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("mfc.log"), logging.StreamHandler()],
)

logging.getLogger("asyncio").setLevel(logging.CRITICAL)


async def main():
    m = MfcClient()
    profile = await m.get_profile("syntack")

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

if __name__ == "__main__":
    import os

    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
