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
    profile = await m.get_profile("SYNTACK")

    print("--Profile--")
    print(f"Username: {profile.username}")
    print(f"Subtitle: {profile.subtitle}")
    print(f"Status: {profile.status}")
    print(f"Avatar: {profile.avatar}")

    print()
    print("--About--")
    print(f"Level: {profile.about.level}")


if __name__ == "__main__":
    import os

    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
