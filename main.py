import os

from mutagen.mp3 import EasyMP3

PATH = r'E:'

for file in os.scandir(PATH):
    if file.name.endswith('.mp3'):
        audio_file = EasyMP3(file)

        file_name = file.name[:-4]

        audio_file['title'] = file_name

        audio_file.save()
