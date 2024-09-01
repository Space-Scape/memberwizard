import discord
import asyncio
from discord.ext import commands
from discord.ui import Button, View
import os  # Import os to get environment variables

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
    ("Aspirational 1", "aspirational1"),
    ("Aspirational 2", "aspirational2")
]

RANK_URLS = {
    "Recruit": "https://i.postimg.cc/fbw5kWMT/image.png",
    "Corporal": "https://i.postimg.cc/zG7yjqYQ/image.png",
    "Sergeant": "https://i.postimg.cc/HnYKb0wR/image.png",
    "TzTok": "https://i.postimg.cc/mkTDMn64/image.png",
    "Officer": "https://i.postimg.cc/6QSb8Jq7/image.png",
    "Commander": "https://i.postimg.cc/cJZ4P20n/image.png",
    "TzKal": "https://i.postimg.cc/59p7zCXd/image.png",
    "Aspirational 1": "https://i.postimg.cc/c4RQYq9K/image.png",
    "Aspirational 2": "https://i.postimg.cc/vTSCtgHz/image.png"
}

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'memberwizard.py script is currently running')

# Monitor thread creation for rank-up and become-a-member channels
@bot.event
async def on_thread_create(thread):
    await asyncio.sleep(2)  # Wait to ensure messages are at the bottom
    
    if thread.parent.name == "rank-up" and thread.name.startswith("Rank-Up-"):
        await show_rank_panel(thread)
    
    elif thread.parent.name == "become-a-member" and thread.name.startswith("Welcome-"):
        embed = discord.Embed(
            description="Please upload screenshots of our base requirements and a staff member will help you shortly.\n\n"
                        "**Important Notes:**\n"
                        "1. Everyone is starting fresh, so please make sure you meet the base requirements.\n"
                        "2. Your nickname in the server must match your RuneScape Name (RSN). You can set this by editing your Server Profile.",
            color=discord.Color.green()
        )
        embed.set_image(url="https://i.postimg.cc/fbw5kWMT/image.png")
        await thread.send(embed=embed)

# Function to show the rank panel
async def show_rank_panel(thread):
    guild = thread.guild
    embed = discord.Embed(
        title="Rank up",
        description="Please post screenshots within your ticket that contain the following:\n"
                    "1: Your in-game name (so we know it's really you).\n"
                    "2: The requirements in the image for the rank that you are applying for.",
        color=discord.Color.green()
    )

    view = View(timeout=None)

    for rank_name, rank_key in RANK_INFO:
        # Use your custom emoji
        custom_emoji = discord.utils.get(guild.emojis, name=rank_key)
        button = Button(label=rank_name, style=discord.ButtonStyle.primary, custom_id=rank_key, emoji=custom_emoji)
        button.callback = create_rank_callback(rank_name)
        view.add_item(button)

    await thread.send(embed=embed, view=view)

# Callback function when a rank is selected
def create_rank_callback(rank_name):
    async def rank_callback(interaction):
        embed = discord.Embed(
            title=f"{rank_name} Requirements",
            description=f"Here are the requirements for {rank_name}:",
            color=discord.Color.blue()
        )
        embed.set_image(url=RANK_URLS[rank_name])
        await interaction.response.send_message(embed=embed, ephemeral=False)

    return rank_callback

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
        description="**Congratulations on becoming a Recruit!**\nWe're thrilled to have you with us. 🎊\n\n"
                    f"First and foremost, please make sure you visit our 📜 **[Clan Rules](https://discord.com/channels/{guild.id}/1272629843552501802)** to ensure you're aware of the guidelines and avoid any accidental rule-breaking.\n\n"
                    "Below are some channels that will help you get started and connect with our community:\n\n"
                    f":busts_in_silhouette: **[Self-Role Assign](https://discord.com/channels/{guild.id}/1272648586198519818)**\n"
                    "     - *Select roles to be pinged for bosses and raids.*\n"
                    "💭 **[General Chat](https://discord.com/channels/{guild.id}/1272629331524587623)**\n"
                    "     - *Drop by and say hello!* 💬\n"
                    "✨ **[Drops and Achievements](https://discord.com/channels/{guild.id}/1272629331524587624)**\n"
                    "     - *Show off your gains and achievements.*\n"
                    "💬 **[Clan Chat](https://discord.com/channels/{guild.id}/1272875477555482666)**\n"
                    "     - *Stay updated on what's happening in the clan.*\n"
                    "🔎 **[PVM Team Finder](https://discord.com/channels/{guild.id}/1272648340940525648)**\n"
                    "     - *Find teams for PVM activities.*\n"
                    "📅 **[Events](https://discord.com/channels/{guild.id}/1272646577432825977)**\n"
                    "     - *Stay informed about upcoming events, competitions, and activities!*\n"
                    "⭐ **[Support Ticket](https://discord.com/channels/{guild.id}/1272648498554077304)**\n"
                    "     - *Contact the staff team by creating a support ticket.*\n"
                    "⚔️ **[Rank Up](https://discord.com/channels/{guild.id}/1272648472184487937)**\n"
                    "     - *Use the buttons in this channel to request a rank up.*\n\n"
                    f"⚠️ *If you encounter any issues, you can always reach out to the* <@&{clan_staff_role_id}> *or use the* **[Support Ticket](https://discord.com/channels/{guild.id}/1272648498554077304)** *channel for assistance.*\n\n"
                    "**We're excited to have you here!**\nGet involved, make new friends, and enjoy your time with us. 🌟",
        color=discord.Color.gold()
    ).set_thumbnail(url="https://i.postimg.cc/fbw5kWMT/image.png")

# Function to send the welcome message to the user's "become-a-member" ticket
async def send_welcome_message(member):
    guild = member.guild
    become_member_channel = discord.utils.get(guild.text_channels, name="become-a-member")
    clan_staff_role_id = 1272635396991221824  # Ensure this ID is correct and matches the "Clan Staff" role
    
    if become_member_channel:
        # Find the user's thread
        thread_name = f"Welcome-{member.name}"
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
