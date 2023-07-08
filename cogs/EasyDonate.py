import datetime

from aiohttp import web
from discord.ext import commands, tasks
import discord
import os
import aiohttp

app = web.Application()
routes = web.RouteTableDef()


class Webserver(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.web_server.start()

        @routes.get('/')
        async def welcome(request):
            json_string = await request.json()
            channel = self.bot.get_channel(1059580780952682556)
            embed = discord.Embed(title=f"**{json_string['customer']}** успешно купил проходку за {json_string['cost']}Р на сервер!",
                                  timestamp=datetime.datetime.utcnow(),
                                  description="Купить проходку можно на нашем [сайте](https://MineSpace.fun/)",
                                  color=0x49aa3c)
            embed.set_footer(text="© MineSpace 2023")
            await channel.send(embed=embed)

            return web.json_response({'ok': True})

        app.add_routes(routes)
        app.router.add_post('/', welcome)


    @commands.Cog.listener()
    async def on_ready(self):
        print("! > Коги с easydonate успешно запущены")



    @tasks.loop()
    async def web_server(self):
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host='127.0.0.1', port=5000)
        await site.start()


    @web_server.before_loop
    async def web_server_before_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Webserver(bot))
