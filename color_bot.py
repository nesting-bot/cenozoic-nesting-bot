
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks

import read


load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')



import discord
from discord.ext import commands
import random

from collections import OrderedDict

queue = OrderedDict()



blacklisted_player_names = ["example", "here",]




intents = discord.Intents.default()
intents.members = True

intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)


@bot.event
async def on_ready():
    check_nest_timer.start()
    read_chat_messages.start()
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')




@bot.command()
async def nest(ctx, *, username=None):
    """Grabs the member's username and @mentions them."""

    member = ctx.author
    user_id = str(ctx.author.id)
    if username is None:
        await ctx.send(f"Hi {member.mention}, please type '?nest [your_username]' (without brackets) to join the queue.")
        return
    elif user_id not in queue:
        queue[user_id] = username
        await ctx.send(f"Hi {member.mention}, '{username}' has been added to the queue.")
        return
    elif user_id in queue:
        if queue[user_id] == username:
            await ctx.send(f"Hi {member.mention}, {username} is already in the queue! Type '?position' to see your position in the queue.")
            return
        elif queue[user_id] != username:
            await ctx.send(f"Hi {member.mention}, you have changed your nesting name from '{queue[user_id]}' to '{username}'.")
            queue[user_id] = username
            return
    else:
        await ctx.send(f"Hi {member.mention}, You're already in the queue!")

@bot.command()
async def remove(ctx):
    """Remove yourself from queue and @mentions them."""
    member = ctx.author
    user_id = str(ctx.author.id)
    if user_id in queue:
        del queue[user_id]
        await ctx.send(f"Hi {member.mention}, you have been removed from the queue.")
        return
    elif user_id not in queue:
        await ctx.send(f"Hi {member.mention}, you are not in the queue.")
        return    
    else:
        await ctx.send(f"Hi {member.mention}, error removing you from the queue!")


@bot.command()
async def position(ctx):
    member = ctx.author

    if str(ctx.author.id) in queue:
        position = list(queue.keys()).index(str(member.id)) + 1
        await ctx.send(f'{member.mention}, You are #{position} in the queue under username: "{queue[str(ctx.author.id)]}"!')
    else:
        await ctx.send(f"{member.mention}, You are not in the queue. If you would like to join, type '?nest [your_username]' (without brackets)")


@bot.command()
async def food(ctx):
    """Fills the nest's food and @mentions the requestor."""
    member = ctx.author
    read.store_food()
    await ctx.send(f'Hi {member.mention}, the food is full in the nest!')

@bot.command()
async def lb(ctx):
    """AGC."""
    member = ctx.author
    await ctx.send(f'Hi {member.mention}, {queue}')

@bot.command()
async def grow(ctx, *, username=None):
    """Grow your animal."""
    member = ctx.author

    user_id = str(ctx.author.id)

    if username in blacklisted_player_names:
        await ctx.send(f"Hi {username}!")
        return
    if username is None:
        await ctx.send(f"Hi {member.mention}, please type '?grow GAME-NAME' to grow your animal.")
        return
    else:
        read.check_player_exists(username)


        cooldown_bool, timer_left =  read.command_is_on_cooldown(username, '?grow')
        print(f"cooldown result: {cooldown_bool, timer_left}")
        if cooldown_bool:
            if timer_left is not None:
                print(f"timer_left = {timer_left}")
                if timer_left > 60:
                    print(f"timer_left = {timer_left}")
                    minutes = int(timer_left) // 60

                    remaining_seconds = int(timer_left) % 60

                    output_time = f"{minutes} minutes, {remaining_seconds} seconds"
                elif timer_left <= 60: 
                    output_time = f"{round(timer_left)} seconds"
                await ctx.send(f"Hi {member.mention}, please wait {output_time} to use ?grow again.")
                return


        await ctx.send(f"Hi {member.mention}, you are going to be grown under username {username}!")
        read.grow_command(username)
        read.update_json_commands(username, '?grow')
        return
        

@bot.command()
async def stuck(ctx, *, username=None):
    """TP's the animal to an admin."""
    member = ctx.author
    user_id = str(ctx.author.id)
    if username is None:
        await ctx.send(f"Hi {member.mention}, please type '?stuck GAME-NAME' to TP your animal to an admin.")
        return
    else:
        await ctx.send(f"Hi {member.mention}, you are going to be TP'd under username {username}!")
        read.stuck_command(username)
        return



@bot.command()
async def timer(ctx):
    """Reports the remaining timer on the nest and @mentions the requestor."""
    member = ctx.author
    timer = read.check_ready_to_invite()
    if timer == "Ready":
        await ctx.send(f'Hi {member.mention}, the nest is ready!')
    else:
        await ctx.send(f'Hi {member.mention}, the nest timer still has {timer} minutes left!')


@tasks.loop(seconds=10)
async def read_chat_messages():
    """Sends a message every 10 seconds."""
    read.read_chat()
    await bot.wait_until_ready()

@tasks.loop(seconds=60)
async def check_nest_timer():
    """Sends a message every 10 seconds."""
    channel_id = 1234567890123456678  # Replace with your channel ID for nesting? Or use the ctx.send for any channel
    channel = bot.get_channel(channel_id)
    time_left = read.check_ready_to_invite()
    if time_left == "Ready":
        if len(queue) == 0:
            #await channel.send("10 minutes has passed, anyone can join!")
            return
        elif len(queue) > 0:
            user_id, username = list(queue.items())[0]
            await channel.send(f"You are being nested <@{user_id}> on name {username}!")
            read.invite_player_to_nest(str(username))
            del queue[user_id]

            if len(queue) == 0:
                await channel.send("No one else is in queue, anyone can join!")
            else:
                user_id, username = list(queue.items())[0]
                await channel.send(f"You are next in line <@{user_id}> on '{username}'!")        
    else:
        pass
    await bot.wait_until_ready()


























































# @bot.command()
# async def add(ctx, left: int, right: int):
#     """Adds two numbers together."""
#     await ctx.send(left + right)


# @bot.command()
# async def roll(ctx, dice: str):
#     """Rolls a dice in NdN format."""
#     try:
#         rolls, limit = map(int, dice.split('d'))
#     except Exception:
#         await ctx.send('Format has to be in NdN!')
#         return

#     result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
#     await ctx.send(result)


# @bot.command(description='For when you wanna settle the score some other way')
# async def choose(ctx, *choices: str):
#     """Chooses between multiple choices."""
#     await ctx.send(random.choice(choices))


# @bot.command()
# async def repeat(ctx, times: int, content='repeating...'):
#     """Repeats a message multiple times."""
#     for i in range(times):
#         await ctx.send(content)


# @bot.command()
# async def joined(ctx, member: discord.Member):
#     """Says when a member joined."""
#     await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


# @bot.group()
# async def cool(ctx):
#     """Says if a user is cool.

#     In reality this just checks if a subcommand is being invoked.
#     """
#     if ctx.invoked_subcommand is None:
#         await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


# @cool.command(name='bot')
# async def _bot(ctx):
#     """Is the bot cool?"""
#     await ctx.send('Yes, the bot is cool.')


bot.run(discord_token)

