# https://www.helloworld.cc - Heft 1 - Seite 52
# Scary cave game -- Original Version CC BY-NC-SA 3.0
# Diese modifizierte Version (C) 2022 Roland Härter r.haerter@wut.de
#
# Umgebaute Version von Ravenswood Manor. Hier ist kein Haus mehr,
# sondern ein generiertes Set von Höhlen.

import time
import sys
import random

# Diese Funktion prüft, ob man einen Schlüssel für den Raum hat.
# Zuerst einmal fragt sie den Spieler höflich, das reicht zum Testen.
def check_key():
    key = input("Do you have the key? ").lower()
    if key in [ "j", "ja", "y", "yes" ]:
        return True
    else:
        return False

'''
# Eine Funktion für das Mitnehmen von Zeug, ursprünglich einmal mit fiesen Fallen
# return: True -> du bist raus, also gestorben, hier nicht genutzt
# Diese Funktion nimmt noch nichts mit, da dafür noch keine Datenstrukturen vorhanden sind
'''
def take(raum):
    global hungerstatus
    global rauminhalt
    gefunden = False
    ding = input("What do you want to take? ").lower().rstrip()
    anzahl,zeug = rauminhalt[raum].split(' ',1)
    if ding == zeug:
        print (f"Each of the {anzahl} {zeug} is too heavy to take with you.")
        gefunden = True
        ''' man sollte etwas essen können '''
        if zeug == 'lichen' and int(anzahl) > 0:
            ''' außer Flechten gibt es nichts essbares in diesen Höhlen '''
            hungerstatus += random.randint(7,24)
            ''' die Flechten werden weniger '''
            rauminhalt[raum] = "{} {}".format(int(anzahl)-1,zeug)
    if ( gefunden == False ):
        print ("I see here no %s" % (ding) )
    return False

# Diese Funktion gibt den Hungerlevel aus
# Andere Effekte können die Variable hungerstatus abfragen
def check_starvation(hungerlevel):
    if hungerlevel < 1:
        print ("You die from lack of food ...")
        return True
    elif hungerlevel < 10:
        print ("You are so weak that you can hardly walk.")
    elif hungerlevel < 20:
        print ("Your stomach growls so loudly that you are afraid of attracting monsters.")
    elif hungerlevel < 50:
        print ("You feel weak. Something to eat would be good now.")
    else:
        print ("You are well. You are full and happy.")
    return False

'''
 Beten hilft, wenn man keinen Ausweg hat. Das entspricht
 dem Spiel 'nethack', abgesehen von den fehlenden Göttern ...

 Hier könnte man das Spiel erweitern. Einen Zähler einbauen,
 und das Beten begrenzen. Oder Gegenrechnen mit erreichten Zielen...
 '''
def pray():
    print("A strange trembling passes through the room.")
    verbindungen_erzeugen()

# Zur Zeit ist nur das Biom in 'look_around' und der Rauminhalt ist
# lediglich generiert
def zeige_rauminhalt():
    inhalt = rauminhalt[current_room]
    print ( inhalt )

# Man kann das Spiel jederzeit verlassen.
def quit():
    print ("There is a bang. Smoke rises. You faint.")
    for i in range(3):      # default: 23 Sekunden, Debug: 3 Sekunden
        time.sleep(1)
        print (".",end="")
        sys.stdout.flush()  # damit die Punkte einzeln erscheinen
    print ("\n\nYou wake up in a meadow of flowers and wonder:")
    print ("Was I really in those strange caves")
    print ("or was it all just a strange dream?")

# Die kurze Anleitung gibt bisher einfach nur die Kommandowörter aus
def usage():
    print ("\tThe following command words are known to the system:\n\n\t",end="")
    for wort in allowed_directions:
        # Mache 'tp' (Teleport) zu einem geheimen Kommando
        if wort == "tp" or wort == 'teleport':
            pass
        else:
            print ("{} ".format(wort),end="")
    print ("\n\n\tViel Spaß\n")

def generate_graphviz_file():
  import os
  import glob
  import generiere_karte
  os.system("mkdir -p Hoelle-Karten")
  result = glob.glob(r"Hoelle-Karten/*.py")
  if len(result) >  0:
    print(f"Welche Datei soll in einen Graphen umgewandelt werden?")
    for i in range(len(result)):
      print(f"{i+1} : {result[i]}")
    num = int(input("Gib mir die Nummer deiner Wunschdatei: "))
    wunschdatei = result[num-1]
    generiere_karte.hauptprogramm(wunschdatei)
    antwort = input(f"Die Datei {wunschdatei} jetzt löschen?").lower()
    if antwort in ['y','j','yes','ja']:
      os.system(f"rm -f {wunschdatei}")
    

# Where can I go from each direction?
# j -> down ; k -> up ; q -> quit
allowed_directions = ["q", "w", "a", "s", "d", "j", "k", "look", "take", "pray", "map", "help"]

# Zufällig generierte Höhlen in fast beliebiger Zahl und Menge
# Begrenzend ist die Zahl der nutzbaren Zeichen, aber man darf
# UTF-8-Zeichen verwenden, wenn man möchte
raumliste = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') # 62 Räume billig erzeugt

'''
Hier werden die Verbindungen der Räume in der Raumliste
zufällig verbunden, mit einer gewissen Wahrscheinlichkeit,
damit es nicht zuviele Verbindungen gibt.
Notfalls - wenn es keinen Ausweg gibt - kann der Spieler
beten 'pray', um ein neues Set Verbindungen zu erzeugen
'''
# Was mir gut gefallen hat, ist die Idee, die speziellen Räume
# aus der Raumliste zu nehmen, bevor man wilde zufällige Dinge
# generiert, und anschließend die speziellen Räume wieder gezielt
# einzufügen.
def generiere_ziel():
    if random.random() > 0.70:  # 30% Wahrscheinlichkeit reicht bei 6 Richtungen
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
    '''
    # das folgende läuft gut unter Linux auch im repl.it ...
    # Ab hier dann für jedes Level einmal rausschreiben, wie es aussieht.
    # Diese Dateien kann man dann mit `generiere_karte.py` umwandeln
    import os
    richtungsname = [ 'east', 'west', 'north', 'south', 'upstairs', 'downstairs' ]
    os.system("mkdir -p Hoelle-Karten")
    datei = open (''.join(('Hoelle-Karten/',str(time.time()),'.py')), "w")
    nummer = 0
    for richtung in east, west, north, south, upstairs, downstairs:
        datei.write("{} = ".format(richtungsname[nummer]))
        nummer += 1
        datei.write(str(richtung))
        datei.write("\n")
    datei.flush()
    datei.close()
    '''
    
verbindungen_erzeugen()

# Put the directions into a compass dictionary
compass = { "w": north, "a": west, "s": south, "d": east, "k": upstairs, "j": downstairs }

import metagenerator as generator
raumbeschreibung, rauminhalt, raumbiome = generator.hauptprogramm(raumliste)
description = raumbeschreibung
look_around = raumbiome # billiger 'hack', um überhaupt etwas in 'look_around' zu haben
#rauminhalt = rauminhalt

# Put in the number of the room you want them to start in
# Man kann das Spiel ein wenig spannender machen, in dem man
# den Startraum zufällig wählt.
# Das ist einfacher als ein ganzes Labyrinth zu generieren.
# Reiner Zufall kann aber zu doofen Lösungen führen, deshalb ist hier
# eine zufällige Auswahl aus einer Liste möglicher Starträume die Lösung
startraeume = raumliste  ## [ 0, 9, 10, 18 ]
current_room = startraeume[random.randrange(len(startraeume))]
# Put in the number of the final room
final_room = raumliste[random.randrange(len(raumliste))]
while final_room == current_room:
    final_room = raumliste[random.randrange(len(raumliste))]

# ------------------------------------------------------------
# Code to move around the map
# ------------------------------------------------------------
command = ""
hungerstatus = 100
raumwechsel_erfolgt = True
print ("\n\t*** Welcome to the hellish caves ***\n")
usage()
while( current_room is not None ):
    if raumwechsel_erfolgt:
        print (f"\nYou are here: {description[current_room]}. ",end='')
    else:
        raumwechsel_erfolgt = True
    hungerstatus = hungerstatus - 1
    if check_starvation(hungerstatus):
        current_room = None
        continue

    # Ask what they want to do and validate it (north, south, east, west only)
    command = input("Which direction do you want to go? ").lower()
    while command not in allowed_directions:
        command = input("Which direction do you want to go? ").lower()
    # Man kann verhungern ...
    if command == "q":
        quit()      #   das Spiel freiwillig aufgeben :-/
        current_room = None
    elif command == "look":
        zeige_rauminhalt()
    elif command == "take":
        if ( take(current_room) ):
            current_room = None     # you managed to die :-)
    # Wenn sonst nichts geht, kann man beten und bekommt neue Verbindungen.
    elif command == "pray":
        pray()
    elif command == 'map':
        generate_graphviz_file()
    elif command == 'help':
        usage()
    # Look up whether a path that way exists and if so, go to that room
    elif compass[command][current_room] is not None:
        # Wenn man einen Raum nicht betreten kann oder darf,
        # geht es wieder zurück, und man bleibt draußen
        previous_room = current_room
        current_room = compass[command][current_room]

        # Es kann verschlossene Höhlen geben (nicht fragen), hier z.B. Raum B
        if current_room == 'B':  # irgend ein Raum muss es sein, das ganze ist bislang nur ein Prototyp
            if not check_key():
                current_room = previous_room
        # See if they are in the final room
        if current_room == final_room:
            result = input ("Do you really want to leave the caves? [yes/No] ").lower()
            if result == "yes" or result == "y":
                current_room = None # Ends the game loop
                print("""
After all the hours spent in these interesting caves full of valuable treasures you decide to go out into the daylight.
""")
                print("You step through the waterfall and walk out.\nJust like that, and now it's all over.")
            else:
                continue
        # Erst und nur nach dem Wechsel in die nächste Höhle wird das Labyrinth neu vernetzt.
        # Das gibt dem Spieler die Möglichkeit, verschiedene Richtungen zu probieren.
        verbindungen_erzeugen() # In der Hölle bleibt kein Weg, wo er eben noch war.

    else:
        print ("Boom. You bounce off. It doesn't go that way. ",end="")
        raumwechsel_erfolgt = False

