# from waitress import serve
# from bot.reminder_bot import main

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())
from bot.reminder_bot import main  # Import your bot's main function

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())  # Run the main async function for the bot
