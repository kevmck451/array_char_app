# Controller App for Phase Array Anechoic Chamber Characterization Experiment

from View.window import SpeakerControlApp
from Controller.controller import Controller


if __name__ == "__main__":

    controller = Controller()

    gui = SpeakerControlApp(controller.handle_event)
    controller.set_gui(gui)
    gui.mainloop()


