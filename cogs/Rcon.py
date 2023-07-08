import discord
from discord import app_commands
from discord.ext import commands
from mctools import RCONClient
import json
global HOST,PORT,PASSWORD
HOST = 'localhost'
PORT = 25575
PASSWORD = "12345"


def command(cmd):
        rcon = RCONClient(HOST, port=PORT)
        if rcon.login(PASSWORD):
            resp = rcon.command(cmd)
            rcon.stop()


class Rcon(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("! > Коги с RCON успешно запущены")

    @app_commands.command(name="whitelistadd", description="Добавить в вайт лист")
    async def whitelistadd(self, interaction: discord.Interaction, nick:str) -> None:
        role = interaction.guild.get_role(968905407697387520)
        if role in interaction.user.roles:
            rcon = RCONClient(HOST, port=PORT)
            if rcon.login(PASSWORD):
                resp = rcon.command(f"easywl add {nick}")
                rcon.stop()
            await interaction.channel.send(f'{nick} успешно добавлен в whitelist')
            logs = self.bot.get_channel(1059176654360027257)
            await logs.send(f"{interaction.user} добавил {nick} в whitelist")
        else:
            await interaction.channel.send("У вас нет прав.")

    @app_commands.command(name="whitelistremove", description="Удалить из вайт листа")
    async def whitelistremove(self, interaction: discord.Interaction, nick:str) -> None:
        role = interaction.guild.get_role(968905407697387520)
        if role in interaction.user.roles:
            rcon = RCONClient(HOST, port=PORT)
            if rcon.login(PASSWORD):
                resp = rcon.command(f"easywl remove {nick}")
                rcon.stop()
            await interaction.channel.send(f'{nick} успешно удален из whitelist')
            logs = self.bot.get_channel(1059176654360027257)
            await logs.send(f"{interaction.user} удалил {nick} из whitelist")
        else:
            await interaction.channel.send("У вас нет прав.")

    @app_commands.command(name="cmd", description="Отправить команду")
    async def cmd(self, interaction: discord.Interaction, command:str) -> None:
        role = interaction.guild.get_role(968905407697387520)
        if role in interaction.user.roles:
            try:
                rcon = RCONClient(HOST, port=PORT)
                if rcon.login(PASSWORD):
                    resp = rcon.command(command)
                    rcon.stop()
                logs = self.bot.get_channel(1059176654360027257)
                await logs.send(f"{interaction.user} отправил команду '{command}' на сервер")
                await interaction.channel.send(f'Команда {command} отправлена на сервер. ')
            except:
                await interaction.channel.send('Непредвиденная ошибка.')
        else:
            await interaction.channel.send("У вас нет прав.")

    @app_commands.command(name="say", description="Написать в чат сервера")
    async def say(self, interaction: discord.Interaction, message:str) -> None:
        role = interaction.guild.get_role(968905407697387520)
        if role in interaction.user.roles:
            rcon = RCONClient(HOST, port=PORT)
            if rcon.login(PASSWORD):
                raz = {"text": "!", "color": "gold"}
                raz = json.dumps(raz)
                dva = {"text": f" {interaction.user} ", "color": "gray"}
                dva = json.dumps(dva)
                tri = {"text": "» ", "color": "gray"}
                tri = json.dumps(tri)
                chet = {"text": f"{message}", "color": "white"}
                chet = json.dumps(chet)
                lol = f'tellraw @a ["",{raz},{dva},{tri},{chet}]'
                resp = rcon.command(lol)
                rcon.stop()
            logs = self.bot.get_channel(1059176654360027257)
            await logs.send(f"{interaction.user} отправил фразу '{message}' на сервер")
            await interaction.channel.send(f'Фраза "{message}" отправлена на сервер. ')
        else:
            await interaction.channel.send("У вас нет прав.")

    @app_commands.command(name="restart", description="Рестартнуть сервер")
    async def restart(self, interaction: discord.Interaction) -> None:
        role = interaction.guild.get_role(968905407697387520)
        if role in interaction.user.roles:
            try:
                rcon = RCONClient(HOST, port=PORT)
                if rcon.login(PASSWORD):
                    resp = rcon.command("restart")
                    rcon.stop()
                logs = self.bot.get_channel(1059176654360027257)
                await logs.send(f"{interaction.user} рестартнул сервер")
                await interaction.channel.send(f'Сервер перезагружается. ')
            except:
                await interaction.channel.send('Непредвиденная ошибка.')
        else:
            await interaction.channel.send("У вас нет прав.")
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Rcon(bot),guild=discord.Object(id=924384808187093032))