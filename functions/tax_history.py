import json
import requests
import discord
import os
import random
import operator
import pandas as pd
from datetime import datetime, timedelta
from registered_nations import registered_dict
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get


with open("config.json") as config:
    data = json.load(config)
    token = data["important"]["token"]
    api_key = data["important"]["api_key"]
    alliance_id = data["important"]["alliance_id"]
    v1_base_url = data["important"]["v1_base_url"]


async def tax_history(ctx, nation_id):
    with open("database/tax_records_v2.json") as tax_records_file:
        tax_data = json.load(tax_records_file)
        records_used = 0
        money = 0
        coal = 0
        oil = 0
        uranium = 0
        iron = 0
        bauxite = 0
        lead = 0
        gasoline = 0
        munitions = 0
        steel = 0
        aluminum = 0
        food = 0
        for iteration, i in enumerate(tax_data):
            times_run = iteration
            nation_tax_data = tax_data[times_run]
            nation_tax_id = nation_tax_data["sender_id"]
            if nation_tax_id == nation_id:
                records_used += 1
                money_tax = nation_tax_data["money"]
                coal_tax = nation_tax_data["coal"]
                oil_tax = nation_tax_data["oil"]
                uranium_tax = nation_tax_data["uranium"]
                iron_tax = nation_tax_data["iron"]
                bauxite_tax = nation_tax_data["bauxite"]
                lead_tax = nation_tax_data["lead"]
                gasoline_tax = nation_tax_data["gasoline"]
                munitions_tax = nation_tax_data["munitions"]
                steel_tax = nation_tax_data["steel"]
                aluminum_tax = nation_tax_data["aluminum"]
                food_tax = nation_tax_data["food"]
                money += int(money_tax)
                coal += int(coal_tax)
                oil += int(oil_tax)
                uranium += int(uranium_tax)
                iron += int(iron_tax)
                bauxite += int(bauxite_tax)
                lead += int(lead_tax)
                gasoline += int(gasoline_tax)
                munitions += int(munitions_tax)
                steel += int(steel_tax)
                aluminum += int(aluminum_tax)
                food += int(food_tax)
        tax_dict = {
            "money": money,
            "coal": coal,
            "oil": oil,
            "uranium": uranium,
            "iron": iron,
            "bauxite": bauxite,
            "lead": lead,
            "gasoline": gasoline,
            "munitions": munitions,
            "steel": steel,
            "aluminum": aluminum,
            "food": food
        }
        await ctx.send(tax_dict)



async def alliance_tax_history(ctx, alliance_id):
    with open("database/tax_records_v2.json") as tax_records_file:
        tax_data = json.load(tax_records_file)
        money = 0
        coal = 0
        oil = 0
        uranium = 0
        iron = 0
        bauxite = 0
        lead = 0
        gasoline = 0
        munitions = 0
        steel = 0
        aluminum = 0
        food = 0
        for iteration, i in enumerate(tax_data):
            times_run = iteration
            nation_tax_data = tax_data[times_run]
            money_tax = nation_tax_data["money"]
            coal_tax = nation_tax_data["coal"]
            oil_tax = nation_tax_data["oil"]
            uranium_tax = nation_tax_data["uranium"]
            iron_tax = nation_tax_data["iron"]
            bauxite_tax = nation_tax_data["bauxite"]
            lead_tax = nation_tax_data["lead"]
            gasoline_tax = nation_tax_data["gasoline"]
            munitions_tax = nation_tax_data["munitions"]
            steel_tax = nation_tax_data["steel"]
            aluminum_tax = nation_tax_data["aluminum"]
            food_tax = nation_tax_data["food"]
            money += int(money_tax)
            coal += int(coal_tax)
            oil += int(oil_tax)
            uranium += int(uranium_tax)
            iron += int(iron_tax)
            bauxite += int(bauxite_tax)
            lead += int(lead_tax)
            gasoline += int(gasoline_tax)
            munitions += int(munitions_tax)
            steel += int(steel_tax)
            aluminum += int(aluminum_tax)
            food += int(food_tax)
        tax_dict = {
            "money": money,
            "coal": coal,
            "oil": oil,
            "uranium": uranium,
            "iron": iron,
            "bauxite": bauxite,
            "lead": lead,
            "gasoline": gasoline,
            "munitions": munitions,
            "steel": steel,
            "aluminum": aluminum,
            "food": food
        }
        await ctx.send(tax_dict)