import json
import requests
import discord
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get


with open("config.json") as config:
    data = json.load(config)
    token = data["important"]["token"]
    api_key = data["important"]["api_key"]
    alliance_id = data["important"]["alliance_id"]
    v1_base_url = data["important"]["v1_base_url"]


def get_tax_records():
    query = f"{{alliances(id: 8861) {{data {{taxrecs {{id,sender_id,date,money,coal,oil,uranium,iron,bauxite,lead,gasoline,munitions,steel,aluminum,food,tax_id}}}}}}}}"
    r = requests.post(f"https://api.politicsandwar.com/graphql?api_key={api_key}", json={"query": query})
    data = r.json()["data"]["alliances"]["data"][0]["taxrecs"]
    for iteration, i in enumerate(data):
        times_run = iteration
        tax_data = data[times_run]
        tax_record_id = tax_data["id"]
        with open("database/old_tax_ids_v2.json") as old_ids:
            old_ids_list = json.load(old_ids)
            if tax_record_id not in old_ids_list:
                old_ids_list.append(tax_record_id)
                with open ("database/old_tax_ids_v2.json", "w") as file:
                    json.dump(old_ids_list, file)
                with open("database/tax_records_v2.json") as tax_records_file:
                    old_records = json.load(tax_records_file)
                    with open("database/tax_records_v2.json", "w") as tax_file:
                        old_records.append(tax_data)
                        json.dump(old_records, tax_file)
            

        