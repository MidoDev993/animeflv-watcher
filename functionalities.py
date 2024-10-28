"""
ALL THE FUNCTIONS FOR INTERACTION WITH THE GUI
"""

from animeflv import AnimeFLV
from pathlib import Path

import dearpygui.dearpygui as dpg
import requests
import webbrowser
from playsound import playsound
#import sqlite3

path = ""
api = AnimeFLV()


def search_list_anime(sender, appdata, current_page:int = 1) -> None:
    """
    SEARCH AND SHOW ALL ANIME LIST AS WRITTEN IN THE SEARCH BAR
    """

    if str(dpg.get_value("bar_search")).lower() == "mondongo":
        playsound("resources/audio/m.mp3")
        return

    is_searching(True, "anime_list")
    dpg.hide_item("change_page")


    try:
        anim = api.search(str(dpg.get_value("bar_search")).strip(), current_page)

    except Exception as ex:
        is_searching(False, "anime_list")
        print(ex)
        return


    if anim != []:
        for _ in anim:
            cover = path.joinpath(f"posters/{_.id}.png") #SEARCH FOR THE FILE ON THE PC

            #DOWNLOAD POSTER
            if not cover.is_file():
                response = requests.get(_.poster)

                if response.status_code == 200:
                    with open(f"{cover}", 'wb') as file:
                        file.write(response.content)

                else:
                    cover = Path("resources/images/cover-not-found.png").absolute()
            #-----------------

            #ADD THE INFORMATION
            with dpg.group(parent="anime_list"):

                #LOAD COVER
                width, height, channels, data = dpg.load_image(str(cover))
                
                if dpg.does_alias_exist(f"{_.id}_poster"):
                    dpg.remove_alias(f"{_.id}_poster")

                with dpg.texture_registry(show=False):
                    dpg.add_static_texture(width=width, height=height, default_value=data, tag=f"{_.id}_poster")
                #----------

                with dpg.group(horizontal=True):
                    dpg.add_image_button(texture_tag=f"{_.id}_poster", width=130, height=185, callback=anime_info_complete, user_data=_.id) #IMAGE COVER

                    with dpg.group():
                        dpg.add_text(default_value=f"Title: {_.title}", bullet=True)
                        dpg.add_text(default_value=f"Type: {_.type}", bullet=True)
                        dpg.add_text(default_value=f"Episodes: {_.episodes}", bullet=True)

                dpg.add_separator()

    else:
        dpg.add_text(default_value='F por ti amige (intentalo una vez mas por si acaso)', parent="anime_list")

    is_searching(False, "anime_list")
    dpg.show_item("change_page")
    dpg.set_value("change_page", current_page)



def anime_info_complete(sender, app_data, userdata) -> None:
    """
    SHOW ALL INFORMATION COMPLETE (INCLUDING ALL LINKS)
    """
    #USER DATA IS THE "id" OF ANIME SELECTED

    is_searching(True, "anime_info")

    if dpg.does_alias_exist("full_cover"):
        dpg.remove_alias("full_cover")

    try:
        anim = api.get_anime_info(userdata)

    except Exception as ex:
        is_searching(False, "anime_info")
        print(ex)
        return

    cover = path.joinpath(f"posters/{userdata}.png") #SEARCH COVER ON THE PC
    width, height, channels, data = dpg.load_image(str(cover))

    with dpg.group(horizontal=True, parent="anime_info"):
        with dpg.texture_registry(show=False):
            dpg.add_static_texture(width=width, height=height, default_value=data, tag="full_cover")

        dpg.add_image(texture_tag=f"full_cover", width=260, height=370) #IMAGE COVER

        with dpg.group():
            #INFO
            dpg.add_text(default_value=f"Titulo: {anim.title}", bullet=True)
            dpg.add_text(default_value=f"Rating: {anim.rating}", bullet=True)
            dpg.add_text(default_value=f"Sipnosis:\n{salto_de_linea(anim.synopsis)}", bullet=True)
            dpg.add_text(default_value=f"Tipo: {anim.type}", bullet=True)
            dpg.add_text(default_value=f"Genero(s): {', '.join(anim.genres)}", bullet=True)
            dpg.add_text(default_value=f"Episodios: {len(anim.episodes)}", bullet=True)
            dpg.add_text(default_value=f"Debut: {anim.debut}", bullet=True)

    try:
        #LINKS
        with dpg.tab_bar(reorderable=True,  parent="anime_info"):
            with dpg.tab(label="Episodios"):
                for ep in range(1, len(anim.episodes)+1):
                    link = api.get_video_servers(userdata, ep)[0]

                    #ALL THE LINKS OF THE ONLY EPISODE
                    with dpg.tree_node(label=str(ep)):
                        with dpg.group(horizontal=True):
                            for servers in link:
                                dpg.add_button(label=servers["title"], user_data=servers["code"], callback=lambda sender, app_data, userdata: webbrowser.open(userdata))


            with dpg.tab(label="Links de descarga"):
                for ep in range(1, len(anim.episodes)+1):
                    link = api.get_links(userdata, ep)

                    with dpg.tree_node(label=str(ep)):
                        with dpg.group(horizontal=True):
                            for server in link:
                                dpg.add_button(label=server.server, user_data=server.url, callback=lambda sender, app_data, userdata: webbrowser.open(userdata))


    except Exception as ex:
        is_searching(False, "anime_info")
        print(ex)
        return

    is_searching(False, "anime_info")



def is_searching(x: bool, item:str) -> None:
    if x:
        dpg.hide_item(item)
        dpg.delete_item(item, children_only=True)
        dpg.show_item("waiting_logo")
        dpg.configure_viewport(item=None, disable_close=True)

    else:
        dpg.hide_item("waiting_logo")
        dpg.show_item(item)
        dpg.configure_viewport(item=None, disable_close=False)
        api.close()



 #TEMP
def salto_de_linea(text: str, each_spaces: int = 20) -> str:
    text = text.split(" ")
    new_text = []
    longitud = int(len(text)/each_spaces) + 2

    b = 0
    for i in range(1, longitud):
        new_text.append(" ".join( text[ b: i*each_spaces ]  ))
        b = (i*each_spaces)

    new_text = "\n".join(new_text)
    return new_text

