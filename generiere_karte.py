#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (c) 2022 r.haerter@wut.de
#
# Dies ist ein kleiner Helfer, um die Karte aus dem selbst
# geschriebenen Textadventure als Bild darzustellen.
# Verwende dazu graphviz, das gibt es für jede Plattform.

# Feste Liste von idealerweise eindeutigen, nicht zu kurzen Namen für die Dictionaries
# Diese Liste muss man vielleicht an sein eigenes Textadventure anpassen!
dicts = [
    'north', 'east', 'south', 'west', 'upward', 'upstairs', 'downward',
    'downstairs', 'teleport', 'watchout'
]


# Zerlege die gefundenen Dictionaries
# ToDo: Man könnte die Richtung nutzen, um die Pfeile in den
#       generierten Graphen zu beschriften
def parse_direction(zeile):
    try:
        richtung, rest = zeile.split('=')
    except:
        if len(zeile) > 0:
            rest = zeile
        else:
            return 'fail'
    # Formatierungsartefakte entfernen
    neu = rest.replace("'", "")
    rest = neu.replace(" ", "")
    listenende = -1
    if rest.rstrip()[-1] == '\\':
        print(
            f"Fortsetzungszeichen erkannt. Deine Karte wird nicht vollständig sein."
        )
        listenende = -2
    # Das Ergebnis in eine Liste zurückverwandeln
    if rest[-1] == '}':
        verbindungsliste = list(rest[:-1].split(','))
    else:
        verbindungsliste = list(rest.strip()[1:listenende].split(','))
    return (verbindungsliste)


def erzeuge_graph(vliste):
    ergebnis = ""
    for element in vliste:
        if element == '':
            pass
        else:
            von, nach = element.split(':')
            if nach == 'None':
                pass
            else:
                if von.startswith('{'):
                    von = von[1:]
                result = f"{von}->{nach}\n"
                ergebnis += result
    return (ergebnis)


def schreibe_graphviz(graph, gvname):
    ergebnis = open(gvname, "w")
    result_head = '''
digraph Ravenswood {
layout=neato
'''
    result_tail = '''
overlap=false
splines=true
label="Your Textadventure Map layed out by Graphviz "
fontsize=12;
}
    '''
    ergebnis.write(result_head)
    ergebnis.write(graph)
    ergebnis.write(result_tail)
    ergebnis.flush()
    ergebnis.close()


def hauptprogramm(fname):
    pyname = fname
    filename, ext = pyname.split('.', 1)  # nur ein Punkt im Namen, bitte
    datei = open(pyname, 'r')
    gvname = filename + '.gv'

    alle_verbindungen = []
    fortsetzung = False
    komplett = False
    zeile = ""
    for line in datei.readlines():
        if line.startswith('#'):
            pass
        elif line.startswith('allowed_commands'):
            pass
        elif line.startswith('compass'):
            pass
        elif line.startswith('rauminhalt'):
            pass
        elif fortsetzung:
            zeile += line.strip()
            if '}' in line:
                fortsetzung = False
                komplett = True
        elif any(richtung in line for richtung in dicts):
            if '=' in line:
                if ':' in line:
                    zeile += line.strip()
                    fortsetzung = True
                if line.strip().endswith('{'):
                    fortsetzung = True
                    komplett = False
                if '}' in line:
                    komplett = True
                    fortsetzung = False
        if komplett == True:
            result = parse_direction(zeile)
            zeile = ""
            if result == 'fail':
                pass
            else:
                alle_verbindungen = alle_verbindungen + result
            komplett = False
    graph = erzeuge_graph(alle_verbindungen)
    schreibe_graphviz(graph, gvname)
    print("Fertig. Die Datei {} wurde erfolgreich erstellt".format(gvname))
    print(
        "Um diese Datei in ein Bild umzuwandeln, brauchst du Graphviz: https://graphviz.org/"
    )
    print(
        f"Damit kann jetzt mit dem Befehl 'neato -Tpng {gvname} > {filename}.png' ein Hausplan erstellt werden."
    )


if __name__ == '__main__':
    hauptprogramm()
