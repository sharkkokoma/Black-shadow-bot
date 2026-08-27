# ⚙️ កំណត់ការតម្លើងទាំងអស់នៅទីនេះ - កែសម្រួលបានតាមចង់
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
CLIENT_ID = os.getenv("CLIENT_ID")

WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL_ID")
LEAVE_CHANNEL_ID = os.getenv("LEAVE_CHANNEL_ID")
MEMBER_COUNT_CHANNEL_ID = os.getenv("MEMBER_COUNT_CHANNEL_ID")
MOD_LOG_CHANNEL_ID = os.getenv("MOD_LOG_CHANNEL_ID")

AUTO_ROLE_ID = os.getenv("AUTO_ROLE_ID")
MUTE_ROLE_ID = os.getenv("MUTE_ROLE_ID")

SERVER_NAME = os.getenv("SERVER_NAME", "BLACK SHADOW")
SERVER_ICON_URL = os.getenv("SERVER_ICON_URL", "")

PORT = int(os.getenv("PORT", 3000))

# 🎨 ពណ៌ Embed (hex, ជា int សម្រាប់ discord.py)
COLOR_WELCOME = 0x8B00FF   # ស្វាយចាស់ (Shadow purple)
COLOR_LEAVE = 0xFF0000     # ក្រហម
COLOR_INFO = 0x2F3136      # ខ្មៅស្រអាប់
COLOR_SUCCESS = 0x4ADE80
COLOR_ERROR = 0xF45B69
COLOR_WARNING = 0xF59E0B

# 🌐 Web3.0 Rules theme colors (neon/cyber gradient feel)
COLOR_WEB3_PRIMARY = 0x9945FF     # neon purple
COLOR_WEB3_ACCENT = 0x14F1D9      # neon cyan

# 🖼️ Welcome card background — ដាក់ URL រូបភាព background ផ្ទាល់ខ្លួន (ទំហំល្អបំផុត 1024x500)
WELCOME_BACKGROUND = "https://i.imgur.com/8Km9tLL.jpg"

# 💬 អត្ថបទសារ — ប្រើ {user} {username} {server} {member_count}
WELCOME_TITLE = "🖤 ស្វាគមន៍មកកាន់ {server} ⚔️"
WELCOME_DESC = (
    "សួស្តី {user}! សូមស្វាគមន៍ចូលរួម **{server}**!\n\n"
    "📌 សូមអានច្បាប់នៅ 📜｜rules\n"
    "🎭 ជ្រើសរើស role នៅ 🎭｜roles-select\n"
    "💬 ចាប់ផ្តើមជជែកនៅ 💬｜general-chat\n\n"
    "អ្នកគឺជាសមាជិកទី **#{member_count}** របស់យើង! 🎉"
)
WELCOME_DM = (
    "សួស្តី {username}! 👋\n\n"
    "សូមស្វាគមន៍មកកាន់ **{server}**! ⚔️🖤\n\n"
    "យើងរីករាយណាស់ដែលមានអ្នកចូលរួម។ សូមអានច្បាប់ និងចូលរួមសកម្មភាពជាមួយពួកយើង!\n\n"
    "រីករាយក្នុងការលេង! 🎮"
)
LEAVE_TITLE = "💔 {username} បានចាកចេញ"
LEAVE_DESC = "**{username}** បានចាកចេញពី **{server}**\n\nពួកយើងនៅសល់ **{member_count}** សមាជិក 😢"
MEMBER_COUNT_FORMAT = "👥 សមាជិក: {member_count}"
