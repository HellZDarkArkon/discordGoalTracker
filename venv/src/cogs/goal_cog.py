import aiohttp
import discord
import src.PayPal
from discord import app_commands
from discord.ext import commands
from src.db import goals

#goal_cog.py

class GoalCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Goal Cog loaded.')

    @commands.command()
    async def sync(self, ctx) -> None:
        fmt=await ctx.bot.tree.sync(guild=ctx.guild)

        await ctx.send(f'Synced {len(fmt)} commands')

    @app_commands.command(name='connectpp', description="Connect PayPal")
    async def connectpp(self, interaction: discord.Interaction, email: str):
        try:
           paypal_client = src.PayPal.PayPalClient()
           access_token = await self.get_paypal_access_token(paypal_client)
           is_authorized = paypal_client.authorize_paypal_account(access_token, email)

           if is_authorized:
               await interaction.response.send_message(f"PayPal account ({email}) authorized successfully.")
           else:
               await interaction.response.send_message(f"PayPal account authorization failed.", ephemeral=True)
        except Exception as e:
            error = f'An error occured: {str(e)}'
            await interaction.response.send_message(error, ephemeral=True)

    @app_commands.command(name='addgoal', description='Add a Goal')
    async def addgoal(self, interaction: discord.Interaction, name: str, price: float, time_limit: int = None):
        """Add a goal to the data dict"""
        try:
            if name in goals.data["goals"]:
                await interaction.response.send_message("Goal already exists.", ephemeral=True)
                return

            #create new dict
            goal_data = {
                "id": name,
                "price": round(price, 2), #Round to 2 decimal places as USD has a precision of 0.01
                "time_limit": time_limit, #Time limit in seconds
            }

            #Add goal to data dict
            goals.data["goals"][name] = goal_data
            if time_limit != None:
                await interaction.response.send_message(f'Goal "{name}" added successfully with a price of ${price} and a time limit of {time_limit} seconds.')
            await interaction.response.send_message(f'Goal "{name}" added successfully with a price of ${price}.', ephemeral=True)
        except Exception as e:
            #Handle exceptions here
            error = f'An error occured: {str(e)}'
            await interaction.response.send_message(error, ephemeral=True)

    @app_commands.command(name='remgoal', description='Remove a Goal')
    async def remgoal(self, interaction: discord.Interaction, name: str):
        try:
            if name not in goals.data["goals"]:
                await interaction.response.send_message("Goal does not exist.", ephemeral=True)
                return

            # Remove goal from dict
            del goals.data["goals"][name]
            await interaction.response.send_message(f'Goal "{name}" removed.', ephemeral=True)
        except Exception as e:
            error = f'An error occurred: {str(e)}'
            await interaction.response.send_message(error, ephemeral=True)

    @app_commands.command(name='getgoal', description='Get the difference for the goal')
    async def getgoal(self, interaction: discord.Interaction, name: str):
        try:
            """Calculate diff between goal price and PayPal balance"""
            if name not in goals.data["goals"]:
                await interaction.response.send_message("Goal does not exist.", ephemeral=True)
                return

            # Init PayPal client
            paypal_client = src.PayPal.PayPalClient()
            access_token = await self.get_paypal_access_token(paypal_client)

            balance_data = paypal_client.get_paypal_balance(access_token)
            if balance_data:
                balance_amount = balance_data["balance"]["total"]["value"]
                pass

            # implement logic to calculate difference
            pp_balance =

            # Create and send an embed with the difference.
            embed = discord.Embed(title=f'Goal Difference for {name}', color=0x00ff00)
            embed.add_field(name="Price", value=f"${goals.data['goals'][name]['price']}", inline=False)
            embed.add_field(name="Paypal Balance", value=f"$0", inline=False)
            embed.add_field(name="Difference", value=f'${difference} remaining', inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            error = f'An error occurred: {str(e)}'
            await interaction.response.send_message(error, ephemeral=True)

    async def get_paypal_access_token(self, paypal_client: src.PayPal.PayPalClient):
        client_id = paypal_client.client_id
        client_secret = paypal_client.client_secret

        token_url = "https://api.sandbox.paypal.com/v1/oauth2/token"

        async with aiohttp.ClientSession() as session:
            auth = aiohttp.BasicAuth(client_id, client_secret)
            params = {
                "grant_type": "client_credentials",
            }

            try:
                async with session.post(token_url, auth=auth, data=params) as response:
                    if response.status == 200:
                        data = await.response.json()
                        access_token = data["access_token"]
                        return access_token
                    else:
                        error_message = await response.text()
                        raise Exception(f"Error getting PayPal access token: {error_message}")
            except Exception as e:
                raise Exception(f"Error getting PayPal access token: {str(e)}")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(GoalCog(client), guilds=[discord.Object(id=1147913598652387340)])
    print(f'GoalCog has been successfully loaded."')