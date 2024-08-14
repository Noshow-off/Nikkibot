import httpx
from pyrogram import Client, filters
from DAXXMUSIC import app

import aiohttp
from pyrogram import Client, filters, enums

#

# Function to fetch BIN information
async def bin_lookup(bin_number):
    astroboyapi = f"https://astroboyapi.com/api/bin.php?bin={bin_number}"

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(astroboyapi) as response:
            if response.status == 200:
                try:
                    bin_info = await response.json()
                    brand = bin_info.get("brand", "N/A")
                    card_type = bin_info.get("type", "N/A")
                    level = bin_info.get("level", "N/A")
                    bank = bin_info.get("bank", "N/A")
                    country = bin_info.get("country_name", "N/A")
                    country_flag = bin_info.get("country_flag", "")
                    
                    bin_info_text = f"""
┏━━━━━━━⍟
┃𝙱𝙸𝙽 𝙻𝙾𝙾𝙺𝚄𝙿 𝚁𝙴𝚂𝚄𝙻𝚃𝚂 🍁
┗━━━━━━━━━━━⊛

[ϟ] 𝙱𝙸𝙽 𝙲𝙾𝙳𝙴: <code>{bin_number}</code>
[ϟ] 𝙲𝙲 𝙸𝙽𝙵𝙾: {brand} - {card_type} - {level}
[ϟ] 𝙱𝙰𝙽𝙺: {bank}
[ϟ] 𝙲𝙾𝚄𝙽𝚃𝚁𝚈: {country} {country_flag}
"""
                    return bin_info_text
                except Exception as e:
                    return f"Error: Unable to retrieve BIN information ({str(e)})"
            else:
                return f"Error: Unable to retrieve BIN information (Status code: {response.status})"

# Command to handle BIN lookup
@app.on_message(filters.command("bin", prefixes="."))
async def bin_command(client, message):
    if len(message.text.split()) >= 2:
        bin_number = message.text.split()[1]
        bin_number = bin_number[:6]
    elif message.reply_to_message and message.reply_to_message.text:
        bin_number = message.reply_to_message.text[:6]
    else:
        await message.reply("𝙿𝚁𝙾𝚅𝙸𝙳𝙴 𝙰 𝚅𝙰𝙻𝙸𝙳 𝙱𝙸𝙽", parse_mode=enums.ParseMode.HTML)
        return
    
    bin_info = await bin_lookup(bin_number)
    user_id = message.from_user.id

    await message.reply(f'''
{bin_info}

[ϟ] 𝙱𝙸𝙽 𝙲𝙷𝙴𝙲𝙺𝙴𝙳 𝙱𝚈 ➺ <a href="tg://user?id={user_id}">{message.from_user.first_name}</a>
''', parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
