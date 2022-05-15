import json
import requests
import discord
import os
import random
import pandas as pd
import datetime
from registered_nations import registered_dict
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get
from functions.get_tax_records_v2 import get_tax_records
from functions.tax_history import tax_history
from functions.tax_history import alliance_tax_history

with open("config.json") as config:
    data = json.load(config)
    token = data["important"]["token"]
    api_key = data["important"]["api_key"]
    alliance_id = data["important"]["alliance_id"]
    v1_base_url = data["important"]["v1_base_url"]


bot = commands.Bot(command_prefix='*')

@bot.event
async def on_ready():
    activity = discord.Game(name="Quit looking at me", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print('We have logged in as {0.user}'.format(bot))
    #get_trade_prices.start()
    #refresh_cities.start()
    #refresh_nations.start()
    #refresh_tax_records.start()



#cities API v1
@tasks.loop(hours=1.0)
async def refresh_cities():
    with open("database/cities.json", "w") as city_file:
        print("Refreshing Cities Data")
        all_cities = requests.get(f"{v1_base_url}all-cities/key={api_key}")
        json_data = all_cities.json()
        data = json_data["all_cities"]
        json.dump(data, city_file)
        city_file.close
    print("City Data Refreshed")

#nations API v1
@tasks.loop(hours=1.0)
async def refresh_nations():
    with open("database/nations.json", "w") as nations_file:
        print("Refreshing Nations Data")
        all_nations = requests.get(f"{v1_base_url}nations/?key={api_key}")
        json_data = all_nations.json()
        data = json_data["nations"]
        json.dump(data, nations_file)
        nations_file.close
    print("Nations Data Refreshed")


@tasks.loop(hours=1.0)
async def get_trade_prices():
    print("Grabbing Trade Prices")
    current_time = datetime.datetime.now()
    print(current_time)
    query = f"{{tradeprices(first: 1){{data {{coal,oil,uranium,iron,bauxite,lead,gasoline,munitions,steel,aluminum,food}}}}}}"
    r = requests.post(f"https://api.politicsandwar.com/graphql?api_key={api_key}", json={"query": query})
    data = r.json()["data"]["tradeprices"]["data"][0]
    with open("database/trade_price_history.json", "w") as trade_price_history_file:
        json.dump(data, trade_price_history_file)
        print("Task Finished")


@tasks.loop(hours=2.0)
async def refresh_tax_records():
    print("Getting Tax Records")
    get_tax_records()
    print("Tax Records Recieved")


@bot.command(name="tax_history")
async def get_tax_history(ctx, nation_id):
    await tax_history(ctx, nation_id)


@bot.command(name="alliance_tax_history")
async def get_alliance_tax_history(ctx, alliance_id):
    await alliance_tax_history(ctx, alliance_id)


#who command for alliances and nations
#arg1 should be either "alliance" or "nation"
@bot.command(name="who")
async def who(ctx, arg1, arg2):
    if arg1 == "nation":
        print("Fetching nation data from file")
        with open("database/nations.json", "r") as nations_file:
            print("Opening file")
            nations_list = json.load(nations_file)
            for iteration, nation_info in enumerate(nations_list):
                print("Looking for info")
                times_run = iteration
                nation_id = nations_list[times_run]["nationid"]
                print(iteration)
                if int(nation_id) == int(arg2):
                    print("Found nation data")
                    name = nations_list[times_run]["nation"]
                    leader_name = nations_list[times_run]["leader"]
                    city_count = nations_list[times_run]["cities"]
                    alliance = nations_list[times_run]["alliance"]
                    score = nations_list[times_run]["score"]
                    total_infrastructure = nations_list[times_run]["infrastructure"]
                    average_infrastructure = int(total_infrastructure) // int(city_count)
                    offensive_wars = nations_list[times_run]["offensivewars"]
                    defensive_wars = nations_list[times_run]["defensivewars"]
                    embed = discord.Embed(title="Retrieved Data",
                                        description="", color=0xFF5733)
                    embed = discord.Embed(title="Nation Id", url=f"http://politicsandwar.com/nation/id={nation_id}",
                                        description="", color=0xFF5733)
                    embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar_url)
                    embed.add_field(name="Nation ID", value=nation_id, inline=True)
                    embed.add_field(name="Nation Name", value=name, inline=True)
                    embed.add_field(name="Leader Name", value=leader_name, inline=True)
                    embed.add_field(name="Score", value=score, inline=True)
                    embed.add_field(name="Alliance", value=alliance, inline=True)
                    embed.add_field(name="Cities", value=city_count, inline=True)
                    embed.add_field(name="Offensive Wars", value=offensive_wars, inline=True)
                    embed.add_field(name="Defensive Wars", value=defensive_wars, inline=True)
                    embed.add_field(name="AvgInfra", value=average_infrastructure, inline=True)
                    embed.set_footer(text="")
                    await ctx.send(embed=embed)
                    print("Nation Data Sent")
                    break
        nations_file.close


@bot.command(name="refresh_enemy_nations")
async def refresh_enemy_nations(ctx, alliance_id):
    print("Refreshing data")
    query = f"{{alliances(id:{alliance_id}) {{data {{nations {{id,alliance_position,nation_name,num_cities,score,soldiers,tanks,aircraft,ships}}}}}}}}"
    r = requests.post(f"https://api.politicsandwar.com/graphql?api_key={api_key}", json={"query": query})
    data = r.json()["data"]["alliances"]["data"][0]["nations"]
    with open('database/enemy_nations.json', 'w') as enemy_nations_file:
        json.dump(data, enemy_nations_file)
        print("Data Refreshed")
    await ctx.send("Data Refreshed")


@bot.command(name="convert_csv")
async def convert_csv(ctx):
    print("Converting json file to csv")
    with open('database/enemy_nations.json') as inputfile:
        df = pd.read_json(inputfile)
    df.to_csv('csvfile.csv')
    print("File converted")
    await ctx.send("File converted")


#does not show all net revenue, only gross nation income
@bot.command(name='revenue')
async def revenue(ctx, nation_id):
    query = f"{{nations(id:{nation_id}) {{data {{gross_national_income}}}}}}"
    r = requests.post(f"https://api.politicsandwar.com/graphql?api_key={api_key}", json={"query": query})
    data = r.json()["data"]["nations"]["data"][0]["gross_national_income"]
    net_revenue = int(data) / 365
    await ctx.send(net_revenue)


@bot.command(name='register')
async def register(ctx, nation_id):
    author = (ctx.message.author.id)
    data = registered_dict
    data[author] = nation_id
    json_object = json.dumps(data, indent = 4)
    with open('registered_nations.py', 'w') as outputfile:
        outputfile.write("registered_dict = " + json_object)
    await ctx.send("Nation Registered")

@register.error
async def register_error(ctx,error):
    if isinstance(error):
        await ctx.send("Something went wrong")


bot.run(token)