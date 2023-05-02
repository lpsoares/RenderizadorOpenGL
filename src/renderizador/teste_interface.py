#!/usr/bin/env python
# -*- coding: utf-8 -*-


# https://github.com/pyimgui/pyimgui/tree/master/doc/examples

from imgui.integrations.glfw import GlfwRenderer
import OpenGL.GL as gl
import glfw
import imgui
import sys


def main():
    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)

    show_custom_window = True

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()



        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", "Cmd+Q", False, True
                )

                if clicked_quit:
                    sys.exit(0)

                imgui.end_menu()
            imgui.end_main_menu_bar()

        opened_state = True
        with imgui.begin("Example Tab Bar"):
            with imgui.begin_tab_bar("MyTabBar") as tab_bar:
                if tab_bar.opened:
                    with imgui.begin_tab_item("Item 1") as item1:
                        if item1.selected:
                            imgui.text("Here is the tab content!")

                    with imgui.begin_tab_item("Item 2") as item2:
                        if item2.selected:
                            imgui.text("Another content...")

                    with imgui.begin_tab_item("Item 3", opened=opened_state) as item3:
                        opened_state = item3.opened
                        if item3.selected:
                            imgui.text("Hello Saylor!")


        imgui.begin("Progress bar example")
        imgui.progress_bar(0.7, (100,20), "Overlay text")
        imgui.end()


        if show_custom_window:
            is_expand, show_custom_window = imgui.begin("Custom window", True)
            if is_expand:
                imgui.text("Bar")
                imgui.text_ansi("B\033[31marA\033[mnsi ")
                imgui.text_ansi_colored("Eg\033[31mgAn\033[msi ", 0.2, 1.0, 0.0)
                imgui.extra.text_ansi_colored("Eggs", 0.2, 1.0, 0.0)
            imgui.end()

        viewport = imgui.get_main_viewport()
        frame_height = imgui.get_frame_height()
        imgui.set_next_window_position(viewport.pos.x-1, viewport.pos.y + viewport.size.y - frame_height)
        imgui.set_next_window_size(viewport.size.x+2, frame_height)
        
        flags = imgui.WINDOW_NO_DECORATION | imgui.WINDOW_NO_INPUTS | \
                imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_SCROLL_WITH_MOUSE | \
                imgui.WINDOW_NO_SAVED_SETTINGS | \
                imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_NO_BACKGROUND | \
                imgui.WINDOW_MENU_BAR

        with imgui.begin("Status Bar", flags=flags):
            with imgui.begin_menu_bar() as menu_bar:
                imgui.text("Here!")
                

        gl.glClearColor(1.0, 1.0, 1.0, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


def impl_glfw_init():
    width, height = 1280, 720
    window_name = "minimal ImGui/GLFW3 example"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        sys.exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        sys.exit(1)

    return window


if __name__ == "__main__":
    main()