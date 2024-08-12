# bot.py
import discord
from discord.ext import commands
from commands import (
    fetch_news,
    set_preferences,
    get_my_preferences,
)
from newsapi import NewsApiClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Initialize the bot, NewsAPI, and other necessary components
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
newsapi = NewsApiClient(api_key=NEWS_API_KEY)
user_preferences = {}
user_articles = {}


@bot.command(name="setpref")
async def set_pref(ctx, *, preference: str):
    await set_preferences(ctx, preference=preference, user_preferences=user_preferences)


@bot.command(name="mypref")
async def my_pref(ctx):
    await get_my_preferences(ctx, user_preferences=user_preferences)


@bot.command(name="news")
async def news_command(ctx, query: str = None, number_of_articles: int = None):
    await fetch_news(
        ctx, query, number_of_articles, newsapi, user_preferences, user_articles
    )


# Run the bot
bot.run(DISCORD_BOT_TOKEN)
