"""
Made by Mido.dev
Support me: https://github.com/MidoDev993

Puedes ver anime de AnimeFLV sin ver los anuncios de m*** :v
NT: vas a ver comentarios en ingles. los escribo asi por la costumbre, ayuda mucho en aprender el idioma xd
"""

import gui
import functionalities
from pathlib import Path


if __name__ == "__main__":
    path = Path(Path.home().joinpath("AnimeFLV media player/posters"))
    path.mkdir(parents=True, exist_ok=True)
    path = path.parent
    functionalities.path = path
    g = gui.show_gui()
    functionalities.api.close()

