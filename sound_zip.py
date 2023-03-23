import os
import tempfile
from PyQt5 import QtCore
import resources_rc


sounds = [':/sound/rs/type.mp3',
          ':/sound/rs/backspace.mp3',
          ':/sound/rs/newlist.mp3',
          ':/sound/rs/deletelist.mp3',
          ':/sound/rs/newstring.mp3']

sounds_paths = {}

for sound in sounds:
    temp_dir = tempfile.mkdtemp()
    sound_data = QtCore.QResource(sound).data()
    sound_name = sound.split("/")[-1]
    sound_path = os.path.join(temp_dir, sound_name)
    sounds_paths[sound_name] = sound_path

    with open(sound_path, "wb") as f:
        f.write(sound_data)


def get_sound(sound):
    return sounds_paths.get(sound)
