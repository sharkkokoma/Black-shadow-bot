# 🖤 BLACK SHADOW Discord Bot ⚔️ (Python / discord.py)
# Welcome system + Moderation + Utility + Fun + Web3.0 Rules — Slash Commands
# Keep-alive 24/7 ready

import asyncio
import discord
from discord.ext import commands

import config
from keep_alive import keep_alive

# ─────────────────────────────
# ១. Intents
# ─────────────────────────────
intents = discord.Intents.default()
intents.members = True          # ចាំបាច់សម្រាប់ on_member_join / on_member_remove
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

COGS = [
    "cogs.welcome",
    "cogs.moderation",
    "cogs.utility",
    "cogs.fun",
    "cogs.rules",
]


# ─────────────────────────────
# ២. Event: Bot Ready — sync slash commands
# ─────────────────────────────
@bot.event
async def on_ready():
    print(f"✅ Bot ចូល login ជោគជ័យជា {bot.user}")
    print("🖤 BLACK SHADOW Bot កំពុងដំណើរការ! ⚔️")

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="BLACK SHADOW ⚔️"))

    try:
        if config.GUILD_ID:
            # Sync ត្រឹមតែ guild តែមួយ — លឿនណាស់ (instant), ល្អសម្រាប់ dev/testing
            guild = discord.Object(id=int(config.GUILD_ID))
            synced = await bot.tree.sync(guild=guild)
            print(f"⚡ Sync {len(synced)} slash commands ទៅ guild {config.GUILD_ID} (instant)")
        else:
            # Sync global — ត្រូវចំណាយពេលរហូតដល់ 1 ម៉ោងដើម្បីលេចលើ Discord ទាំងអស់
            synced = await bot.tree.sync()
            print(f"⚡ Sync {len(synced)} slash commands global (អាចចំណាយពេលដល់ 1 ម៉ោងដើម្បីលេច)")
    except Exception as e:
        print(f"❌ Error sync slash commands: {e}")


# ─────────────────────────────
# ៣. Error handling សម្រាប់ 24/7 stability
# ─────────────────────────────
@bot.event
async def on_error(event, *args, **kwargs):
    print(f"❌ Error ក្នុង event {event}")
    import traceback
    traceback.print_exc()


# ─────────────────────────────
# ៤. ផ្ទុក Cogs ទាំងអស់
# ─────────────────────────────
async def load_cogs():
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"📦 Cog ផ្ទុករួច: {cog}")
        except Exception as e:
            print(f"❌ មិនអាចផ្ទុក cog {cog}: {e}")


# ─────────────────────────────
# ៥. ចាប់ផ្តើម Bot (ជាមួយ auto-reconnect)
# ─────────────────────────────
async def start_bot():
    async with bot:
        await load_cogs()
        await bot.start(config.TOKEN)


def main():
    if not config.TOKEN:
        print("❌ រកមិនឃើញ DISCORD_TOKEN ក្នុងឯកសារ .env! សូមចម្លង .env.example ទៅ .env ហើយបំពេញ token។")
        return

    keep_alive()  # ចាប់ផ្តើម Flask keep-alive server មុន bot login

    while True:
        try:
            asyncio.run(start_bot())
        except discord.errors.LoginFailure:
            print("❌ Token មិនត្រឹមត្រូវ! សូមពិនិត្យ DISCORD_TOKEN ក្នុង .env")
            break
        except KeyboardInterrupt:
            print("👋 Bot បានបិទដោយដៃ")
            break
        except Exception as e:
            print(f"❌ Bot crash: {e}")
            print("🔄 កំពុងព្យាយាមភ្ជាប់ឡើងវិញក្នុង 10 វិនាទី...")
            import time
            time.sleep(10)


if __name__ == "__main__":
    main()
