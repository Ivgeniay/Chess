from game.application import Application
import asyncio


async def main():
    app = Application()
    app.run()
    await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())
