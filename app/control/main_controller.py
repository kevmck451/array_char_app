from app.control.View.Control_Window import Main_Window
from app.control.Controller.controller import Controller

if __name__ == "__main__":
    controller = Controller()
    gui = Main_Window(controller.handle_event)
    controller.set_gui(gui)
    gui.mainloop()

