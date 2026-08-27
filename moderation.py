# ⚔️ Moderation Commands — kick, ban, unban, mute, unmute, warn, clear, lock, unlock, slowmode, nickname
import discord
from discord import app_commands
from discord.ext import commands
import config
import datetime


async def log_action(guild: discord.Guild, embed: discord.Embed):
    """ផ្ញើ log ទៅ mod-log channel បើមាន configure"""
    if not config.MOD_LOG_CHANNEL_ID:
        return
    try:
        channel = guild.get_channel(int(config.MOD_LOG_CHANNEL_ID))
        if channel:
            await channel.send(embed=embed)
    except Exception as e:
        print(f"❌ Error ផ្ញើ mod log: {e}")


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ═══════════ KICK ═══════════
    @app_commands.command(name="kick", description="បណ្តេញសមាជិកចេញពី server")
    @app_commands.describe(member="សមាជិកដែលត្រូវបណ្តេញ", reason="មូលហេតុ")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "មិនបានបញ្ជាក់"):
        if member.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message("⚠️ អ្នកមិនអាចបណ្តេញសមាជិកដែលមាន role ខ្ពស់ជាង ឬស្មើអ្នកបានទេ", ephemeral=True)

        try:
            await member.send(f"🚫 អ្នកត្រូវបានបណ្តេញចេញពី **{interaction.guild.name}**\nមូលហេតុ: {reason}")
        except Exception:
            pass

        await member.kick(reason=reason)
        embed = discord.Embed(title="👢 Kick", color=config.COLOR_WARNING, timestamp=discord.utils.utcnow())
        embed.add_field(name="សមាជិក", value=f"{member} ({member.id})", inline=False)
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=False)
        embed.add_field(name="មូលហេតុ", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)
        await log_action(interaction.guild, embed)

    # ═══════════ BAN ═══════════
    @app_commands.command(name="ban", description="Ban សមាជិកចេញពី server")
    @app_commands.describe(member="សមាជិកដែលត្រូវ ban", reason="មូលហេតុ", delete_days="លុបសារចាស់ប៉ុន្មានថ្ងៃ (0-7)")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "មិនបានបញ្ជាក់", delete_days: app_commands.Range[int, 0, 7] = 0):
        if member.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message("⚠️ អ្នកមិនអាច ban សមាជិកដែលមាន role ខ្ពស់ជាង ឬស្មើអ្នកបានទេ", ephemeral=True)

        try:
            await member.send(f"🔨 អ្នកត្រូវបាន ban ពី **{interaction.guild.name}**\nមូលហេតុ: {reason}")
        except Exception:
            pass

        await member.ban(reason=reason, delete_message_days=delete_days)
        embed = discord.Embed(title="🔨 Ban", color=config.COLOR_ERROR, timestamp=discord.utils.utcnow())
        embed.add_field(name="សមាជិក", value=f"{member} ({member.id})", inline=False)
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=False)
        embed.add_field(name="មូលហេតុ", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)
        await log_action(interaction.guild, embed)

    # ═══════════ UNBAN ═══════════
    @app_commands.command(name="unban", description="Unban អ្នកប្រើប្រាស់ (ដាក់ User ID)")
    @app_commands.describe(user_id="User ID របស់អ្នកដែលត្រូវ unban")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str):
        try:
            user = await self.bot.fetch_user(int(user_id))
            await interaction.guild.unban(user)
            embed = discord.Embed(title="✅ Unban", description=f"បាន unban **{user}**", color=config.COLOR_SUCCESS)
            await interaction.response.send_message(embed=embed)
            await log_action(interaction.guild, embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ មិនអាច unban បានទេ: {e}", ephemeral=True)

    # ═══════════ MUTE / TIMEOUT ═══════════
    @app_commands.command(name="mute", description="Timeout សមាជិកមួយរយៈពេល")
    @app_commands.describe(member="សមាជិកដែលត្រូវ mute", minutes="រយៈពេល (នាទី)", reason="មូលហេតុ")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, minutes: app_commands.Range[int, 1, 40320], reason: str = "មិនបានបញ្ជាក់"):
        duration = datetime.timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        embed = discord.Embed(title="🔇 Mute (Timeout)", color=config.COLOR_WARNING, timestamp=discord.utils.utcnow())
        embed.add_field(name="សមាជិក", value=f"{member} ({member.id})", inline=False)
        embed.add_field(name="រយៈពេល", value=f"{minutes} នាទី", inline=False)
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=False)
        embed.add_field(name="មូលហេតុ", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)
        await log_action(interaction.guild, embed)

    # ═══════════ UNMUTE ═══════════
    @app_commands.command(name="unmute", description="ដកចេញ Timeout")
    @app_commands.describe(member="សមាជិកដែលត្រូវ unmute")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        await member.timeout(None)
        embed = discord.Embed(title="🔊 Unmute", description=f"បាន unmute {member.mention}", color=config.COLOR_SUCCESS)
        await interaction.response.send_message(embed=embed)
        await log_action(interaction.guild, embed)

    # ═══════════ WARN ═══════════
    @app_commands.command(name="warn", description="ព្រមានសមាជិក")
    @app_commands.describe(member="សមាជិកដែលត្រូវព្រមាន", reason="មូលហេតុ")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        try:
            await member.send(f"⚠️ អ្នកទទួលបានការព្រមានក្នុង **{interaction.guild.name}**\nមូលហេតុ: {reason}")
        except Exception:
            pass
        embed = discord.Embed(title="⚠️ Warning", color=config.COLOR_WARNING, timestamp=discord.utils.utcnow())
        embed.add_field(name="សមាជិក", value=f"{member} ({member.id})", inline=False)
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=False)
        embed.add_field(name="មូលហេតុ", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)
        await log_action(interaction.guild, embed)

    # ═══════════ CLEAR / PURGE ═══════════
    @app_commands.command(name="clear", description="លុបសារជាច្រើនក្នុងម្តង")
    @app_commands.describe(amount="ចំនួនសារត្រូវលុប (1-100)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]):
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"🗑️ បានលុប **{len(deleted)}** សារ", ephemeral=True)

    # ═══════════ LOCK ═══════════
    @app_commands.command(name="lock", description="Lock channel (រារាំង @everyone ផ្ញើសារ)")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction):
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = False
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(description="🔒 Channel នេះត្រូវបាន lock", color=config.COLOR_WARNING)
        await interaction.response.send_message(embed=embed)

    # ═══════════ UNLOCK ═══════════
    @app_commands.command(name="unlock", description="Unlock channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = None
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(description="🔓 Channel នេះត្រូវបាន unlock", color=config.COLOR_SUCCESS)
        await interaction.response.send_message(embed=embed)

    # ═══════════ SLOWMODE ═══════════
    @app_commands.command(name="slowmode", description="កំណត់ slowmode សម្រាប់ channel")
    @app_commands.describe(seconds="ចំនួនវិនាទី (0 = បិទ)")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: discord.Interaction, seconds: app_commands.Range[int, 0, 21600]):
        await interaction.channel.edit(slowmode_delay=seconds)
        msg = f"🐢 Slowmode កំណត់ត្រឹម **{seconds}** វិនាទី" if seconds > 0 else "🐇 Slowmode បានបិទ"
        await interaction.response.send_message(embed=discord.Embed(description=msg, color=config.COLOR_INFO))

    # ═══════════ NICKNAME ═══════════
    @app_commands.command(name="nickname", description="ប្តូរ nickname របស់សមាជិក")
    @app_commands.describe(member="សមាជិក", new_nick="ឈ្មោះថ្មី")
    @app_commands.checks.has_permissions(manage_nicknames=True)
    async def nickname(self, interaction: discord.Interaction, member: discord.Member, new_nick: str):
        old_nick = member.display_name
        await member.edit(nick=new_nick)
        await interaction.response.send_message(embed=discord.Embed(description=f"✏️ ប្តូរឈ្មោះ {member.mention}: `{old_nick}` → `{new_nick}`", color=config.COLOR_SUCCESS))

    # ═══════════ Error handler សម្រាប់ permission errors ═══════════
    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("⚠️ អ្នកមិនមាន permission គ្រប់គ្រាន់ដើម្បីប្រើ command នេះទេ", ephemeral=True)
        else:
            print(f"❌ Moderation command error: {error}")
            if not interaction.response.is_done():
                await interaction.response.send_message(f"❌ មានបញ្ហា: {error}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
