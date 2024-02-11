import nextcord
import random
import os
import requests
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    game = nextcord.Game("Finding memes with @vvendetta")
    await bot.change_presence(status=nextcord.Status.idle, activity=game)

    for guild in bot.guilds:
        welcome_message = f"Hey there! I'm {bot.user.name}! I'm ready to make you funny with memes and generate pictures in {guild.name}!"

        channel = nextcord.utils.get(guild.channels, name="memes")

        if channel:
            await channel.send(welcome_message)

# duck generator
def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.slash_command(name='duck', description="Sends a duck picture")
async def duck(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)

# dog generator
def get_dog_image_url():
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.slash_command(name='dog', description="Sends a dog picture")
async def dog(ctx):
    image_url = get_dog_image_url()
    await ctx.send(image_url)

# memes
@bot.command(name='animals', description="Sends you a random animal.")
async def animals(ctx):
    animals_folder = "image"
    animals = [f for f in os.listdir(animals_folder) if os.path.isfile(os.path.join(animals_folder, f))]

    if animals:
        random_animals = os.path.join(animals_folder, random.choice(animals))
        with open(random_animals, 'rb') as f:
            picture = nextcord.File(f)
        await ctx.send(file=picture)
    else:
        await ctx.send("No animal found.")
