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
           password = getpass.getpass(prompt= '        PASSWORD:  ')
           f_path = "assets/accounts.json"
           with open(f_path, 'r') as accounts:
               users = json.load(accounts)
               if u_name in users.keys():
                   print("[!]Username alreadys exists.\n[!]Please Sign In\n")
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
           password = getpass.getpass(prompt= '        PASSWORD: ')
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
         
         
         print("\nDATE:" ,date)
         print("TIME:",now)
         
         
def MyCalc(num1, num2, oper):
      
     
      if oper == "+":
           result = num1 + num2
           print("\n[+]Result is: ",result)
           
      elif oper == "-":
           result = num1 - num2
           print("\n[+]Result is: ",result)

      elif oper == "/":
           result = num1 / num2
           print("\n[+]Result is: ",result)

      elif oper == "*":
           result = num1 * num2
           print("\n[+]Result is: ",result)
           

      
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
    
     password = string.ascii_letters+string.digits+string.punctuation
    
     for pwd in range(numinput):
         pw = ""
     for c in range(length):
         pw += random.choice(password)
     
     print("\n")
     print("  +" * 20) 
     print("   [+]GENERATED", app, "PASSWORD:","[",pw,"]\n")        
     print("  +" * 20)
     time.sleep(1)
     
     sav = input("[+]Save the password (Y)es/(N)o: ") 
     if sav == "Y":
         f = open('Passwords/password.txt', 'a')
         f.write(app+":" +pw)
         f.close()
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
        count=0
        with open("assets/questions.json", 'r+') as h:
             for line in h:
               count+=1
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
    i = len(message) -1
    
    while i >= 0:
        trans = trans + message[i]
        i = i-1
    
    print("=========DECRYPTED MESSAGE=========")      
    print(trans)    
    print("=================================")
    
def crypt():
    
    message = input('MSG: ')
    trans = ''
    i = len(message) -1
    
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
        
          account_sid = 'ACc381f5ab9d1427278ab3d9efe195c8ab'
          auth_token = '8aa4a1db28e44bff949590b2be663544'

          client = Client(account_sid, auth_token)

          to = input("[*]RECIPIENT: ")
          message = client.messages.create(
    							from_='+1 959 214 4455',
    							body = trans,
    							to = to
    						)
          time.sleep(1)
          print("\n[*]Message sent successfully.\n[*]Auth Token:", message.sid)
    
    







    
print("\n")
print("    ****"*5)
print("        [       ICREATIVE CO.        ]")
print("    ****"*5)

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
   print("  **"*7)
   print("           THE HUB")
   print("  **"*7)
   dtime()
   print("\nLoading, please wait....")
   time.sleep(3)
   print("    =================")
   print(   "       PROGRAMMES"   )
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
      oper = input("[*] Choose Operater (+,-,/,*)\n: ")
      MyCalc(num1, num2, oper)

      time.sleep(2)
      ch = input("Do you wish to continue? (Y)es / (N)o: ")    
     
      if ch == "Y" or "y":
              MyCalc(num1, num2, oper)
      elif ch == "N" or "n":
               break
           
           
           
           
   if choice == "b":
         print("===================================")
         print(" [R]ock, [P]aper, [S]cissors v1.0")
         print("===================================")
         time.sleep(2)
         print("[*] LOCATION: THe Hub")
         time.sleep(1.5)
         print("[*] MISSION: Deafeat the r@nd0m A.I\n")
         time.sleep(1.5)
         print("[*] Choose your WEAPON")
         print("[R]ock, [P]aper, [S]cissors")
         intro = input(": ")
         if not re.match("[SsRrPp]", intro):
             print("Chose a letter:")
             print("[R]ock, [P]aper, [S]cissors")
             continue
 
         rps(intro)
         
         name = input("Play Again ?")
        
         if not re.match("[Yy]", name):
                break
         else:
                rps(intro) 
       
   
   if choice == "c":
      print("===================================")
      print("      Friendly Cow v1.0")
      print("===================================")
      

      name=input("What is your name,stranger? \n:")
      print("\n{ Good M00'ning", name,"}")

      print("              \   ^__^      ") 
      print("               \  (oo)\_______   *")
      print("                  (__)\       )\/")
      print("                      ||----w |  ")
      print("                      ||     ||   ")

      time.sleep(2)
      print("\n{ Welcome to the FORTUNATE COW}\n")

      print("                       \   ^__^      ") 
      print("                        \  (oo)\_______   *")
      print("                           (__)\       )\/")
      print("                               ||----w |  ")
      print("                               ||     ||   ")
      
      time.sleep(2)
      
      fortune_list=['happy', 'sad', 'joy', 'happy', 'blessed', 'angry', 'hate', 'caring', 'passionate']

      fortune = random.choice(fortune_list)

      print("\n{ Here is Your Fortune::",fortune,"}")

      print("                               \   ^__^      ") 
      print("                                \  (oo)\_______   *")
      print("                                   (__)\       )\/")
      print("                                       ||----w |  ")
      print("                                       ||     ||   ")
      
             
      name = input("Play Again(y/n): ")
        
      if not re.match("[Yy]", name):
                break
      else:
            signin()



   if choice == "d":
     print("===================================")
     print("  ----Password Manager v1.0----")
     print("===================================")
     
     numinput = 5
     
     app = input("\n[+] Generating password for: ")
     length = int(input("\n[+] Password length: "))
     
     
     pwmgr(numinput, app, length)
     
     
     name = input("Play Again ?")
        
     if not re.match("[Yy]", name):
                break
     else:
            pwmgr(numinput, app, length)

   if choice == "e":

     print("===================================")
     print(" ----YouTube Downloader v1.0----")
     print("===================================")
     
     url = input("Enter the video url: ")
     youdl(url)

     
   if choice == "f":
     print("===================================")
     print(" Instagram Profile Downloader v1.0")
     print("===================================")
     
     
     bot = instaloader.Instaloader()
     link = input("Enter the target username: ")
     print(bot.download_profile(link,profile_pic_only=True))

 
   
   if choice == "g":
     print("===================================")
     print("  ----Inbuilt Dictionary v1.0----")
     print("===================================")
     
     dict = PyDictionary()
     
     word = dict.meaning(input("Enter you word: "))
     print(word)
     
   
   if choice == "h":
     print("===================================")
     print("  Video-Audio converter v1.0----")
     print("===================================")

     vid = input("Enter the video to be converted: ")
     
     video = moviepy.editor.VideoFileClip(vid)
     audio = video.audio
     
     audio.write_audiofile(vid)
     print("Conversion Successfully") 


   
   
   if choice == "i":
     print("===================================")
     print(" ----Text-Audio Converter v1.0----")
     print("===================================")
     
     files = input("File to be transcribed:")
     path = open(files, 'rb')
     reader = PyPDF2.PdfFileReader(path)
     page = reader.getPage(0)
     text = page.extractText()
     
     speak = pyttsx3.init()
     speak.say(text)
     speak.runAndWait()


   if choice == "j":
     print("===================================")
     print("     ----Mirror! Mirror! v1.0----")
     print("===================================")
     audio = "Audios/audio.mp3"
     language = 'en'
     text = input("What is your desire:")
     clip = gTTS(text, lang = language, slow=False)
     
     clip.save(audio)
     playsound(audio)

   if choice == "k":
     print("===================================")
     print("     ----iBrowser v1.0----")
     print("===================================")

     url = input("URL of the webpage: ")
     webbrowser.open_new(url)
     
   if choice == "l":
       print("===================================")
       print("       ----The Quiz Show----")
       print("===================================")
       
       counter = int(input("\n[+] Number of players: "))
       players = []
      
       for i in range(counter):
             p_name = input("\n[+] Player name: ")
             players.append(p_name)
             
             
       print("\n[+] Confirm players:", players)
        
       ch = input("(Y)es/(N)o:")
        
       if not re.match("[Yy]", ch):
             break 
       else:
            print("\n==========QUIZ START==========")
            score = 0
            n = count()
            wait()
            with open("assets/questions.json", 'r+') as f:
                 j = json.load(f)
                 for i in range(n):
                        no_of_questions = len(j)
                        ch = random.randint(0, no_of_questions-1)
                        chose = random.choice(players)
                        print(chose,"TURN\n")
                        print(f'\nQ{i+1} {j[ch]["question"]}\n')
                        for option in j[ch]["options"]:
                            print(option)
                        answer = input("\nEnter your answer: ")
                        if j[ch]["answer"][0] == answer[0].upper():
                            print("\nYou are correct")
                            score+=1
                        else:
                            print("\nYou are incorrect")
                        del j[ch]
                        print(f'\nFINAL SCORE: {score}')
          
   if choice == "m":
        print("==========================")
        print("=======E N I G M A========")
        print("==========================")        
        print("[x]ENCRYPTOR/DECRYPTOR PROGRAM")
        ch = input("1.ENCRYPT  2.DECRYPT \n:")
        
        if ch == "1":
            crypt()
            
        elif ch == "2":
            decrypt()
            
        else: 
            print("incorrect value: Exiting program")
            break
