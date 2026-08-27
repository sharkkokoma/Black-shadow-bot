# 🖤 Welcome / Leave / Auto-role / Member Count
import discord
from discord.ext import commands
import config
from welcome_card import generate_welcome_card


def format_message(template: str, member=None, guild=None, member_count=None) -> str:
    return (
        template.replace("{user}", member.mention if member else "")
        .replace("{username}", member.name if member else "")
        .replace("{server}", config.SERVER_NAME or (guild.name if guild else ""))
        .replace("{member_count}", str(member_count) if member_count is not None else "")
    )


class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def update_member_count_channel(self, guild: discord.Guild):
        if not config.MEMBER_COUNT_CHANNEL_ID:
            return
        try:
            channel = guild.get_channel(int(config.MEMBER_COUNT_CHANNEL_ID))
            if channel and isinstance(channel, discord.VoiceChannel):
                new_name = config.MEMBER_COUNT_FORMAT.replace("{member_count}", str(guild.member_count))
                await channel.edit(name=new_name)
        except Exception as e:
            print(f"❌ Error ធ្វើបច្ចុប្បន្នភាព member count: {e}")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        member_count = guild.member_count

        # ១. Auto-role
        if config.AUTO_ROLE_ID:
            try:
                role = guild.get_role(int(config.AUTO_ROLE_ID))
                if role:
                    await member.add_roles(role)
                    print(f"✅ បានផ្តល់ role \"{role.name}\" ទៅ {member}")
                else:
                    print("⚠️ រកមិនឃើញ AUTO_ROLE_ID ក្នុង server — ពិនិត្យ .env")
            except Exception as e:
                print(f"❌ មិនអាចផ្តល់ role បានទេ: {e}")

        # ២. Welcome message (Embed + Image)
        if config.WELCOME_CHANNEL_ID:
            try:
                channel = guild.get_channel(int(config.WELCOME_CHANNEL_ID))
                if channel:
                    image_buffer = await generate_welcome_card(member, member_count, config.WELCOME_BACKGROUND)
                    file = discord.File(image_buffer, filename="welcome-card.png")

                    embed = discord.Embed(
                        title=format_message(config.WELCOME_TITLE, member, guild, member_count),
                        description=format_message(config.WELCOME_DESC, member, guild, member_count),
                        color=config.COLOR_WELCOME,
                    )
                    embed.set_image(url="attachment://welcome-card.png")
                    if config.SERVER_ICON_URL:
                        embed.set_thumbnail(url=config.SERVER_ICON_URL)
                    elif guild.icon:
                        embed.set_thumbnail(url=guild.icon.url)
                    embed.set_footer(text=config.SERVER_NAME, icon_url=(guild.icon.url if guild.icon else None))
                    embed.timestamp = discord.utils.utcnow()

                    await channel.send(content=member.mention, embed=embed, file=file)
                else:
                    print("⚠️ រកមិនឃើញ WELCOME_CHANNEL_ID — ពិនិត្យ .env")
            except Exception as e:
                print(f"❌ Error ក្នុងការផ្ញើ welcome message: {e}")

        # ៣. DM Welcome
        if config.WELCOME_DM:
            try:
                dm_text = format_message(config.WELCOME_DM, member, guild, member_count)
                await member.send(dm_text)
            except Exception:
                print(f"ℹ️ មិនអាចផ្ញើ DM ទៅ {member} (គាត់ប្រហែលបិទ DM)")

        # ៤. Member count
        await self.update_member_count_channel(guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        guild = member.guild
        member_count = guild.member_count

        if config.LEAVE_CHANNEL_ID:
            try:
                channel = guild.get_channel(int(config.LEAVE_CHANNEL_ID))
                if channel:
                    embed = discord.Embed(
                        title=format_message(config.LEAVE_TITLE, member, guild, member_count),
                        description=format_message(config.LEAVE_DESC, member, guild, member_count),
                        color=config.COLOR_LEAVE,
                    )
                    embed.set_thumbnail(url=member.display_avatar.replace(size=256, format="png").url)
                    embed.set_footer(text=config.SERVER_NAME, icon_url=(guild.icon.url if guild.icon else None))
                    embed.timestamp = discord.utils.utcnow()
                    await channel.send(embed=embed)
            except Exception as e:
                print(f"❌ Error ក្នុងការផ្ញើ leave message: {e}")

        await self.update_member_count_channel(guild)


async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))
