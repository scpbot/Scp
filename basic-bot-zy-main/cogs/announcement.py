import configparser
import asyncio
import disnake
from disnake.ext import commands
from cogs.utils.sanitizing import sanitize_emoji
from cogs.utils.i18n import StaticResponse

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Get logo and color from config
logo = config['server']['logo']
colour = int(config['server']['colour'], 16)  # Convert hex string to int

static_response = StaticResponse()

class Announcement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="announce")
    async def message_group(self, inter):
        pass

    @message_group.sub_command(name="new", description=static_response.get("brief-message-new"))
    @commands.guild_only()
    async def new(self, inter):
        if not self.bot.isadmin(inter.author, inter.guild.id):
            await inter.send(self.bot.response.get("new-reactionrole-noadmin", guild_id=inter.guild.id))
            return
        
        await inter.send("Please send the announcement message.")

        # Wait for the next message from the user
        def check(msg):
            return msg.author == inter.author and msg.channel == inter.channel

        try:
            user_message = await self.bot.wait_for('message', check=check, timeout=60)  # 60 seconds timeout
        except asyncio.TimeoutError:
            return await inter.send("You took too long to respond. Please try again.")

        await inter.send("Please mention the channel where the announcement will be posted.")

        # Wait for the next message which should be a channel mention
        try:
            channel_message = await self.bot.wait_for('message', check=check, timeout=60)
            channel = channel_message.channel_mentions[0] if channel_message.channel_mentions else None
            
            if not channel:
                return await inter.send("You need to mention a valid channel. Please try again.")

        except asyncio.TimeoutError:
            return await inter.send("You took too long to respond. Please try again.")

        # Create the embed for the announcement
        embed = disnake.Embed(
            title="📢 Announcement!!",
            description=user_message.content,
            color=colour  # Set the color from the config
        )
        embed.set_footer(text="Timestamp: " + disnake.utils.utcnow().strftime('%Y-%m-%d %H:%M:%S'), icon_url=logo)  # Set the footer with a logo
        
        # Send the embed to the mentioned channel
        await channel.send(embed=embed)
        await inter.send(f"Announcement sent to {channel.mention}!")

def setup(bot):
    bot.add_cog(Announcement(bot))
