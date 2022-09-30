from model.data import Vault, User, VaultItem
from view import tui


class TuiController:
    def __init__(self,vault:Vault):
        self.vault = vault
        self.current_user: User | None = None

    def list_entries(self) -> None:
        """
        List all entries
        :return: None
        """
        entries = self.vault.get_items(self.current_user)
        if len(entries) == 0:
            tui.show("No entries yet.")
        else:
            for entry in entries:
                tui.show(f"{entry.name}")

    def show_entry(self) -> None:
        """
        Show full details of selected entry
        :return: None
        """
        entry_id = tui.ask_user("Type entry name: ")
        entry = self.vault.get_item(self.current_user, entry_id)
        if entry is not None:
            tui.show(f"Login: {entry.login}, MdP: {entry.password}")
        else:
            tui.error("No entry at this name.")

    def edit_entry(self) -> None:
        """
        Update entry
        :return: None
        """
        entry_id = tui.ask_user("Type entry name: ")
        entry = self.vault.get_item(self.current_user, entry_id)
        if entry is not None:
            new_name = tui.ask_user(f"Type new name ({entry.name}): ", entry.name)
            new_login = tui.ask_user(
                f"Type new entry login ({entry.login}): ", entry.login
            )
            new_password = tui.ask_user(
                f"Type new entry password ({entry.password}): ", entry.password
            )

            new_entry = VaultItem(name=new_name, login=new_login, password=new_password)
            self.vault.edit_item(entry, new_entry)
        else:
            tui.error("No entries found at this name.")

    def delete_entry(self) -> None:
        """
        Remove an entry from vault
        :return: None
        """
        entry_id = tui.ask_user("Type entry name: ")
        entry = self.vault.get_item(self.current_user, entry_id)
        if entry is not None:
            self.vault.delete_item(entry)
        else:
            tui.error("No entries found at this name.")

    def add_entry(self) -> None:
        """
        Add an entry to the vault
        :return: None
        """
        entry_name = tui.ask_user("Type entry name (must be unique!): ")
        entry = self.vault.get_item(self.current_user, entry_name)
        if entry is None:
            entry_login = tui.ask_user("Type login: ")
            entry_password = tui.ask_user("Type password: ")

            entry = VaultItem(
                name=entry_name, login=entry_login, password=entry_password
            )
            self.vault.add_item(self.current_user, entry)
        else:
            tui.error("Name already exists. Please retry.")

    def search_entry(self) -> None:
        """
        Search entries
        :return: None
        """
        search_string = tui.ask_user("Type beginning of entry name to search: ")
        for item in self.vault.find_items(self.current_user, search_string):
            tui.show(f"{item.name}")

    def vault_menu(self, user: User) -> None:
        """
        Show vault menu
        :return: None
        """
        self.current_user = user

        while True:
            match tui.vault_menu():
                case "0":
                    return
                case "1":
                    self.list_entries()
                case "2":
                    self.show_entry()
                case "3":
                    self.add_entry()
                case "4":
                    self.edit_entry()
                case "5":
                    self.delete_entry()
                case "6":
                    self.search_entry()
                case _:
                    tui.error("Choix invalide!")

    def login(self) -> None:
        """
        Log user
        :return: None
        """
        log_in = tui.ask_user("Type your username: ")
        password = tui.ask_user("Type your password: ")
        user = self.vault.get_user(log_in)
        if user is None or user.password != password:
            tui.error("Unknown user or password mismatch. Try Again")

        else:
            self.vault_menu(user)

    def create_user(self) -> None:
        """
        Register new user
        :return: None
        """
        log_in = tui.ask_user("Type your username: ")
        password = tui.ask_user("Type your password:  ")
        confirm = tui.ask_user("Confirm your password: ")

        if password == confirm:
            user = User(login=log_in, password=password)
            if not self.vault.add_user(user):
                tui.show("User already exists. Please log in")
            else:
                tui.show("You are added. Please log in")
        else:
            tui.error("Password mismatch. Please try again")

    def remove_user(self) -> None:
        """
        Remove user
        :return: None
        """
        log_in = tui.ask_user("Type your username: ")
        password = tui.ask_user("Type your password: ")
        confirm = tui.ask_user("Confirm your password: ")

        if password == confirm:
            user = User(login=log_in, password=password)
            if self.vault.remove_user(user):
                tui.show("User removed from the system")
            else:
                tui.error("User not found")
        else:
            tui.error("Password mismatch. Please retry")

    def menu(self) -> None:
        """
        Main menu
        :return: None
        """
        while True:
            match tui.menu():
                case "0":
                    exit(0)
                case "1":
                    self.login()
                case "2":
                    self.create_user()
                case "3":
                    self.remove_user()
                case _:
                    tui.show("Invalid choice")
