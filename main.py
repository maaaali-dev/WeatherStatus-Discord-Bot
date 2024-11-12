import discord
from discord.ext import commands
import requests

# Discord Token and Open Weather API Key
DISCORD_TOKEN = ''
OPENWEATHER_API_KEY = ''

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = {
            "temperature": data["main"]["temp"],
            "temp_min": data["main"]["temp_min"],
            "temp_max": data["main"]["temp_max"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"],
            "city": data["name"],
            "country": data["sys"]["country"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "icon": data["weather"][0]["icon"],
        }
        return weather
    else:
        return None

@bot.event
async def on_ready():
    print(f'{bot.user} is now online')
    await bot.tree.sync()

@bot.tree.command(name="weather", description="Shows the current weather")
async def weather(interaction: discord.Interaction, city: str):
    weather_data = get_weather(city)
    if weather_data:
        icon_url = f"http://openweathermap.org/img/wn/{weather_data['icon']}@2x.png"

        embed = discord.Embed(
            title=f"Weather in {weather_data['city']}, {weather_data['country']}",
            description=f"Currently: {weather_data['description'].capitalize()}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=icon_url)
        embed.add_field(name="🌡️ Temperature", value=f"{weather_data['temperature']}°C", inline=False)
        embed.add_field(name="🌡️ Max-Min Temperature", value=f"{weather_data['temp_min']} - {weather_data['temp_max']}°C", inline=False)
        embed.add_field(name="🌬️ Feels Like", value=f"{weather_data['feels_like']}°C", inline=False)
        embed.add_field(name="💧 Humidity", value=f"{weather_data['humidity']}%", inline=False)
        embed.add_field(name="💨 Wind Speed", value=f"{weather_data['wind_speed']} m/s", inline=False)
        embed.set_footer(text="Data provided by OpenWeather")
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("City not found or something went wrong")

bot.run(DISCORD_TOKEN)