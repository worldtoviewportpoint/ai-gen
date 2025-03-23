from discord.ext import commands
from discord import app_commands
from typing import Literal
import discord
import random
required_role = "Buyer"

def get_file_text(predX, predY):
    return f"""aimbot-enabled = "1";
aimbot-smoothing = "1";
camera-smoothing = "1";
aimbot-sensitivity = "1";
aimbot-bind = "67";
aimbot-bind-mode = "1";
aimbot-part = "2";
streamproof = "0";
v-sync = "1";
show_name = "0";
show_boxes = "0";
show_fov = "0";
show_deadzone = "0";
show_tracers = "0";
prediction = "1";
stickyaim = "1";
teamcheck = "0";
knockcheck = "0";
aimbot-fov = "93";
filled_fov = "0";
aimbot-deadzone = "0";
filled_deadzone = "0";
pred_x = "{predX}";
pred_y = "{predY}";
x_offset = "0";
y_offset = "0";
deadzone_flag = "0";
fov_flag = "0";
prediction_dot = "0";
pred_dot_type = "0";
tracer_type = "0";
shake = "0";
shake_x = "0";
shake_y = "0";
box_type = "0";
aimbot_type = "1";
no_jump = "0";
"""

class Vector2:
    def __init__(self, x = None, y = None):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

def random_16_char_string():
    s = ""
    for i in range(16):
        s += random.choice("QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjkklzxcvbnm12345890098765432")

    return s

def get_line(factor):
    return Vector2(7.317 + -0.01578 * factor, 8 + -0.01608 * factor)

bot = commands.Bot(command_prefix='__disabled__', intents=discord.Intents.all())
bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for /generate"))


@bot.hybrid_command(
    name="generate",
    description="Generate a config"
)
@app_commands.describe(
    game="The game you want to generate the config for",
    latency="Your Ping in MilliSeconds"
)
async def generate(ctx,
                   game: Literal["Da Hood"],
                   latency: int
                   ):

    r = discord.utils.get(ctx.guild.roles, name = required_role)

    if r not in ctx.author.roles:
        await ctx.reply(embed = discord.Embed(title = ">>> No permission."), ephemeral = True)
        return

    file_name = f"{random_16_char_string()}.cfg"

    solution = get_line(latency)

    with open(file_name, 'w') as file:
        file.write(
            get_file_text(
                solution.x,
                solution.y
            )
        )

    await ctx.reply(">>> Check our DMs!", ephemeral=True)

    channel = ctx.channel
    await ctx.message.author.send(embed=discord.Embed(title=">>> Your config is here!",
                                                      description="Bot written by \`worldtoscreen\`"),
                                  file=discord.File(file_name))


bot.run() # add token here