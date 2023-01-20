#!/usr/bin/python3
#
# Generatoren und Meta-Generatoren
# (c) 2022 r.haerter@wut.de
#
import time
import random
random.seed(time.time())

# was auf dem Boden liegt, was man mitnehmen kann
items = [ "rubys", "emeralds", "amethysts", "sapphires", "lapis lazulis", "beryls", "garnets" ]

''' generate_description() erzeugt einen Raum '''
def generate_description(my_room, roomname):
    # die Räume sind hier Höhlen
    # die Größe "average" bräuchte eine Anpassung, es ist 'An average ...'
    sizes = [ "tiny", "small", "dinky", "little", "shrimpy", "medium", "normal", "large", "very large", "huge", "giant" ]
    rooms = [ "cave", "grotto", "chamber", "cavern", "antre" ]
    # was man in Höhlen so sieht
    things = [ "nothing special",
               "nothing special",
               "nothing special",
               "nothing special",
               "nothing special",
               "nothing special",
               "nothing special",
               "nothing special",
               "nothing special",
               "nothing special",
               "lakes",
               "gravel",
               "gravel",
               "gravel",
               "gravel",
               "gravel",
               "gravel",
               "rocks",
               "rocks",
               "rocks",
               "rocks",
               "stalagmites",
               "stalactites",
               "stalagmites",
               "stalactites",
               "stalagmites",
               "stalactites",
               "gemstones",
               "gemstones",
               "gemstones",
               "lichens",
               "lichens",
               "lichens",
               "lichens",
               "lichens",
               ]
    amounts = [ "no ", "a few ", "some ", "scattered ", "occasional ", "many ", "lots of " ]
    #
    size = sizes[random.randrange(len(sizes))]
    room = rooms[random.randrange(len(rooms))]
    thing = things[random.randrange(len(things))]
    if thing == "nothing special":
        amount = ""
    else:
        amount = amounts[random.randrange(len(amounts))]
    description = "A {} {} with {}{}".format(size,room,amount,thing)
    my_room[roomname] = description
    return True

''' any() wäre eine moderne Alternative zu dieser Funktion '''
def steintest(my_description):
    gesteine = ['gravel', 'rocks', "stalagmites", "stalactites" ]
    for stein in gesteine:
        if stein in my_description:
            return True
    return False

''' Passend zur Raumgröße und Menge eine Anzahl erzeugen '''
def wuerfle_anzahl_item(my_description):
    # die oben definierten Größenwörter aufgeteilt in drei Klassen
    klein = [ "tiny", "small", "dinky", "little", "shrimpy"]
    normal = ["medium", "normal"]
    #gross = ["large", "very large", "huge", "giant" ]
    anzahl = 0
    for size in klein:
        if size in my_description:
            anzahl = random.randrange(5) + 1
    for size in normal:
        if size in my_description:
            anzahl = random.randrange(9) + 2
    if anzahl > 0:
        kleine_menge = ["no ", "a few ", "some ", "scattered ", "occasional "]
        for menge in kleine_menge:
            if menge in my_description:
                anzahl = (anzahl // 2) + 1
    if 'large' in my_description:
        anzahl = random.randrange(13) + 3
    elif 'huge' in my_description:
        anzahl = random.randrange(17) + 5
    elif 'giant' in my_description:
        anzahl = random.randrange(23) + 7
    return anzahl

''' Rauminhalt generieren - je nach Wunsch mehr oder weniger viel '''
''' Die Anzahl wird ausgewertet und dazu passende Mengen Inhalt erzeugt. '''
''' Damit alle Antworten strukturell gleich sind, bestehen sie alle aus
    einer Zahl, einem Leerzeichen und dem eigentlichen Inhalt. '''
def generate_content(my_content, my_biom, roomname, my_description):
    anzahl_items = wuerfle_anzahl_item(my_description)
    if 'with no' in my_description:
        my_content[roomname] = "0 nix"
        my_biom[roomname] = "dry"
    elif 'gemstones' in my_description:
        my_content[roomname] = "{} ruby".format(anzahl_items)
        my_biom[roomname] = "gem" 
    elif 'lakes' in my_description:
        my_content[roomname] = "1 water"
        my_biom[roomname] = "wet"
    elif 'lichens' in my_description:
        my_content[roomname] = "{} lichen".format(anzahl_items * 3)
        my_biom[roomname] = "light"
    elif steintest(my_description):
        my_content[roomname] = "{} rocks".format(anzahl_items * 5)
        my_biom[roomname] = "stony"
    else:
        my_content[roomname] = '123456789 surprise' # sollte nicht erreicht werden
        my_biom[roomname] = ""
    return True

''' Das hauptprogramm() erzeugt
    + ein Dictionary voller Beschreibungen und
    + ein Dictionary mit dem zugehörigen Rauminhalt
    + ein Dictionary mit dem Biom '''
def hauptprogramm(raumliste):
    # Ein Dictionary voller Raumbeschreibungen 
    raumbeschreibung = {}
    # Ein Dictionary voller Rauminhalte und eines mit den Biomen
    rauminhalt = {}
    raumbiome = {}
    for raum in raumliste:
        generate_description(raumbeschreibung, raum)
        generate_content(rauminhalt, raumbiome, raum, raumbeschreibung[raum])
    # Beschreibungen und Inhalte als Tupel an die aufrufende Funktion
    return (raumbeschreibung, rauminhalt, raumbiome)

''' das testprogramm() probiert es aus, mit einfachen Namen '''
def testprogramm():
    raumnamen = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    raumliste = list(raumnamen)

    (raumbeschreibung, rauminhalt, raumbiome) = hauptprogramm(raumliste)
    for raum in raumbeschreibung:
        print("Raum {}: {} mit {} und Biom {}".format(raum,raumbeschreibung[raum],rauminhalt[raum], raumbiome[raum]))
    
if __name__ == "__main__":
    testprogramm()
