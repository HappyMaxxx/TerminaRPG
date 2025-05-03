import sys
import os
import tty
import termios
import time
import random
from pyfiglet import Figlet
import pickle
import shutil
import colorama
import copy

import texts
import settings

colorama.init()


class InputHandler:
    def __init__(self):
        self.move_dict = {
            'w': 'Up',
            's': 'Down',
            'd': 'Right',
            'a': 'Left',
            'ц': 'Up',
            'і': 'Down',
            'в': 'Right',
            'ф': 'Left',
        }

    def get_input(self, mode):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            char = sys.stdin.read(1).lower()

            if char == '\x1b':
                sequence = sys.stdin.read(2)
                if mode in ['normal', 'map']:
                    if sequence == '[A':
                        return 'Up'
                    elif sequence == '[B':
                        return 'Down'
                    elif sequence == '[C':
                        return 'Right'
                    elif sequence == '[D':
                        return 'Left'

            if mode == 'menu':
                if char in ['1', '2', '3', '4', '5', '0']:
                    return char
                
                return -1

            elif mode == 'settings':
                if char in ['1', '2', '0']:
                    return char
                return -1

            elif mode == 'normal':
                if char in self.move_dict:
                    return self.move_dict[char]
                elif char == 'm' or char == 'ь':
                    return 'Map'
                elif char == 'c' or char == 'c':
                    return 'C'
                elif char == '0':
                    return 'Esc'
                elif char == 'i' or char == 'ш':
                    return 'I'
                return -1

            elif mode == 'command':
                if char in ['0', 'n', 'c', 'т', 'с']:
                    return 'Esc'
                elif char == 'm' or char == 'ь':
                    return 'Map'
                elif char == 'i' or char == 'ш':
                    return 'I'
                return -1

            elif mode == 'map':
                if char in self.move_dict:
                    return self.move_dict[char]
                elif char in ['0', 'n', 'm', 'т', 'ь']:
                    return 'Esc'
                elif char == 'c' or char == 'с':
                    return 'C'
                elif char == 'i' or char == 'ш':
                    return 'I'
                return -1

            elif mode == 'inventory':
                if char in ['0', 'n', 'c', 'm', 'т', 'ь', 'с']:
                    return 'Esc'
                return -1

            elif mode == 'fight' or mode == 'pause':
                if char in ['1', '2', '3', '4', '5', '0']:
                    return char
                return -1

            return -1

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


class Settings:
    def __init__(self):
        self.language = 'en'

    def save(self):
        with open("settings.pkl", 'wb') as f:
            pickle.dump(self, f)


class Menu:
    is_watched_intro = False

    def __init__(self):
        try:
            with open("settings.pkl", 'rb') as f:
                self.sett = pickle.load(f)
        except FileNotFoundError:
            self.sett = Settings()
        self.input_handler = InputHandler()

    def settings_menu(self):
        while True:
            settings.clear()
            for i in texts.settings(self.sett.language):
                print(i)

            print("> ", end='')
            sys.stdout.flush()

            choice = self.input_handler.get_input('settings')
            if choice == '1':
                if self.sett.language == 'ua':
                    self.sett.language = 'en'
                else:
                    self.sett.language = 'ua'
                    
                if isinstance(self, Game):
                    self.sett = self.load_set()

            elif choice == '2':
                pass

            elif choice == '0':
                self.sett.save()
                break

    def start_new_game(self):
        global curent_time, gamemode, process, mapp, hero, inventar, game

        if os.path.exists("gamesave.pkl"):
            os.remove("gamesave.pkl")

        curent_time = Time(hours=8)
        gamemode = Gamemode()
        process = Processmode()
        mapp = Map()
        hero = Hero(mapp=mapp)
        inventar = Inventory()
        game = Game(hero, mapp, curent_time, gamemode, process, inventar, settings=self.sett, menu=self)
        hero.set_game(game)
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
        if not self.is_watched_intro:
            self.is_watched_intro = True
            self.write((list(f.renderText('TerminaRPG'))), 0.002)
        else:
            print(f.renderText('TerminaRPG'))
        print()

    @staticmethod
    def load_game():
        with open("gamesave.pkl", 'rb') as f:
            game = pickle.load(f)
        game.hero.add_hero_on_map()
        game.process.mode = 'menu'
        game.sett = Menu.load_set()
        return game

    @staticmethod
    def load_set():
        try:
            with open("settings.pkl", 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            with open("settings.pkl", 'wb') as f:
                sett = Settings()
                pickle.dump(sett, f)
            return sett

    def show_menu(self):
        settings.clear()
        self.print_intro()
        for i in texts.menu(self.sett.language):
            print(i)
        print("> ", end='')
        sys.stdout.flush()

    @staticmethod
    def dell_all():
        try:
            del curent_time
            del gamemode
            del process
            del mapp
            del hero
            del inventar
            del game
        except:
            pass

    def start(self):
        while True:
            self.__init__()
            self.show_menu()
            choice = self.input_handler.get_input('menu')
            if choice == '1':
                self.dell_all()
                self.start_new_game()
            elif choice == '2':
                print("Loading game...")
                settings.clear()
                if not os.path.exists("gamesave.pkl"):
                    print("No save file")
                    time.sleep(2)
                    settings.clear()
                    continue

                self.dell_all()
                self.load_game().main_process()

            elif choice == '3':
                # TODO: how to play
                pass

            elif choice == '4':
                self.settings_menu()

            elif choice in ['5', '0']:
                print("Exiting...")
                break


class Game:
    def __init__(self, hero, mapp, time, gamemode, processmode, inventory, settings, menu):
        self.hero = hero
        self.mapp = mapp
        self.time = time
        self.gamemode = gamemode
        self.process = processmode
        self.inventory = inventory
        self.sett = settings
        self.menu = menu
        self.enemies = []
        self.index = -1
        self.input_handler = InputHandler()

    def save(self):
        with open("gamesave.pkl", 'wb') as f:
            pickle.dump(self, f)

    def main_process(self):
        self.menu.load_set()
        while True:
            self.save()
            if self.process.mode == 'menu':
                settings.clear()
                self.print_pause()

                print('> ', end='')
                sys.stdout.flush()
                char = self.input_handler.get_input('menu')

                if char == -1:
                    continue

                if char == '1':
                    self.process.mode = 'ingame'

                elif char == "2":
                    self.menu.settings_menu()

                elif char == '0':
                    settings.clear()
                    return

            elif self.process.mode == 'sett':
                pass

            else:
                if self.hero.curent_hp <= 0:
                    settings.clear()
                    print("Hero is dead")
                    time.sleep(2)
                    self.process.mode = 'menu'
                    continue

                settings.clear()
                self.time.get_daytime()

                if self.gamemode.mode == 'normal':
                    self.index = -1
                    self.mapp.print_map(self.hero, self.gamemode, self.time, self.sett.language)
                    char = self.input_handler.get_input('normal')

                    if char == -1:
                        continue

                    elif char == 'Esc':
                        self.save()
                        self.process.mode = 'menu'
                        continue

                    elif char in ['Up', 'Down', 'Right', 'Left']:
                        self.hero.move(char, self.time, self)
                        if len(self.enemies) > 0:
                            for i, enemy in enumerate(self.enemies):
                                try:
                                    if enemy.is_hero_stepping_on(self.hero):
                                        self.index = i
                                        self.gamemode.mode = 'fight'
                                        break
                                except ValueError:
                                    pass

                        if len(self.enemies) < settings.MAX_ENEMIES and self.time.get_day() >= 1:
                            if self.time.daytime == 3:
                                if random.random() < 0.6:
                                    self.create_enemy()

                            elif self.time.daytime == 2:
                                if random.random() < 0.2:
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
                    self.mapp.print_map(self.hero, self.gamemode, self.time, self.sett.language)
                    print("> ", end='')
                    sys.stdout.flush()
                    char = self.input_handler.get_input('command')

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

                    char = self.input_handler.get_input('map')

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
                    sys.stdout.flush()
                    char = self.input_handler.get_input('inventory')

                    if char == -1:
                        continue

                    elif char == 'Esc':
                        self.gamemode.mode = 'normal'
                        continue

                elif self.gamemode.mode == 'fight':
                    self.fight(self.index)
                    self.index = -1

                elif self.gamemode.mode == 'pause':
                    self.handle_pause()

    def create_enemy(self):
        enemy = Enemy(self.mapp)
        self.enemies.append(enemy)

    def print_pause(self):
        for i in texts.paus(self.sett.language):
            print(i)

    def fight(self, index):
        while True:
            settings.clear()
            text = texts.fight_mode(self.sett.language)

            print(text[0], '\n')
            print(f"{text[6]} {self.hero.curent_hp}/{self.hero.max_hp}")
            print(self.hero.print_hp())
            print(f"{self.enemies[index].name} the {self.enemies[index].enemy_type} {text[6]} {self.enemies[index].curent_hp}/{self.enemies[index].max_hp}")
            print(self.enemies[index].print_hp())
            print()
            print(text[1])
            print(text[2])
            print(text[3])
            print(text[4])
            print(text[7])
            print("> ", end='')
            sys.stdout.flush()

            time.sleep(0.1)

            char = self.input_handler.get_input('fight')
            heal_chance = self.enemies[index].enemy_types[self.enemies[index].enemy_type]['heal_chance']
            if char == -1:
                continue

            elif char == '0':
                self.gamemode.mode = 'pause'
                self.handle_pause()

            elif char == '1':
                if self.hero.curent_hp <= 0:
                    settings.clear()
                    print("Hero is dead")
                    time.sleep(2)
                    self.gamemode.mode = 'normal'
                    self.process.mode = 'menu'
                    break
                else:
                    self.hero.atack(self.enemies[index], self)
                    settings.clear()

                if self.enemies[index].curent_hp <= 0:
                    self.hero.add_coins(self.enemies[index].generate_coin())
                    self.enemies[index].dead_enemy(game=self)
                    del self.enemies[index]
                    self.gamemode.mode = 'normal'
                    break
                else:
                    if random.random() < heal_chance:
                        self.enemies[index].heal()
                    else:
                        self.enemies[index].atack(self.hero, self)

            elif char == '3':
                self.hero.heal(5)

                if self.enemies[index].curent_hp <= 0:
                    self.hero.add_coins(self.enemies[index].generate_coin())
                    self.enemies[index].dead_enemy(game=self)
                    del self.enemies[index]
                    self.gamemode.mode = 'normal'
                    break
                else:
                    if random.random() < heal_chance:
                        self.enemies[index].heal()
                    else:
                        self.enemies[index].atack(self.hero, self)

    def handle_pause(self):
        while self.gamemode.mode == 'pause':
            settings.clear()
            self.print_pause()

            print("> ", end='')
            sys.stdout.flush()
            char = self.input_handler.get_input('pause')

            if char == '1':
                self.gamemode.mode = 'fight'
            elif char == '2':
                self.menu.settings_menu()
            elif char == '0':
                settings.clear()
                print(texts.live_fight(self.sett.language))
                time.sleep(2)
                break


class Entity:
    def __init__(self, max_hp, curent_hp: int = -1, damage=None):
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

    def atack(self, other, game, weapon=None):
        if weapon is None:
            other.minus_hp(self.damage, game)

    def print_hp(self, bars=20):
        remaining_hp = round(self.curent_hp / self.max_hp * bars)
        lost_hp = (bars - remaining_hp)
        if isinstance(self, Hero):
            return f'{colorama.Fore.GREEN}|{remaining_hp * "█"}{lost_hp * "_"}|{colorama.Style.RESET_ALL}'
        else:
            return f'{colorama.Fore.RED}|{remaining_hp * "█"}{lost_hp * "_"}|{colorama.Style.RESET_ALL}'

    @staticmethod
    def find_damage(damage):
        if isinstance(damage, list):
            return random.randint(damage[0], damage[1])
        return damage

    def heal(self, heal=5):
        if isinstance(self, Hero):
            if self.curent_hp + heal > self.max_hp:
                self.curent_hp = self.max_hp
            else:
                self.curent_hp += heal

        elif isinstance(self, Enemy):
            healings = self.enemy_types[self.enemy_type]['healing']
            heal = random.randint(healings[0], healings[1])
            if self.curent_hp + heal > self.max_hp:
                self.curent_hp = self.max_hp
            else:
                self.curent_hp += heal


class Hero(Entity):
    def __init__(self, max_hp: int = 100, curent_hp=-1, damage=[0, 2], mapp=None, coins=0):
        if mapp is None:
            raise ValueError("Map is not defined")

        super().__init__(max_hp=max_hp, curent_hp=curent_hp, damage=damage)
        self.mapp = mapp
        self.coins = coins
        self.spawn_hero()

    def set_game(self, game):
        self.game = game

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

    def spawn_hero(self, i: int = 2, j: int = 4):
        full_map = self.mapp.full_map
        self.hero_symbol = full_map[i][0][j]
        str_before = full_map[i][0][:j]
        str_after = full_map[i][0][j + 1:]
        full_map[i][0] = str_before + 'H' + str_after
        self.mapp.full_map = full_map
        self.add_hero_on_map()

    def add_hero_on_map(self):
        visible_map = self.mapp.visible_map
        pos = self.get_hero_position()
        i = pos[0]
        j = pos[1]
        visible_map[i][0] = visible_map[i][0][:j] + 'H' + visible_map[i][0][j + 1:]
        self.unlock_map(settings.VISIBILITY_X, settings.VISIBILITY_Y)

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
        self.unlock_map(settings.VISIBILITY_X, settings.VISIBILITY_Y)
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
            settings.clear()
            game.mapp.print_map(self, game.gamemode, game.time, game.sett.language)

    @property
    def symbol(self):
        return self.hero_symbol

    @symbol.setter
    def symbol(self, hs):
        self.hero_symbol = hs

    def add_coins(self, coins):
        self.coins += coins


class Enemy(Entity):
    enemys = ['goblin', 'skeleton', 'orc']
    monster_names = settings.monster_names
    enemy_types = settings.enemy_types

    def __init__(self, mapp):
        self.enemy_type = random.choice(self.enemys)

        super().__init__(self.enemy_types[self.enemy_type]['max_hp'], curent_hp=-1, damage=self.enemy_types[self.enemy_type]['damage'])
        self.name = random.choice(self.monster_names)
        self.enemy_type = self.enemy_type
        self.mapp = mapp
        self.enemy_symbol = None
        self.pos_x = self.set_enemy_x()
        self.pos_y = self.set_enemy_y()

        while self.validate_enemy_position():
            self.pos_x = self.set_enemy_x()
            self.pos_y = self.set_enemy_y()

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
            if full_map[self.pos_x][0][self.pos_y] in ['≈', 'H', 'O', 'G', 'S']:
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

    def is_hero_stepping_on(self, hero):
        return self.pos_x == hero.get_hero_position()[0] and self.pos_y == hero.get_hero_position()[1]

    def dead_enemy(self, game):
        full_map = self.mapp.full_map
        game.hero.hero_symbol = self.enemy_symbol
        full_map[self.pos_x][0] = full_map[self.pos_x][0][:self.pos_y] + "H" + full_map[self.pos_x][0][self.pos_y + 1:]

    def generate_coin(self):
        if self.enemy_type == 'goblin':
            coins = random.randint(1, 2)
        elif self.enemy_type == 'skeleton':
            coins = random.randint(1, 3)
        elif self.enemy_type == 'orc':
            coins = random.randint(2, 5)
        return coins


class Time:
    def __init__(self, minutes=0, hours=0, days=0):
        self.minutes = self.validate_time(minutes) % 60
        self.hours = self.validate_time(hours) % 24
        self.days = self.validate_time(days)
        self.daytime = 1

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
        if value not in range(0, 4):
            raise ValueError("Invalid daytime")

        self.__daytime = value

    def get_daytime(self):
        dt = self.get_time()[:2]

        if dt[0] == '0':
            dt = dt[1]

        dt = int(dt)

        if dt >= 4 and dt < 6:
            self.daytime = 0
        elif dt >= 6 and dt < 18:
            self.daytime = 1
        elif dt >= 18 and dt < 20:
            self.daytime = 2
        else:
            self.daytime = 3

    @staticmethod
    def format_time(time):
        return str(time).rjust(2, '0')


class Gamemode:
    def __init__(self):
        self.mode = 'normal'

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value: str) -> None:
        if value not in ['normal', 'command', 'map', 'inventory', 'fight', 'pause']:
            raise ValueError("Invalid mode")

        self.__mode = value


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


class Map:
    def __init__(self, range_x=8, range_y=15, start_x=0, start_y=0):
        self.full_map = copy.deepcopy(settings.full_map)
        HAIGH = len(self.full_map)
        WIDTH = len(self.full_map[0][0])
        self.visible_map = [["#" * WIDTH] * 1 for _ in range(HAIGH)]

        self.range_x = range_x
        self.range_y = range_y
        self.start_x = start_x
        self.start_y = start_y
        self.max_x = start_x + range_x
        self.max_y = start_y + range_y

    @staticmethod
    def get_terminal_size():
        return shutil.get_terminal_size((40, 20))

    def print_map(self, hero, gamemode, curent_time, language):
        print(texts.play_menu(language)[0])
        print('-' * self.get_terminal_size().columns)
        curent_mode = gamemode.mode

        hero_pos = hero.get_hero_position()
        left_x = hero_pos[0] - settings.VISIBILITY_Y - 1
        right_x = hero_pos[0] + settings.VISIBILITY_Y + 2
        left_y = hero_pos[1] - settings.VISIBILITY_X - 2
        right_y = hero_pos[1] + settings.VISIBILITY_X + 3

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
                colored_line += settings.COLORS.get(symbol, colorama.Fore.RESET) + symbol
                colored_line += colorama.Fore.RESET
            try:
                text = texts.map_right(language)
                locations = texts.locations(language)
                print(colored_line,
                    # HERO LOCATION
                      f'  {text[0]} \b{locations[hero.hero_symbol]} {text[1]} {hero.hero_symbol}'
                        if i == start_x else '',
                    # TIME 
                      f'{text[2]} \b{curent_time.get_day()} {text[3]} \b{curent_time.get_time()} '
                      f'{settings.emoji_by_time[curent_time.daytime]}' if i == start_x + 1 else '',
                    # MONEY   
                      f'{text[5]} \b{hero.coins}' if i == start_x + 2 else '',
                    # HP
                      f'\b{hero.print_hp()} {text[4]} \b{hero.curent_hp}/{hero.max_hp}'
                        if i == start_x + 3 else '',
                    # GAME MODE
                      f'\b\b{curent_mode.upper()}' if i == start_x + 4 else '')
            except:
                pass
        print('-' * self.get_terminal_size().columns)

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
            if self.startとし_y - 1 >= 0:
                self.start_y -= 1
                self.max_y -= 1

    def print_full_map(self, game):
        print(texts.play_menu(game.sett.language)[0])
        print('-' * self.get_terminal_size().columns)

        curent_mode = game.gamemode.mode
        for i in range(self.start_x, self.max_x):
            colored_line = ''
            for j in range(self.start_y, self.max_y):
                symbol = self.visible_map[i][0][j]
                colored_line += settings.COLORS.get(symbol, colorama.Fore.RESET) + symbol
                colored_line += colorama.Fore.RESET
            text = texts.map_right(game.sett.language)
            locations = texts.locations(game.sett.language)
            print(colored_line, f' {text[0]} \b{locations[game.hero.hero_symbol]}' if i == self.start_x else '',
                  f'\b{text[2]} \b{game.time.get_day()} {text[3]} \b{game.time.get_time()}' if i == self.start_x + 1 else '',
                  f'{curent_mode.upper()}' if i == self.max_x - 1 else '')
        print('-' * self.get_terminal_size().columns)

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
    settings.clear()