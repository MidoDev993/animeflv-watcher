"""
GUI
"""
import dearpygui.dearpygui as dpg
import functionalities


def show_gui() -> None:
    dpg.create_context()
    dpg.create_viewport(
        title="AnimeFLV media player (fuck you ads! >:3) 1.0.0",
        small_icon="resources/images/favicon.ico",
        large_icon="resources/images/favicon.ico",
        width=640,
        height=480)
    dpg.setup_dearpygui()

    #ALL WINDOW FROM HEADER ->
    #PREFERENCES
    with dpg.window(label="Preferencias", modal=True, show= False, tag="Preferences"):
        dpg.add_slider_float(label="Escala global de las letras",
                             min_value=0.1, max_value=2,
                             default_value=1, 
                             callback=lambda sender, appdata: dpg.set_global_font_scale(appdata)
                             )


    #MAIN
    with dpg.window(tag="main"):

        #HEADER
        with dpg.menu_bar():
            dpg.add_button(label="Preferences", callback=lambda sender, appdata: dpg.show_item("Preferences"))
            #dpg.add_button(label="Creditos", tag="Creditos")


        #SECTIONS
        with dpg.tab_bar(reorderable=True):

            #ANIME INFORMATIONS
            with dpg.tab(label="Informacion de animes", tag="info_sec"):

                with dpg.group(horizontal=True): #BARRA DE BUSQUEDA
                    dpg.add_input_text(tag="bar_search", hint="Barra de busqueda. Aqui escribes hasta mondongo si quieres", user_data=1)
                    dpg.add_text(default_value="Buscando UwU (no me culpes de por tu internet de mierda)...", show=False, tag="waiting_logo") #do CHANGE FOR GIF LOADING
                    dpg.add_button(label="Buscar", callback=functionalities.search_list_anime, user_data=1)

                dpg.add_input_int(label="pagina actual", min_value=1, min_clamped=True, tag="change_page", show=False, callback=lambda sender, appdata: functionalities.search_list_anime(sender, appdata, appdata))

                with dpg.group(horizontal=True):
                    dpg.add_child_window(tag="anime_list", height=-1, width=320, horizontal_scrollbar=True, show=False)
                    dpg.add_child_window(tag="anime_info", height=-1, width=-1, horizontal_scrollbar=True, show=False)


            #do MEDIA PLAYER
            dpg.add_tab(label="Reproductor (cocinandose todavia :>)")

        dpg.focus_item("bar_search")

    dpg.set_primary_window(window="main", value=True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
