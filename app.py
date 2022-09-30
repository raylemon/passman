from controller.tuiController import TuiController
from controller.guiController import GuiController
from view.gui import MainGui
from model.data import Vault
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--console",help="Terminal User Interface")
    args = parser.parse_args()
    vault = Vault("data.db")

    if args.console:
        control = TuiController(vault)
        control.menu()
    else:
        control = GuiController(vault)
        view = MainGui()
        view.controller = control
        control.view = view
        control.start()
