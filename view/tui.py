import colorama.ansi
from colorama import init, Fore, Style

init(autoreset=True)  # for colorama


def show(message: str):
    """
    Print message to screen
    :param message: message to write
    :return: Nothing
    """
    print(message)


def ask_user(message: str, default: str = None) -> str:
    """
    Read input from console
    :param message: prompt message
    :param default: default value
    :return: response from the user or default
    """
    return input(message) or default


def error(message: str):
    """
    Show error
    :param message: message to write
    :return: Nothing
    """
    print(Fore.RED + message)


def vault_menu() -> str:
    """
    Display vault menu
    :return: choice
    """
    print(colorama.ansi.clear_screen())
    print(Style.BRIGHT + "Your vault")
    print(
        """
    \r1. List entries
    \r2. Show entry
    \r3. Add entry
    \r4. Update entry
    \r5. Delete entry
    \r6. Search entry by name

    \r0. Back to main menu
    """
    )
    ch = ""
    while not ch.isdigit() and ch not in ["0", "1", "2", "3", "4", "5", "6"]:
        ch = ask_user("Your choice: ")
    return ch


def menu() -> str:
    """
    Display main menu
    :return: choice
    """
    print(colorama.ansi.clear_screen())
    print(Style.BRIGHT + "Passman - PASSword MANager")
    print(
        """
    \r1. Login
    \r2. New account
    \r3. Delete account

    \r0. Quit
    """
    )

    ch = ""
    while not ch.isdigit() or ch not in ["0", "1", "2", "3"]:
        ch = ask_user("Your choice: ")

    return ch
