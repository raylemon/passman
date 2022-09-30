from controller.tuiController import TuiController
from model.data import Vault

if __name__ == "__main__":
    vault = Vault("data.db")
    control = TuiController(vault)
    control.menu()
