# Imports
import time

import discord
import datetime
import asyncio
from discord.utils import get


from config import *
from discord.ext import commands
from discord import ui, app_commands

# Variables


from cogs.Rcon import command


# Bot

class PersistentViewBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all())
        self.role_message_channel_id = 1087445706140307466
        self.role_message_id = 1096896191557537873  # ID of the message that can be reacted to to add/remove a role.
        self.emoji_to_role = {
            discord.PartialEmoji(name='📰'): 1096896599969501254,  # ID of the role associated with unicode emoji '🔴'.
            discord.PartialEmoji(name='📣'): 1096896639903481918,  # ID of the role associated with unicode emoji '🟡'.
            discord.PartialEmoji(name='💡'): 1096894406612766861,  # ID of the role associated with a partial emoji's ID.
        }

    async def setup_hook(self):
        await self.load_extension('cogs.Rcon')
        await self.load_extension('cogs.EasyDonate')
        await self.load_extension('cogs.ticket')


        await bot.tree.sync(guild=discord.Object(id=1087033528568524902))

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("У вас нет прав на выполнение данной команды.")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("Команда не найдена!")


    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally, add the role.
            await payload.member.add_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        member = guild.get_member(payload.user_id)
        if member is None:
            # Make sure the member still exists and is valid.
            return

        try:
            # Finally, remove the role.
            await member.remove_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    async def on_ready(self):
        messg = await self.get_channel(self.role_message_channel_id).fetch_message(self.role_message_id)
        for emoji in self.emoji_to_role:
            await messg.add_reaction(emoji)
        self.remove_command('help')
        print(f'Бот успешно запущен как {self.user}')
        print('>------<')
        guild = self.get_guild(1087033528568524902)
        while True:
            await bot.change_presence(status=discord.Status.idle, activity=discord.Game('маенкрафт'))
            await asyncio.sleep(5)
            await bot.change_presence(status=discord.Status.idle,
                                      activity=discord.Game('очке зонтика паьлчиком'))
            await asyncio.sleep(5)
            await bot.change_presence(status = discord.Status.idle, activity = discord.Activity(name = 'за развитием сервера', type = discord.ActivityType.watching))
            await asyncio.sleep(5)


bot = PersistentViewBot()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("У вас нет прав на выполнение данной команды.")
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Команда не найдена!")
    if isinstance(error, app_commands.MissingPermissions):
        await ctx.send("Команда не найдена!")
    if isinstance(error, app_commands.BotMissingPermissions):
        await ctx.send("Команда не найдена!")


@bot.event
async def on_message(message):
    if message.channel.id == 1087748993125191700:
        if not message.content.startswith("<@&1096896639903481918>"):
            await message.add_reaction('💣')
            await message.author.send(
                embed=discord.Embed(description=f"""Привет! Пингуй пожалуйста @Объявления""", color=0xe74c3c))
            time.sleep(5)
            await message.delete()
        elif message.content.startswith("<@&1096896639903481918>"):
            await message.add_reaction('<:social_down:1096900793761800222>')
            await message.add_reaction('<:social_up:1096900790863536240>')
            await message.add_reaction('<:like:1096900782281998407>')
        else:
            return
    elif message.channel.id == 1087753241703485460:
        if not message.content.startswith("<@&1096894406612766861>"):
            await message.add_reaction('💣')
            await message.author.send(
                embed=discord.Embed(description=f"""Привет! Пингуй пожалуйста @Идея""", color=0xe74c3c))
            time.sleep(5)
            await message.delete()
        elif message.content.startswith("<@&1096894406612766861>"):
            await message.add_reaction('<:social_down:1096900793761800222>')
            await message.add_reaction('<:social_up:1096900790863536240>')
            await message.add_reaction('<:like:1096900782281998407>')
        else:
            return
    elif message.channel.id == 1087033529805832205:
        if not message.content.startswith("<@&1096896599969501254>"):
            await message.add_reaction('💣')
            await message.author.send(
                embed=discord.Embed(description=f"""Привет! Пингуй пожалуйста @Новости""", color=0xe74c3c))
            time.sleep(5)
            await message.delete()
        elif message.content.startswith("<@&1096896599969501254>"):
            await message.add_reaction('<:no:1096900789781397645>')
            await message.add_reaction('<:yes:1096900784903426191>')
            await message.add_reaction('<:like:1096900782281998407>')
    else:
        return


@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel != None:
        if after.channel.id == 968866389735653406:
            guild = bot.get_guild(924384808187093032)
            category = get(guild.categories, id=1036363272137494608)

            channel2 = await member.guild.create_voice_channel(
                name=f'Канал-{member.display_name}',
                category=category
            )

            await channel2.set_permissions(member, connect=True, manage_channels=True)
            await member.move_to(channel2)

            def check(x, y, z):
                return len(channel2.members) == 0

            await bot.wait_for('voice_state_update', check=check)
            await channel2.delete()


@commands.has_any_role(968905407697387520)
@bot.hybrid_command(name='embed', description="Выводит embed сообщение", with_app_command=True)
@app_commands.guilds(discord.Object(id=1087033528568524902))
async def embed(ctx, description:str, title:str = None):
    description = description.replace(r"\n", "\n")
    if title is None:
        embed = discord.Embed(description=description,color=0x2f3136)
        embed.set_footer(text="© MineSpace 2023")
        await ctx.channel.send(embed=embed)

    else:
        embed = discord.Embed(title=title,description=description,color=0x2f3136)
        embed.set_footer(text="© MineSpace 2023")
        await ctx.channel.send(embed=embed)
    await bot.close()

bot.run(settings['token'])


