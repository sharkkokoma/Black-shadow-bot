# 🛠️ Utility Commands — ping, userinfo, serverinfo, avatar, banner, roleinfo, membercount, uptime, botinfo
import discord
from discord import app_commands
from discord.ext import commands
import config
import time
import platform

START_TIME = time.time()


class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ═══════════ PING ═══════════
    @app_commands.command(name="ping", description="មើល latency របស់ bot")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(title="🏓 Pong!", description=f"Latency: **{latency}ms**", color=config.COLOR_INFO)
        await interaction.response.send_message(embed=embed)

    # ═══════════ USERINFO ═══════════
    @app_commands.command(name="userinfo", description="មើលព័ត៌មានសមាជិក")
    @app_commands.describe(member="សមាជិកដែលចង់មើល (ទុកទទេ = ខ្លួនអ្នក)")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        roles = [r.mention for r in reversed(member.roles) if r.name != "@everyone"]
        embed = discord.Embed(title=f"👤 {member}", color=member.color if member.color.value else config.COLOR_INFO)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nickname", value=member.display_name, inline=True)
        embed.add_field(name="Bot?", value="✅" if member.bot else "❌", inline=True)
        embed.add_field(name="ចូល Discord", value=discord.utils.format_dt(member.created_at, "R"), inline=True)
        embed.add_field(name="ចូល Server", value=discord.utils.format_dt(member.joined_at, "R") if member.joined_at else "N/A", inline=True)
        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join(roles[:15]) if roles else "គ្មាន", inline=False)
        await interaction.response.send_message(embed=embed)

    # ═══════════ SERVERINFO ═══════════
    @app_commands.command(name="serverinfo", description="មើលព័ត៌មាន server")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title=f"🏰 {guild.name}", color=config.COLOR_INFO)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="ម្ចាស់", value=str(guild.owner), inline=True)
        embed.add_field(name="សមាជិក", value=guild.member_count, inline=True)
        embed.add_field(name="បង្កើតនៅ", value=discord.utils.format_dt(guild.created_at, "R"), inline=True)
        embed.add_field(name="Text channels", value=len(guild.text_channels), inline=True)
        embed.add_field(name="Voice channels", value=len(guild.voice_channels), inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Boost level", value=f"Level {guild.premium_tier} ({guild.premium_subscription_count} boosts)", inline=True)
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        await interaction.response.send_message(embed=embed)

    # ═══════════ AVATAR ═══════════
    @app_commands.command(name="avatar", description="មើលរូបភាព avatar ពេញ")
    @app_commands.describe(member="សមាជិកដែលចង់មើល (ទុកទទេ = ខ្លួនអ្នក)")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        embed = discord.Embed(title=f"🖼️ Avatar របស់ {member.display_name}", color=config.COLOR_INFO)
        embed.set_image(url=member.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    # ═══════════ BANNER ═══════════
    @app_commands.command(name="banner", description="មើល banner របស់សមាជិក")
    @app_commands.describe(member="សមាជិកដែលចង់មើល (ទុកទទេ = ខ្លួនអ្នក)")
    async def banner(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        user = await self.bot.fetch_user(member.id)
        if not user.banner:
            return await interaction.response.send_message("⚠️ សមាជិកនេះគ្មាន banner ទេ", ephemeral=True)
        embed = discord.Embed(title=f"🎏 Banner របស់ {member.display_name}", color=config.COLOR_INFO)
        embed.set_image(url=user.banner.url)
        await interaction.response.send_message(embed=embed)

    # ═══════════ ROLEINFO ═══════════
    @app_commands.command(name="roleinfo", description="មើលព័ត៌មាន role")
    @app_commands.describe(role="Role ដែលចង់មើល")
    async def roleinfo(self, interaction: discord.Interaction, role: discord.Role):
        embed = discord.Embed(title=f"🎭 {role.name}", color=role.color if role.color.value else config.COLOR_INFO)
        embed.add_field(name="ID", value=role.id, inline=True)
        embed.add_field(name="ពណ៌", value=str(role.color), inline=True)
        embed.add_field(name="សមាជិកមាន role នេះ", value=len(role.members), inline=True)
        embed.add_field(name="Mentionable?", value="✅" if role.mentionable else "❌", inline=True)
        embed.add_field(name="Hoisted?", value="✅" if role.hoist else "❌", inline=True)
        embed.add_field(name="បង្កើតនៅ", value=discord.utils.format_dt(role.created_at, "R"), inline=True)
        await interaction.response.send_message(embed=embed)

    # ═══════════ MEMBERCOUNT ═══════════
    @app_commands.command(name="membercount", description="មើលចំនួនសមាជិកសរុប")
    async def membercount(self, interaction: discord.Interaction):
        guild = interaction.guild
        humans = sum(1 for m in guild.members if not m.bot)
        bots = sum(1 for m in guild.members if m.bot)
        embed = discord.Embed(title=f"👥 សមាជិក {guild.name}", color=config.COLOR_INFO)
        embed.add_field(name="សរុប", value=guild.member_count, inline=True)
        embed.add_field(name="មនុស្ស", value=humans, inline=True)
        embed.add_field(name="Bots", value=bots, inline=True)
        await interaction.response.send_message(embed=embed)

    # ═══════════ BOTINFO ═══════════
    @app_commands.command(name="botinfo", description="មើលព័ត៌មាន bot")
    async def botinfo(self, interaction: discord.Interaction):
        uptime_seconds = int(time.time() - START_TIME)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        embed = discord.Embed(title=f"🖤 {self.bot.user.name}", color=config.COLOR_WELCOME)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Users", value=sum(g.member_count for g in self.bot.guilds), inline=True)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Uptime", value=f"{hours}h {minutes}m {seconds}s", inline=True)
        embed.add_field(name="discord.py", value=discord.__version__, inline=True)
        embed.add_field(name="Python", value=platform.python_version(), inline=True)
        await interaction.response.send_message(embed=embed)

    # ═══════════ INVITE ═══════════
    @app_commands.command(name="invite", description="យក invite link របស់ bot")
    async def invite(self, interaction: discord.Interaction):
        client_id = config.CLIENT_ID or self.bot.user.id
        url = f"https://discord.com/oauth2/authorize?client_id={client_id}&permissions=8&scope=bot%20applications.commands"
        embed = discord.Embed(title="🔗 Invite Bot", description=f"[ចុចទីនេះដើម្បីអញ្ជើញ bot]({url})", color=config.COLOR_INFO)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))
