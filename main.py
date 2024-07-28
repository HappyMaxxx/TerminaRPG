import sys
import os
import tty
import termios
import time
import random
from pyfiglet import Figlet
import pickle

import texts

import colorama
colorama.init()

class Settings:
    def __init__(self):
        self.language = 'en'

    def save(self):
        with open("settings.pkl", 'wb') as f:
            pickle.dump(self, f)


class Menu:
    def __init__(self):
        try:
            with open("settings.pkl", 'rb') as f:
                self.sett = pickle.load(f)
        except FileNotFoundError:
            self.sett = Settings()

    @staticmethod
    def settings_menu(self):
        while True:
            Menu.clear()
            for i in texts.settings(self.sett.language):
                print(i)

            print("> ", end='')
            choice = Menu.get_char()
            if choice == '1':
                if self.sett.language == 'ua':
                    self.sett.language = 'en'
                else:
                    self.sett.language = 'ua'
                self.sett.save()
                if isinstance(self, Game):
                    self.sett = Menu.load_set()

            elif choice == '2':
                pass

            elif choice == '0':
                self.sett.save()
                break

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    def start_new_game(self):
        global curent_time, gamemode, process, mapp, heroe, inventar, game

        curent_time = Time(hours = 8)
        gamemode = Gamemode()
        process = Processmode()
        mapp = Map()
        heroe = Heroe(mapp = mapp)
        inventar = Inventory()
        game = Game(heroe, mapp, curent_time, gamemode, process, inventar, settings = self.sett)
        game.main_process()

    @staticmethod
    def write(text_list, delay):
        for row in text_list:
            for char in row:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(delay)

    def print_intro(self):
        f = Figlet(font='gothic')
        self.write((list(f.renderText('TerminaRPG'))), 0.002)
        print()

    @staticmethod
    def load_game():
        with open("gamesave.pkl", 'rb') as f:
            game = pickle.load(f)
        game.heroe.add_heroe_on_map()
        game.process.mode = 'menu'
        game.sett = Menu.load_set() 
        return game
    
    @staticmethod
    def load_set():
        with open("settings.pkl", 'rb') as f:
            return pickle.load(f)

    def show_menu(self):
        self.clear()
        self.print_intro()
        for i in texts.menu(self.sett.language):
            print(i)
        print("> ", end='')

    @staticmethod
    def dell_all():
        try:
            del curent_time
            del gamemode
            del process
            del mapp
            del heroe
            del inventar
            del game
        except:
            pass
    
    @staticmethod
    def get_char():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            char = sys.stdin.read(1)
            return char
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def start(self):
        while True:
            self.__init__()
            self.show_menu()
            choice = self.get_char()
            if choice == '1':
                self.dell_all()
                self.start_new_game()
            elif choice == '2':
                print("Loading game...")
                self.clear()
                if not os.path.exists("gamesave.pkl"):
                    print("No save file")
                    time.sleep(2)
                    self.clear()
                    continue

                self.dell_all()
                self.load_game().main_process()

            elif choice == '3':
                # TODO: how to play
                pass

            elif choice == '4':
                self.settings_menu(self)

            elif choice in ['5', '0']:
                print("Exiting...")
                break


class Game:
    def __init__(self, heroe, mapp, time, gamemode, processmode, inventory, settings):
        self.heroe = heroe
        self.mapp = mapp
        self.time = time
        self.gamemode = gamemode
        self.process = processmode
        self.inventory = inventory
        self.sett = settings
        self.enemies = []

    def save(self):
        with open("gamesave.pkl", 'wb') as f:
            pickle.dump(self, f)

    def main_process(self):
        Menu.load_set()
        while True:
            self.save()
            if self.process.mode == 'menu':
                Menu.clear()
                self.print_pause()

                print('> ', end='')
                char = self.process.get_char_map()

                if char == -1:
                    continue

                if char == '1':
                    self.process.mode = 'ingame'

                elif char == "2":
                    Menu.settings_menu(self)

                elif char == '0':
                    Menu.clear()
                    return

            elif self.process.mode == 'sett':
                pass

            else:
                if self.heroe.curent_hp <= 0:
                    Menu.clear()
                    print("Heroe is dead")
                    time.sleep(2)
                    self.process.mode = 'menu'
                    continue

                Menu.clear()
                self.time.get_daytime()

                if self.gamemode.mode == 'normal':
                    index = -1
                    self.mapp.print_map(self.heroe, self.gamemode, self.time, self.sett.language)
                    char = self.gamemode.get_char_n()

                    if char == -1:
                        continue

                    elif char == 'Esc':
                        self.save()
                        self.process.mode = 'menu'
                        continue

                    elif char in ['Up', 'Down', 'Right', 'Left']:
                        self.heroe.move(char, self.time, self)
                        if len (self.enemies) > 0:
                            for i, enemy in enumerate(self.enemies):
                                try:
                                    if enemy.is_hero_stepping_on(self.heroe):
                                        index = i
                                        self.gamemode.mode = 'fight'
                                        break
                                except ValueError:
                                    pass

                        if len(self.enemies) < 5 and self.time.get_day() >= 1:
                            if self.time.daytime == 'ніч':
                                if random.randint(0, 10) in [1, 2, 3, 4]:
                                    self.create_enemy()
                                self.create_enemy()

                            elif self.time.daytime == 'вечір':
                                if random.randint(0, 10) in [1, 2]:
                                    self.create_enemy()
                                self.create_enemy()

                        continue

                    elif char == 'C':
                        self.gamemode.mode = 'command'
                        continue

                    elif char == 'Map':
                        self.gamemode.mode = "map"
                        continue

                    elif char == "I":
                        self.gamemode.mode = "inventory"
                        continue

                elif self.gamemode.mode == 'command':
                    self.mapp.print_map(self.heroe, self.gamemode, self.time, self.sett.language)
                    print("> ", end='')
                    char = self.gamemode.get_char_c()

                    if char == -1:
                        continue

                    elif char == 'Esc':
                        self.gamemode.mode = 'normal'
                        continue

                    elif char == 'Map':
                        self.gamemode.mode = 'map'
                        continue

                    elif char == "I":
                        self.gamemode.mode = "inventory"
                        continue

                elif self.gamemode.mode == 'map':
                    self.mapp.print_full_map(self)

                    char = self.gamemode.get_char_m()

                    if char == -1:
                        continue

                    elif char == 'Esc':
                        self.gamemode.mode = 'normal'
                        continue

                    elif char == 'C':
                        self.gamemode.mode = 'command'
                        continue

                    elif char in ['Up', 'Down', 'Right', 'Left']:
                        self.mapp.move_full_map(char)
                        continue

                    elif char == "I":
                        self.gamemode.mode = "inventory"
                        continue

                elif self.gamemode.mode == 'inventory':
                    self.inventory.show_inventory()
                    print("> ", end='')
                    char = self.gamemode.get_char_i()

                    if char == -1:
                        continue

                    elif char == 'Esc':
                        self.gamemode.mode = 'normal'
                        continue

                elif self.gamemode.mode == 'fight':
                    self.fite(index)
                    index = -1

    def create_enemy(self):
        enemy = Enemy(self.mapp)
        self.enemies.append(enemy)

    def print_pause(self):
        for i in texts.paus(self.sett.language):
            print(i)
        print()

    def fite(self, index):
        while True:
            Menu.clear()
            print("Fight")

            print(f"v1mer's HP: {self.heroe.curent_hp}/{self.heroe.max_hp}")
            print(self.heroe.print_hp())
            print(f"{self.enemies[index].name} the {self.enemies[index].enemy_type} HP: {self.enemies[index].curent_hp}/{self.enemies[index].max_hp}")
            print(self.enemies[index].print_hp())
            print()
            print("1. Атакувати")
            print("2. Захиститись")
            print("3. Використати заклинання")
            print("4. Втекти")
            print("0. Вийти")
            print("> ", end='')

            time.sleep(0.1)

            char = self.gamemode.get_char_f()

            if char == -1:
                continue

            elif char == 'Esc':
                self.gamemode.mode = 'normal'
                break

            elif char == '0':
                Menu.clear()
                return

            elif char == '1':
                if self.heroe.curent_hp <= 0:
                    Menu.clear()
                    print("Heroe is dead")
                    time.sleep(2)
                    self.gamemode.mode = 'normal'
                    self.process.mode = 'menu'
                    break
                else:
                    self.heroe.atack(self.enemies[index])
                    Menu.clear()

                if self.enemies[index].curent_hp <= 0:
                    self.heroe.add_coins(self.enemies[index].generate_coin())
                    self.enemies[index].dead_enemy(game = self)
                    del self.enemies[index]
                    self.gamemode.mode = 'normal'
                    break
                else:
                    self.enemies[index].atack(self.heroe)

            elif char == '3':
                self.heroe.heal(5)

                if self.enemies[index].curent_hp <= 0:
                    self.heroe.add_coins(self.enemies[index].generate_coin())
                    self.enemies[index].dead_enemy(game = self)
                    del self.enemies[index]
                    self.gamemode.mode = 'normal'
                    break
                else:
                    self.enemies[index].atack(self.heroe)


class Entity:
    def __init__(self, max_hp, curent_hp: int = -1, damage = None):
        self.max_hp = max_hp
        self.curent_hp = max_hp if curent_hp == -1 else curent_hp
        self.damage = damage
    
    @property
    def curent_hp(self):
        return self.__curent_hp
    
    @curent_hp.setter
    def curent_hp(self, value):
        self.__curent_hp = value

    def __iadd__(self, other):
        self.curent_hp -= other
        return self
    
    def minus_hp(self, damage, game):
        damage = self.find_damage(damage)
        self.curent_hp -= damage
        # if self.curent_hp <= 0:
        #     if isinstance(self, Heroe):
        #         raise ValueError("Heroe is dead")
        #     else:
        #         # self.dead_enemy(game)
                    
            # game.gamemode.mode = 'normal'
    
    def atack(self, other, weapon = None):
        if weapon is None:
            other.minus_hp(self.damage, game)

        # TODO: weapon damage
    
    def print_hp(self, bars = 20):
        remaining_hp = round(self.curent_hp / self.max_hp * bars)
        lost_hp = (bars - remaining_hp)
        if isinstance(self, Heroe):
            return f'{colorama.Fore.GREEN}|{remaining_hp * "█"}{lost_hp * "_"}|{colorama.Style.RESET_ALL}'
        else:
            return f'{colorama.Fore.RED}|{remaining_hp * "█"}{lost_hp * "_"}|{colorama.Style.RESET_ALL}'

    @staticmethod
    def find_damage(damage):
        if isinstance(damage, list):
            return random.randint(damage[0], damage[1])
        return damage
    

class Heroe(Entity):
    def __init__(self, max_hp: int = 100, curent_hp = -1, damage = [0, 2], mapp = None, coins = 0):
        if mapp is None: raise ValueError("Map is not defined")

        super().__init__(max_hp = max_hp, curent_hp = curent_hp, damage = damage)
        self.mapp = mapp
        self.coins = coins
        self.spawn_heroe()
        pass
    
    def unlock_map(self, radius_x, radius_y):
        hero_pos = self.get_hero_position()
        i = hero_pos[0]
        j = hero_pos[1]
        visible_map = self.mapp.visible_map
        full_map = self.mapp.full_map
        for x in range(-radius_y, radius_y + 1):
            for y in range(-radius_x, radius_x + 1):
                if i + x >= 0 and i + x < len(visible_map) and j + y >= 0 and j + y < len(visible_map[i + x][0]):
                    if (i + x, j + y) == hero_pos:
                        visible_map[i + x][0] = visible_map[i + x][0][:j + y] + 'H' + visible_map[i + x][0][j + y + 1:]
                    else:
                        visible_map[i + x][0] = visible_map[i + x][0][:j + y] + full_map[i + x][0][j + y] + visible_map[i + x][0][j + y + 1:]

    def spawn_heroe(self, i: int = 5, j: int = 3):
        full_map = self.mapp.full_map
        self.hero_symbol = full_map[i][0][j]
        full_map[i][0][j] == 'H'
        self.add_heroe_on_map()

    def add_heroe_on_map(self):
        visible_map = self.mapp.visible_map
        pos = self.get_hero_position()
        i = pos[0]
        j = pos[1]
        visible_map[i][0] = visible_map[i][0][:j] + 'H' + visible_map[i][0][j + 1:]
        self.unlock_map(self.mapp.VISIBILITY_X, self.mapp.VISIBILITY_Y)

    def get_hero_position(self):
        full_map = self.mapp.full_map
        for i in range(len(full_map)):
            for j in range(len(full_map[i][0])):
                if full_map[i][0][j] == "H":
                    return (i, j)
                
    def move(self, direction, other, game):
        full_map = self.mapp.full_map
        hero_pos = self.get_hero_position()
        i, j = hero_pos
        new_i, new_j = i, j
        deep_water = '≈'
        chenge = False
        if direction == 'Up':
            if i - 1 >= 0 and full_map[i - 1][0][j] != deep_water:
                new_i -= 1
                chenge = True
        elif direction == 'Down':
            if i + 1 < len(full_map) and full_map[i + 1][0][j] != deep_water:
                new_i += 1
                chenge = True
        elif direction == 'Right':
            if j + 1 < len(full_map[i][0]) and full_map[i][0][j + 1] != deep_water:
                new_j += 1
                chenge = True
        elif direction == 'Left':
            if j - 1 >= 0 and full_map[i][0][j - 1] != deep_water:
                new_j -= 1
                chenge = True

        if not chenge:
            return
        
        new_hero_symbol = full_map[new_i][0][new_j]

        full_map[i][0] = full_map[i][0][:j] + self.hero_symbol + full_map[i][0][j + 1:]
        full_map[new_i][0] = full_map[new_i][0][:new_j] + 'H' + full_map[new_i][0][new_j + 1:]

        self.hero_symbol = new_hero_symbol
        self.unlock_map(self.mapp.VISIBILITY_X, self.mapp.VISIBILITY_Y)
        for i in range(10):
            if new_hero_symbol == '▲':
                other += 3
                time.sleep(0.03)
            elif new_hero_symbol == '♣':
                other += 2
                time.sleep(0.02)
            else:
                other += 1
                time.sleep(0.01)
            Menu.clear()
            game.mapp.print_map(self, game.gamemode, game.time, game.sett.language)
    
    @property
    def symbol(self):
        return self.hero_symbol
    
    @symbol.setter
    def symbol(self, hs):
        self.hero_symbol = hs

    def heal(self, hp):
        self.curent_hp += hp
        if self.curent_hp > self.max_hp:
            self.curent_hp = self.max_hp
    
    def add_coins(self, coins):
        self.coins += coins


class Enemy(Entity):
    enemys = ['goblin', 'skeleton', 'orc']
    monster_names = ["Xenomorph", "Nemesis", "Balrog",
    "Demogorgon", "Godzilla", "Cthulhu", "Kaonashi",
    "Sephiroth", "Tyrant", "Gorgon", "Dementor",
    "Gengar", "Mothra", "Gremlin", "Dracula",
    "Frieza", "Zergling", "Wendigo", "Behemoth",
    "Smaug", "Ghoul", "Necromorph", "Rancor",
    "Leviathan", "Predator", "Kaiju", "Balverine",
    "Cerberus", "Sauron", "Majin Buu", "Reaper",
    "Doom Slayer", "Kraid", "Jotun", "Revenant",
    "Spectre", "Vamp", "Naga", "Hydralisk",
    "Beholder", "Lich King", "Goliath", "Zeromus",
    "Darkspawn", "Creeper", "Molten Man", "Nightmare",
    "Orochi", "Poo", "Siren", "Rick Sanchez", "Thanos",
    "Ultron", "Venom", "Wolverine", "Xenomorph",
    "Yoda", "Aragorn", "Bane"
    ]

    enemy_types = {
        'goblin': {
            'max_hp': 10,
            'damage': [0, 2]
        },
        'skeleton': {
            'max_hp': 15,
            'damage': [0, 3]
        },
        'orc': {
            'max_hp': 20,
            'damage': [2, 4]
        }
    }

    def __init__(self, mapp):
        self.enemy_type = random.choice(self.enemys)

        super().__init__(self.enemy_types[self.enemy_type]['max_hp'], curent_hp = -1, damage = self.enemy_types[self.enemy_type]['damage'])
        self.name = random.choice(self.monster_names)
        self.enemy_type = self.enemy_type
        self.mapp = mapp
        self.enemy_symbol = None
        self.pos_x = self.set_enemy_x()
        self.pos_y = self.set_enemy_y()
        
        while self.validate_enemy_position():
            self.pos_x = self.set_enemy_x()
            self.pos_x = self.set_enemy_y()

        self.spawn_enemy()

    @property
    def enemy_symbol(self):
        return self.__enemy_symbol

    @enemy_symbol.setter
    def enemy_symbol(self, value):
        self.__enemy_symbol = value

    def set_enemy_x(self):
        return random.randint(0, len(self.mapp.full_map) - 1)

    def set_enemy_y(self):
        return random.randint(0, len(self.mapp.full_map[self.pos_x][0]) - 1)

    def validate_enemy_position(self):
        full_map = self.mapp.full_map
        try:
            if full_map[self.pos_x][0][self.pos_y] in ['≈', 'H']:
                return True
        except IndexError:
            return True
        
        return False

    def spawn_enemy(self):
        full_map = self.mapp.full_map
        while True:
            self.enemy_symbol = full_map[self.pos_x][0][self.pos_y]
            full_map[self.pos_x][0] = full_map[self.pos_x][0][:self.pos_y] + self.enemy_type[0].upper() + full_map[self.pos_x][0][self.pos_y + 1:]
            break
    
    def is_hero_stepping_on(self, heroe):
        return self.pos_x == heroe.get_hero_position()[0] and self.pos_y == heroe.get_hero_position()[1]

    def dead_enemy(self, game):
        full_map = self.mapp.full_map
        game.heroe.hero_symbol = self.enemy_symbol
        full_map[self.pos_x][0] = full_map[self.pos_x][0][:self.pos_y] + "H"+ full_map[self.pos_x][0][self.pos_y + 1:]

    def generate_coin(self):
        if self.enemy_type == 'goblin':
            coins = random.randint(1, 2)
        elif self.enemy_type == 'skeleton':
            coins = random.randint(1, 3)
        elif self.enemy_type == 'orc':
            coins = random.randint(2, 5)
        return coins

class Time:
    emoji_by_time = {
    "світанок": "🌅",
    "день": "🌞",
    "вечір": "🌇",
    "ніч": "🌙"
    }

    def __init__(self, minutes=0, hours=0, days=0):
        self.minutes = self.validate_time(minutes) % 60
        self.hours = self.validate_time(hours) % 24
        self.days = self.validate_time(days)
        self.daytime = 'день'

    def __iadd__(self, other):
        self.minutes += other
        while self.minutes >= 60:
            self.hours += 1
            self.minutes -= 60

            if self.hours >= 24:
                self.days += 1
                self.hours -= 24

        return self
    
    def validate_time(self, x):
        if x < 0 or isinstance(x, int) == False:
            raise ValueError('Invalid time value')
        return x

    def __str__(self):
        return f'{self.format_time(self.hours)}:{self.format_time(self.minutes)}'

    def __repr__(self):
        return self.__str__()

    def get_day(self):
        return self.days

    def get_time(self):
        return self.__str__()

    @property
    def daytime(self):
        return self.__daytime
    
    @daytime.setter
    def daytime(self, value: str) -> None:
        if value not in ['світанок', 'день', 'вечір', 'ніч']:
            raise ValueError("Invalid daytime")
        
        self.__daytime = value

    def get_daytime(self):
        dt = self.get_time()[:2]

        if dt[0] == '0':
            dt = dt[1]

        dt = int(dt)

        if dt >= 4 and dt < 6:
            self.daytime = "світанок"
        elif dt >= 6 and dt < 18:
            self.daytime = "день"
        elif dt >= 18 and dt < 20:
            self.daytime = "вечір"
        else:
            self.daytime = "ніч"

    @staticmethod
    def format_time(time):
        return str(time).rjust(2, '0')


class Gamemode:
    move_dict = {
        'w': 'Up',
        's': 'Down',
        'd': 'Right',
        'a': 'Left',
    }

    def __init__(self):
        self.mode = 'normal'

    @property
    def mode(self):
        return self.__mode
    
    @mode.setter
    def mode(self, value: str) -> None:
        if value not in ['normal', 'command', 'map', 'inventory', 'fight']:
            raise ValueError("Invalid mode")
        
        self.__mode = value

    def get_char_n(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            char = sys.stdin.read(1)
            char = char.lower()

            if char == '\x1b':
                sequence = sys.stdin.read(2)
                if sequence == '[A':  
                    return 'Up'
                elif sequence == '[B':  
                    return 'Down'
                elif sequence == '[C': 
                    return 'Right'
                elif sequence == '[D': 
                    return 'Left'
            
            elif char in ['w', 's', 'd', 'a']:
                return self.move_dict[char]
            elif char == 'm':
                return 'Map'
            elif char == 'c':
                return 'C'
            elif char == '0': 
                return 'Esc'
            elif char == 'i':
                return 'I'
            else:
                return -1
            
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    @staticmethod
    def get_char_c():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            char = sys.stdin.read(1)
            char = char.lower()  

            if char in ['0', 'n', 'c']:
                return 'Esc'
            elif char == 'm':
                return 'Map'
            elif char == 'i':
                return 'I'
            else:
                return -1
            
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def get_char_m(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            char = sys.stdin.read(1)
            char = char.lower()  
            if char == '\x1b':
                sequence = sys.stdin.read(2)
                if sequence == '[A':  
                    return 'Up'
                elif sequence == '[B':  
                    return 'Down'
                elif sequence == '[C': 
                    return 'Right'
                elif sequence == '[D': 
                    return 'Left'
                
            elif char in ['w', 's', 'd', 'a']:
                return self.move_dict[char]
            elif char in ['0', 'n', 'm']:
                return 'Esc'
            elif char == 'c':
                return 'C'
            elif char == 'i':
                return 'I'
            else:
                return -1
            
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def get_char_f(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            char = sys.stdin.read(1)
            char = char.lower()  

            if char in ['1', '2', '3', '4', '0']:
                return char
            else:
                return -1
            
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def get_char_i(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            char = sys.stdin.read(1)
            char = char.lower()  

            if char in ['0', 'n', 'c', 'm']:
                return 'Esc'
            else:
                return -1
            
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


class Processmode:
    def __init__(self):
        self.mode = 'menu'

    @property
    def mode(self):
        return self.__mode
    
    @mode.setter
    def mode(self, value: str) -> None:
        if value not in ['menu', 'ingame', 'sett']:
            raise ValueError("Invalid mode")
        
        self.__mode = value

    @staticmethod
    def get_char_map():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            char = sys.stdin.read(1)
            char = char.lower()  

            if char in ['1', '2', '3', '4', '0']:
                return char
            else:
                return -1
            
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


class Map:
    COLORS = {
        '~': '\x1b[38;5;31m',
        '≈': '\x1b[38;5;33m',
        '.': '\x1b[38;5;148m', 
        '♣': colorama.Fore.GREEN, 
        '▲': colorama.Fore.WHITE,
        'H': colorama.Fore.RED 
    }

    VISIBILITY_X = 2
    VISIBILITY_Y = 1

    def __init__(self, range_x = 8, range_y = 15, start_x = 0, start_y = 0):
        self.full_map = [
            ["≈≈≈~.......▲♣♣♣....~≈≈≈~~....♣♣♣♣"],
            ["≈≈~~~.....♣▲.♣♣...~≈≈≈~~......♣.."],
            ["~~..H...▲▲▲.....~~~♣♣.....≈~....♣"],
            ["....♣..▲▲▲▲.♣♣♣..~♣♣♣.▲▲~~≈≈~...."],
            ["...♣♣♣♣♣♣......♣♣♣♣..~~~≈≈≈~~...."],
            ["♣....♣♣♣.♣♣~♣♣.....♣♣~~≈≈≈≈~..♣.."],
            ["..♣♣..♣♣..♣~≈≈♣♣♣.....~~~≈~..♣♣.."],
            ["♣♣♣.......♣.~♣♣♣......♣♣♣~~.♣♣..▲"],
            ["▲▲.♣♣♣.......▲..♣♣♣...♣♣♣.▲♣♣.♣.."],
            ["▲~▲.♣.♣.......▲.▲..♣♣♣♣♣.▲▲▲♣♣♣.."],
            ["~▲▲..♣♣....▲▲♣▲.....♣♣♣..▲..▲...▲"],
            ["▲▲.♣...........♣♣♣♣......♣♣....▲."],
            ["...♣.♣..▲....♣♣♣.♣♣♣♣.♣.~.♣♣..▲▲♣"],
            ['♣.▲▲...♣...♣♣.♣♣..♣♣..~~~≈≈≈.♣..♣'],
            ['♣.♣▲▲▲....▲▲...♣♣...~~≈≈≈≈~...♣♣.']]
        HAIGH = len(self.full_map)
        WIDTH = len(self.full_map[0][0])
        self.visible_map = [["#" * WIDTH] * 1 for _ in range(HAIGH)]

        self.range_x = range_x
        self.range_y = range_y
        self.start_x = start_x
        self.start_y = start_y
        self.max_x = start_x + range_x
        self.max_y = start_y + range_y

    def print_map(self, heroe, gamemode, curent_time, language):
        print(texts.play_menu(language)[0])
        curent_mode = gamemode.mode

        hero_pos = heroe.get_hero_position()
        left_x = hero_pos[0] - self.VISIBILITY_Y - 1
        right_x = hero_pos[0] + self.VISIBILITY_Y + 2
        left_y = hero_pos[1] - self.VISIBILITY_X - 2
        right_y = hero_pos[1] + self.VISIBILITY_X + 3

        if left_x < 0:
            n = abs(left_x)
            right_x += n
            left_x = 0

        if right_x > len(self.visible_map):
            n = right_x - len(self.visible_map)
            left_x -= n
            right_x = len(self.visible_map)

        if left_y < 0:
            n = abs(left_y)
            right_y += n
            left_y = 0

        if right_y > len(self.visible_map[0][0]):
            n = right_y - len(self.visible_map[0][0])
            left_y -= n
            right_y = len(self.visible_map[0][0])
        
        start_x = left_x
        end_x = right_x
        start_y = left_y
        end_y = right_y

        for i in range(start_x, end_x):
            colored_line = ''
            for j in range(start_y, end_y):
                symbol = self.visible_map[i][0][j]
                colored_line += self.COLORS.get(symbol, colorama.Fore.RESET) + symbol
                colored_line += colorama.Fore.RESET
            try:
                text = texts.map_rigt(language)
                locations = texts.locations(language)
                print(colored_line, f'  {text[0]} \b{locations[heroe.hero_symbol]} {text[1]} {heroe.hero_symbol}' if i == start_x else '',
                    f'{text[2]} \b{curent_time.get_day()} {text[3]} \b{curent_time.get_time()} {curent_time.emoji_by_time[curent_time.daytime]}' if i == start_x + 1 else '',
                    f'{text[4]} \b{heroe.curent_hp}/{heroe.max_hp} {text[5]} \b{heroe.coins}' if i == start_x + 2 else '',
                    f'\b{heroe.print_hp()}' if i == start_x + 3 else '',
                    f'\b\b{curent_mode.upper()}' if i == start_x + 4 else '')
            except:
                pass

    def move_full_map(self, direction):
        if direction == 'Up':
            if self.start_x - 1 >= 0:
                self.start_x -= 1
                self.max_x -= 1
        elif direction == 'Down':
            if self.max_x + 1 < len(self.visible_map) + 1:
                self.start_x += 1
                self.max_x += 1
        elif direction == 'Right':
            if self.max_y + 1 < len(self.visible_map[0][0]) + 1:
                self.start_y += 1
                self.max_y += 1
        elif direction == 'Left':
            if self.start_y - 1 >= 0:
                self.start_y -= 1
                self.max_y -= 1    

    def print_full_map(self, game):
        print(texts.play_menu(game.sett.language)[0])

        curent_mode = game.gamemode.mode
        for i in range(self.start_x, self.max_x):
            colored_line = ''
            for j in range(self.start_y, self.max_y):
                symbol = self.visible_map[i][0][j]
                colored_line += self.COLORS.get(symbol, colorama.Fore.RESET) + symbol
                colored_line += colorama.Fore.RESET
            text = texts.map_rigt(game.sett.language)
            locations = texts.locations(game.sett.language)
            print(colored_line, f' {text[0]} \b{locations[game.heroe.hero_symbol]}' if i == self.start_x else '',
                f'\b{text[2]} \b{game.time.get_day()} {text[3]} \b{game.time.get_time()}' if i == self.start_x + 1 else '',
                f'{curent_mode.upper()}' if i == self.max_x - 1 else '')
    
    def update_visible_map(self):
        for i in range(len(self.full_map)):
            for j in range(len(self.full_map[i][0])):
                self.visible_map[i][0] = self.visible_map[i][0][:j] + self.full_map[i][0][j] + self.visible_map[i][0][j + 1:]


class Inventory:
    def __init__(self):
        self.items = []
        self.max_items = 10

    def add_item(self, item):
        if len(self.items) < self.max_items:
            self.items.append(item)
        else:
            print("Inventory is full")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
        else:
            print("Item not found")

    def show_inventory(self):
        print("Inventory:")
        if len(self.items) == 0:
            print("Inventory is empty")
        else:
            for item in self.items:
                print(item)


if __name__ == "__main__":
    menu = Menu()
    menu.start()
    menu.clear()