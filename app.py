users: dict[str, str] = {}  # dict[login,password]
vault: dict[
    str, dict[str, tuple[str, str]]
] = {}  # dict[user_login,dict[entry_name,tuple[login,password]]]


def list_entries(user_vault: dict[str, tuple[str, str]]) -> None:
    """
    List all entries
    :param user_vault: dictionary of entries
    :return: None
    """

    if len(user_vault) == 0:
        print("No entries yet.")
    else:
        for entry in user_vault.keys():
            print(entry)


def show_entry(user_vault: dict[str, tuple[str, str]]) -> None:
    """
    Show full details of selected entry
    :param user_vault: dictionary of entries
    :return: None
    """

    entry_id = input("Type entry name: ")
    if entry_id in user_vault.keys():
        entry = user_vault[entry_id]
        print(f"Login: {entry[0]}, MdP: {entry[1]}")
    else:
        print("No entry at this name.")


def edit_entry(user_vault: dict[str, tuple[str, str]]) -> None:
    """
    Update entry
    :param user_vault: dictionary of entries
    :return: None
    """
    entry_id = input("Type entry name: ")
    if entry_id in user_vault.keys():
        entry = user_vault[entry_id]
        new_name = input(f"Type new name ({entry_id}): ") or entry_id
        new_login = input(f"Type new entry login ({entry[0]}): ") or entry[0]
        new_password = input(f"Type new entry password ({entry[1]}): ") or entry[1]

        del user_vault[entry_id]
        user_vault[new_name] = (new_login, new_password)
    else:
        print("No entries found at this name.")


def delete_entry(user_vault: dict[str, tuple[str, str]]) -> None:
    """
    Remove an entry from vault
    :param user_vault: dictionary of entries
    :return: None
    """
    entry_id = input("Type entry name: ")
    if entry_id in user_vault.keys():
        del user_vault[entry_id]
    else:
        print("No entries found at this name.")


def add_entry(user_vault: dict[str, tuple[str, str]]) -> None:
    """
    Add an entry to the vault
    :param user_vault: dictionary of entries
    :return: None
    """
    entry_name = input("Type entry name (must be unique!): ")
    if entry_name not in user_vault.keys():
        entry_login = input("Type login: ")
        entry_password = input("Type password: ")

        entry = (entry_login, entry_password)
        user_vault[entry_name] = entry
    else:
        print("Name already exists. Please retry.")


def search_entry(user_vault: dict[str, tuple[str, str]]) -> None:
    """
    Search entries
    :param user_vault: dictionary of entries
    :return: None
    """
    search_string = input("Type beginning of entry name to search: ")
    for item in user_vault.keys():
        if item.startswith(search_string):
            print(item)


def vault_menu(user_vault: dict[str, tuple[str, str]]) -> None:
    """
    Show vault menu
    :param user_vault: dictionary of entries
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
            list_entries(user_vault)
        elif ch == "2":
            show_entry(user_vault)
        elif ch == "3":
            add_entry(user_vault)
        elif ch == "4":
            edit_entry(user_vault)
        elif ch == "5":
            delete_entry(user_vault)
        elif ch == "6":
            search_entry(user_vault)
        else:
            print("Choix invalide!")


def login() -> None:
    """
    Log user
    :return: None
    """
    log_in = input("Type your username: ")
    password = input("Type your password: ")
    if log_in not in users.keys():
        print("Unknown user. Please register first")
        return
    else:
        if password == users[log_in]:
            vault_menu(vault[log_in])
        else:
            print("Password mismatch")


def create_user() -> None:
    """
    Register new user
    :return: None
    """
    log_in = input("Type your username: ")
    password = input("Type your password:  ")
    confirm = input("Confirm your password: ")

    if password == confirm:
        if log_in in users.keys():
            print("User already exists. Pleas log in")
        else:
            users[log_in] = password
            vault[log_in] = {}
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
        if log_in in users.keys():
            del users[log_in]
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
    menu()