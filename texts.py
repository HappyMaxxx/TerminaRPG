def menu(lang):

    menu_ua = ["1. НОВА ГРА",
               '2. ЗАВАНАТЖИТИ ГРУ',
               "3. ЯК ГРАТИ",
               "4. НАЛАШТУВАННЯ",
               "0. ВИХІД"]
    
    menu_en = ["1. NEW GAME",
               "2. LOAD GAME",
               "3. HOW TO PLAY",
               "4. SETTINGS",
               "0. EXIT"]
    
    if lang == "ua":
        return menu_ua
    elif lang == "en":
        return menu_en

#PAUSE MENU
def paus(lang):

    paus_ua = [" --- Пауза --- ",
            "1. ПРОДОВЖИТИ",
            "2. НАЛАШТУВАННЯ",
            "0. ВИЙТИ",
            ""]

    paus_en = [" --- Pause --- ",
            "1. CONTINUE",
            "2. SETTINGS",
            "0. EXIT",
            ""]
    
    if lang == "ua":
        return paus_ua
    elif lang == "en":
        return paus_en

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
    set_ua = [" --- НАЛАШТУВАННЯ --- ",
            "",
            "0. ЗБЕРЕГТИ ЗМІНИ ТА ПОВЕРНУТИСЬ",
            "1. ЗМІНИТИ МОВУ",
            "Мова зараз ua(Українська), змінити на en(English)",
            ""
            ]

    set_en = [" --- SETTINGS --- ",
            "",
            "0. SAVE CHANGES AND RETURN",
            "1. CHANGE LANGUAGE",
            "Currently language is en(English), change to ua(Українська)",
            ""
            ]
    
    if lang == "ua":
        return set_ua
    
    elif lang == "en":
        return set_en

def play_menu(lang):
    play_menu_ua = ["0. ЗБЕРЕГТИ І ВИЙТИ\n",
                ""]

    play_menu_en = ["0. SAVE AND QUIT\n",
                    ""]
    
    if lang == "ua":
        return play_menu_ua
    
    elif lang == "en":
        return play_menu_en