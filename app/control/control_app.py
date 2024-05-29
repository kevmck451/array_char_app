# Controller App for Phase Array Anechoic Chamber Characterization Experiment

from app.control.View.window import SpeakerControlApp
from app.control.Controller.controller import Controller


if __name__ == "__main__":

    controller = Controller()

    gui = SpeakerControlApp(controller.handle_event)
    controller.set_gui(gui)
    gui.mainloop()


