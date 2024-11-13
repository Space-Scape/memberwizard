import discord
import asyncio
from discord.ext import commands
import os  # Import os to get environment variables

# Channel ID Constants
RANK_UP_CHANNEL_ID = 1272648472184487937  # Replace with the actual ID of your rank-up channel
BECOME_MEMBER_CHANNEL_ID = 1272648453264248852  # Replace with the actual ID of your become-a-member channel
RULES_CHANNEL_ID = 1272629843552501802
SELF_ROLE_CHANNEL_ID = 1272648586198519818
SUPPORT_TICKET_CHANNEL_ID = 1272648498554077304

# Dictionary of rank images
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

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)  # Disable the default help command

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'memberwizard.py script is currently running')

# Monitor thread creation for "rank-up" and "become-a-member" channels
@bot.event
async def on_thread_create(thread):
    await asyncio.sleep(2)  # Wait to ensure messages are at the bottom

    # Detect threads in "rank-up" channel with format RankName-Nickname
    if thread.parent.id == RANK_UP_CHANNEL_ID and "-" in thread.name:
        # Extract the rank from the thread name (e.g., "Commander" from "Commander-SpaceScape")
        rank_name = thread.name.split("-")[0]

        # Get the image URL for the rank, if it exists
        rank_image_url = RANK_URLS.get(rank_name, None)

        # Construct the rank-up message
        embed = discord.Embed(
            title=f"Request a Rank Up for {rank_name} :crossed_swords:",
            description="### Important: 📢\n"
                        "1. No Bank Screenshots! 🚫🏦\n"
                        "2. Full client screenshots with chatbox open 📸\n"
                        "3. Please make sure you meet the requirements ⚔️\n"
                        "4. Your server nickname should match your RSN 👤\n\n"
                        "Select the role you are eligible for below.\n",
            color=discord.Color.red()
        )

        # Set the image in the embed if the rank image exists
        if rank_image_url:
            embed.set_image(url=rank_image_url)
        else:
            print(f"No image found for rank: {rank_name}")

        await thread.send(embed=embed)
    
    # Send welcome message in the "become-a-member" channel only
    elif thread.parent.id == BECOME_MEMBER_CHANNEL_ID and thread.name.startswith("Welcome-"):
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
        # Search for the thread using either the nickname or username
        thread_name_nickname = f"Welcome-{member.nick}" if member.nick else None
        thread_name_username = f"Welcome-{member.name}"
        
        # Find the thread that matches either the nickname or username
        thread = discord.utils.find(
            lambda t: t.name == thread_name_nickname or t.name == thread_name_username,
            become_member_channel.threads
        )
        
        if thread:
            embed = create_welcome_embed(guild, clan_staff_role_id)
            await thread.send(embed=embed)
        else:
            print(f"Thread not found for {member.name} or {member.nick}")
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
