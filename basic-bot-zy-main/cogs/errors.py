import traceback
from disnake.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        if isinstance(error, commands.errors.NotOwner):
            await inter.send(self.bot.response.get("not-owner", guild_id=inter.guild.id))
        elif isinstance(error, commands.errors.NoPrivateMessage):
            await inter.send(self.bot.response.get("no-dm"))
        else:
            traceback.print_tb(error.__traceback__)
            print(error)


def setup(bot):
    bot.add_cog(Errors(bot))
