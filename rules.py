# ⛓️ /rules — bảng nội quy phong cách Web3.0 (neon/cyber gradient)
import discord
from discord import app_commands
from discord.ext import commands
import config
from rules_banner import generate_rules_banner


# Nội quy mặc định — có thể chỉnh sửa trực tiếp ở đây
DEFAULT_RULES = [
    ("⟦ 01 ⟧ RESPECT PROTOCOL", "គោរពគ្នាទៅវិញទៅមក — ហាមជេរប្រមាថ សើចចំអក ឬ bully សមាជិកណាម្នាក់"),
    ("⟦ 02 ⟧ NO SPAM", "ហាមផ្ញើសារដដែលៗច្រើនដង ឬ flood channel"),
    ("⟦ 03 ⟧ CONTENT POLICY", "ហាមផុសខ្លឹមសារអាសអាភាស hate speech ឬ political drama"),
    ("⟦ 04 ⟧ NO UNAUTHORIZED ADS", "ហាមផ្សព្វផ្សាយ server/link ខាងក្រៅដោយគ្មានការអនុញ្ញាត"),
    ("⟦ 05 ⟧ CHANNEL USAGE", "ប្រើ channel ត្រូវតាមគោលបំណងរបស់វា"),
    ("⟦ 06 ⟧ STAY ACTIVE", "ចូលរួម clan wars/events ដើម្បីរក្សា role និង status"),
    ("⟦ 07 ⟧ TRUST THE CHAIN", "គោរពការសម្រេចចិត្តរបស់ Admin/Moderator — សម្រេចចុងក្រោយ"),
    ("⟦ 08 ⟧ IDENTITY STANDARD", "ឈ្មោះ និង avatar ត្រូវសមរម្យ"),
]

ENFORCEMENT = "⚠️ ការមិនគោរព Protocol → **Warning → Timeout → Kick → Ban**"


def build_rules_embed(guild: discord.Guild) -> discord.Embed:
    embed = discord.Embed(
        description=(
            "```\n"
            "> INITIALIZING SERVER PROTOCOL...\n"
            "> STATUS: ACTIVE\n"
            "```\n"
            "*ការចូលរួម server នេះមានន័យថាអ្នកយល់ព្រមតាម Protocol ខាងក្រោម*"
        ),
        color=config.COLOR_WEB3_PRIMARY,
    )
    embed.set_image(url="attachment://rules-banner.png")

    for name, value in DEFAULT_RULES:
        embed.add_field(name=name, value=value, inline=False)

    embed.add_field(name="⛔ ENFORCEMENT", value=ENFORCEMENT, inline=False)
    embed.set_footer(text=f"⛓ {config.SERVER_NAME} • Verified Protocol", icon_url=(guild.icon.url if guild.icon else None))
    embed.timestamp = discord.utils.utcnow()
    return embed


class Rules(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="rules", description="បង្កើត/ប្រកាស Server Rules រចនាប័ទ្ម Web3.0 (Admin)")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def rules(self, interaction: discord.Interaction):
        await interaction.response.defer()

        banner_buffer = generate_rules_banner(config.SERVER_NAME)
        file = discord.File(banner_buffer, filename="rules-banner.png")
        embed = build_rules_embed(interaction.guild)

        await interaction.channel.send(file=file, embed=embed)
        await interaction.followup.send("✅ បានប្រកាស Server Rules ជោគជ័យ! ⛓️", ephemeral=True)

    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("⚠️ អ្នកត្រូវការ permission **Manage Server** ដើម្បីប្រើ command នេះ", ephemeral=True)
        else:
            print(f"❌ Rules command error: {error}")
            if not interaction.response.is_done():
                await interaction.response.send_message(f"❌ មានបញ្ហា: {error}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Rules(bot))
