from dis import disco
import logging
import dotenv
import os
import discord
import requests

COMMAND = "!joke"
dotenv.load_dotenv()

async def maybe_send_a_joke(client, message, target_channel):
    if COMMAND in message.content.lower() and message.channel.id == int(target_channel):
        logging.debug(f"Detected {COMMAND}")
        await send_a_joke(message)


async def send_a_joke(message):
    joke = requests.get("https://icanhazdadjoke.com/",headers={"Accept": "text/plain"})
    if not joke.ok:
        logging.error(f"Failed getting joke.. response: {joke.status_code}:{joke.text}")
        return
    await message.reply(joke.text)
    logging.debug(f"Sent joke: {joke.text}")

def start_bot():
    target_channel = os.environ['PROD_CHANNEL_ID']
    if os.environ.get('BOT_TEST'):
        logging.info("Detected testing environment")
        target_channel = os.environ['TEST_CHANNEL_ID']
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f"Logged on as {client.user.name}")

    @client.event
    async def on_message(message):
        await maybe_send_a_joke(client, message, target_channel)

    @client.event
    async def on_message_edit(_before, after):
        await maybe_send_a_joke(client, after, target_channel)

    token = os.environ['DISCORD_TOKEN']
    client.run(token)

if __name__ == "__main__":
    logging.basicConfig(filename="bot.log", level=logging.DEBUG)
    start_bot()