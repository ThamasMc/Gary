import requests

from discord.ext.commands import Bot
from discord import Game

BOT_PREFIX = ('!')
TOKEN = 'YOURTOKENHERE'
client = Bot(command_prefix=BOT_PREFIX)
client.count = 0
client.gary_list = ['G', 'R', 'Y']
client.initiative_order = {}

def gary_str():
  client.gary_list.insert(1, 'A')
  return ''.join(client.gary_list)

@client.command()
async def gary():
  await client.say(gary_str())

@client.command(pass_context=True)
async def hello(context):
  await client.say("Hello " + context.message.author.display_name)

@client.command()
async def reset_gary():
  client.gary_list = ['G', 'R', 'Y']

@client.command(
                pass_context=True,
                aliases=['init', 'i']
                )
async def lets_go(context, number):
  print(context.message.author.display_name + " " + number)
  player_name = context.message.author.display_name
  client.initiative_order[player_name] = int(number)
  print(client.initiative_order)

@client.command()
async def list_init():
  sorted_list = sorted(client.initiative_order, key=client.initiative_order.__getitem__)
  print(sorted_list)
  bot_response = 'Initiative Order: \n'
  for item in sorted_list:
    print(item + ': ' + str(client.initiative_order[item]))
    bot_response += item + ': ' + str(client.initiative_order[item]) + '\n'
  print('---------------------------------------------------------`')
  await client.say(bot_response)

@client.command()
async def reset_init():
  client.initiative_order = {}

@client.command(
                description='Will add an entry to the initiative order with a name and number',
                brief='Add someone to initiative',
                aliases=['add_enemy','test_init', 'ae', 'spf']
                )
async def spoof_init(name, number):
  client.initiative_order[name] = int(number)

@client.command()
async def spell( *, spell_name):
  url = "http://www.dnd5eapi.co/api/spells/"
  response = requests.get(url).json()
  for result in response['results']:
    if result['name'].lower() == spell_name.lower():
      new_url = result['url']
  if new_url == url:
    await client.say("Spell: " + spell_name  +" not found")
  else:
    response = requests.get(new_url).json()
    spell_name = response['name']
    components = ' , '.join(response['components'])
    description = ''.join(response['desc'])
    higher_text = response.get('higher_level', '')
    higher_text = ''.join(higher_text)
    final_response = "Found spell: " + spell_name + "\n"
    final_response += "Level " + str(response['level']) + " " + response['school']['name'] + "\n"
    final_response += "Casting Time: " + response['casting_time'] + " | " + "Ritual: " + response['ritual'] + " | Components: " + components + "\n"
    final_response += "Duration: " + response['duration'] + " | Concentration: "  + response['concentration'] + "\n"
    final_response += description + "\n"
    final_response += higher_text
    await client.say(final_response)
    

@client.event
async def on_ready():
  await client.change_presence(game=Game(name="being a real boy"))
  print ('Logged in as')
  print (client.user.name)
  print (client.user.id)
  print ('------------------')

client.run(TOKEN)
