from disnake.ext import commands


class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot Status ready!")
        await self.bot.database_updates()


def setup(bot):
    bot.add_cog(Ready(bot))
