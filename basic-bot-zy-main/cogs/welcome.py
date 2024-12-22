import os
import configparser
import asyncio
import disnake
import logging
from disnake.ext import commands
import sqlite3
from cogs.utils.sanitizing import sanitize_emoji
from cogs.utils.i18n import StaticResponse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Connect to SQLite database
def db_connect():
    # Create 'files' directory if it does not exist
    db_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files')
    os.makedirs(db_directory, exist_ok=True)
    
    # Define the path for the SQLite database
    db_path = os.path.join(db_directory, 'welcome.db')
    conn = sqlite3.connect(db_path)
    return conn

# Create the table if it doesn't exist
def create_table():
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS welcome_config (
            guild_id INTEGER PRIMARY KEY,
            color INTEGER,
            title TEXT,
            message TEXT,
            channel_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()

create_table()

static_response = StaticResponse()

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="welcome")
    async def message_group(self, inter):
        pass

    @message_group.sub_command(name="setcolor", description="Set the welcome message embed color.")
    @commands.guild_only()
    async def set_color(self, inter, color: str):
        color_hex = int(color, 16)  # Expecting color in hex format
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO welcome_config (guild_id, color) VALUES (?, ?)', (inter.guild.id, color_hex))
        conn.commit()
        conn.close()
        await inter.send(f"Welcome message color set to {color}.")

    @message_group.sub_command(name="settitle", description="Set the welcome message embed title.")
    @commands.guild_only()
    async def set_title(self, inter, title: str):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO welcome_config (guild_id, title) VALUES (?, ?)', (inter.guild.id, title))
        conn.commit()
        conn.close()
        await inter.send(f"Welcome message title set to `{title}`.")

    @message_group.sub_command(name="setmessage", description="Set the welcome message.")
    @commands.guild_only()
    async def set_message(self, inter, *, msg: str):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO welcome_config (guild_id, message) VALUES (?, ?)', (inter.guild.id, msg))
        conn.commit()
        conn.close()
        await inter.send(f"Welcome message set to: `{msg}`.")

    @message_group.sub_command(name="setchannel", description="Set the channel for welcome messages.")
    @commands.guild_only()
    async def set_channel(self, inter, channel: disnake.TextChannel):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO welcome_config (guild_id, channel_id) VALUES (?, ?)', (inter.guild.id, channel.id))
        conn.commit()
        conn.close()
        await inter.send(f"Welcome messages will be sent to {channel.mention}.")
        
    @message_group.sub_command(name="test", description="Testing welcome message sending")
    @commands.guild_only()
    async def test_welcome(self, inter, member: disnake.Member):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute('SELECT color, title, message, channel_id FROM welcome_config WHERE guild_id = ?', (inter.guild.id,))
        config = cursor.fetchone()
        conn.close()

        if config:
            color, title, message, channel_id = config
            channel = self.bot.get_channel(channel_id)
            if channel:
                embed = disnake.Embed(
                    title=title or "Welcome!",
                    description=message.replace("$USER", member.mention) if message else f"Welcome {member.mention}!",
                    color=color or 0x3498db  # Default color if none is set
                )
                await channel.send(embed=embed)
                await inter.send(f"Welcome message sent to {member.mention} in {channel.mention}.")
            else:
                await inter.send("Channel not found.")
        else:
            await inter.send("No welcome configuration found for this server.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        logging.info(f"{member.name} has joined the guild {member.guild.name}.")

        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute('SELECT color, title, message, channel_id FROM welcome_config WHERE guild_id = ?', (member.guild.id,))
        config = cursor.fetchone()
        conn.close()

        if config:
            color, title, message, channel_id = config
            channel = self.bot.get_channel(channel_id)
            if channel:
                embed = disnake.Embed(
                    title=title or "Welcome!",
                    description=message.replace("$USER", member.mention) if message else f"Welcome {member.mention}!",
                    color=color or 0x3498db  # Default color if none is set
                )
                embed.set_thumbnail(url=member.avatar.url)
                await channel.send(embed=embed)
                logging.info(f"Sent welcome message to {member.mention} in {channel.mention}.")
            else:
                logging.warning(f"Channel for welcome messages not found: {channel_id}.")
        else:
            logging.warning(f"No welcome configuration found for guild: {member.guild.name}.")

def setup(bot):
    bot.add_cog(Welcome(bot))
