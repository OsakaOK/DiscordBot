import discord
from discord.ext import commands
from utils import update_article_message, handle_reaction_navigation


async def fetch_news(
    ctx, query, number_of_articles, newsapi, user_preferences, user_articles
):
    if query is None or query.isdigit():
        query = user_preferences.get(ctx.author.id, "general")

    if number_of_articles is None:
        number_of_articles = 5

    try:
        # Fetch articles from NewsAPI
        articles = newsapi.get_everything(
            q=query,
            qintitle=query,
            language="en",
            sort_by="relevancy",
            page_size=number_of_articles,
        )

        if articles["articles"]:
            user_articles[ctx.author.id] = {
                "articles": articles["articles"],
                "current": 0,
            }
            await show_article(ctx, user_articles)
        else:
            await ctx.send("No news found for that topic.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


async def show_article(ctx, user_articles):
    user_data = user_articles.get(ctx.author.id)
    if user_data:
        article = user_data["articles"][user_data["current"]]
        title = article.get("title", "[No Title]")
        description = article.get("description", "[No Description]")
        url = article.get("url", "")

        embed = discord.Embed(title=title, description=description, url=url)
        embed.set_footer(
            text=f"Article {user_data['current'] + 1} of {len(user_data['articles'])}"
        )

        message = await ctx.send(embed=embed)
        await message.add_reaction("◀️")  # Previous
        await message.add_reaction("▶️")  # Next

        await handle_reaction_navigation(message, user_articles, ctx.author.id, ctx.bot)


async def set_preferences(ctx, *, preference: str, user_preferences):
    user_preferences[ctx.author.id] = preference
    await ctx.send(f"Your preference has been set to: {preference}")


async def get_my_preferences(ctx, user_preferences):
    preference = user_preferences.get(ctx.author.id, None)
    if preference:
        await ctx.send(f"Your current preference is: {preference}")
    else:
        await ctx.send("You have no preferences set.")
