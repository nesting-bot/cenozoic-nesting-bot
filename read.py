import pyautogui as pg
import os
import re
from datetime import datetime
import random
import time
import pyperclip
import json
from dotenv import load_dotenv
from openai import OpenAI

from tools import grab_text, grab_number, screenshot_for_text, read_json, dump_json

load_dotenv()
chat_token = os.getenv('CHATGPT_TOKEN')

os.chdir(os.path.dirname(os.path.abspath(__file__)))


time.sleep(1)


discord_link = "discord.gg/LinkHere"

# Screenshot Locations
total = (0, 0, 3000, 3060)
timer_int_one = (2417, 653, 30, 37)
timer_int_two = (2445, 656, 21, 30)
total_timer = (2416, 653, 53, 38)
food_location = (2224, 554, 100, 50)
food_click_location = (2535, 980)
close_button_location = (2489,1763,125,45)
ready_location = (2093, 653, 104, 41)
player_search_click_field = (2200, 340)
player_name_click_location = (1580, 340)
invite_player_click_location = (2290, 1790)
steam_name_location = (1380, (293), 420, 75)











def check_command_timer_on_player(player_name):
    pass



def copy_and_paste_text(text):
    time.sleep(.2)
    pg.press('enter')
    time.sleep(.2)
    pyperclip.copy(text)
    time.sleep(.1)
    pg.hotkey("ctrl", "v")
    time.sleep(.1)
    pg.press('enter')
    time.sleep(.1)



def check_nest_open():
    close_button = grab_text(screenshot_for_text(close_button_location, "Close"))
    if close_button == 'Close':
        return True
    else:
        close_button = grab_text(screenshot_for_text(close_button_location, "Close"))
        if close_button == 'Close':
            return True           
        else:
            return False


def close_nest():
    pg.click(2650, 1815)

def open_nest():
    if not check_nest_open():
        pg.press('e')
        time.sleep(.5)
        if check_nest_open():
            print("Nest is open!")
            return True
        else:
            print("ERROR: Unable to open nest!")
            pg.press('b')
            time.sleep(.5)
    if not check_nest_open():
        pg.press('e')
        time.sleep(.5)
        if check_nest_open():
            print("Nest is open!")
            return True
        else:
            print("ERROR: Unable to open nest!")
            return False

def store_food():
    open_nest()
    if check_nest_open():
        food_number_text = grab_number(screenshot_for_text(food_location, "food"))
        print(food_number_text)

        if food_number_text is None:
            for i in range(30):
                pg.click(food_click_location)
                time.sleep(.05)
            print("Filled Food!")
            close_nest() 

            return
        else:
            if food_number_text >= 300:
                print("Food is full!")
                close_nest() 
                return True
            current_food = int(food_number_text)
            times_to_click = (310 - current_food) / 10

            for i in range(int(times_to_click)):
                pg.click(food_click_location)
                time.sleep(.05)
            print("Filled Food!")
            close_nest() 
            return True
    else:
        print("ERROR: Unable to store food.!")
        close_nest() 
        return False





def check_ready_to_invite():
    open_nest()
    ready_to_invite = grab_text(screenshot_for_text(ready_location, "ready_to_invite"))
    if ready_to_invite == 'Ready':
        print("Ready to invite!")
        close_nest()
        return "Ready"
    else:
        # total_timer
        timer_left = grab_number(screenshot_for_text(total_timer, "first_x"))
        print(timer_left)
        if timer_left is None:
            print("Using Text Grabber")
            timer_left = grab_number(screenshot_for_text(timer_int_one, "first_x"))
            print(timer_left)
        close_nest()            
        return timer_left
    
    


witty_help_command_messages = [
    # "Hello {username}! I am a bot with multiple commands, can talk, and... uhh... that's all really?",
    f"I'm an automated Bot, with multiple commands. Извините, русский алфавит должен использовать Discord - {discord_link}",
    # "I am Nesting Bot, a bot with not much to do, so I just make nests for {username} and follow commands.",
]

help_command_messages = [
    "Try typing '?discord', '?grow', '?stuck', or my favorite,                 '?chat [write a sentence]'."
    # "Try typing '?discord', '?grow', or '?stuck'."
]

discord_command_messages = [
    "Welcome {username}! Our discord link is:",
    "Maybe you should guess at what the link is...                                Just kidding, it's:",
    "This is the link to our fun discord, where you can have... fun! I guess? (Link below)",
    "Yeah, you'll have to type this in yourself, good luck remembering all the random letters and numbers! *Evil laugh*",
]

grow_command_messages = [
    "{username}, you are being grown!",
    "{username} is being grown. If you want a grow, type   ?grow",
    "{username} needs to be grown. Don't worry, I can make that happen!",
    

]

grow_command_followup_messages = [
    "{username} is now an adult. Good luck surviving the wild!",
    "... Look at you {username}, all grown up! I'm proud of you!",
    "You have been grown {username}. You're on your own now.",
    "Adulthood is like a rollercoaster ride. {username} — hold on tight and try not to scream.",
    "You're officially an adult {username}! Time to start pretending you know what you're doing.",
    "Adulthood: where {username}'s back goes out more than they do.",
    "Happy adulting {username}! May your coffee be strong and your Mondays short.",
    'Growing up means learning "just one more episode" is a lie.',
]

stuck_command_messages = [
    "Looks like we need to save {username} again!",
    "{username} got stuck in deep mud, and I guess I'll have to get {username} out of it! Hah, funny joke, right... right?",
    "You are stuck {username}, but no one is here to help. It looks like you'll have to walk back home. *tsk tsk*                                       Just kidding, I'll help.",
    "{username}, what did I say about jumping into rocks? It gets you stuck! Physics, am I right?",
    "I guess 'stuck' is {username}'s new middle name!",
    "I see {username} is practicing your damsel-in-distress routine.",
    "Well, this isn't exactly what {username} had in mind for a weekend getaway.",
    "It looks like {username} found a new way to get attention!",
    "Is this the universe's way of telling {username} to slow down?",
    "Help! {username} has fallen, and can’t get up.",
    "I guess {username} took 'stuck in a rut' a bit too literally.",
    "Can we get {username} a refund on today's adventure, please?",
    "Rescue me now, laugh at me later! {username} has a good story to tell.", 
    "Next time, {username}, bring a map and a GPS...",
    "{username} has always wanted to be the hero, but I guess today {username} is the one needing rescue.",
    "Stuck again? {username} should really start a loyalty program with their rescuers.",
    "I didn't think 'getting stuck' would be {username}'s superpower.",
    "I knew {username} should have read the manual first.",
    "If this was a movie, now would be the perfect time for a heroic entrance.",]




def grow_command(player_name):
    time.sleep(.1)
    copy_and_paste_text(f"/grow {player_name}")
    time.sleep(1)   
    copy_and_paste_text(f"/grow {player_name}")
    copy_and_paste_text(f"{player_name} has been grown using Discord commands - ?discord") 
    time.sleep(.2)
    

def stuck_command(player_name):
    copy_and_paste_text(f"/bring {player_name}")
    copy_and_paste_text(f"{player_name} has been TP'd using Discord commands - ?discord")
    



command_list = ["?help", "?discord", "?heal", "?grow", "?cool", "?stuck", "?chat", "?weather"]









def check_player_exists(player_name, timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
    display_name = player_name
    player_name = player_name.lower()
    json_data = read_json()

    # "?help", "?discord", "?heal", "?grow", "?cool", "?stuck", "?chat", "?weather"
    blank_timestamp_last_used = {
        "?grow": None,
        "?chat": None,
        "?stuck": None,
        "?weather": None,
        "?help": None,
        "?discord": None,
        "?heal": None,
        "?cool": None,
        "other": None
    }
    blank_number_commands_used = {
        "?grow": 0,
        "?chat": 0,
        "?stuck": 0,
        "?weather": 0,
        "?help": 0,
        "?discord": 0,
        "?heal": 0,
        "?cool": 0,
        "other": 0
    }

    if player_name not in json_data["players"]:
        json_data["players"][player_name] = {"timestamp_last_used": blank_timestamp_last_used, "number_commands_used": blank_number_commands_used, "last_interaction": timestamp}
        
        json_data["players"][player_name]["last_interaction"] = timestamp
        print("Added player JSON: " + player_name)


    else:
        json_data["players"][player_name]["last_interaction"] = timestamp
        print("Added player JSON: " + player_name)

    dump_json(json_data)

def update_json_commands(player_name, command, timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
    player_name = player_name.lower()
    json_data = read_json()

    # "?help", "?discord", "?heal", "?grow", "?cool", "?stuck", "?chat", "?weather"
    blank_timestamp_last_used = {
        "?grow": None,
        "?chat": None,
        "?stuck": None,
        "?weather": None,
        "?help": None,
        "?discord": None,
        "?heal": None,
        "?cool": None,
        "other": None
    }
    blank_number_commands_used = {
        "?grow": 0,
        "?chat": 0,
        "?stuck": 0,
        "?weather": 0,
        "?help": 0,
        "?discord": 0,
        "?heal": 0,
        "?cool": 0,
        "other": 0
    }

    if player_name not in json_data["players"]:
        json_data["players"][player_name] = {"timestamp_last_used": blank_timestamp_last_used, "number_commands_used": blank_number_commands_used, "last_interaction": timestamp}
        
        json_data["players"][player_name]["last_interaction"] = timestamp
        json_data["players"][player_name]["timestamp_last_used"][command] = (timestamp)

        commands_used = json_data["players"][player_name]["number_commands_used"][command]
        commands_used += 1
        json_data["players"][player_name]["number_commands_used"][command] = (commands_used)


    else:
        json_data["players"][player_name]["last_interaction"] = timestamp
        json_data["players"][player_name]["timestamp_last_used"][command] = (timestamp)

        commands_used = json_data["players"][player_name]["number_commands_used"][command]
        commands_used += 1
        json_data["players"][player_name]["number_commands_used"][command] = (commands_used)

    dump_json(json_data)










def command_is_on_cooldown(player_name, command):
    player_name = player_name.lower()

    #              10 min * 60 sec
    growth_cooldown = (10 * 60)

    if command in command_list: 
        json_data = read_json()
        try:
            last_used_time = json_data["players"][player_name]["timestamp_last_used"][command]
            if last_used_time:
                now_timestamp = datetime.now()
                last_used_time_obj = datetime.strptime(last_used_time, "%Y-%m-%d %H:%M:%S")
                time_left = now_timestamp - last_used_time_obj

                if command == "?grow":
                    if time_left.total_seconds() > growth_cooldown:
                        return False, None
                    else: return True, (growth_cooldown - time_left.total_seconds())

                if time_left.total_seconds() > 120:
                    return False, None
                else: return True, None

            else: return False, None
        except KeyError: return False, None



blacklisted_player_names = ["example", "here",]

def read_chat():
    print("reading chat")
    def handle_chat_commands(text_chat_line):
        print(f"handle_chat_commands: {text_chat_line}")
        try:
            username, message = text_chat_line.split(" : ")

            typing_username = username
            message_list = message.split(" ")
            check_player_exists(username)


            # Manual hard-coding names that the OCR couldn't quite get right.
            if username in blacklisted_player_names:
                return

            if username.lower().startswith("ribica"):
                typing_username = username = "ribica11"
                print(f"RIIIBIIII")

            if username.lower().startswith("matitahana"):
                typing_username = username = "Mätitahana"

            if username.lower().startswith('rose_"'):
                typing_username = username = 'Rose_"0w0"'


            if username.lower().startswith("kitty"):
                typing_username = username = "k!tty"

            if username.lower().startswith("your local"):
                typing_username = username = "your"
         
            if username.lower().startswith("king_panzer"):
                typing_username = username = "kıng_pAnzer"
                print(f"Kiiiing")         
         
         
            print(f"u:m ==   {typing_username}:{message_list}")

            search_input= message_list[0]
            search_command = ""
            for i in search_input.split():
                if i == ' ':
                    pass
                else:
                    search_command += i



            cooldown_bool, timer_left =  command_is_on_cooldown(username, search_command)
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


                    copy_and_paste_text(f"{username}, please wait {output_time} to use {search_command} again.")
                return

            if search_command in command_list:
                update_json_commands(username, search_command)
            else:
                update_json_commands(username, "other")



            if search_command == "?help" or search_command == "2help" or search_command == "%help":
                copy_and_paste_text("I'm an automated Bot, with multiple commands. If you have special characters in your name, please use the Discord.")
                copy_and_paste_text(f"Извините, чат-бот не распознает русский алфавит, поэтому для команд необходимо использовать Discord. - {discord_link}")
                copy_and_paste_text("如果这些机器人命令不起作用，请在 Steam 名称中仅使用英文字母")
                help_command_message = random.choice(help_command_messages).format(username=username)
                copy_and_paste_text(help_command_message)


            elif search_command == "?discord" or search_command == "2discord" or search_command == "%discord":
                discord_message = random.choice(discord_command_messages).format(username=username)
                copy_and_paste_text(discord_message)
                copy_and_paste_text(discord_link)



            elif search_command == "?heal" or search_command == "2heal" or search_command == "%heal":
                copy_and_paste_text("Sorry, but '?heal' isn't a command, but a fairytale. Like Santa Claus, or your mother's love.")
                
            elif search_command == "?grow" or search_command == "2grow" or search_command == "%grow" or search_command == "!grow" or search_command == "29grow" or search_command == "Pgrow":
                print("Grow command used!")
                grow_message = random.choice(grow_command_messages).format(username=username)
                copy_and_paste_text(grow_message)
                copy_and_paste_text(f"/grow {typing_username}")
                time.sleep(1)
                copy_and_paste_text(f"/grow {typing_username}")
                grow_followup_message = random.choice(grow_command_followup_messages).format(username=username)
                copy_and_paste_text(grow_followup_message)
                
            

            elif search_command == "?cool" or search_command == "2cool" or search_command == "%cool":
                copy_and_paste_text(f"Yes, {typing_username} is cool!")
                

            elif search_command == "?stuck" or search_command == "2stuck" or search_command == "%stuck" or search_command == "!stuck": 
                stuck_message = random.choice(stuck_command_messages).format(username=username)
                copy_and_paste_text(stuck_message)
                copy_and_paste_text(f"/bring {typing_username}")



            elif search_command == "?chat" or search_command == "2chat" or search_command == "?question" or search_command == "2question" or search_command == "%chat": 

                player_message_string = ' '.join(message_list[1:])


                client = OpenAI(api_key=chat_token)

                # Define the context and player's message
                context = "You are a player on an animal survival game. Don't ask questions. Don't ask if people want help or assistance. Be a friendly player. Stay in-character, and keep the response to under 350 characters."
                player_message = player_message_string

                # Combine context and player's message
                prompt = f"{context}\n\nPlayer message to you: \"{player_message}\""

                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="gpt-3.5-turbo",
                )
                # print(chat_completion)
                # print()
                # print()
                message_content = chat_completion.choices[0].message.content
                # print(message_content)
                
                time.sleep(.2)
                pg.press('enter')
                time.sleep(.2)
                pg.typewrite(message_content+"      (AI Response, not human)", .008)
                pg.press('enter')
                time.sleep(.2)
                

            elif search_command == "?weather" or search_command == "?}weather" or search_command == "?]weather":
                time.sleep(.2)
                pg.press('enter')
                time.sleep(.2)
                pg.typewrite("This feature is disabled until my human comes back online!", .008)
                pg.press('enter')
                time.sleep(.2)
                


                time.sleep(.2)
                # if message_list[1] == "clear":
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.typewrite(f"Making it clear and sunny!", .008)
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.typewrite(f"/weather clear", .008)
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.typewrite(f"There, it is all sunny now!", .008)
                #     pg.press('enter')
                #     time.sleep(.2)

                # elif message_list[1] == "cloudy":
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.typewrite(f"Making it cloudy!", .008)
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.typewrite(f"/weather overcast", .008)
                #     pg.press('enter')
                #     time.sleep(.2)                 
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.typewrite(f"The sky looks dull today.", .008)
                #     pg.press('enter')
                #     time.sleep(.2)


                # elif message_list[1] == "rain":
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.typewrite(f"Making it rain!", .008)
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.typewrite(f"/weather rain", .008)
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.typewrite(f"Bring your raincoat, since it's going to be a wet day today!", .008)
                #     pg.press('enter')
                #     time.sleep(.2)


                # elif message_list[1] == "snow":
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.typewrite(f"Making it COLD!", .008)
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.typewrite(f"/weather snow", .008)
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.typewrite(f"The first snowflakes are falling!", .008)
                #     pg.press('enter')
                #     time.sleep(.2)



                # else:
                #     pg.press('enter')
                #     time.sleep(.2)
                #     pg.typewrite(f"The options are: ?weather clear, ?weather cloudy, ?weather rain, ?weather snow", .008)
                #     pg.press('enter')
                #     time.sleep(.2)                
                # time.sleep(.2)


            elif search_command == "?time": pass

            elif search_command == "?animal": pass
            # elif search_command == "?nest":   # Nesting is only available to our discord members. You can join us at: DISCORD!       
            

            #     time_left = check_ready_to_invite()
            #     if time_left == "Ready":
            #         time.sleep(.2)
            #         pg.press('enter')
            #         time.sleep(.2)
            #         pg.typewrite(f"{typing_username}, you are being nested in!", .008)
            #         pg.press('enter')
            #         time.sleep(.2) 
            #         invite_player_to_nest(typing_username)
                        
            #     else:
            
            #         time.sleep(.2)
            #         pg.press('enter')
            #         time.sleep(.2)
            #         pg.typewrite(f"The timer still has {time_left} minutes!", .008)
            #         pg.press('enter')
            #         time.sleep(.2)                       


        except Exception as e:
            print("ERROR: " + str(e))


    # Read Chat

    pg.press('enter')
    time.sleep(.5)

    timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    textfile_name = "chat " + str(timestamp_now) + ".txt"

    safe_filename = re.sub(r'[\\/:"*?<>|]', '', textfile_name.replace(' ', '_'))

    with open(safe_filename, "w") as text_file:
        text_file.write("")


    chat_output_list = []
    increment = 0
    for i in range(16):
        # print(f"reading chat line {str(i+1)}")
        chat_location = (2670, (1444+increment), 1058, 34)
        

        chat_message_text = grab_text(screenshot_for_text(chat_location, "p" + str(i+1)))
        
        if chat_message_text is None:
            chat_message_text = grab_text(screenshot_for_text(chat_location, "p" + str(i+1)))
        elif chat_message_text is not None:
            # print(f"chat_message   ==   {chat_message_text}")
            chat_output_list.append(chat_message_text)
            # print(chat_output_list)
    
            with open(safe_filename, "a") as text_file:
                text_file.write(f"{chat_message_text}\n")
            
        increment += 34

    # Process scraped chat messages



    pg.press('enter')
    time.sleep(.5)    
    for chat_message_text in chat_output_list[13:]:
        handle_chat_commands(chat_message_text)



    




def invite_player_to_nest(player_name):
    open_nest()

    check_invite = check_ready_to_invite() 
    if check_invite == "Ready":
        open_nest()
        pg.click(player_search_click_field)
        pg.hotkey('ctrl', 'a')
        time.sleep(.2)
        pg.press('backspace')
        time.sleep(.2)
        pyperclip.copy(str(player_name))
        pg.hotkey("ctrl", "v")
        time.sleep(.1)
        pg.mouseDown(player_name_click_location)
        time.sleep(.1)
        pg.mouseUp(player_name_click_location)
        time.sleep(.1)
        pg.mouseDown(player_name_click_location)
        time.sleep(.1)
        pg.mouseUp(player_name_click_location)
        time.sleep(.1)
        pg.mouseDown(invite_player_click_location)
        time.sleep(.1)
        pg.mouseUp(invite_player_click_location)
        time.sleep(.1)
        pg.mouseDown(invite_player_click_location)
        time.sleep(.1)
        pg.mouseUp(invite_player_click_location)
        time.sleep(.1)
        pg.click(player_search_click_field)
        time.sleep(.2)
        pg.hotkey('ctrl', 'a')
        time.sleep(.1)
        pg.press('backspace')
        time.sleep(.1)
        close_nest()
    else:
        print("Player not ready to invite.!")
        close_nest()
        return check_invite


time.sleep(2)

# check_ready_to_invite()
# read_chat()
# grow_command('Test')



