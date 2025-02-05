from waitress import serve
from bot.reminder_bot import main

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
