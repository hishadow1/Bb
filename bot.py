import discord
from discord.ext import commands
from discord import app_commands
import json
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)
TREE = bot.tree

VPS_FILE = "vps_data.json"

# Create file if not exists
if not os.path.exists(VPS_FILE):
    with open(VPS_FILE, "w") as f:
        json.dump({}, f)

def load_vps():
    with open(VPS_FILE, "r") as f:
        return json.load(f)

def save_vps(data):
    with open(VPS_FILE, "w") as f:
        json.dump(data, f, indent=2)

@bot.event
async def on_ready():
    await TREE.sync()
    print(f"✅ Logged in as {bot.user}")

@TREE.command(name="crate", description="Create a new VPS with selected specs")
@app_commands.describe(
    name="VPS name",
    cpu="Number of CPU cores",
    ram="Amount of RAM in GB",
    disk="Disk size in GB"
)
async def crate(interaction: discord.Interaction, name: str, cpu: int, ram: int, disk: int):
    vps = load_vps()
    if name in vps:
        await interaction.response.send_message(f"❌ VPS '{name}' already exists.", ephemeral=True)
        return

    vps[name] = {
        "cpu": cpu,
        "ram": ram,
        "disk": disk,
        "owner": interaction.user.name
    }
    save_vps(vps)
    await interaction.response.send_message(f"✅ VPS '{name}' created with {cpu} CPU, {ram}GB RAM, {disk}GB Disk.")

@TREE.command(name="delete", description="Delete a VPS by name")
@app_commands.describe(name="VPS name to delete")
async def delete(interaction: discord.Interaction, name: str):
    vps = load_vps()
    if name not in vps:
        await interaction.response.send_message(f"❌ VPS '{name}' does not exist.", ephemeral=True)
        return

    del vps[name]
    save_vps(vps)
    await interaction.response.send_message(f"🗑️ VPS '{name}' deleted.")

@TREE.command(name="listvps", description="List all created VPS")
async def listvps(interaction: discord.Interaction):
    vps = load_vps()
    if not vps:
        await interaction.response.send_message("📭 No VPS found.")
        return

    msg = "**🖥️ Current VPS List:**\n"
    for name, info in vps.items():
        msg += f"• **{name}** - {info['cpu']} CPU, {info['ram']}GB RAM, {info['disk']}GB Disk (Owner: {info['owner']})\n"
    await interaction.response.send_message(msg)

# ⬇️ START BOT HERE ⬇️
bot.run("MTM5Mzc5MDYzNjY5OTk0NzA5MA.Gg6KfA.pwlg4yw0Nm7ghkOQhksd3nssRNX7J7kjSpdE3c")
