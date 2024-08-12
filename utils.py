# utils.py
import discord


async def update_article_message(message, user_articles, user_id, bot):
    user_data = user_articles.get(user_id)
    if user_data:
        articles = user_data["articles"]
        current_index = user_data["current"]
        if 0 <= current_index < len(articles):
            article = articles[current_index]
            title = article.get("title", "[No Title]")
            description = article.get("description", "[No Description]")
            url = article.get("url", "")

            embed = discord.Embed(title=title, description=description, url=url)
            embed.set_footer(text=f"Article {current_index + 1} of {len(articles)}")

            await message.edit(embed=embed)
        else:
            await message.edit(content="The current article index is out of bounds.")
    else:
        await message.edit(content="You have no articles to browse.")


async def handle_reaction_navigation(message, user_articles, user_id, bot):
    def check(reaction, user):
        return user == bot.user and str(reaction.emoji) in ["◀️", "▶️"]

    while True:
        try:
            reaction, user = await bot.wait_for(
                "reaction_add", timeout=60.0, check=check
            )
            if user.id == user_id:
                user_data = user_articles.get(user_id)
                if user_data:
                    if str(reaction.emoji) == "◀️":
                        user_data["current"] = (user_data["current"] - 1) % len(
                            user_data["articles"]
                        )
                    elif str(reaction.emoji) == "▶️":
                        user_data["current"] = (user_data["current"] + 1) % len(
                            user_data["articles"]
                        )

                    await update_article_message(message, user_articles, user_id, bot)
                    await message.remove_reaction(reaction.emoji, user)
        except Exception as e:
            print(f"An error occurred: {e}")
            break
