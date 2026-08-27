# 🎉 Fun Commands — coinflip, dice, 8ball, rps, poll, say, embed
import discord
from discord import app_commands
from discord.ext import commands
import config
import random


EIGHTBALL_RESPONSES = [
    "ចាស មិនខាន! ✅", "ប្រហែលជាចាស 🤔", "មិនច្បាស់ទេ ព្យាយាមសួរម្តងទៀត 🔄",
    "ទេ មិនគួរទេ ❌", "សំណាងល្អណាស់! 🍀", "កុំសង្ឃឹមច្រើនពេក 😅",
    "ដាច់ខាតជាចាស! 💯", "ខ្ញុំមិនអាចប្រាប់បានទេឥឡូវនេះ 🌫️",
]

RPS_CHOICES = {"stone": "🪨 Stone", "paper": "📄 Paper", "scissors": "✂️ Scissors"}


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ═══════════ COINFLIP ═══════════
    @app_commands.command(name="coinflip", description="បោះកាក់ (Head ឬ Tail)")
    async def coinflip(self, interaction: discord.Interaction):
        result = random.choice(["🪙 Head", "🪙 Tail"])
        await interaction.response.send_message(embed=discord.Embed(description=f"លទ្ធផល: **{result}**", color=config.COLOR_INFO))

    # ═══════════ DICE ═══════════
    @app_commands.command(name="dice", description="បោះឡុកឡាក់ (1-6)")
    async def dice(self, interaction: discord.Interaction):
        result = random.randint(1, 6)
        await interaction.response.send_message(embed=discord.Embed(description=f"🎲 អ្នកបានលេខ: **{result}**", color=config.COLOR_INFO))

    # ═══════════ 8BALL ═══════════
    @app_commands.command(name="8ball", description="សួរសំណួរទៅ Magic 8-Ball")
    @app_commands.describe(question="សំណួររបស់អ្នក")
    async def eightball(self, interaction: discord.Interaction, question: str):
        answer = random.choice(EIGHTBALL_RESPONSES)
        embed = discord.Embed(color=config.COLOR_WELCOME)
        embed.add_field(name="❓ សំណួរ", value=question, inline=False)
        embed.add_field(name="🎱 ចម្លើយ", value=answer, inline=False)
        await interaction.response.send_message(embed=embed)

    # ═══════════ ROCK PAPER SCISSORS ═══════════
    @app_commands.command(name="rps", description="លេង ជល់ដំបង-ក្រដាស-កន្ត្រៃជាមួយ bot")
    @app_commands.describe(choice="ជម្រើសរបស់អ្នក")
    @app_commands.choices(choice=[
        app_commands.Choice(name="🪨 Stone", value="stone"),
        app_commands.Choice(name="📄 Paper", value="paper"),
        app_commands.Choice(name="✂️ Scissors", value="scissors"),
    ])
    async def rps(self, interaction: discord.Interaction, choice: app_commands.Choice[str]):
        user_choice = choice.value
        bot_choice = random.choice(list(RPS_CHOICES.keys()))

        if user_choice == bot_choice:
            result = "🤝 ស្មើគ្នា!"
        elif (
            (user_choice == "stone" and bot_choice == "scissors")
            or (user_choice == "paper" and bot_choice == "stone")
            or (user_choice == "scissors" and bot_choice == "paper")
        ):
            result = "🎉 អ្នកឈ្នះ!"
        else:
            result = "😢 Bot ឈ្នះ!"

        embed = discord.Embed(color=config.COLOR_WELCOME)
        embed.add_field(name="អ្នក", value=RPS_CHOICES[user_choice], inline=True)
        embed.add_field(name="Bot", value=RPS_CHOICES[bot_choice], inline=True)
        embed.add_field(name="លទ្ធផល", value=result, inline=False)
        await interaction.response.send_message(embed=embed)

    # ═══════════ POLL ═══════════
    @app_commands.command(name="poll", description="បង្កើត poll ដោយ reaction 👍👎")
    @app_commands.describe(question="សំណួរ poll")
    async def poll(self, interaction: discord.Interaction, question: str):
        embed = discord.Embed(title="📊 Poll", description=question, color=config.COLOR_INFO)
        embed.set_footer(text=f"បង្កើតដោយ {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)
        msg = await interaction.original_response()
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

    # ═══════════ SAY (admin) ═══════════
    @app_commands.command(name="say", description="ឱ្យ bot និយាយអត្ថបទ (Admin)")
    @app_commands.describe(message="អត្ថបទដែលចង់ឱ្យ bot ផ្ញើ")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message("✅ បានផ្ញើ!", ephemeral=True)
        await interaction.channel.send(message)

    # ═══════════ EMBED BUILDER (admin) ═══════════
    @app_commands.command(name="embed", description="បង្កើត embed message ផ្ទាល់ខ្លួន (Admin)")
    @app_commands.describe(title="ចំណងជើង", description="អត្ថបទ", color="ពណ៌ hex (ឧ. #8B00FF)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def embed_cmd(self, interaction: discord.Interaction, title: str, description: str, color: str = "#8B00FF"):
        try:
            color_int = int(color.replace("#", ""), 16)
        except ValueError:
            color_int = config.COLOR_INFO
        embed = discord.Embed(title=title, description=description, color=color_int)
        embed.set_footer(text=config.SERVER_NAME)
        await interaction.response.send_message("✅ បានបង្កើត embed!", ephemeral=True)
        await interaction.channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))
