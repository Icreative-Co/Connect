import random
from datetime import *
import string
import re
import time
from PyDictionary import PyDictionary
import pyttsx3
import PyPDF2
from gtts import gTTS
from playsound import playsound
import moviepy.editor
import sys
import webbrowser
import instaloader
import json
from pytube import YouTube
import getpass
from twilio.rest import Client

user = []

def signup():
    print("        =======CREATE ACCOUNT=======")
    u_name = input("        USERNAME: ")
    password = getpass.getpass(prompt='        PASSWORD:  ')
    f_path = "assets/accounts.json"
    with open(f_path, 'r') as accounts:
        users = json.load(accounts)
        if u_name in users.keys():
            print("[!]Username already exists.\n[!]Please Sign In\n")
            signin()
        else:
            with open(f_path, 'w') as accounts:
                users[u_name] = [password, "PLAYER"]
                accounts.seek(0)
                json.dump(users, accounts)
                print("[*]Account Created Successfully!\n")

def signin():
    print("         ========LOGIN PANEL=========")
    username = input("        USERNAME: ")
    password = getpass.getpass(prompt='        PASSWORD: ')
    f_path = "assets/accounts.json"
    with open(f_path, 'r') as u_acc:
        users = json.load(u_acc)
    if username not in users.keys():
        print("[!]Account doesn't Exist!\n[!]Please Sign Up\n")
        signup()
    elif username in users.keys():
        if users[username][0] != password:
            print("[!]Incorrect Password!\n[!]Try Again\n")
            signin()
        elif users[username][0] == password:
            print("\n           ====Login Successful.====\n")
            user.append(username)
            user.append(users[username][1])
            time.sleep(1)

def dtime():
    current_time = datetime.now()
    now = current_time.strftime("%H:%m:%S")
    date = current_time.strftime("%d/%m/%Y")
    print("\nDATE:", date)
    print("TIME:", now)

def MyCalc(num1, num2, oper):
    if oper == "+":
        result = num1 + num2
        print("\n[+]Result is:", result)
    elif oper == "-":
        result = num1 - num2
        print("\n[+]Result is:", result)
    elif oper == "/":
        result = num1 / num2
        print("\n[+]Result is:", result)
    elif oper == "*":
        result = num1 * num2
        print("\n[+]Result is:", result)

def rps(intro):
    print("\n[+]You chose: " + intro)
    choses = ['R', 'P', 'S']
    opponent = random.choice(choses)
    print("\n[+]Comp chose: " + opponent)
    time.sleep(2)
    print("\n------Rolling Dice------")
    time.sleep(1.5)
    print("\n[+]Predicting Outcome......")
    time.sleep(2)

    if opponent == str.upper(intro):
        print("\n[[Tie]]")
    elif opponent == 'R' and intro.upper() == 'S':
        print("\n[[Scissors beats rock, comp wins!]]\n")
    elif opponent == 'S' and intro.upper() == 'P':
        print("\n[[Scissors beats paper, Comp wins!]]\n")
    elif opponent == 'P' and intro.upper() == 'R':
        print("\n[[Paper beats rock, Comp wins!]]\n")
    else:
        print("\n[[You win!]]\n")

def pwmgr(numinput, app, length):
    password = string.ascii_letters + string.digits + string.punctuation

    for pwd in range(numinput):
        pw = ""
        for c in range(length):
            pw += random.choice(password)

    print("\n")
    print("  +" * 20)
    print("   [+]GENERATED", app, "PASSWORD:", "[", pw, "]\n")
    print("  +" * 20)
    time.sleep(1)

    sav = input("[+]Save the password (Y)es/(N)o: ")
    if sav == "Y":
        with open('Passwords/password.txt', 'a') as f:
            f.write(app + ":" + pw + "\n")
    print("")
    print("  +" * 20)
    print("  [+] Generated", app, "Password saved in password.txt")
    print("  +" * 20, "\n")

def youdl(url):
    yt = YouTube(url)
    video = yt.streams.first()
    print("[*] Downloading....")
    video.download()
    print("[*] Download Successful!")

def count():
    count = 0
    with open("assets/questions.json", 'r+') as h:
        for line in h:
            count += 1
        return count

def wait():
    print("..\n")
    time.sleep(1)
    print("....\n")
    time.sleep(1)
    print("........\n")
    time.sleep(1)
    print("..........\n")

def decrypt():
    message = input('[*]MSG: ')
    trans = ''
    i = len(message) - 1
    while i >= 0:
        trans = trans + message[i]
        i = i-1
    print("=========DECRYPTED MESSAGE=========")
    print(trans)
    print("=================================")

def crypt():
    message = input('MSG: ')
    trans = ''
    i = len(message) - 1
    while i >= 0:
        trans = trans + message[i]
        i = i-1
    print("\n=========ENCRYPTED MESSAGE=========")
    print(trans)
    print("=================================")

    ch = input("\n[*]Send Message y/n: ")
    if not re.match("[Yy]", ch):
        print("[*]EXITING PROGRAM....")
    else:
        account_sid = 'replace with yours'
        auth_token = 'replace with yours'
        client = Client(account_sid, auth_token)
        to = input("[*]RECIPIENT: ")
        message = client.messages.create(
            from_='+1 959 214 4455',
            body=trans,
            to=to
        )
        time.sleep(1)
        print("\n[*]Message sent successfully.\n[*]Auth Token:", message.sid)

# New functions for saving and loading quiz progress
def save_progress(player_name, current_score, answered_questions, remaining_questions):
    progress = {
        "player_name": player_name,
        "current_score": current_score,
        "answered_questions": answered_questions,
        "remaining_questions": remaining_questions
    }
    
    with open(f'{player_name}_progress.json', 'w') as file:
        json.dump(progress, file)
    print("Progress saved successfully!")

def load_progress(player_name):
    try:
        with open(f'{player_name}_progress.json', 'r') as file:
            progress = json.load(file)
        print("Progress loaded successfully!")
        return progress
    except FileNotFoundError:
        print("No saved progress found for this player.")
        return None

# Main program starts here
print("\n")
print("    ****" * 5)
print("        [       ICREATIVE CO.        ]")
print("    ****" * 5)

print("\n            1.SIGN IN   2.SIGN UP")

ch = input("                     :")
if ch == "1":
    signin()
elif ch == "2":
    signup()
else:
    print("[!]Wrong Value! Try Again")
    sys.exit()

while True:
    print("\n Welcome to...\n")
    print("  **" * 7)
    print("           THE HUB")
    print("  **" * 7)
    dtime()
    print("\nLoading, please wait....")
    time.sleep(3)
    print("    =================")
    print("       PROGRAMMES")
    print("    =================")
    print("{a} = MyCalc")
    print("{b} = Rock, Paper, Scissors")
    print("{c} = Friendly Cow")
    print("{d} = PasswordManager")
    print("{e} = YouTube Downloader")
    print("{f} = Instagram Pic Downloader")
    print("{g} = Personal Dictionary")
    print("{h} = Video-Audio Converter")
    print("{i} = Text-audio Converter")
    print("{j} = Mirror! Mirror!")
    print("{k} = iBrowser")
    print("{l} = Quiz Show")
    print("{m} = ENIGMA")
    print("{q} = Quit the programme")
    choice = input("\n>")

    if choice == "q":
        break

    if choice == "a":
        print("======================================")
        print("    --    ---  ---                 ")
        print("    --     --  --            ..       ")
        print("  ------    ----    -----  ------     ")
        print("    --     --  --            ..       ")
        print("    --    ---  ---                   ")
        print("=======================================")
        num1 = int(input("\n[*] Enter first number: "))
        num2 = int(input("[*] Enter second number: "))
        oper = input("[*] Choose operation [+, -, *, /]: ")
        MyCalc(num1, num2, oper)

    elif choice == "b":
        print("======================================")
        print("                ------  --    ----            ")
        print("                --  --  --    --   --          ")
        print("                  ----  --    ----          ")
        print("                --  --  --    --   --          ")
        print("                ------  ----  ----             ")
        print("=======================================")
        intro = input("[*]Choose rock(R), paper(P), scissors(S) : ")
        rps(intro)

    elif choice == "c":
        print("======================================")
        print("          --   --       ----           ")
        print("          --   --     --    --            ")
        print("          --   --    --      --           ")
        print("          --   --     --    --          ")
        print("           -----        ----              ")
        print("=======================================")

        print("..... Mooooooooooooooooooo!.....")

    elif choice == "d":
        print("======================================")
        print("         -----  --   --  -------        ")
        print("        --       -- --   --     --       ")
        print("        --        ---    --     --       ")
        print("        --       -- --   --     --       ")
        print("         -----  --   --  -------        ")
        print("=======================================")

        numinput = int(input("[+]How many passwords would you like to generate?: "))
        app = input("[+]Application for this password: ")
        length = int(input("[+]Choose length of password to be generated: "))
        pwmgr(numinput, app, length)

    elif choice == "e":
        print("======================================")
        print("        -----  --    --  -----         ")
        print("        --      --   --  --   --          ")
        print("        -----  --   --  -----           ")
        print("        --      --   --  --   --          ")
        print("        -----  -------  -----             ")
        print("=======================================")

        url = input("[+]Enter YouTube link: ")
        youdl(url)

    elif choice == "f":
        print("======================================")
        print("           --       --  -------   ")
        print("          --       --  --        ")
        print("          --   --  --  -------       ")
        print("          -- --   --  --           ")
        print("           --       --  -------  ")
        print("=======================================")

        bot = instaloader.Instaloader()
        acc = input("[+]Enter Instagram profile name: ")
        bot.download_profile(acc, profile_pic_only=True)

    elif choice == "g":
        print("======================================")
        print("          ----  --  -------   ")
        print("          --    --  --        ")
        print("          --    --  -------   ")
        print("          --    --  --        ")
        print("          ----  --  -------  ")
        print("=======================================")

        dictionary = PyDictionary()
        word = input("\n[*]Enter word: ")
        mean = dictionary.meaning(word)
        print("\n[*]MEANING:", mean)

        syn = dictionary.synonym(word)
        print("\n[*]SYNONYMS:", syn)

        ant = dictionary.antonym(word)
        print("\n[*]ANTONYMS:", ant)

    elif choice == "h":
        print("======================================")
        print("      -------  -----    --   --  --  -------   ")
        print("      --       --   --  --   --  --  --        ")
        print("      -------  -----     -- --   --  -------    ")
        print("      --       --   --   -- --   --  --        ")
        print("      -------  -----       --    --  -------  ")
        print("=======================================")

        video = input("[+]Enter name of video file: ")
        video = moviepy.editor.VideoFileClip(video)
        audio = video.audio
        audio.write_audiofile("sample.mp3")
        print("[*]Audio Successfully Extracted.")

    elif choice == "i":
        print("======================================")
        print("          -------  --    ----             ")
        print("             --     --   --   --           ")
        print("             --     --   --   --            ")
        print("          -------  ----  ----                ")
        print("=======================================")

        tex = input("[+]Enter text: ")
        tts = gTTS(tex)
        tts.save("test.mp3")
        playsound("test.mp3")

    elif choice == "j":
        print("======================================")
        print("       ----  --  -------   ")
        print("       --    --  --        ")
        print("       --    --  -------   ")
        print("       --    --  --        ")
        print("       ----  --  -------  ")
        print("=======================================")

        decrypt()

    elif choice == "k":
        print("======================================")
        print("         -------  --    --  -----         ")
        print("         --       --   --   --   --           ")
        print("         -------  --   --   -----           ")
        print("         --       --   --   --   --           ")
        print("         --       -------   -----            ")
        print("=======================================")

        print("\n[*]1.Open a webpage\n[*]2.Perform a search")
        ch = input("[+]Enter: ")
        if ch == "1":
            link = input("[+]Enter link: ")
            webbrowser.open(link)
        elif ch == "2":
            link = input("[+]Enter search: ")
            webbrowser.open("https://www.google.com/search?q=" + link)
        else:
            print("[!]Try again")

    elif choice == "l":
        print("======================================")
        print("     -----   --    --  -----   ")
        print("     --   --  --   --  --        ")
        print("     --   --  --   --  -----     ")
        print("     --   --  --   --  --         ")
        print("     -----    -------  -----   ")
        print("=======================================")

        # Quiz Show starts here
        print("Welcome to the Quiz Show!")

        player_name = user[0]
        progress = load_progress(player_name)
        if progress:
            score = progress['current_score']
            answered_questions = progress['answered_questions']
            remaining_questions = progress['remaining_questions']
        else:
            score = 0
            answered_questions = []
            remaining_questions = list(range(1, count() + 1))

        for question_id in remaining_questions:
            with open("assets/questions.json", 'r+') as file:
                questions = json.load(file)
                question = questions[str(question_id)]

            print("\n" + question['question'])
            for option in question['options']:
                print(option)

            answer = input("Choose the correct option: ")

            if answer.lower() == question['answer'].lower():
                print("Correct!")
                score += 1
            else:
                print("Incorrect. The correct answer was:", question['answer'])

            answered_questions.append(question_id)
            remaining_questions.remove(question_id)

            save_choice = input("Do you want to save your progress? (yes/no): ")
            if save_choice.lower() == "yes":
                save_progress(player_name, score, answered_questions, remaining_questions)

            cont = input("Do you want to continue the quiz? (yes/no): ")
            if cont.lower() == "no":
                save_progress(player_name, score, answered_questions, remaining_questions)
                break

        print(f"\nFinal Score: {score}")
        print("Thank you for playing the Quiz Show!")

    elif choice == "m":
        print("======================================")
        print("        --  --   -----   ")
        print("        --  --   --       ")
        print("        --  --   -----   ")
        print("        --  --   --        ")
        print("        -------  -----   ")
        print("=======================================")

        crypt()

    else:
        print("\n[!]Invalid input! Please try again.\n")
