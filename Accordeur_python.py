"""le code a l'air de déconner avec les octaves,
les notes sont toujours (quelques erreurs mais pas
souvent) justes mais pas les octaves"""

import math
import pyaudio
import wave
import numpy as np
import sys
import struct
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from scipy import signal
from scipy.io import wavfile
from scipy.fftpack import fft, ifft, fftfreq


# Enregistrement de l'audio

filename = "rec.wav"

chunk = 1024 # définition des paramètres d'enregistrements
FORMAT = pyaudio.paInt16
channels = 1
sample_rate = 44100
record_seconds = 2
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels = channels,
                rate = sample_rate,
                input = True,
                output = True,
                frames_per_buffer = chunk)

frames = []
print('Enregistrement en cours')
for i in range(int(44100 / chunk * record_seconds)):
    data = stream.read(chunk)
    stream.write(data)
    frames.append(data)
print('Fin')

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(filename, "wb") # Sauvegarde du fichier audio
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(sample_rate)
wf.writeframes(b"".join(frames))

wf.close()



# Analyse de la fréquence

frate,data = wavfile.read('rec.wav') # Récupération de l'audio enregistré précédemment

w = np.fft.fft(data) # Calcul et affichage de la fréquence
freqs = np.fft.fftfreq(len(w))

idx = np.argmax(np.abs(w))
freq = freqs[idx]
freqhz = abs(freq * frate)

##print(freqhz, "Hz")



# Importation des notes et fréquences d'Excel vers Python

source = open('fqnt.csv', 'r')
N, F = [], []
for row in csv.reader(source,delimiter=";"):
    N.append(row[0])
    F.append(row[1])


# Correspondance entre la fréquence et la note
v=int(input("précision"))
for i in range(len(N)):
    val=float(F[i])
    if val>=(freqhz-v) and val<=(freqhz+v):
        note = N[i]
        ##print(note)



# Affichage des résultats

a = "Ceci correspond à la note", note   # Si le programme affiche "'note' non défini", càd que la fréquence ne correspond à aucune note
b = "Fréquence =", freqhz
freql = [freqhz-0.005, freqhz, freqhz+0.005]

plt.plot(freqhz,freq,'bo-',lw=1,label='fréquence')
plt.legend()
plt.grid()
plt.tick_params(        #permet de supprimer la légende à gauche du graphique
    axis='y',
    which='both',
    left=False,
    right=False,
    labelleft=False)
plt.xlabel(b)
plt.ylabel(a)
plt.title("Résultats")
plt.show()
plt.savefig('plot')
plt.clf()