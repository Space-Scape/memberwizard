import discord
import asyncio
from discord.ext import commands
from discord.ui import Button, View
import os  # Import os to get environment variables

# Channel ID Constants
RANK_UP_CHANNEL_ID = 1272648472184487937
BECOME_MEMBER_CHANNEL_ID = 1272648453264248852
RULES_CHANNEL_ID = 1272629843552501802
SELF_ROLE_CHANNEL_ID = 1272648586198519818
SUPPORT_TICKET_CHANNEL_ID = 1272648498554077304

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)  # Disable the default help command

# Basic setup for ranks and rank panel
RANK_INFO = [
    ("Recruit", "recruit"),
    ("Corporal", "corporal"),
    ("Sergeant", "sergeant"),
    ("TzTok", "tztok"),
    ("Officer", "officer"),
    ("Commander", "commander"),
    ("TzKal", "tzkal"),
    ("Twisted", "twisted"),
    ("Sanguine", "sanguine")
]

RANK_URLS = {
    "Recruit": "https://i.postimg.cc/4xQvGn4j/image.png",
    "Corporal": "https://i.postimg.cc/qqQ008Yz/image.png",
    "Sergeant": "https://i.postimg.cc/yNTLLvSg/image.png",
    "TzTok": "https://i.postimg.cc/2S0wvVph/image.png",
    "Officer": "https://i.postimg.cc/RF5nnB0w/image.png",
    "Commander": "https://i.postimg.cc/wxF79JDX/image.png",
    "TzKal": "https://i.postimg.cc/FzKCdqGg/image.png",
    "Twisted": "https://i.postimg.cc/GttFFTN6/image.png",
    "Sanguine": "https://i.postimg.cc/MTPyZkmy/image.png"
}

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'memberwizard.py script is currently running')

# Monitor thread creation for the "become-a-member" channel only
@bot.event
async def on_thread_create(thread):
    await asyncio.sleep(2)  # Wait to ensure messages are at the bottom
    
    # Handle welcome message in the "become-a-member" channel only
    if thread.parent.id == BECOME_MEMBER_CHANNEL_ID and thread.name.startswith("Welcome-"):
        embed = discord.Embed(
            title="Welcome :wave:",
            description="### Please upload screenshots of our base requirements and a staff member will help you when available. :hourglass: ###\n"
                        "## **Important:**  :loudspeaker: ##\n"
                        "### 1. No Bank Screenshots! :no_entry_sign: :bank: ###\n"
                        "### 2. Full client screenshots with chatbox open :camera: ###\n"
                        "### 3. Please make sure you meet the requirements :crossed_swords: ###\n"
                        "### 4. Your server nickname must match your RSN :bust_in_silhouette: ###\n"
                        "# Base requirements to join: #",
            color=discord.Color.green()
        )
        embed.set_image(url="https://i.postimg.cc/fbw5kWMT/image.png")
        await thread.send(embed=embed)

# Handle the addition of the "Recruit" role
@bot.event
async def on_member_update(before, after):
    # Check if the "Recruit" role was added
    recruit_role = discord.utils.get(after.guild.roles, name="Recruit")
    if recruit_role and recruit_role not in before.roles and recruit_role in after.roles:
        await send_welcome_message(after)

# Function to create the welcome message embed
def create_welcome_embed(guild, clan_staff_role_id):
    return discord.Embed(
        title="🎉 Welcome to the Clan! 🎉",
        description="**We're thrilled to have you with us!** 🎊\n\n"
                    f"First and foremost, please make sure you visit our 📜 **[Clan Rules](https://discord.com/channels/{guild.id}/{RULES_CHANNEL_ID})** to ensure you're aware of the guidelines.\n\n"
                    "Below are some channels that will help you get started:\n\n"
                    f"💡 **[Self-Role Assign](https://discord.com/channels/{guild.id}/{SELF_ROLE_CHANNEL_ID})**\n"
                    "     - *Select roles to be pinged for bosses and raids.*\n"
                    "💭 **[General Chat](https://discord.com/channels/{guild.id}/1272629331524587623)**\n"
                    "     - *Drop by and say hello!* 💬\n"
                    "✨ **[Drops and Achievements](https://discord.com/channels/{guild.id}/1272629331524587624)**\n"
                    "     - *Show off your gains and achievements.*\n"
                    "💬 **[Clan Chat](https://discord.com/channels/{guild.id}/1272875477555482666)**\n"
                    "     - *Stay updated on what's happening in the clan.*\n"
                    "🏹 **[PVM Team Finder](https://discord.com/channels/{guild.id}/1272648340940525648)**\n"
                    "     - *Find teams for PVM activities.*\n"
                    ":loudspeaker: **[Events](https://discord.com/channels/{guild.id}/1272646577432825977)**\n"
                    "     - *Stay informed about upcoming events, competitions, and activities!*\n"
                    "⭐ **[Support Ticket](https://discord.com/channels/{guild.id}/{SUPPORT_TICKET_CHANNEL_ID})**\n"
                    "     - *Contact the staff team by creating a support ticket.*\n"
                    "⚔️ **[Rank Up](https://discord.com/channels/{guild.id}/{RANK_UP_CHANNEL_ID})**\n"
                    "     - *Use the buttons in this channel to request a rank up.*\n\n"
                    f"⚠️ *If you encounter any issues, you can always reach out to the Clan Staff or use the* **[Support Ticket](https://discord.com/channels/{guild.id}/{SUPPORT_TICKET_CHANNEL_ID})** *channel for assistance.*\n\n"
                    "**We're excited to have you here!**\nGet involved, make new friends, and enjoy your time with us. 🌟",
        color=discord.Color.gold()
    ).set_thumbnail(url="https://i.postimg.cc/fbw5kWMT/image.png")

# Function to send the welcome message to the user's "become-a-member" ticket
async def send_welcome_message(member):
    guild = member.guild
    become_member_channel = guild.get_channel(BECOME_MEMBER_CHANNEL_ID)
    clan_staff_role_id = 1272635396991221824  # Ensure this ID is correct and matches the "Clan Staff" role
    
    if become_member_channel:
        # Use the unique member ID for finding the thread
        thread_name = f"Welcome-{member.id}"
        thread = discord.utils.get(become_member_channel.threads, name=thread_name)
        
        if thread:
            embed = create_welcome_embed(guild, clan_staff_role_id)
            await thread.send(embed=embed)
        else:
            print(f"Thread not found: {thread_name}")
    else:
        print("Channel not found: become-a-member")

# Command to manually trigger the welcome message in the current channel
@bot.command()
async def welcome(ctx):
    guild = ctx.guild
    clan_staff_role_id = 1272635396991221824  # Ensure this ID is correct and matches the "Clan Staff" role
    
    embed = create_welcome_embed(guild, clan_staff_role_id)
    await ctx.send(embed=embed)

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
