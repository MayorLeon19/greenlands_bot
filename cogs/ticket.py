import datetime

import discord
from discord import app_commands, ui
from discord.ext import commands
from discord.utils import get
from mee6_py_api import API
from cogs.Rcon import command

mee6API = API(1087033528568524902)
id_channel_ticket_logs = 1096892647697821858
id_staff_role = 1087037553913364601
global embed_color
embed_color = 0x2f3136
class Questionnaire(ui.Modal, title='Получение проходки'):
    name = ui.TextInput(label='Ваш никнейм')

    def __init__(self) -> None:
        super().__init__()



    async def on_submit(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(1087040322455994438)  # получаем объект роли*
        await interaction.user.add_roles(role)  # выдаем автору роль
        command(f"easywl add {self.name}")
        channel = get(interaction.guild.channels, id=1096892647697821858)
        embed = discord.Embed(title=f"{self.name} успешно получил проходку на сервер!",
                              timestamp=datetime.datetime.utcnow(),
                              description="Если ты тоже хочешь получить проходку бесплатно, то достигни 15 уровня в нашем боте!",
                              color=0x49aa3c)
        embed.set_footer(text="© MineSpace 2023")
        await channel.send(embed=embed)
        await interaction.response.send_message('Вам успешно выдана проходка!', ephemeral=True)



### TICKET SYSTEM ###

class Select(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Суд", value="Суд", description='Если Вам нужно обратиться в суд.', emoji='💲'),
            discord.SelectOption(label="Жалоба", value="Жалоба", description='Если вы хотите подать жалобу.',
                                 emoji='▶'),
        ]
        super().__init__(placeholder="Выберите действие", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        category = get(guild.categories, name="тикеты")
        rol_staff = guild.get_role(id_staff_role)
        if self.values[0] == "Суд":
            channel = await guild.create_text_channel(name=f'📞・суд-{interaction.user.name}', category=category)

            await channel.set_permissions(interaction.guild.get_role(interaction.guild.id), send_messages=False,
                                          read_messages=False)
            await channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=True,
                                          embed_links=True, attach_files=True, read_message_history=True,
                                          external_emojis=True)
            await channel.set_permissions(rol_staff, send_messages=True, read_messages=True, add_reactions=True,
                                          embed_links=True, attach_files=True, read_message_history=True,
                                          external_emojis=True, manage_messages=True)

            embed_question = discord.Embed(title=f'Суд - Привет, {interaction.user.name}!',
                                           description='В этом тикете ты можешь обратиться в суд.\n\nЕсли Вы нуждаетесь в срочной помощи - нажмите кнопку `🔔 Вызвать модерацию`.',
                                           color=embed_color)
            embed_question.set_thumbnail(url=interaction.user.avatar)

            await channel.send(interaction.user.mention, embed=embed_question, view=Call_Staff())
        elif self.values[0] == "Жалоба":
            channel = await guild.create_text_channel(name=f'📝・жалоба-{interaction.user.name}', category=category)

            await channel.set_permissions(interaction.guild.get_role(interaction.guild.id), send_messages=False,
                                          read_messages=False)
            await channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=True,
                                          embed_links=True, attach_files=True, read_message_history=True,
                                          external_emojis=True)
            await channel.set_permissions(rol_staff, send_messages=True, read_messages=True, add_reactions=True,
                                          embed_links=True, attach_files=True, read_message_history=True,
                                          external_emojis=True, manage_messages=True)

            embed_question = discord.Embed(title=f'Жалоба - Привет, {interaction.user.name}!',
                                           description='В этом тикете ты можешь подать жалобу.\n\nЕсли Вы нуждаетесь в срочной помощи - нажмите на кнопку `🔔 Вызвать модерацию`.',
                                           color=embed_color)
            embed_question.set_thumbnail(url=interaction.user.avatar)

            await channel.send(interaction.user.mention, embed=embed_question, view=Call_Staff())


class SelectView(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(Select())




class TicketStart(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Создать тикет', style=discord.ButtonStyle.green, emoji='🎲',
                       custom_id='persistent_view:ticket')
    async def ticketstart(self, interaction: discord.Interaction, button: discord.ui.Button):
        canal = interaction.channel

        canal_logs = interaction.guild.get_channel(id_channel_ticket_logs)
        await interaction.response.send_message(view=SelectView(), ephemeral=True)


class Call_Staff(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Вызвать модерацию', style=discord.ButtonStyle.blurple, emoji='🔔',
                       custom_id='persistent_view:call_staff')
    async def callstaff(self, interaction: discord.Interaction, button: discord.ui.Button):
        canal = interaction.channel
        canal_logs = interaction.guild.get_channel(id_channel_ticket_logs)
        embed_llamar_staff = discord.Embed(description=f"🔔 {interaction.user.mention} вызвал модерацию.",
                                           color=embed_color)
        await canal.send(f'<@&{id_staff_role}>', embed=embed_llamar_staff, delete_after=20)

    @discord.ui.button(label='Закрыть тикет', style=discord.ButtonStyle.blurple, emoji='🔐',
                       custom_id='persistent_view:close_ticket')
    async def closeticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        canal_logs = interaction.guild.get_channel(id_channel_ticket_logs)
        embed_cerrar_ticket = discord.Embed(description=f"⚠️ Вы действительно хотите закрыть тикет?", color=embed_color)
        await interaction.response.send_message(interaction.user.mention, embed=embed_cerrar_ticket, view=Close_Podt())


class Close_Podt(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Да', style=discord.ButtonStyle.green, emoji='✅', custom_id='persistent_view:close_yes')
    async def closeyes(self, interaction: discord.Interaction, button: discord.ui.Button):
        canal = interaction.channel
        canal_logs = interaction.guild.get_channel(id_channel_ticket_logs)
        await canal.delete()
        embed_logs = discord.Embed(title="Тикеты", description=f"", timestamp=datetime.datetime.utcnow(),
                                   color=embed_color)
        embed_logs.add_field(name="Тикет", value=f"{canal.name}", inline=True)
        embed_logs.add_field(name="Закрыт (кем) - ", value=f"{interaction.user.mention}", inline=False)
        embed_logs.set_thumbnail(url=interaction.user.avatar)
        await canal_logs.send(embed=embed_logs)

    @discord.ui.button(label='Нет', style=discord.ButtonStyle.red, emoji='❌', custom_id='persistent_view:close_no')
    async def closeno(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()


# Payment
class Complete_Pay(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Я оплатил', style=discord.ButtonStyle.green, emoji='✅',
                       custom_id='persistent_view:complete')
    async def completepay(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(1087033528568524905)
        await interaction.channel.send(f"{role.mention}, проверьте деньги от {interaction.user.mention}")


class Choose_Method_Pay(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        url = f"https://MineSpace.fun/"
        self.add_item(discord.ui.Button(label="EasyDonate", url=url, emoji="📡"))

    @discord.ui.button(label='Получить проходку', style=discord.ButtonStyle.green, emoji='💳',
                       custom_id='persistent_view:getlvl')
    async def getlvl(self, interaction: discord.Interaction, button: discord.ui.Button):

        role = interaction.guild.get_role(1087040322455994438)  # получаем объект роли*

        level = await mee6API.levels.get_user_level(interaction.user.id)
        if level >= 15:
            if role in interaction.user.roles:
                await interaction.response.send_message("Ошибка! У вас уже есть проходка!", ephemeral=True)
            else:
                await interaction.response.send_modal(Questionnaire())
        else:
            await interaction.response.send_message("Ошибка! У вас нет 15 уровня!", ephemeral=True)

    @discord.ui.button(label='Оплата на карту(напрямую)', style=discord.ButtonStyle.green, emoji='💳',
                       custom_id='persistent_view:qiwi')
    async def other(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        category = get(guild.categories, name="тикеты")
        rol_staff = guild.get_role(id_staff_role)
        channel = await guild.create_text_channel(name=f'❔・маркет-{interaction.user.name}', category=category)

        await channel.set_permissions(interaction.guild.get_role(interaction.guild.id), send_messages=False,
                                      read_messages=False)
        await channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=True,
                                      embed_links=True, attach_files=True, read_message_history=True,
                                      external_emojis=True)
        await channel.set_permissions(rol_staff, send_messages=True, read_messages=True, add_reactions=True,
                                      embed_links=True, attach_files=True, read_message_history=True,
                                      external_emojis=True, manage_messages=True)

        embed_question = discord.Embed(title=f'Маркет - Привет, {interaction.user.name}!',
                                       description='В этом тикете ты можешь купить проходку.\n\nЕсли Вы нуждаетесь в срочной помощи - нажмите на кнопку `🔔 Вызвать модерацию`.',
                                       color=embed_color)
        embed_question.set_thumbnail(url=interaction.user.avatar)

        await channel.send(interaction.user.mention, embed=embed_question, view=Call_Staff())
        embed_question = discord.Embed(
            description=f"Сейчас вы должны перевести на карту 0001-0002-1234-5678 платеж в размере 79₽ с примечанием `user:'{interaction.user}' id:'{interaction.user.id}' ch:'{interaction.channel}'`\n"
                        f"После успешной оплаты, администраторы рассмотрят платеж и выдадут вам проходку.",
            color=embed_color)
        embed_question.set_thumbnail(url=interaction.user.avatar)
        await channel.send(interaction.user.mention, embed=embed_question, view=Complete_Pay())


class Shop_Product(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Купить проходку', style=discord.ButtonStyle.blurple, emoji='🎟',
                       custom_id='persistent_view:prohodkaа')
    async def payprohodkaa(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Выберите способ оплаты", view=Choose_Method_Pay(), ephemeral=True)


class ticket(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        bot.add_view(TicketStart())
        bot.add_view(Call_Staff())
        bot.add_view(Close_Podt())
        bot.add_view(Shop_Product())
        bot.add_view(Choose_Method_Pay())
        bot.add_view(Complete_Pay())

    @commands.Cog.listener()
    async def on_ready(self):
        print("! > Коги с тикетом успешно запущены")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("У вас нет прав на выполнение данной команды.")
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("Команда не найдена!")
        if isinstance(error, app_commands.MissingPermissions):
            await ctx.send("Команда не найдена!")
        if isinstance(error, app_commands.BotMissingPermissions):
            await ctx.send("Команда не найдена!")

    @app_commands.command(name="setup_oplata", description="Установить магазин")
    @app_commands.checks.has_any_role(968905407697387520)
    async def __oplata(self, interaction):
        await interaction.channel.send(
            embed = discord.Embed(title ='Магазин', description = 'Добро пожаловать в наш магазин. Тут вы можете купить проходку или еще что-то в нашем магазине. Выберите товар который вы хотите купить', colour = discord.Color.gold()), view=Shop_Product())

    # Setup ticket command
    @app_commands.command(name="setup_ticket", description="Установить тикет")
    @app_commands.checks.has_any_role(968905407697387520)
    async def __ticket(self,interaction):
        await interaction.channel.send(
            embed=discord.Embed(title='Тикеты',
                                description='Добро пожаловать в систему тикетов.\nЗдесь Вам помогут практически с любым вопросом/проблемой/подачей дела на суд.\n\nЧтобы создать тикет - нажмите на кнопку `Создать тикет` ниже.',
                                colour=discord.Color.gold()), view=TicketStart())

    @app_commands.checks.has_any_role(968905407697387520)
    @app_commands.command(name="rank", description="Ваш ранг")
    async def rank(self, interaction):
        xp = await mee6API.levels.get_user_xp(interaction.user.id)
        level = await mee6API.levels.get_user_level(interaction.user.id)
        embed = discord.Embed(title=f"Ранг {interaction.user}", color=0x49aa3c)
        embed.add_field(name="Ваш уровень: ", value=f"{level}", inline=True)
        embed.add_field(name="Ваш exp: ", value=f"{xp}", inline=True)
        embed.set_footer(text="© MineSpace 2023")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ticket(bot),guild=discord.Object(id=1087033528568524902))