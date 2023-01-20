# https://www.helloworld.cc - Heft 1 - Seite 52
# Scary cave game -- Original Version CC BY-NC-SA 3.0
# Diese modifizierte Version (C) 2023 Roland Härter r.haerter@wut.de

import time
import sys
import random


def check_key():
    key = input("Do you have the key? ").lower()
    if key in ["j", "ja", "y", "yes"]:
        return True
    else:
        return False


def take(raum):
    global hungerstatus
    global rauminhalt
    gefunden = False
    ding = input("What do you want to take? ").lower().rstrip()
    anzahl, zeug = rauminhalt[raum].split(' ', 1)
    if ding == zeug:
        print(f"Each of the {anzahl} {zeug} is too heavy to take with you.")
        gefunden = True
        if zeug == 'lichen' and int(anzahl) > 0:
            hungerstatus += random.randint(7, 24)
            rauminhalt[raum] = "{} {}".format(int(anzahl) - 1, zeug)
    if (gefunden == False):
        print("I see here no %s" % (ding))
    return False


def check_starvation(hungerlevel):
    if hungerlevel < 1:
        print("You die from lack of food ...")
        return True
    elif hungerlevel < 10:
        print("You are so weak that you can hardly walk.")
    elif hungerlevel < 20:
        print(
            "Your stomach growls so loudly that you are afraid of attracting monsters."
        )
    elif hungerlevel < 50:
        print("You feel weak. Something to eat would be good now.")
    else:
        print("You are well. You are full and happy.")
    return False


def pray():
    print("A strange trembling passes through the room.")
    verbindungen_erzeugen()


def zeige_rauminhalt():
    inhalt = rauminhalt[current_room]
    print(inhalt)


def quit():
    print("There is a bang. Smoke rises. You faint.")
    for i in range(3):
        time.sleep(1)
        print(".", end="")
        sys.stdout.flush()
    print("\n\nYou wake up in a meadow of flowers and wonder:")
    print("Was I really in those strange caves")
    print("or was it all just a strange dream?")


def usage():
    print("\tThe following command words are known to the system:\n\n\t",
          end="")
    for wort in allowed_commands:
        if wort == "tp" or wort == 'teleport':
            pass
        else:
            print("{} ".format(wort), end="")
    print("\n")


def generate_graphviz_file():
    print("Well, there are no maps to show...")
    import os
    import glob
    import generiere_karte
    os.system("mkdir -p Hoelle-Karten")
    result = glob.glob(r"Hoelle-Karten/*.py")
    if len(result) > 0:
        print(f"Welche Datei soll in einen Graphen umgewandelt werden?")
        for i in range(len(result)):
            print(f"{i+1} : {result[i]}")
        num = int(input("Gib mir die Nummer deiner Wunschdatei: "))
        wunschdatei = result[num - 1]
        generiere_karte.hauptprogramm(wunschdatei)
        antwort = input(f"Die Datei {wunschdatei} jetzt löschen?").lower()
        if antwort in ['y', 'j', 'yes', 'ja']:
            os.system(f"rm -f {wunschdatei}")


# w a s d as usual; j -> down; k -> up; q -> quit
allowed_commands = [
    "q", "w", "a", "s", "d", "j", "k", "look", "take", "pray", "map", "help"
]

raumliste = list(
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')


def generiere_ziel():
    if random.random() > 0.50:
        return raumliste[random.randrange(len(raumliste))]
    else:
        return None


north = {}
south = {}
east = {}
west = {}
upstairs = {}
downstairs = {}


def verbindungen_erzeugen():
    for raum in raumliste:
        for richtung in east, west, north, south, upstairs, downstairs:
            richtung[raum] = generiere_ziel()


verbindungen_erzeugen()

compass = {
    "w": north,
    "a": west,
    "s": south,
    "d": east,
    "k": upstairs,
    "j": downstairs
}

import metagenerator as generator

raumbeschreibung, rauminhalt, raumbiome = generator.hauptprogramm(raumliste)
description = raumbeschreibung
look_around = raumbiome

startraeume = raumliste
current_room = startraeume[random.randrange(len(startraeume))]
final_room = raumliste[random.randrange(len(raumliste))]
while final_room == current_room:
    final_room = raumliste[random.randrange(len(raumliste))]

command = ""
hungerstatus = 100
raumwechsel_erfolgt = True
print("\n\t*** Welcome to the hellish caves ***\n")
usage()
print("\n\tHave fun!\n")

while (current_room is not None):
    if raumwechsel_erfolgt:
        print(f"\nYou are here: {description[current_room]}. ", end='')
    else:
        raumwechsel_erfolgt = True
    hungerstatus = hungerstatus - 1
    if check_starvation(hungerstatus):
        current_room = None
        continue

    command = input("What do you want to do? ").lower()
    while command not in allowed_commands:
        command = input("No such command. What do you want to do? ").lower()
    if command == "q":
        quit()
        current_room = None
    elif command == "look":
        zeige_rauminhalt()
    elif command == "take":
        if (take(current_room)):
            current_room = None
    elif command == "pray":
        pray()
    elif command == 'map':
        generate_graphviz_file()
    elif command == 'help':
        usage()
    # Look up whether a path that way exists and if so, go to that room
    elif compass[command][current_room] is not None:
        previous_room = current_room
        current_room = compass[command][current_room]
        if current_room == 'B':
            if not check_key():
                current_room = previous_room
        if current_room == final_room:
            result = input(
                "Do you really want to leave the caves? [yes/No] ").lower()
            if result == "yes" or result == "y":
                current_room = None
                print("""
After all the hours spent in these interesting caves full of valuable treasures you decide to go out into the daylight.
""")
                print(
                    "You step through the waterfall and walk out.\nJust like that, and now it's all over."
                )
            else:
                continue
        verbindungen_erzeugen()

    else:
        print("Boom. You bounce off. It doesn't go that way. ", end="")
        raumwechsel_erfolgt = False
