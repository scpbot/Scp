from sqlite3 import Error as DatabaseError
import disnake
from disnake.ext import commands
from cogs.utils.i18n import StaticResponse

static_response = StaticResponse()


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="admin", description=static_response.get("brief-admin"))
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def admin(
        self,
        inter,
        action: str = commands.Param(description=static_response.get("admin-option-action"), choices={"add", "remove", "list"}),
        role: disnake.Role = commands.Param(description=static_response.get("admin-option-role"), default=None),
    ):
        await inter.response.defer()
        if role is None or action == "list":
            # Lists all admin IDs in the database, mentioning them if possible
            try:
                admin_ids = self.bot.db.get_admins(inter.guild.id)
            except DatabaseError as error:
                await self.bot.report(
                    self.bot.response.get("db-error-fetching-admins", guild_id=inter.guild.id).format(exception=error),
                    inter.guild.id,
                )
                return

            adminrole_objects = []
            for admin_id in admin_ids:
                adminrole_objects.append(disnake.utils.get(inter.guild.roles, id=admin_id).mention)

            if adminrole_objects:
                await inter.edit_original_message(
                    content=self.bot.response.get("adminlist-local", guild_id=inter.guild.id).format(
                        admin_list="\n- ".join(adminrole_objects)
                    )
                )
            else:
                await inter.edit_original_message(content=self.bot.response.get("adminlist-local-empty", guild_id=inter.guild.id))

        elif action == "add":
            # Adds an admin role ID to the database
            try:
                self.bot.db.add_admin(role.id, inter.guild.id)
            except DatabaseError as error:
                await self.bot.report(
                    self.bot.response.get("db-error-admin-add", guild_id=inter.guild.id).format(exception=error), inter.guild.id
                )
                return

            await inter.edit_original_message(content=self.bot.response.get("admin-add-success", guild_id=inter.guild.id))

        elif action == "remove":
            # Removes an admin role ID from the database
            try:
                self.bot.db.remove_admin(role.id, inter.guild.id)
            except DatabaseError as error:
                await self.bot.report(
                    self.bot.response.get("db-error-admin-remove", guild_id=inter.guild.id).format(exception=error),
                    inter.guild.id,
                )
                return

            await inter.edit_original_message(content=self.bot.response.get("admin-remove-success", guild_id=inter.guild.id))


def setup(bot):
    bot.add_cog(Admin(bot))
