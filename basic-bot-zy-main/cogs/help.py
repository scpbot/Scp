from disnake.ext import commands
from cogs.utils.i18n import StaticResponse

static_response = StaticResponse()


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="help", description=static_response.get("brief-help"))
    @commands.guild_only()
    async def hlp(self, inter):
        if self.bot.isadmin(inter.author, inter.guild.id):
            await inter.response.defer()
            await inter.edit_original_message(
                content=self.bot.response.get("help-messages-title", guild_id=inter.guild.id)
                + self.bot.response.get("help-new", guild_id=inter.guild.id)
                + self.bot.response.get("help-edit", guild_id=inter.guild.id)
                + self.bot.response.get("help-reaction", guild_id=inter.guild.id)
                + self.bot.response.get("help-settings-title", guild_id=inter.guild.id)
                + self.bot.response.get("help-notify", guild_id=inter.guild.id)
                + self.bot.response.get("help-colour", guild_id=inter.guild.id)
                + self.bot.response.get("help-activity", guild_id=inter.guild.id)
                + self.bot.response.get("help-systemchannel", guild_id=inter.guild.id)
                + self.bot.response.get("help-language", guild_id=inter.guild.id)
                + self.bot.response.get("help-admins-title", guild_id=inter.guild.id)
                + self.bot.response.get("help-admin", guild_id=inter.guild.id)
                + self.bot.response.get("help-bot-control-title", guild_id=inter.guild.id)
                + self.bot.response.get("help-kill", guild_id=inter.guild.id)
                + self.bot.response.get("help-restart", guild_id=inter.guild.id)
                + self.bot.response.get("help-update", guild_id=inter.guild.id)
                + self.bot.response.get("help-version", guild_id=inter.guild.id)
                + self.bot.response.get("help-footer", guild_id=inter.guild.id).format(version=self.bot.version)
            )
        else:
            await inter.send(content=self.bot.response.get("not-admin", guild_id=inter.guild.id))


def setup(bot):
    bot.add_cog(Help(bot))
