import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv 
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

profanity = ["bad word", "bad123", "bad","dog"]

def create_user_table():
    connection = sqlite3.connect(f'{BASE_DIR}\\users_warnings.db')
    cursor = connection.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS "users_per_guild" (
            "user_id" INTEGER, 
            "warnings_count" INTEGER,
            "guide_id" INTEGER,
            PRIMARY KEY("user_id", "guide_id")
        )
    """)

    connection.commit()
    connection.close()
    
create_user_table()

def increase_and_get_warnings(user_id: int, guide_id: int):
    connection = sqlite3.connect(f"{BASE_DIR}\\users_warnings.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT warnings_count
        FROM users_per_guild
        WHERE user_id = ? AND guide_id = ?
    """, (user_id, guide_id))

    result = cursor.fetchone()

    if result is None:
        cursor.execute("""
            INSERT INTO users_per_guild (user_id, warnings_count, guide_id)
            VALUES (?, 1, ?)
        """, (user_id, guide_id))

        connection.commit()
        connection.close()

        return 1
    
    cursor.execute(""" 
        UPDATE users_per_guild
        SET warnings_count = ?
        WHERE user_id = ? AND guide_id = ?
    """, (result[0] + 1, user_id, guide_id))

    connection.commit()
    connection.close()

    return result[0] + 1

def get_warnings(user_id: int, guide_id: int):
    connection = sqlite3.connect(f"{BASE_DIR}\\users_warnings.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT warnings_count 
        FROM users_per_guild 
        WHERE user_id = ? AND guide_id = ?
    """, (user_id, guide_id))
    
    result = cursor.fetchone()
    connection.close()
    
    return result[0] if result else 0

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')  

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(msg):
    if msg.author.id != bot.user.id:
        await msg.channel.send(f'Assalamualaikum: {msg.author.name}!')
        
        for term in profanity:
            if term.lower() in msg.content.lower():
                num_warnings = increase_and_get_warnings(msg.author.id, msg.guild.id)

                if num_warnings >= 3:
                    await msg.author.ban(reason="Exceeded maximum number of warnings")
                    await msg.channel.send(f"{msg.author.mention} has been banned for repeating profanity")
                else:
                    await msg.channel.send(f"{msg.author.mention} has been warned for repeating profanity. Warnings remaining: {3 - num_warnings}")
                    await msg.delete()
                break
    
    await bot.process_commands(msg)

@bot.tree.command(name="greet", description="sends a greeting message to user")
async def greet(interaction: discord.Interaction):
    username = interaction.user.mention
    await interaction.response.send_message(f'Hello there {username}!')

bot.run(TOKEN)