from dis import disco
import logging
import dotenv
import os
import discord
import requests


dotenv.load_dotenv()

async def send_a_joke(client):
    joke = requests.get("https://icanhazdadjoke.com/",headers={"Accept": "text/plain"})
    if not joke.ok:
        logging.error(f"Failed getting joke.. response: {joke.status_code}:{joke.text}")
        return
    channel_id = int(os.environ['CHANNEL_ID'])
    channel = client.get_channel(channel_id)
    await channel.send(joke.text)

def start_bot():
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f"Logged on as {client.user.name}")

    @client.event
    async def on_message(message):
        if "joke" in message.content.lower() and message.channel.id == int(os.environ['CHANNEL_ID']):
            await send_a_joke(client)

    token = os.environ['DISCORD_TOKEN']
    client.run(token)

if __name__ == "__main__":
    logging.basicConfig(filename="bot.log", level=logging.DEBUG)
    start_bot()