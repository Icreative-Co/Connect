#!/usr/bin/env python3
"""
icreative.py v2 - Full-featured multi-tool CLI

"""

from __future__ import annotations
import os
import sys 
import json
import time
import random
import re
import string
import getpass
import hashlib
import binascii
import math
import cmath
import statistics
import itertools
import threading
import secrets
import base64
import collections
import pytube
import yt_dlp
from functools import reduce
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
from urllib.parse import urljoin, urlparse


# Optional runtime imports handled gracefully
_optional = {}

def try_import(name: str):
    try:
        module = __import__(name)
        _optional[name] = True
        return module
    except Exception:
        _optional[name] = False
        return None

# Optional modules
requests = try_import("requests")
bs4 = try_import("bs4")  # BeautifulSoup4
yt_dlp = try_import("yt_dlp")
pytube = try_import("pytube")
instaloader = try_import("instaloader")
moviepy = try_import("moviepy")
gtts_mod = try_import("gtts")
edge_tts = try_import("edge_tts")
pyttsx3_mod = try_import("pyttsx3")
playsound_mod = try_import("playsound")
simpleaudio = try_import("simpleaudio")
twilio_mod = try_import("twilio")

# -------------------------------------------------------------------------------------------------------
# Paths & constants
# -------------------------------------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
PASSWORDS_DIR = os.path.join(BASE_DIR, "Passwords")
PROGRESS_DIR = os.path.join(BASE_DIR, "progress")
ACCOUNTS_FILE = os.path.join(ASSETS_DIR, "accounts.json")
QUESTIONS_FILE = os.path.join(ASSETS_DIR, "questions.json")
PASSWORD_STORE = os.path.join(PASSWORDS_DIR, "passwords.txt")
SAVE_FILE = os.path.join(PROGRESS_DIR, "game_progress.json")

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(PASSWORDS_DIR, exist_ok=True)
os.makedirs(PROGRESS_DIR, exist_ok=True)

# -------------------------
# ASCII Animations (small)
# -------------------------
def anim_loading(text="Loading", duration=1.2, speed=0.15):
       end = time.time() + duration
       while time.time() < end:
            for dots in range(1, 4):
                sys.stdout.write(f"\r{text}{'.' * dots} ")
                sys.stdout.flush()
                time.sleep(speed)
       print("\r" + " " * (len(text) + 6) + "\r", end="")        

# -------------------------------------------------------------------------------------------------------
# Security (password hashing)
# -------------------------------------------------------------------------------------------------------
def _hash_password(password: str, salt: Optional[bytes] = None) -> Dict[str, str]:
    if salt is None:
        salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return {"salt": binascii.hexlify(salt).decode("ascii"), "hash": binascii.hexlify(dk).decode("ascii")}

def _verify_password(stored_hash_hex: str, stored_salt_hex: str, provided_password: str) -> bool:
    salt = binascii.unhexlify(stored_salt_hex)
    new = hashlib.pbkdf2_hmac("sha256", provided_password.encode("utf-8"), salt, 200_000)
    return binascii.hexlify(new).decode("ascii") == stored_hash_hex

# -------------------------------------------------------------------------------------------------------
# Accounts management
# -------------------------------------------------------------------------------------------------------
def load_accounts() -> Dict[str, Any]:
    if not os.path.exists(ACCOUNTS_FILE):
        # create default accounts
        hashed_admin = _hash_password("admin")
        default = {
            "admin": {"password_hash": hashed_admin["hash"], "salt": hashed_admin["salt"], "role": "ADMIN"}
        }
        with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=2)
        return default
    try:
        with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("[!] accounts.json corrupt — backing up and creating new file.")
        os.rename(ACCOUNTS_FILE, ACCOUNTS_FILE + ".bak")
        return load_accounts()

def save_accounts(accounts: Dict[str, Any]) -> None:
    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
        json.dump(accounts, f, indent=2)

def signup() -> Optional[str]:
    print("        =======CREATE ACCOUNT=======")
    accounts = load_accounts()
    while True:
        u_name = input("        USERNAME: ").strip()
        if not u_name:
            print("[!] Username cannot be empty.")
            continue
        if u_name in accounts:
            print("[!] Username already exists.\n[!]Please Sign In\n")
            return None
        password = getpass.getpass(prompt='        PASSWORD:  ')
        if not password:
            print("[!] Password cannot be empty.")
            continue
        hashed = _hash_password(password)
        accounts[u_name] = {"password_hash": hashed["hash"], "salt": hashed["salt"], "role": "PLAYER"}
        save_accounts(accounts)
        print("[*]Account Created Successfully!\n")
        return u_name

def signin() -> Optional[Tuple[str, str]]:
    print("         ========LOGIN PANEL=========")
    username = input("        USERNAME: ").strip()
    password = getpass.getpass(prompt='        PASSWORD: ')
    accounts = load_accounts()
    if username not in accounts:
        print("[!]Account doesn't Exist!\n[!]Please Sign Up\n")
        return None
    acct = accounts[username]
    attempts = 0
    while attempts < 4:
        if _verify_password(acct["password_hash"], acct["salt"], password):
            print("\n           ====Login Successful.====\n")
            return username, acct.get("role", "PLAYER")
        else:
            attempts += 1
            print("[!]Incorrect Password!\n[!]Try Again\n")
            password = getpass.getpass(prompt='        PASSWORD: ')
    print("[!]Too many failed attempts.")
    return None

# -------------------------------------------------------------------------------------------------------
# Utilities
# -------------------------------------------------------------------------------------------------------
def dtime():
    current_time = datetime.now()
    now = current_time.strftime("%H:%M:%S")
    date = current_time.strftime("%d/%m/%Y")
    print("\nDATE:", date)
    print("TIME:", now)

def safe_load_json(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[!] Missing file: {path}")
        return None
    except json.JSONDecodeError:
        print(f"[!] Failed to parse JSON: {path}")
        return None

# -------------------------------------------------------------------------------------------------------
# Tools (original)
# -------------------------------------------------------------------------------------------------------
memory = 0  # global memory to store last result


# ---------------------------------------------------------------------------------------------------------------------------------
# ADVANCED CAL
# ---------------------------------------------------------------------------------------------------------------------------------
def AdvancedCalc():
    global memory
    print("\n==== Advanced Calculator ===")
    print("Supports: basic arithmetic, trig, hyperbolic, logs, exponentials, factorials")
    print("Specialized domains:")
    print(" - Statistics: mean([1,2,3]), median([..]), stdev([..]), variance([..])")
    print(" - Combinatorics: factorial(n), comb(n,k), perm(n,k)")
    print(" - Linear algebra (vectors): dot([1,2,3],[4,5,6]), cross([1,0,0],[0,1,0])")
    print(" - Modular arithmetic: mod(a,m), pow(base,exp,mod)")
    print(" - Complex numbers: complex(a,b), phase(), polar(), rect()")
    print("Memory usage: type 'M' to reuse last result.")
    print("Examples of commands you can try:")
    print("  1.) 3 + 4 * 2")
    print("  2.) sin(pi/2) + cos(0)")
    print("  3.) sqrt(16) + factorial(5)")
    print("  4.) mean([10,20,30]) + M")
    print("  5.) dot([1,2,3],[4,5,6]) * 2")
    print("Type 'exit' to return to main menu.")
    print("==============================\n")

    # Helper functions
    def dot(v1, v2):
        return sum(x*y for x, y in zip(v1, v2))

    def cross(v1, v2):
        if len(v1) == 3 and len(v2) == 3:
            x1, y1, z1 = v1
            x2, y2, z2 = v2
            return [y1*z2 - z1*y2, z1*x2 - x1*z2, x1*y2 - y1*x2]
        else:
            raise ValueError("Cross product only defined for 3D vectors")

    def mod(a, m):
        return a % m

    def factorial(n):
        return math.factorial(n)

    def comb(n, k):
        return math.comb(n, k)

    def perm(n, k):
        return math.perm(n, k)

    while True:
        expr = input("[Calc]> ").strip()
        if expr.lower() in ("exit", "quit"):
            break

        # Replace memory placeholder
        expr = expr.replace("M", str(memory))

        try:
            allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
            allowed_names.update({
                "abs": abs, "round": round, "memory": memory, "factorial": factorial,
                "comb": comb, "perm": perm, "dot": dot, "cross": cross, "mod": mod,
                "mean": statistics.mean, "median": statistics.median,
                "stdev": statistics.stdev, "variance": statistics.variance,
                "complex": complex, "phase": cmath.phase, "polar": cmath.polar,
                "rect": cmath.rect, "sum": sum, "reduce": reduce,
                "pi": math.pi, "e": math.e
            })

            result = eval(expr, {"__builtins__": None}, allowed_names)
            print(f"[+] Result: {result}")
            memory = result
        except Exception as e:
            print("[!] Error evaluating expression:", e)



# -------------------------
# GAME CENTER
# -------------------------
def game_center():
    """
    Single-file Game Center with:
     - XP / Levels
     - Unlockable games
     - ASCII animations
     - Boss battles
     - Inventory & items
     - Achievements
     - Persistent save (game_progress.json)
    Drop-in ready; uses only Python standard library.
    """

    # -------------------------
    # Utilities & Persistence
    # -------------------------
    def now_ts():
        return datetime.utcnow().isoformat() + "Z"

    # default structure
    default_state = {
        "meta": {"created": now_ts(), "last_played": None},
        "profile": {
            "xp": 0,
            "level": 1,
            "coins": 0,
            "inventory": {},      # item_name -> count
            "achievements": {},   # ach_key -> {unlocked:bool, ts:...}
        },
        "scoreboard": {},         # game_key -> {wins, loss, ties, played}
        "unlocked_games": [],     # list of game keys unlocked
        "bosses_defeated": 0
    }

    # try load
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            state = default_state.copy()
    else:
        state = default_state.copy()

    # helpers
    def save_state():
        state["meta"]["last_played"] = now_ts()
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    def ensure_score(game_key):
        sb = state["scoreboard"]
        if game_key not in sb:
            sb[game_key] = {"wins": 0, "loss": 0, "ties": 0, "played": 0}

    def award_score(game_key, result):
        ensure_score(game_key)
        sb = state["scoreboard"][game_key]
        sb["played"] += 1
        if result == "win":
            sb["wins"] += 1
        elif result == "loss":
            sb["loss"] += 1
        elif result == "tie":
            sb["ties"] += 1
        save_state()

    # -------------------------
    # XP, Level, Rewards
    # -------------------------
    def xp_to_level(xp):
        # simple quadratic curve: level (lvl) requires 100 * lvl^2 XP
        lvl = 1
        while xp >= 100 * (lvl ** 2):
            lvl += 1
        return lvl

    def add_xp(amount):
        state["profile"]["xp"] += amount
        old_lvl = state["profile"]["level"]
        new_lvl = xp_to_level(state["profile"]["xp"])
        if new_lvl > old_lvl:
            state["profile"]["level"] = new_lvl
            # reward on level up
            reward_coins = 10 * new_lvl
            state["profile"]["coins"] += reward_coins
            show_message(f"LEVEL UP! Now level {new_lvl}. +{reward_coins} coins rewarded.")
            unlock_by_level(new_lvl)
            unlock_achievement("level_up", f"Reached level {new_lvl}")
        save_state()

    def show_message(msg, delay=1.1):
        print("\n" + "=" * 40)
        print(msg)
        print("=" * 40 + "\n")
        time.sleep(delay)

    # -------------------------
    # Inventory & Items
    # -------------------------
    ITEMS = {
        "1": {"name": "Health Potion", "desc": "Restore 15 HP", "type": "heal", "value": 15, "price": 5},
        "2": {"name": "Mega Potion", "desc": "Restore 40 HP", "type": "heal", "value": 40, "price": 20},
        "3": {"name": "Bomb", "desc": "Deal 20 damage to enemy", "type": "attack", "value": 20, "price": 15},
        "4": {"name": "Shield", "desc": "Block next enemy hit", "type": "shield", "value": 1, "price": 12},
    }

    def add_item(key, count=1):
        inv = state["profile"]["inventory"]
        inv[key] = inv.get(key, 0) + count
        save_state()

    def remove_item(key, count=1):
        inv = state["profile"]["inventory"]
        if inv.get(key, 0) >= count:
            inv[key] -= count
            if inv[key] <= 0:
                inv.pop(key, None)
            save_state()
            return True
        return False

    def show_inventory():
        inv = state["profile"]["inventory"]
        if not inv:
            print("Inventory empty.")
            return
        print("\nInventory:")
        for k, v in inv.items():
            item = ITEMS.get(k, {"name": k})
            print(f" - {item['name']} (x{v}) : {item.get('desc','')}")
        print("")

    # -------------------------
    # Achievements
    # -------------------------
    ACHIEVEMENTS = {
        "first_win": {"title": "First Win", "desc": "Win your first game"},
        "level_up": {"title": "Level Up", "desc": "Reach a new level"},
        "boss_slayer": {"title": "Boss Slayer", "desc": "Defeat a boss"},
        "collector": {"title": "Collector", "desc": "Obtain 5 different items"},
    }

    def unlock_achievement(key, note=""):
        if key not in state["profile"]["achievements"] or not state["profile"]["achievements"][key].get("unlocked", False):
            state["profile"]["achievements"][key] = {"unlocked": True, "ts": now_ts(), "note": note}
            show_message(f"Achievement unlocked: {ACHIEVEMENTS.get(key,{'title':key})['title']}")
            save_state()

    # -------------------------
    # Unlockable games by level
    # -------------------------
    UNLOCK_RULES = {
        "RPS": 1,            # default unlocked
        "NumberGuess": 1,
        "DiceBattle": 2,     # unlock at level 2
        "TypingTest": 2,
        "Hangman": 3,
        "TicTacToe": 3,
        "BossBattle": 4,     # boss unlocked at level 4
        "HackSim": 5,
    }

    # ensure default unlocked
    if not state.get("unlocked_games"):
        # unlock those with requirement <= current level
        cur_level = state["profile"]["level"]
        for k, req in UNLOCK_RULES.items():
            if req <= cur_level:
                state["unlocked_games"].append(k)
        save_state()

    def unlock_by_level(level):
        for k, req in UNLOCK_RULES.items():
            if req <= level and k not in state["unlocked_games"]:
                state["unlocked_games"].append(k)
                show_message(f"New game unlocked: {k} (Level {req} requirement met)")

    def is_unlocked(key):
        return key in state["unlocked_games"]

    # -------------------------
    # BOSS ANIMATION
    # -------------------------
    def anim_boss_intro(name):
        frames = [
            f"!!! BOSS APPROACHES: {name} !!!",
            f" > {name} is looming... prepare yourself!",
            f" >> {name} roars!",
        ]
        for f in frames:
            print(f)
            time.sleep(0.7)

    # -------------------------
    # Core mini-games (integrated)
    # Each game should call award_score and add XP/coins
    # -------------------------
    def game_rps():
        key = "RPS"
        if not is_unlocked(key):
            print("This game is locked. Reach required level to unlock.")
            return
        anim_loading("Starting RPS", 0.9)
        rounds = 3
        wins = losses = ties = 0
        choices = {"R": "Rock", "P": "Paper", "S": "Scissors"}
        for r in range(rounds):
            print(f"\nRound {r+1}/{rounds}")
            ch = input("[R/P/S] or 'exit' to stop: ").strip().upper()
            if ch == "EXIT":
                break
            if ch not in choices:
                print("Invalid.")
                continue
            comp = random.choice(list(choices.keys()))
            print(f"You: {choices[ch]} | Comp: {choices[comp]}")
            if ch == comp:
                print("Tie.")
                ties += 1
                award = 2
                add_xp(2)
            elif (ch == "R" and comp == "S") or (ch == "P" and comp == "R") or (ch == "S" and comp == "P"):
                print("You win!")
                wins += 1
                add_xp(8)
                state["profile"]["coins"] += 2
            else:
                print("You lose.")
                losses += 1
                add_xp(4)
        # record scoreboard
        if wins > losses:
            award_score(key, "win")
            unlock_achievement("first_win", "Won RPS")
        elif wins < losses:
            award_score(key, "loss")
        else:
            award_score(key, "tie")
        save_state()

    def game_number_guess():
        key = "NumberGuess"
        if not is_unlocked(key):
            print("This game is locked.")
            return
        anim_loading("Number Guess", 0.6)
        target = random.randint(1, 100)
        tries = 7
        won = False
        while tries > 0:
            try:
                g = input(f"Guess (1-100). {tries} tries left: ").strip()
                if g.lower() == "exit":
                    break
                g = int(g)
            except:
                print("Invalid.")
                continue
            if g == target:
                print("You guessed correctly!")
                add_xp(15)
                state["profile"]["coins"] += 5
                won = True
                break
            elif g < target:
                print("Higher.")
            else:
                print("Lower.")
            tries -= 1
        if won:
            award_score(key, "win")
        else:
            award_score(key, "loss")
        save_state()

    def game_dice_battle():
        key = "DiceBattle"
        if not is_unlocked(key):
            print("Locked. Reach higher level.")
            return
        anim_loading("Dice Battle", 0.6)
        rounds = 3
        player = comp = 0
        for i in range(rounds):
            input("Press Enter to roll...")
            p = random.randint(1, 6)
            c = random.randint(1, 6)
            print(f"You: {p} | Comp: {c}")
            if p > c:
                player += 1
                add_xp(6)
            elif p < c:
                comp += 1
                add_xp(3)
            else:
                add_xp(2)
            time.sleep(0.4)
        if player > comp:
            print("You win the dice duel!")
            award_score(key, "win")
            state["profile"]["coins"] += 4
        elif player < comp:
            print("You lost the duel.")
            award_score(key, "loss")
        else:
            print("It's a tie.")
            award_score(key, "tie")
        save_state()

    def game_typing_test():
        key = "TypingTest"
        if not is_unlocked(key):
            print("Locked.")
            return
        anim_loading("Typing Test", 0.5)
        texts = [
            "programming is fun",
            "security requires practice",
            "python makes automation easy",
            "open source powers innovation"
        ]
        target = random.choice(texts)
        print("Type this exactly:\n")
        print(target)
        input("Press Enter to start...")
        t0 = time.time()
        typed = input(">> ").rstrip("\n")
        t1 = time.time()
        duration = max(0.1, t1 - t0)
        wpm = len(typed.split()) / duration * 60
        accuracy = sum(1 for i, ch in enumerate(typed) if i < len(target) and ch == target[i]) / len(target) * 100
        print(f"Speed: {wpm:.1f} WPM | Accuracy: {accuracy:.1f}%")
        if accuracy >= 85:
            print("Great typing!")
            add_xp(12)
            state["profile"]["coins"] += 3
            award_score(key, "win")
        else:
            print("Keep practicing.")
            add_xp(4)
            award_score(key, "loss")
        save_state()

    def game_hangman():
        key = "Hangman"
        if not is_unlocked(key):
            print("Locked.")
            return
        anim_loading("Hangman", 0.5)
        words = ["python", "creative", "terminal", "keyboard", "function", "matrix", "security"]
        word = random.choice(words)
        guessed = set()
        attempts = 6
        while attempts > 0:
            display = "".join(c if c in guessed else "_" for c in word)
            print("\nWord:", display, "Attempts left:", attempts)
            if "_" not in display:
                print("You won!")
                add_xp(10)
                award_score(key, "win")
                save_state()
                return
            g = input("Guess letter or 'exit': ").strip().lower()
            if g == "exit":
                return
            if len(g) != 1 or not g.isalpha():
                print("Invalid input.")
                continue
            if g in guessed:
                print("Already guessed.")
                continue
            guessed.add(g)
            if g not in word:
                attempts -= 1
        print("You lost! Word was:", word)
        add_xp(3)
        award_score(key, "loss")
        save_state()

    def game_tictactoe():
        key = "TicTacToe"
        if not is_unlocked(key):
            print("Locked.")
            return
        anim_loading("TicTacToe", 0.5)
        board = [" "] * 9

        def show():
            print("\n")
            print(board[0], "|", board[1], "|", board[2])
            print("--+---+--")
            print(board[3], "|", board[4], "|", board[5])
            print("--+---+--")
            print(board[6], "|", board[7], "|", board[8])

        def check(sym):
            wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
            return any(all(board[i] == sym for i in w) for w in wins)

        while True:
            show()
            move = input("Your move (1-9) or exit: ")
            if move.lower() == "exit":
                return
            if not move.isdigit() or not 1 <= int(move) <= 9:
                print("Invalid.")
                continue
            i = int(move) - 1
            if board[i] != " ":
                print("Taken.")
                continue
            board[i] = "X"
            if check("X"):
                show()
                print("You win!")
                add_xp(12)
                award_score(key, "win")
                save_state()
                return
            free = [idx for idx, v in enumerate(board) if v == " "]
            if not free:
                show()
                print("Draw!")
                award_score(key, "tie")
                save_state()
                return
            bot = random.choice(free)
            board[bot] = "O"
            if check("O"):
                show()
                print("You lose.")
                add_xp(5)
                award_score(key, "loss")
                save_state()
                return

    def game_hacksim():
        key = "HackSim"
        if not is_unlocked(key):
            print("Locked.")
            return
        anim_loading("HackSim", 0.6)
        steps = ["scan", "enum", "exploit", "inject", "escalate", "extract"]
        for s in steps:
            print(f"> {s} -> type '{s}' to continue")
            inp = input("-> ").strip().lower()
            if inp != s:
                print("Exploit failed!")
                add_xp(2)
                award_score(key, "loss")
                save_state()
                return
            print("OK")
            time.sleep(0.25)
        print("Simulated hack successful!")
        add_xp(20)
        state["profile"]["coins"] += 15
        award_score(key, "win")
        save_state()

    # -------------------------
    # Boss battles (strategic)
    # -------------------------
    def boss_battle():
        key = "BossBattle"
        if not is_unlocked(key):
            print("Boss battles locked. Reach a higher level.")
            return
        anim_boss_intro("DreadTitan")
        player_hp = 80
        boss_hp = 120 + 10 * state.get("bosses_defeated", 0)
        shield_active = False
        print(f"Boss HP: {boss_hp} | Your HP: {player_hp}")
        while player_hp > 0 and boss_hp > 0:
            print("\nActions: [a]ttack [i]tem [h]eal [s]hield [run]")
            act = input("> ").strip().lower()
            if act == "a":
                dmg = random.randint(8, 18)
                boss_hp -= dmg
                print(f"You hit boss for {dmg}. Boss HP: {boss_hp}")
            elif act == "i":
                show_inventory()
                it = input("Item key to use (or cancel): ").strip()
                if it in state["profile"]["inventory"]:
                    if it == "bomb":
                        print("You used bomb! massive damage.")
                        boss_hp -= ITEMS["bomb"]["value"]
                        remove_item(it, 1)
                    elif it == "health_potion":
                        heal = ITEMS["health_potion"]["value"]
                        player_hp += heal
                        print(f"Healed {heal} HP.")
                        remove_item(it, 1)
                    elif it == "shield":
                        print("Shield activated for one hit.")
                        shield_active = True
                        remove_item(it, 1)
                    else:
                        print("Used item.")
                else:
                    print("No such item.")
            elif act == "h":
                heal = random.randint(10, 20)
                player_hp += heal
                print(f"Healed {heal} HP.")
            elif act == "s":
                shield_active = True
                print("Shield will block next boss attack.")
            elif act == "run":
                print("You fled from the boss.")
                add_xp(2)
                award_score(key, "loss")
                save_state()
                return
            else:
                print("Unknown action.")

            # boss turn
            if boss_hp > 0:
                bd = random.randint(6, 20)
                if shield_active:
                    print("Shield blocked the boss attack!")
                    shield_active = False
                else:
                    player_hp -= bd
                    print(f"Boss hits you for {bd}. Your HP: {player_hp}")

        if player_hp > 0 and boss_hp <= 0:
            print("BOSS DEFEATED! You are victorious!")
            add_xp(60 + 10 * state.get("bosses_defeated", 0))
            state["profile"]["coins"] += 50
            state["bosses_defeated"] = state.get("bosses_defeated", 0) + 1
            award_score(key, "win")
            unlock_achievement("boss_slayer", f"Defeated boss #{state['bosses_defeated']}")
            save_state()
        else:
            print("You were defeated by the boss.")
            add_xp(10)
            award_score(key, "loss")
            save_state()

    # -------------------------
    # Shop for items
    # -------------------------
    def shop():
        print("\n")
        print("===" * 10)
        print("Welcome to the shop. \nYou can buy items with coins.")
        print(f"Coins: {state['profile'].get('coins',0)}")
        print("===" * 10)
        print("\nAvailable Items: ")
        print("------------------")        
        for k, v in ITEMS.items():
            print(f"{k}: {v['name']} ( {v['desc']} ) == Price: {v['price']} coins")
        choice = input("[*] Enter item key to buy or 'exit': ").strip()
        if choice == "exit":
            return
        if choice not in ITEMS:
            print("[!]No such item.")
            return
        price = ITEMS[choice]["price"]
        if state["profile"].get("coins", 0) < price:
            print("[!]Insufficient coins. Play games to earn coins.")
            return
        state["profile"]["coins"] -= price
        add_item(choice, 1)
        print(f"Bought 1 x {ITEMS[choice]['name']}")
        # check collector achievement
        if len(state["profile"]["inventory"].keys()) >= 5:
            unlock_achievement("collector", "Collected 5 items")
        save_state()

    # -------------------------
    # Scoreboard & Profile display
    # -------------------------
    def show_scoreboard():
        print("\n=== SCOREBOARD ===")
        if not state["scoreboard"]:
            print("No games played yet.")
        else:
            for g, v in state["scoreboard"].items():
                print(f"{g}: played={v['played']} wins={v['wins']} loss={v['loss']} ties={v['ties']}")
        print("\nProfile:")
        p = state["profile"]
        print(f"Level: {p.get('level',1)}  XP: {p.get('xp',0)}  Coins: {p.get('coins',0)}")
        print("Inventory count:", sum(state["profile"].get("inventory",{}).values()))
        print("Achievements:")
        if not p.get("achievements"):
            print(" - (none)")
        else:
            for k, info in p["achievements"].items():
                title = ACHIEVEMENTS.get(k, {}).get("title", k)
                print(f" - {title} ({'unlocked' if info.get('unlocked') else 'locked'})")
        print(f"Bosses defeated: {state.get('bosses_defeated', 0)}")
        input("\nPress Enter to continue...")

    # -------------------------
    # Main menu loop
    # -------------------------
    while True:
        print("\n" + "=" * 48)
        print("                      GAME CENTER")
        print("=" * 48)
        print("Unlocked games: ", ", ".join(state.get("unlocked_games", [])) or "(none)")
        print(f"Level {state['profile'].get('level',1)} | XP {state['profile'].get('xp',0)} | Coins {state['profile'].get('coins',0)}")
        print("-" * 48)
        print("1) Rock Paper Scissors (RPS)           (unlocks at lvl 1)")
        print("2) Number Guess                        (lvl 1)")
        print("3) Dice Battle                         (lvl 2)")
        print("4) Typing Test                         (lvl 2)")
        print("5) Hangman                             (lvl 3)")
        print("6) Tic Tac Toe                         (lvl 3)")
        print("7) HackSim                             (lvl 5)")
        print("8) Boss Battle                         (lvl 4)")
        print("9) Shop / Inventory")
        print("10) Show Scoreboard & Profile")
        print("11) Save & Exit Game Center")
        print("-" * 48)
        choice = input("Select an option: ").strip()

        if choice == "1":
            game_rps()
        elif choice == "2":
            game_number_guess()
        elif choice == "3":
            game_dice_battle()
        elif choice == "4":
            game_typing_test()
        elif choice == "5":
            game_hangman()
        elif choice == "6":
            game_tictactoe()
        elif choice == "7":
            game_hacksim()
        elif choice == "8":
            boss_battle()
        elif choice == "9":
            shop()
        elif choice == "10":
            show_scoreboard()
        elif choice == "11":
            save_state()
            print("Progress saved. Exiting Game Center.")
            break
        else:
            print("Invalid selection. Enter a number from the menu.")

    # finalized save on exit
    save_state()
    print("Thank you for playing. Your progress has been saved.")



# ---------------------------------------------------------------------------------------------------------------------------------
# MIND PAL CHAT
# ---------------------------------------------------------------------------------------------------------------------------------
def mental_chat():
    """
    MindPal — Personality System (v1)
    Six personalities:
      - zen
      - motivator
      - therapist
      - programmer
      - stoic
      - friendly

    Usage:
      /modes           -> list available personalities
      /mode <name>     -> switch to a personality
      /stats           -> show mood & session stats
      /memory          -> show recent chat memory
      /clear           -> clear memory
      /help            -> show commands
      /exit            -> quit chat
    """

    # ---------- session storage ----------
    session_memory = collections.deque(maxlen=40)  # store last messages
    mood_counts = collections.Counter()
    messages = 0
    start_ts = time.time()

    # default personality
    current_personality = "friendly"

    # game suggestions (generic). If you integrate game_center, replace with dynamic list.
    GAME_SUGGESTIONS = {
        "low": ["Tic-Tac-Toe (gentle round)", "Snake (short run)", "Hangman (calm)"],
        "stress": ["Breathing + Mini-Game: Rock–Paper–Scissors", "Typing Test (focus)"],
        "coding": ["HackSim (fun)", "Debug puzzle (RPS variant)", "Tic-Tac-Toe to clear head"],
        "angry": ["Dice Duel (quick)", "Rock–Paper–Scissors (fast)"],
        "neutral": ["Snake", "Dice Duel", "Typing Test"]
    }

    # personalities config: tone templates, behavior tweaks
    PERSONALITIES = {
        "zen": {
            "label": "Zen (calm, meditative)",
            "greeting": "You're in Zen mode — calm, slow, reflective.",
            "reply_style": lambda text: f"(zen) {text} — breathe in... breathe out...",
            "game_bias": ["low", "neutral"],
            "suggestion_prefix": "A calm pick:",
        },
        "motivator": {
            "label": "Motivator (energetic, hype)",
            "greeting": "Motivator mode activated — let's get hyped!",
            "reply_style": lambda text: f"🔥 {text} Let's GO!",
            "game_bias": ["neutral", "coding"],
            "suggestion_prefix": "Get moving with:",
        },
        "therapist": {
            "label": "Therapist (reflective, mirroring)",
            "greeting": "Therapist mode — I’ll reflect and help you reframe.",
            "reply_style": lambda text: f"I hear: \"{text}\". Tell me more.",
            "game_bias": ["low", "stress"],
            "suggestion_prefix": "Consider trying:",
        },
        "programmer": {
            "label": "Programmer Buddy (practical, debugging tips)",
            "greeting": "Programmer Buddy ready — let's debug that stress.",
            "reply_style": lambda text: f"(dev) {text} — have you tried isolating the issue?",
            "game_bias": ["coding", "neutral"],
            "suggestion_prefix": "Dev-friendly game:",
        },
        "stoic": {
            "label": "Stoic (short, logical, grounding)",
            "greeting": "Stoic mode — concise, logical, grounding responses.",
            "reply_style": lambda text: f"{text}. Focus on facts.",
            "game_bias": ["neutral"],
            "suggestion_prefix": "A measured choice:",
        },
        "friendly": {
            "label": "Friendly (warm, casual)",
            "greeting": "Friendly companion here — chat freely.",
            "reply_style": lambda text: f"😊 {text}",
            "game_bias": ["neutral", "low"],
            "suggestion_prefix": "You might enjoy:",
        }
    }

    # message templates per personality category (helpers)
    TEMPLATES = {
        "encourage": [
            "You're doing great even if it doesn't feel like it.",
            "Small progress is still progress.",
            "One step at a time — you got this."
        ],
        "reframe": [
            "What would you tell a friend in the same situation?",
            "Is there a smaller part of the problem you can solve right now?"
        ],
        "practical": [
            "Try isolating the function that fails and write a minimal test.",
            "Rubber-duck the logic: say the flow aloud for 60 seconds."
        ],
        "calm": [
            "Close your eyes for 20 seconds and count breaths.",
            "Stand up, stretch shoulders forward/back twice."
        ],
        "fun": [
            "A short game break can reset your focus — 2 minutes!",
            "Play a light reflex game to reboot your attention."
        ]
    }

    # mood detection keywords
    MOOD_KEYWORDS = {
        "low": ["tired", "sad", "down", "lost", "hopeless", "blue"],
        "stress": ["stress", "stressed", "anxiety", "panic", "overwhelmed"],
        "coding": ["bug", "error", "fail", "crash", "stuck", "debug"],
        "angry": ["angry", "mad", "frustrated", "annoyed"],
        "neutral": ["ok", "fine", "good", "cool", "ready"]
    }

    def detect_mood(user_text):
        txt = user_text.lower()
        scores = {k: 0 for k in MOOD_KEYWORDS}
        for mood, keywords in MOOD_KEYWORDS.items():
            for kw in keywords:
                if kw in txt:
                    scores[mood] += 1
        # pick mood with highest count, default neutral
        best = max(scores, key=lambda k: scores[k])
        if scores[best] == 0:
            return "neutral"
        return best

    def short_breathing():
        print("\n🫁 Short breathing: inhale... (2s) ... exhale... (2s)")
        time.sleep(0.6)
        print("...one more time...")
        time.sleep(0.6)
        print("Alright — feeling a touch lighter?\n")

    def mini_mission():
        mission = random.choice([
            "Stand up and stretch for 30s.",
            "Drink a glass of water and breathe deeply.",
            "Close your eyes and count 10 slow breaths.",
            "Write down the first small step to solve the problem."
        ])
        print("\n🎯 Mini Mission:", mission)
        print("Complete it and tell me how it felt.\n")

    def suggest_games(mood, personality):
        # personality influences bias; use mood suggestions then personality bias
        base = GAME_SUGGESTIONS.get(mood, GAME_SUGGESTIONS["neutral"])
        bias = PERSONALITIES[personality]["game_bias"]
        # mix base with personality bias choices:
        picks = list(base)
        for b in bias:
            picks.extend(GAME_SUGGESTIONS.get(b, []))
        # unique, keep order
        seen = set()
        pick_list = []
        for p in picks:
            if p not in seen:
                seen.add(p)
                pick_list.append(p)
        return pick_list[:5]

    def show_help():
        print("\nCommands:")
        print("  /modes            - list available personalities")
        print("  /mode <name>      - switch personality (e.g. /mode zen)")
        print("  /stats            - show session stats")
        print("  /memory           - show recent chat memory")
        print("  /clear            - clear memory")
        print("  /breathe          - quick breathing exercise")
        print("  /mission          - give one mini mission")
        print("  /help             - show this help")
        print("  /exit             - exit chat\n")

    # welcome
    print("\n==== MindPal — Personality Companion ====")
    print("Type /help to see commands. Type /modes to list personalities.")
    print(f"Starting in '{current_personality}' personality. Say hello!\n")
    print(PERSONALITIES[current_personality]["greeting"])
    print()

    # main loop
    while True:
        try:
            user = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting MindPal.")
            break

        if not user:
            print(PERSONALITIES[current_personality]["reply_style"]("I'm listening — whenever you are ready."))
            continue

        # handle commands
        if user.startswith("/"):
            cmd = user.split()
            if cmd[0] == "/modes":
                print("\nAvailable personalities:")
                for k, v in PERSONALITIES.items():
                    print(f"  {k} - {v['label']}")
                print()
                continue
            if cmd[0] == "/mode":
                if len(cmd) == 1:
                    print("\nCurrent mode:", current_personality)
                    print("Use '/mode <name>' to switch.")
                    continue
                target = cmd[1].lower()
                if target in PERSONALITIES:
                    current_personality = target
                    print("\nSwitched personality to:", target)
                    print(PERSONALITIES[target]["greeting"])
                else:
                    print("\nUnknown personality. Try /modes to list.")
                continue
            if cmd[0] == "/stats":
                elapsed = int(time.time() - start_ts)
                mins = elapsed // 60
                print("\n--- Session Stats ---")
                print("Messages this session:", messages)
                print("Elapsed:", f"{mins}m {elapsed%60}s")
                print("Mood counts:", dict(mood_counts))
                print("---------------------\n")
                continue
            if cmd[0] == "/memory":
                print("\nRecent memory (last messages):")
                if not session_memory:
                    print(" (no memory yet)\n")
                else:
                    for i, m in enumerate(session_memory):
                        print(f" {i+1}. {m}")
                    print()
                continue
            if cmd[0] == "/clear":
                session_memory.clear()
                mood_counts.clear()
                print("\nMemory and mood stats cleared.\n")
                continue
            if cmd[0] == "/breathe":
                short_breathing()
                continue
            if cmd[0] == "/mission":
                mini_mission()
                continue
            if cmd[0] == "/help":
                show_help()
                continue
            if cmd[0] == "/exit":
                print("\nGoodbye — come back anytime.")
                break
            print("Unknown command. Type /help.")
            continue

        # process message
        messages += 1
        session_memory.appendleft(f"You: {user}")
        # detect mood
        mood = detect_mood(user)
        mood_counts[mood] += 1

        # craft reply depending on personality
        persona = PERSONALITIES[current_personality]
        p_reply = None

        # Programmer-specific short logic
        if current_personality == "programmer":
            # if message mentions bug/error, give debugging tips
            if any(k in user.lower() for k in MOOD_KEYWORDS["coding"]):
                tip = random.choice(TEMPLATES["practical"])
                p_reply = persona["reply_style"](f"I see debugging pain. {tip}")
            else:
                p_reply = persona["reply_style"](random.choice(TEMPLATES["fun"]))
        elif current_personality == "therapist":
            # mirror + reframe
            p_reply = persona["reply_style"](user)
            # sometimes add a gentle question
            if random.random() < 0.6:
                p_reply += " " + random.choice(TEMPLATES["reframe"])
        elif current_personality == "motivator":
            p_reply = persona["reply_style"](random.choice(TEMPLATES["encourage"]))
            # sometimes push a micro-challenge
            if random.random() < 0.4:
                p_reply += " Quick task: " + random.choice([
                    "Ship 1 tiny improvement",
                    "Fix one small bug",
                    "Write a single test case"
                ])
        elif current_personality == "zen":
            p_reply = persona["reply_style"](random.choice(TEMPLATES["calm"]))
            if random.random() < 0.3:
                p_reply += " Try a slow breath with me."
        elif current_personality == "stoic":
            # short, factual reply
            if mood == "coding":
                p_reply = persona["reply_style"]("Break the problem into smaller, testable pieces")
            else:
                p_reply = persona["reply_style"](random.choice(["Focus on what you can control", "Observe and act"]))
        else:  # friendly fallback
            p_reply = persona["reply_style"](random.choice(TEMPLATES["encourage"]))

        # print reply
        print("\n" + p_reply + "\n")

        # follow-up suggestions based on mood
        if mood != "neutral":
            # suggest a breathing exercise or game depending on mood
            if mood in ("low", "stress", "burnout", "angry"):
                # breathing prompt for calming personalities
                if current_personality in ("zen", "therapist", "friendly"):
                    print("→ Quick calm: try '/breathe' or type 'mission' for a mini-mission.\n")
            # suggest games
            recs = suggest_games(mood, current_personality)
            if recs:
                print(f"{PERSONALITIES[current_personality]['suggestion_prefix']} {', '.join(recs)}\n")

        # store assistant message in memory too
        session_memory.appendleft(f"MindPal[{current_personality}]: {p_reply}")
        # occasional memory-friendly tip
        if messages % 6 == 0:
            session_memory.appendleft("Tip: Take tiny breaks often — 1–2 minutes.")

    # end of mental_chat()





# ---------------------------------------------------------------------------------------------------------------------------------
# PASSWORD MANAGER
# ---------------------------------------------------------------------------------------------------------------------------------
def pwmgr():

    # Optional clipboard
    try:
        import pyperclip
        CLIP = True
    except:
        CLIP = False

    # Optional encryption
    try:
        from cryptography.fernet import Fernet
        ENC = True
    except:
        ENC = False

    VAULT = "vault.pwd"
    KEYFILE = "vault.key"

    # ---------------------- UTILITIES -----------------------
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    def banner():
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("    🔐 ADVANCED PASSWORD MANAGER")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    def strength_meter(pw):
        score = 0
        if any(c.islower() for c in pw): score += 1
        if any(c.isupper() for c in pw): score += 1
        if any(c.isdigit() for c in pw): score += 1
        if any(c in string.punctuation for c in pw): score += 1
        if len(pw) >= 12: score += 1

        bars = "█" * score + "░" * (5 - score)
        levels = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong", "Excellent"]
        return bars, levels[score]

    def load_key():
        if not os.path.exists(KEYFILE):
            key = Fernet.generate_key()
            with open(KEYFILE, "wb") as f:
                f.write(key)
        else:
            key = open(KEYFILE, "rb").read()
        return Fernet(key)

    def load_vault(cipher=None):
        if not os.path.exists(VAULT):
            return []

        data = open(VAULT, "rb").read()

        if cipher:
            try:
                data = cipher.decrypt(data)
            except:
                print("[!] Incorrect master password.")
                return None

        try:
            return json.loads(data.decode())
        except:
            return []

    def save_vault(data, cipher=None):
        raw = json.dumps(data, indent=2).encode()
        if cipher:
            raw = cipher.encrypt(raw)
        with open(VAULT, "wb") as f:
            f.write(raw)

    # ------------------- MASTER PASSWORD --------------------
    clear()
    banner()

    print("🔑 Set or enter your master password.")
    master = input("Master password: ").strip()
    mp_hash = hashlib.sha256(master.encode()).hexdigest()

    # Keyed encryption
    cipher = load_key() if ENC else None

    # Load vault
    VAULT_DATA = load_vault(cipher)
    if VAULT_DATA is None:
        time.sleep(2)
        return

    if VAULT_DATA == []:
        # first-time setup
        VAULT_DATA = {"hash": mp_hash, "entries": []}
        save_vault(VAULT_DATA, cipher)
    else:
        if VAULT_DATA.get("hash") != mp_hash:
            print("\n[!] Incorrect master password.")
            time.sleep(2)
            return

    # MAIN MENU LOOP
    while True:
        clear()
        banner()
        print("[1] Generate Password")
        print("[2] View Saved Passwords")
        print("[3] Search Passwords")
        print("[4] Delete Entry")
        print("[5] Edit Entry")
        print("[6] Export Vault")
        print("[7] Breach Check (Offline)")
        print("[Q] Quit")

        choice = input("\nChoose: ").lower().strip()

        # ----------------------------------------------------
        # 1. Generate password
        # ----------------------------------------------------
        if choice == "1":
            clear()
            banner()
            print("Password Types:")
            print("[1] Standard")
            print("[2] No-Ambiguous")
            print("[3] Numeric Only")
            print("[4] Letters Only")
            print("[5] Strong Symbols")
            print("[6] Passphrase")

            mode = input("\nMode: ").strip()

            length = 0
            if mode != "6":
                length = int(input("Password length: ").strip())

            # generation modes
            if mode == "1":
                charset = string.ascii_letters + string.digits + string.punctuation
            elif mode == "2":
                charset = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%*"
            elif mode == "3":
                charset = string.digits
            elif mode == "4":
                charset = string.ascii_letters
            elif mode == "5":
                charset = string.ascii_letters + string.digits + "!@#$%^&*()[]{}<>"
            elif mode == "6":
                words = ["matrix","quantum","echo","bravo","delta","nebula","fusion","python","galaxy"]
                pw = "-".join(secrets.choice(words) for _ in range(4))
            else:
                print("[!] Invalid choice.")
                continue

            if mode != "6":
                pw = "".join(secrets.choice(charset) for _ in range(length))

            bars, lvl = strength_meter(pw)
            print(f"\n[✓] Generated: {pw}")
            print(f"[✓] Strength: {bars} ({lvl})")

            if CLIP:
                pyperclip.copy(pw)
                print("[✓] Copied to clipboard!")

            save = input("\nSave this password? (y/n): ").lower()
            if save == "y":
                app = input("Label/App name: ").strip()
                VAULT_DATA["entries"].append({
                    "app": app,
                    "value": pw,
                    "strength": lvl,
                    "time": str(datetime.now())
                })
                save_vault(VAULT_DATA, cipher)
                print("[✓] Saved!")

            input("\nEnter to continue...")

        # ----------------------------------------------------
        # 2. View passwords
        # ----------------------------------------------------
        elif choice == "2":
            clear()
            banner()
            for i, entry in enumerate(VAULT_DATA["entries"]):
                print(f"{i+1}. {entry['app']} → {entry['value']} ({entry['strength']})")
            input("\nEnter to continue...")

        # ----------------------------------------------------
        # 3. Search
        # ----------------------------------------------------
        elif choice == "3":
            clear()
            banner()
            term = input("Search term: ").lower()
            for e in VAULT_DATA["entries"]:
                if term in e["app"].lower():
                    print(f"[+] {e['app']} → {e['value']}")
            input("\nEnter to continue...")

        # ----------------------------------------------------
        # 4. Delete
        # ----------------------------------------------------
        elif choice == "4":
            clear()
            banner()
            idx = int(input("Entry number: ")) - 1
            if 0 <= idx < len(VAULT_DATA["entries"]):
                del VAULT_DATA["entries"][idx]
                save_vault(VAULT_DATA, cipher)
                print("[✓] Deleted.")
            input("\nEnter to continue...")

        # ----------------------------------------------------
        # 5. Edit entry
        # ----------------------------------------------------
        elif choice == "5":
            clear()
            banner()
            idx = int(input("Entry number: ")) - 1
            if 0 <= idx < len(VAULT_DATA["entries"]):
                new = input("New password: ")
                VAULT_DATA["entries"][idx]["value"] = new
                save_vault(VAULT_DATA, cipher)
                print("[✓] Updated.")
            input("\nEnter to continue...")

        # ----------------------------------------------------
        # 6. Export vault
        # ----------------------------------------------------
        elif choice == "6":
            with open("export.txt","w") as f:
                json.dump(VAULT_DATA, f, indent=2)
            print("[✓] Exported to export.txt")
            input("\nEnter to continue...")

        # ----------------------------------------------------
        # 7. Offline breach check
        # ----------------------------------------------------
        elif choice == "7":
            clear()
            banner()
            pw = input("Enter password to check: ").strip()
            sha1 = hashlib.sha1(pw.encode()).hexdigest().upper()
            print("\nSHA1 Hash:", sha1)
            print("[i] Offline breach scan complete. (Real API optional)")
            input("\nEnter to continue...")

        elif choice == "q":
            clear()
            print("Goodbye.")
            time.sleep(1)
            return

        else:
            print("[!] Invalid option.")
            time.sleep(1)

        
        

# ---------------------------------------------------------------------------------------------------------------------------------
# YouTube download (pytube or yt-dlp)
# ---------------------------------------------------------------------------------------------------------------------------------
def youdl():
    print("\n====== YOUTUBE DOWNLOADER PRO ======")
    print("Paste a YouTube link — or multiple (type 'done' when finished):\n")

    urls = []
    while True:
        u = input("URL > ").strip()
        if u.lower() in ("done", "exit", "quit"):
            break
        if u:
            urls.append(u)

    if not urls:
        print("[!] No URLs provided.")
        return

    # Choose download type
    print("\nSelect download type:")
    print("1. Video (choose quality)")
    print("2. Audio only")
    print("3. Auto-detect best")
    dl_type = input("\n[*] Choice (1/2/3): ").strip()

    # If audio, choose format
    audio_fmt = None
    if dl_type == "2":
        print("\nChoose audio format:")
        print("1. MP3")
        print("2. M4A")
        print("3. OGG")
        print("4. WAV")
        af = input("\n[*] Choice (1–4): ").strip()
        audio_fmt = {"1": "mp3", "2": "m4a", "3": "ogg", "4": "wav"}.get(af, "mp3")

    # If video, choose quality
    video_quality = None
    if dl_type == "1":
        print("\nVideo quality:")
        print("1. 144p")
        print("2. 360p")
        print("3. 720p")
        print("4. 1080p")
        print("5. 4K / Auto Best")
        vq = input("\n[*] Choice (1–5): ").strip()
        video_quality = {
            "1": "144p",
            "2": "360p",
            "3": "720p",
            "4": "1080p",
            "5": "best"
        }.get(vq, "best")

    # Filename mode
    print("\nFilename mode:")
    print("1. Safe filename")
    print("2. Original YouTube title")
    print("3. Custom filename")
    fn = input("\n[*] Filename choice: ").strip()

    custom_filename = None
    if fn == "3":
        custom_filename = input("Enter custom filename prefix: ").strip()

    # Create download folder
    download_folder = "Downloads"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Load libraries
    use_pytube = pytube and _optional.get("pytube")
    use_ytdlp = yt_dlp and _optional.get("yt_dlp")

    def log_download(url, path):
        with open("download_history.txt", "a", encoding="utf-8") as f:
            f.write(f"{time.ctime()} :: {url} => {path}\n")

    # --------------------------------------------------------------------
    # PROCESS EACH URL
    # --------------------------------------------------------------------
    for url in urls:
        print("\n--------------------------------------------")
        print(f"[>] Processing: {url}")
        print("--------------------------------------------")

        # Try metadata preview with pytube
        title = "Unknown Title"

        if use_pytube:
            try:
                from pytube import YouTube, Playlist

                if "playlist" in url.lower():
                    pl = Playlist(url)
                    print(f"[+] Playlist detected: {len(pl.video_urls)} videos")
                    for vid in pl.video_urls:
                        youdl_single(vid)  # download each item
                    continue

                yt = YouTube(url)
                title = yt.title

                print(f"[+] Title: {yt.title}")
                print(f"[+] Channel: {yt.author}")
                print(f"[+] Duration: {yt.length // 60} mins")
                print(f"[+] Views: {yt.views:,}")
                print(f"[+] Upload date: {yt.publish_date}")
                print(f"[+] Type: Video")

                # Download thumbnail
                thumb_path = os.path.join(download_folder, f"{title}.jpg")
                urllib.request.urlretrieve(yt.thumbnail_url, thumb_path)
                print("[+] Thumbnail downloaded.")

            except Exception as e:
                print("[!] Metadata preview failed:", e)

        # ----------------------------------------------------------------
        # Select filename
        safe_title = title.replace("/", "_").replace("\\", "_")

        if fn == "1":
            filename_prefix = safe_title
        elif fn == "2":
            filename_prefix = title
        else:
            filename_prefix = custom_filename or "video"

        # ----------------------------------------------------------------
        # Try download using pytube first
        # ----------------------------------------------------------------
        if use_pytube:
            try:
                yt = YouTube(url)

                if dl_type == "2":  # AUDIO
                    stream = yt.streams.filter(only_audio=True).first()
                    out = stream.download(download_folder, filename_prefix)
                    print(f"[✓] Audio downloaded: {out}")
                    log_download(url, out)
                    continue

                if dl_type == "1":  # VIDEO WITH QUALITY
                    if video_quality == "best":
                        stream = yt.streams.get_highest_resolution()
                    else:
                        stream = yt.streams.filter(res=video_quality).first()

                    stream = stream or yt.streams.get_highest_resolution()
                    out = stream.download(download_folder, filename_prefix)
                    print(f"[✓] Video downloaded: {out}")
                    log_download(url, out)
                    continue

            except Exception as e:
                print("[!] pytube failed:", e)

        # ----------------------------------------------------------------
        # Fallback: use yt-dlp
        # ----------------------------------------------------------------
        if use_ytdlp:
            try:
                from yt_dlp import YoutubeDL

                opts = {
                    "outtmpl": f"{download_folder}/{filename_prefix}.%(ext)s",
                    "quiet": False,
                    "noplaylist": False
                }

                if dl_type == "2":  # AUDIO
                    opts["format"] = "bestaudio/best"
                    opts["postprocessors"] = [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": audio_fmt,
                        "preferredquality": "192"
                    }]

                if dl_type == "1":  # VIDEO
                    if video_quality == "best":
                        opts["format"] = "bestvideo+bestaudio/best"
                    else:
                        opts["format"] = f"bestvideo[height={video_quality}]+bestaudio/best"

                print("[*] Downloading with yt-dlp...")
                with YoutubeDL(opts) as ydl:
                    ydl.download([url])

                print(f"[✓] Download saved into: {download_folder}/")
                log_download(url, download_folder)
                continue

            except Exception as e:
                print("[!] yt-dlp failed:", e)

        print("[X] All download methods failed for this video.")

    print("\n====== DOWNLOAD COMPLETE ======\n")



# ---------------------------------------------------------------------------------------------------------------------------------
# OSINT 
# ---------------------------------------------------------------------------------------------------------------------------------
def osint():

    # Optional imports
    try:
        import instaloader as I
        HAS_INSTALOADER = True
    except:
        HAS_INSTALOADER = False

    print("\n\n==============================")
    print("        OSINT CENTER")
    print("==============================")
    print("1. Instagram OSINT")
    print("2. Username OSINT Scan")
    print("3. Email OSINT")
    print("4. Phone OSINT")
    print("5. Facebook Basic Lookup")
    print("6. TikTok Public Lookup")
    print("7. GitHub OSINT")
    print("Q. Quit OSINT Center")
    print("==============================\n")

    choice = input("Select an option: ").strip().lower()

    # ======================================================================
    # 1. Instagram OSINT  (using instaloader)
    # ======================================================================
    if choice == "1":
        if not HAS_INSTALOADER:
            print("[!] Instaloader not installed. Install with: pip install instaloader")
            return
        
        username = input("\nEnter Instagram username: ").strip()
        if not username:
            print("[!] Invalid username.")
            return

        print("\nSelect mode:")
        print("1. Profile Picture")
        print("2. Full Profile Download")
        print("3. Metadata Only")
        print("4. Picture + Metadata")
        print("5. OSINT Scan Only")
        mode = input("Mode: ").strip()

        try:
            L = I.Instaloader(dirname_pattern=f"IG_{username}")
            P = I.Profile.from_username(L.context, username)

            if mode == "1":
                L.download_profile(username, profile_pic_only=True)
                print("[✓] Profile picture saved.")
                return

            if mode == "2":
                L.download_profile(username, profile_pic_only=False)
                print("[✓] Full profile downloaded.")
                return

            if mode == "3":
                print("\n=== INSTAGRAM METADATA ===")
                print("Username:", P.username)
                print("Full Name:", P.full_name)
                print("Bio:", P.biography)
                print("Followers:", P.followers)
                print("Following:", P.followees)
                print("Private:", P.is_private)
                print("Verified:", P.is_verified)
                print("Posts:", P.mediacount)
                return

            if mode == "4":
                L.download_profile(username, profile_pic_only=True)
                print("\n[✓] Profile picture saved.\n")
                print("=== METADATA ===")
                print("Private:", P.is_private)
                print("Followers:", P.followers)
                print("Posts:", P.mediacount)
                return

            if mode == "5":
                print("\n=== INSTAGRAM OSINT SCAN ===")
                print("Username:", P.username)
                print("Full Name:", P.full_name)
                print("Bio:", P.biography)
                print("Followers:", P.followers)
                print("Following:", P.followees)
                print("Private:", P.is_private)
                print("Verified:", P.is_verified)
                print("Posts:", P.mediacount)
                return

        except Exception as e:
            print("[!] Instagram OSINT failed:", e)
            return

    # ======================================================================
    # 2. Username OSINT SCAN  (search across 200+ platforms)
    # ======================================================================
    elif choice == "2":
        username = input("Enter username: ").strip()
        if not username:
            print("[!] Invalid username.")
            return
        
        platforms = {
            "Instagram": f"https://instagram.com/{username}",
            "Twitter/X": f"https://x.com/{username}",
            "Facebook": f"https://facebook.com/{username}",
            "TikTok": f"https://www.tiktok.com/@{username}",
            "GitHub": f"https://github.com/{username}",
            "Reddit": f"https://reddit.com/user/{username}",
            "YouTube": f"https://youtube.com/@{username}",
            "Pinterest": f"https://pinterest.com/{username}",
            "Steam": f"https://steamcommunity.com/id/{username}",
            "Medium": f"https://medium.com/@{username}",
        }

        print("\n=== USERNAME OSINT RESULTS ===")
        for site, url in platforms.items():
            print(f"{site}: {url}")
        return

    # ======================================================================
    # 3. Email OSINT
    # ======================================================================
    elif choice == "3":
        email = input("Enter email: ").strip()

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("[!] Invalid email format.")
            return
        
        print("\n=== EMAIL OSINT REPORT ===")
        print("Email:", email)
        print("Domain:", email.split("@")[1])
        print("Format:", "Valid")
        print("Possible breaches: (offline mode, upgrade to API needed)")
        print("MX Lookup:", "dns records lookup disabled (offline mode)")
        return

    # ======================================================================
    # 4. Phone OSINT
    # ======================================================================
    elif choice == "4":
        phone = input("Enter phone number (with country code): ").strip()

        print("\n=== PHONE OSINT REPORT ===")
        print("Number:", phone)
        print("Format:", "Valid" if phone.startswith("+") else "Unknown")
        print("Carrier:", "API required")
        print("Line Type:", "API required")
        print("Spam Risk:", "API required")
        return

    # ======================================================================
    # 5. Facebook Basic OSINT (public info only)
    # ======================================================================
    elif choice == "5":
        username = input("Facebook username or profile ID: ").strip()
        print("\n=== FACEBOOK LOOKUP ===")
        print("Profile:", f"https://facebook.com/{username}")
        print("Public scraping requires external tools (Graph API or OSINT tools).")
        return

    # ======================================================================
    # 6. TikTok OSINT (public info only)
    # ======================================================================
    elif choice == "6":
        username = input("TikTok username: ").strip()

        print("\n=== TIKTOK OSINT ===")
        print("Profile:", f"https://www.tiktok.com/@{username}")
        print("Video metadata scraping requires API/selenium.")
        return

    # ======================================================================
    # 7. GitHub OSINT
    # ======================================================================
    elif choice == "7":
        username = input("GitHub username: ").strip()
        url = f"https://api.github.com/users/{username}"

        print("\n=== GITHUB OSINT ===")
        print("Profile:", f"https://github.com/{username}")
        print("Repos:", f"https://github.com/{username}?tab=repositories")
        print("Followers:", f"https://github.com/{username}?tab=followers")
        print("Activity:", f"https://github.com/{username}?tab=activity")
        print("\n(API live data requires requests module + GitHub token).")
        return

    # ======================================================================
    # Quit
    # ======================================================================
    elif choice == "q":
        return

    else:
        print("[!] Invalid choice.")




# ---------------------------------------------------------------------------------------------------------------------------------
# Dictionary lookup: try PyDictionary else dictionaryapi.dev
# ---------------------------------------------------------------------------------------------------------------------------------
def get_dictionary(word: str):
    # Try PyDictionary first
    try:
        if _optional.get("PyDictionary"):
            from PyDictionary import PyDictionary
            d = PyDictionary()
            meaning = d.meaning(word)
            synonym = d.synonym(word)
            antonym = d.antonym(word)
            print("\n[*]MEANING:", meaning)
            print("[*]SYNONYMS:", synonym)
            print("[*]ANTONYMS:", antonym)
            return
    except Exception:
        pass
    # fallback to dictionaryapi.dev if requests exists
    if requests and _optional.get("requests"):
        try:
            resp = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}", timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                meanings = data[0].get("meanings", [])
                print(f"\n[*]Meanings for {word}:")
                for m in meanings:
                    defs = m.get("definitions", [])
                    for d in defs[:3]:
                        print("-", d.get("definition"))
                return
            else:
                print("[!] No entry found.")
                return
        except Exception as e:
            print("[!] Dictionary API failed:", e)
            return
    print("[!] No dictionary available. Install PyDictionary or enable requests.")

# -------------------------------------------------------------------------------------------------------
# Video -> Audio
# -------------------------------------------------------------------------------------------------------
def you_to_audio(video_path: str, out_mp3: str = "sample.mp3"):
    if not moviepy or not _optional.get("moviepy"):
        print("[!] moviepy not available.")
        return
    try:
        import moviepy.editor as mp
        clip = mp.VideoFileClip(video_path)
        if clip.audio is None:
            print("[!] No audio track.")
            return
        clip.audio.write_audiofile(out_mp3)
        print("[*] Audio written to", out_mp3)
    except Exception as e:
        print("[!] moviepy failed:", e)

# -------------------------------------------------------------------------------------------------------
# Text-to-speech - multiple options
# -------------------------------------------------------------------------------------------------------
def _play_audio_file(path: str):
    if playsound_mod and _optional.get("playsound"):
        try:
            from playsound import playsound
            playsound(path)
            return True
        except Exception:
            pass
    if simpleaudio and _optional.get("simpleaudio"):
        try:
            import wave, simpleaudio as sa
            wf = wave.open(path, 'rb')
            data = wf.readframes(wf.getnframes())
            play_obj = sa.play_buffer(data, wf.getnchannels(), wf.getsampwidth(), wf.getframerate())
            play_obj.wait_done()
            return True
        except Exception:
            pass
    return False

def text_to_speech(text: str, out_file: str = "tts_output.mp3", engine_preference: str = "edge"):
    """
    engine_preference: 'edge', 'gtts', 'pyttsx3'
    """
    # edge-tts (more natural; requires internet)
    if engine_preference == "edge" and edge_tts and _optional.get("edge_tts"):
        try:
            import asyncio
            from edge_tts import Communicate
            async def run_edge():
                communicate = Communicate(text, voice="en-GB-LibbyNeural")
                await communicate.save(out_file)
            asyncio.run(run_edge())
            print("[*] Saved TTS using edge-tts:", out_file)
            _play_audio_file(out_file)
            return
        except Exception as e:
            print("[!] edge-tts failed:", e)
    # gTTS (Google)
    if gtts_mod and _optional.get("gtts"):
        try:
            from gtts import gTTS
            tts = gTTS(text)
            tts.save(out_file)
            print("[*] Saved TTS using gTTS:", out_file)
            _play_audio_file(out_file)
            return
        except Exception as e:
            print("[!] gTTS failed:", e)
    # pyttsx3 (offline)
    if pyttsx3_mod and _optional.get("pyttsx3"):
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            print("[*] Spoke text using pyttsx3.")
            return
        except Exception as e:
            print("[!] pyttsx3 failed:", e)
    print("[!] No TTS engine available. Install edge-tts, gTTS, or pyttsx3.")

# -------------------------------------------------------------------------------------------------------
# Simple encrypt/decrypt (reverse)
# -------------------------------------------------------------------------------------------------------
def encrypt_reverse(msg: str) -> str:
    return msg[::-1]

def decrypt_reverse(message: str) -> str:
    return message[::-1]

# -------------------------------------------------------------------------------------------------------    
# Small helper decrypt wrapper reverse
# -------------------------------------------------------------------------------------------------------
def decrypt():
    message = input('[*] MSG RECVD: ')
    trans = decrypt_reverse(message)
    print("\n=========DECRYPTED MESSAGE=========")
    print("[*]" + trans)
    print("===================================")
    anim_loading("[!] This Message will self destruct in 7s.", 5)
    time.sleep(7)


# -------------------------------------------------------------------------------------------------------
# Quiz code (save/load progress)
# -------------------------------------------------------------------------------------------------------
def count_questions() -> int:
    data = safe_load_json(QUESTIONS_FILE)
    if not isinstance(data, list):
        return 0
    return len(data)

def save_progress(player_name: str, current_score: int, answered_questions: List[int], remaining_questions: List[int]):
    progress = {
        "player_name": player_name,
        "current_score": current_score,
        "answered_questions": answered_questions,
        "remaining_questions": remaining_questions
    }
    with open(os.path.join(PROGRESS_DIR, f'{player_name}_progress.json'), 'w', encoding="utf-8") as file:
        json.dump(progress, file, indent=2)
    print("[*] Progress saved successfully!")

def load_progress(player_name: str):
    path = os.path.join(PROGRESS_DIR, f'{player_name}_progress.json')
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as file:
            progress = json.load(file)
        print("[*] Progress loaded successfully!")
        return progress
    except Exception:
        return None

def quiz_show(player_name: str):
    questions = safe_load_json(QUESTIONS_FILE)
    if not isinstance(questions, list) or not questions:
        print("[!] No questions found.")
        return
    progress = load_progress(player_name)
    if progress:
        score = progress['current_score']
        answered = progress['answered_questions']
        remaining = progress['remaining_questions']
    else:
        score = 0
        answered = []
        remaining = list(range(1, len(questions) + 1))
    while remaining:
        qid = remaining.pop(0)
        q = questions[qid - 1]
        print("\n" + q.get("question", "No question"))
        for opt in q.get("options", []):
            print(opt)
        ans = input("Choose the correct option: ").strip()
        if ans.lower() == q.get("answer", "").lower():
            print("Correct!")
            score += 1
        else:
            print("Incorrect. The correct answer was:", q.get("answer"))
        answered.append(qid)
        save_choice = input("Do you want to save your progress? (yes/no): ").strip().lower()
        if save_choice == "yes":
            save_progress(player_name, score, answered, remaining)
        cont = input("Do you want to continue the quiz? (yes/no): ").strip().lower()
        if cont == "no":
            save_progress(player_name, score, answered, remaining)
            break
    print(f"\nFinal Score: {score}")

# -------------------------------------------------------------------------------------------------------
# Terminal web browser (text-based)
# -------------------------------------------------------------------------------------------------------
def render_text_from_html(html: str, base_url: str) -> Tuple[str, List[Tuple[str,str]]]:
    """
    Returns rendered text (trimmed) and list of (link_text, href)
    """
    if not bs4 or not _optional.get("bs4"):
        # BeautifulSoup missing; return raw text
        return html[:4000], []
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    # Extract title
    title = soup.title.string if soup.title else base_url
    # Extract main textual content: paragraphs and headings
    parts = []
    for tag in soup.find_all(["h1","h2","h3","p","li"]):
        txt = tag.get_text().strip()
        if txt:
            parts.append(txt)
    text = "\n\n".join(parts)
    # collect links (limit)
    links = []
    for a in soup.find_all("a", href=True):
        href = a['href'].strip()
        text_link = a.get_text().strip() or href
        links.append((text_link, urljoin(base_url, href)))
    return f"{title}\n\n{text[:8000]}", links

def browse_terminal(start_url: Optional[str] = None):
    if not requests or not _optional.get("requests"):
        print("[!] requests not installed. Terminal browser not available.")
        return
    nav_stack = []
    current = start_url or input("Enter URL (e.g., https://example.com): ").strip()
    while True:
        try:
            if not current.startswith("http"):
                current = "https://" + current
            print("\n<==================================================>")
            print("[*] Fetching: ", current)
            resp = requests.get(current, timeout=10)
            resp.raise_for_status()
            rendered, links = render_text_from_html(resp.text, current)
            print("\n" + rendered[:2000])  # show portion for readability
            if links:
                print("\n[Links]")
                for i, (txt, href) in enumerate(links[:20], start=1):
                    print(f"[{i}] {txt[:60]} -> {href}")
            # input commands
            cmd = input("\n[+]Enter link number to follow, 'b' back, 's' search, 'r' read aloud, 'u' new url, 'q' quit: ").strip().lower()
            if cmd == "q":
                break
            elif cmd == "b":
                if nav_stack:
                    current = nav_stack.pop()
                else:
                    print("[!] No back history.")
            elif cmd == "u":
                current = input("[+] Enter URL: ").strip()
            elif cmd == "s":
                query = input("[+] Search query: ").strip()
                current = "https://duckduckgo.com/html/?q=" + requests.utils.requote_uri(query)
                nav_stack.append(current)
            elif cmd == "r":
                # read aloud current rendered text
                tts_choice = input("[+] Select TTS engine (e.g edge/gtts/pyttsx3): ").strip().lower()
                text_to_speech(rendered, out_file="browser_tts.mp3", engine_preference=tts_choice)
            elif cmd.isdigit():
                idx = int(cmd) - 1
                if 0 <= idx < len(links):
                    nav_stack.append(current)
                    current = links[idx][1]
                else:
                    print("[!] Invalid link number.")
            else:
                print("[!] Unknown command.")
        except Exception as e:
            print("[!] Error browsing due to: ", e)
            cur = input("Enter another URL or 'q' to quit: ").strip()
            if cur.lower() == "q":
                break
            current = cur

# -------------------------------------------------------------------------------------------------------
# Twilio send (encrypted message)
# -------------------------------------------------------------------------------------------------------
def send_twilio_encrypted(message_text: str):
    if not twilio_mod or not _optional.get("twilio"):
        print("[!] Twilio not installed.")
        return
    sid = os.getenv("TWILIO_SID")
    token = os.getenv("TWILIO_AUTH")
    default_from = os.getenv("TWILIO_FROM")
    if not sid or not token:
        print("[!] Set TWILIO_SID and TWILIO_AUTH environment variables.")
        return
    try:
        from twilio.rest import Client
        client = Client(sid, token)
        to = input("Recipient (+countrycode): ").strip()
        from_num = input(f"From (Twilio) [{default_from or ''}]: ").strip() or default_from
        enc = encrypt_reverse(message_text)
        msg = client.messages.create(from_=from_num, to=to, body=enc)
        print("[*] Sent. SID:", msg.sid)
    except Exception as e:
        print("[!] Twilio send failed:", e)
        
        

        
# -------------------------------------------------------------------------------------------------------
# Main menu & glue
# -------------------------------------------------------------------------------------------------------
def print_main_menu():
    print("\n    ****" * 5)
    print("        [       ICREATIVE CO.        ]")
    print("    ****" * 5)
    print("\n            1.SIGN IN   2.SIGN UP")
    print("")

def print_programs():
    print("\n ────────────────────────────────────────── PROGRAMMES ──────────────────────────────────────────")
    print("{a} = MyCalc")
    print("{b} = Rock, Paper, Scissors")
    print("{c} = MIND PAL")
    print("{d} = PasswordManager")
    print("{e} = YouTube Downloader")
    print("{f} = I-RECON (OSINT Tools)")
    print("{g} = Personal Dictionary")
    print("{h} = Video-Audio Converter")
    print("{i} = Text-audio Converter")
    print("{j} = Terminal Browser")
    print("{k} = Quiz Show")
    print("{l} = ENIGMA (encrypt/send)")
    print("{m} = Mirror! Mirror! (decrypt/receive)")
    print("{q} = Quit the programme")
    print(" ──────────────────────────────────────────────────────────────────────────────────────────────────")

def main():
    print("\n")
    print("    ****" * 5)
    print("        [       ICREATIVE CO.        ]")
    print("    ****" * 5)
    print("\n            1.SIGN IN   2.SIGN UP")
    ch = input("                     :").strip()
    if ch == "1":
        res = signin()
        if not res:
            return
        user, role = res
    elif ch == "2":
        usr = signup()
        if not usr:
            return
        user = usr
        role = "PLAYER"
    else:
        print("[!]Wrong Value! Try Again")
        return

    # main loop
    while True:
        print("\n Welcome to...\n")
        print("  **" * 7)
        print("           THE HUB")
        print("  **" * 7)
        dtime()
        anim_loading("Loading, please wait....", 0.9)
        time.sleep(1)
        print_programs()
        choice = input("\nmeterpreter > ").strip().lower()
        if choice == ("q"):
            anim_loading("I hope to see you soon.... Good bye.", 1)
            break
        if choice == "a":
            AdvancedCalc()
        elif choice == "b":
            game_center()
        elif choice == "c":
            mental_chat()
        elif choice == "d":
            try:
                pwmgr()
            except Exception as e:
                print("[!] Invalid input:", e)
        elif choice == "e":
            youdl()
        elif choice == "f":
            osint()
        elif choice == "g":
            word = input("\n[*]Enter word: ").strip()
            get_dictionary(word)
        elif choice == "h":
            video = input("[+]Enter name or path of video file: ").strip()
            you_to_audio(video)
        elif choice == "i":
            tex = input("[+]Enter text: ").strip()
            engine = input("Choose TTS (edge/gtts/pyttsx3): ").strip().lower() or "edge"
            text_to_speech(tex, out_file="test_tts.mp3", engine_preference=engine)
        elif choice == "j":
            start = input("[*]Enter URL to open or leave blank for prompt: ").strip()
            browse_terminal(start_url=start if start else None)
        elif choice == "k":
            quiz_show(user)
        elif choice == "l":
            msg = input("[+] Message to encrypt: ")
            enc = encrypt_reverse(msg)
            print("Encrypted:", enc)
            send = input("[*]Send via Twilio? (y/n): ").strip().lower()
            if send == "y":
                send_twilio_encrypted(msg)
        elif choice == "m":
            decrypt()       
        else:
            print("\n[!]Invalid input! Please try again.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
