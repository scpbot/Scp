import os
from sys import platform
from shutil import copy
import disnake
from disnake.ext import commands, tasks
from cogs.utils.i18n import StaticResponse

static_response = StaticResponse()


class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def restart(self):
        # Create a new python process of bot.py and stops the current one
        os.chdir(self.bot.directory)
        python = "python" if platform == "win32" else "python3"
        cmd = os.popen(f"nohup {python} bot.py &")
        cmd.close()

    @commands.slash_command(name="bot")
    async def controlbot_group(self, inter):
        pass

    @commands.is_owner()
    @controlbot_group.sub_command(name="kill", description=static_response.get("brief-kill"))
    async def kill(self, inter):
        await inter.response.defer()
        await inter.edit_original_message(content=self.bot.response.get("shutdown", guild_id=inter.guild.id))
        await self.bot.close()

    @commands.is_owner()
    @controlbot_group.sub_command(name="restart", description=static_response.get("brief-restart"))
    async def restart_cmd(self, inter):
        if platform != "win32":
            self.restart()
            await inter.response.defer()
            await inter.edit_original_message(content=self.bot.response.get("restart", guild_id=inter.guild.id))
            await self.bot.close()
        else:
            await inter.send(self.bot.response.get("windows-error", guild_id=inter.guild.id))
            
def setup(bot):
    bot.add_cog(Control(bot))
