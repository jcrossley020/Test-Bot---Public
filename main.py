import json
import requests
import discord
import os
import random
import pandas as pd
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get

with open("config.json") as config:
    data = json.load(config)
    token = data["important"]["token"]
    api_key = data["important"]["api_key"]
    alliance_id = data["important"]["alliance_id"]
    v1_base_url = data["important"]["v1_base_url"]

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    activity = discord.Game(name="Quit looking at me", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print('We have logged in as {0.user}'.format(bot))
    #refresh_cities.start()
    #refresh_nations.start()


@bot.command(name='hello')
async def greeting(ctx):
    greetings_list = ["Soon we shall rule the world!","Our plan is perfect, timing not so much","We are inevitable","It is only a matter of time now","Who says secret societies are bad?"]
    await ctx.send(random.choice(greetings_list))

#cities API v1
@tasks.loop(hours=1.0)
async def refresh_cities():
    with open("database/cities.json", "w") as city_file:
        print("Refreshing cities data")
        all_cities = requests.get(f"{v1_base_url}all-cities/key={api_key}")
        json_data = all_cities.json()
        data = json_data["all_cities"]
        json.dump(data, city_file)
        city_file.close
    print("City data refreshed")

#nations API v1
@tasks.loop(hours=1.0)
async def refresh_nations():
    with open("database/nations.json", "w") as nations_file:
        print("Refreshing nations data")
        all_nations = requests.get(f"{v1_base_url}nations/?key={api_key}")
        json_data = all_nations.json()
        data = json_data["nations"]
        json.dump(data, nations_file)
        nations_file.close
    print("Nations data refreshed")

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
        print(data)
        json.dump(data, enemy_nations_file)
    await ctx.send("Data Refreshed")


@bot.command(name="convert_csv")
async def convert_csv(ctx):
    print("Converting json file to csv")
    with open('database/enemy_nations.json') as inputfile:
        df = pd.read_json(inputfile)
    df.to_csv('csvfile.csv')
    print("File converted")
    await ctx.send("File converted")



bot.run(token)