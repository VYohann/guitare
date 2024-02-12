import pygame
import numpy as np
import time

tablature = [''] * 1

tablature[0] = '''
E||----------------------|----------------------|----------------------|
B||--3----3--------------|-------3---------3----|----------------------|
G||--2----2----2----2----|--2---------2---------|-------2---------2----|
D||------------2----2----|----------------------|--2---------2---------|
A||----------------------|----------------------|----------------------|
E||----------------------|----------------------|----------------------|
'''

def generate_guitar_note(frequency, duration, sample_rate):
    sample_points = int(duration * sample_rate)
    t = np.linspace(0, duration, sample_points, endpoint=False)
    guitar_wave = np.sin(frequency * t * 2 * np.pi) + np.sin(2 * frequency * t * 2 * np.pi) * 0.5
    # Dupliquer les données mono pour obtenir des données stéréo
    stereo_wave = np.column_stack((guitar_wave, guitar_wave))
    return (stereo_wave * 32767).astype(np.int16)

def play(corde, fret, channel):
    if corde < 1 or corde > 6:
        print("Numéro de corde invalide. Doit être entre 1 et 6.")
        return
    if fret < 0:
        print("Numéro de frette invalide. Doit être supérieur ou égal à 0.")
        return
    if channel == 0:
        pygame.mixer.init()
        channel = pygame.mixer.Channel(corde)
        
    frequencies = [82.41, 110.00, 146.83, 196.00, 246.94, 329.63]
    note_freq = frequencies[corde - 1] * 2 ** (fret / 12)

    duration = 0.8
    sample_rate = 44100
    note_wave = generate_guitar_note(note_freq, duration, sample_rate)
    
    # Jouer le son sur le canal spécifié
    channel.play(pygame.sndarray.make_sound(note_wave))
#exemple
#play(corde, fret, channel)   channel = 0 si simple note
play(1, 0, 0)
time.sleep(0.5)
play(1, 1, 0)
time.sleep(0.5)
play(1, 2, 0)
time.sleep(0.5)    

def play_tablature(tablature):
    lines = tablature.strip().split('\n')
    strings = lines
    strings.reverse()

    # Initialiser pygame
    pygame.mixer.init()

    # Créer des canaux sonores pour chaque corde
    channels = [pygame.mixer.Channel(i) for i in range(6)]

    # Initialiser la variable pour le délai entre chaque frette
    fret_delay = 0.10

    for i in range(len(strings[0])):
        notes_to_play = []  # Stocker les notes à jouer simultanément
        for j, string in enumerate(strings):
            if string[i].isdigit():
                note = int(string[i])
                if string[i+1] == '-' and string[i-1] == '-':
                    notes_to_play.append((j+1, note))  # Ajouter la note à la liste des notes à jouer
                elif string[i].isdigit() and string[i+1].isdigit():
                    notes_to_play.append((j+1, note+10+int(string[i+1])))  # Ajouter la note à la liste des notes à jouer
        
        # Jouer toutes les notes simultanément
        for corde, fret in notes_to_play:
            play(corde, fret, channels[corde-1])
        
        # Attendre le délai entre chaque frette
        time.sleep(fret_delay)

for tab in tablature:
    play_tablature(tab)
