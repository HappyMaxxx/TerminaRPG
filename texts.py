def menu(lang):
    if lang == "ua":
        return ["1. НОВА ГРА",
               '2. ЗАВАНАТЖИТИ ГРУ',
               "3. ЯК ГРАТИ",
               "4. НАЛАШТУВАННЯ",
               "0. ВИХІД"]
    
    elif lang == "en":
        return ["1. NEW GAME",
               "2. LOAD GAME",
               "3. HOW TO PLAY",
               "4. SETTINGS",
               "0. EXIT"]

#PAUSE MENU
def paus(lang):
    if lang == "ua":
        return [" --- Пауза --- ",
            "1. ПРОДОВЖИТИ",
            "2. НАЛАШТУВАННЯ",
            "0. ВИЙТИ",
            ""]
    
    elif lang == "en":
        return [" --- Pause --- ",
            "1. CONTINUE",
            "2. SETTINGS",
            "0. EXIT",
            ""]

#MAP TEXTS
def map_rigt(lang):
    map_r_ua = ['Локація зараз:',
                '\b, символ:',
                ' День:',
                '\b, час:',
                'ОЗ:',
                'Монети:'
                ]
    map_r_en = ['Current location: ',
                '\b, symbol: ',
                ' Day: ',
                '\b, time: ',
                'HP: ',
                'Coins: '
                ]
    
    if lang == "ua":
        return map_r_ua
    elif lang == "en":
        return map_r_en

#HOW TO PLAY MENU
htp_ua = ["Вся ця гра - це рольова гра в терміналі, тому вам доведеться використовувати команди",
          "для виконання певних дій:",
          "",
          "-h, help: ви можете скористатися цими командами, щоб вивести список усіх команд",
          "з коротким описом."]

htp_en = ["This whole game is an RPG in a terminal, so you have to use commands",
          "to do certain things:"
          "",
          "-h, help: you can use this commands to display a list of all commands",
          "with brief descriptions."]

#SETTINGS
def settings(lang):
    if lang == "ua":
        return [" --- НАЛАШТУВАННЯ --- ",
            "",
            "0. ЗБЕРЕГТИ ЗМІНИ ТА ПОВЕРНУТИСЬ",
            "1. ЗМІНИТИ МОВУ",
            "Мова зараз ua(Українська), змінити на en(English)",
            ""
            ]
    
    elif lang == "en":
        return [" --- SETTINGS --- ",
            "",
            "0. SAVE CHANGES AND RETURN",
            "1. CHANGE LANGUAGE",
            "Currently language is en(English), change to ua(Українська)",
            ""
            ]

def play_menu(lang):
    if lang == "ua":
        return ["0. ПАУЗА\n",
                ""]
    
    elif lang == "en":
        return ["0. PAUSE\n",
                ""]
    
def locations(language):
    if language == 'ua':
        return {
            '~': 'Мілководдя',
            '.': 'Рівнина',
            '♣': 'Ліс',
            '▲': 'Гори'
        }
    
    elif language == 'en':
        return {
            '~': 'Shallow Water',
            '.': 'Plain',
            '♣': 'Forest',
            '▲': 'Mountains'
        }