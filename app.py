from data import Vault, User, VaultItem


def list_entries(user: User) -> None:
    """
    List all entries
    :param user: owner
    :return: None
    """
    entries = vault.get_items(user)
    if len(entries) == 0:
        print("No entries yet.")
    else:
        for entry in entries:
            print(entry.name)


def show_entry(user: User) -> None:
    """
    Show full details of selected entry
    :param user: owner
    :return: None
    """
    entry_id = input("Type entry name: ")
    entry = vault.get_item(user, entry_id)
    if entry is not None:
        print(f"Login: {entry.login}, MdP: {entry.password}")
    else:
        print("No entry at this name.")


def edit_entry(user: User) -> None:
    """
    Update entry
    :param user: owner
    :return: None
    """
    entry_id = input("Type entry name: ")
    entry = vault.get_item(user, entry_id)
    if entry is not None:
        new_name = input(f"Type new name ({entry.name}): ") or entry.name
        new_login = input(f"Type new entry login ({entry.login}): ") or entry.login
        new_password = (
            input(f"Type new entry password ({entry.password}): ") or entry.password
        )

        new_entry = VaultItem(name=new_name, login=new_login, password=new_password)
        vault.edit_item(user, entry, new_entry)
    else:
        print("No entries found at this name.")


def delete_entry(user: User) -> None:
    """
    Remove an entry from vault
    :param user: owner
    :return: None
    """
    entry_id = input("Type entry name: ")
    entry = vault.get_item(user, entry_id)
    if entry is not None:
        vault.delete_item(user, entry)
    else:
        print("No entries found at this name.")


def add_entry(user: User) -> None:
    """
    Add an entry to the vault
    :param user: owner
    :return: None
    """
    entry_name = input("Type entry name (must be unique!): ")
    entry = vault.get_item(user, entry_name)
    if entry is None:
        entry_login = input("Type login: ")
        entry_password = input("Type password: ")

        entry = VaultItem(name=entry_name, login=entry_login, password=entry_password)
        vault.add_item(user, entry)
    else:
        print("Name already exists. Please retry.")


def search_entry(user: User) -> None:
    """
    Search entries
    :param user: owner
    :return: None
    """
    search_string = input("Type beginning of entry name to search: ")
    for item in vault.find_items(user, search_string):
        print(item.name)


def vault_menu(user: User) -> None:
    """
    Show vault menu
    :param user: owner
    :return: None
    """
    while True:
        print("Your vault")
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
            ch = input("Your choice: ")

        if ch == "0":
            return
        elif ch == "1":
            list_entries(user)
        elif ch == "2":
            show_entry(user)
        elif ch == "3":
            add_entry(user)
        elif ch == "4":
            edit_entry(user)
        elif ch == "5":
            delete_entry(user)
        elif ch == "6":
            search_entry(user)
        else:
            print("Choix invalide!")


def login() -> None:
    """
    Log user
    :return: None
    """
    log_in = input("Type your username: ")
    password = input("Type your password: ")
    user = User(log_in, password)
    if not vault.validate_user(user):
        print("Unknown user or password mismatch. Try Again")

    else:
        vault_menu(user)


def create_user() -> None:
    """
    Register new user
    :return: None
    """
    log_in = input("Type your username: ")
    password = input("Type your password:  ")
    confirm = input("Confirm your password: ")

    if password == confirm:
        user = User(login=log_in, password=password)
        if not vault.add_user(user):
            print("User already exists. Please log in")
        else:
            print("You are added. Please log in")
    else:
        print("Password mismatch. Please try again")


def remove_user() -> None:
    """
    Remove user
    :return: None
    """
    log_in = input("Type your username: ")
    password = input("Type your password: ")
    confirm = input("Confirm your password: ")

    if password == confirm:
        user = User(login=log_in, password=password)
        if vault.remove_user(user):
            print("User removed from the system")
        else:
            print("User not found")
    else:
        print("Password mismatch. Please retry")


def menu() -> None:
    """
    Main menu
    :return: None
    """
    while True:
        print("Passman - PASSword MANager")
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
            ch = input("Your choice: ")

        if ch == "0":
            exit(0)
        elif ch == "1":
            login()
        elif ch == "2":
            create_user()
        elif ch == "3":
            remove_user()
        else:
            print("Invalid choice")


# main app launcher
if __name__ == "__main__":
    vault: Vault = Vault()
    menu()
