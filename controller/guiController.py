from __future__ import annotations

from hashlib import sha256

from model.data import Vault, User, VaultItem
from view.gui import MainGui


class GuiController:
    def __init__(self,vault:Vault):
        self._view = None
        self.vault = vault
        self.current_user: User | None = None
        self.entries: list[VaultItem] = []
        self.index = 0

    def start(self):
        self.view.mainloop()

    def register(self, log_in: str, password: str, confirm: str):
        if password == confirm:
            user = User(
                login=log_in, password=sha256(password.encode("utf-8")).hexdigest()
            )
            if not self.vault.add_user(user):
                self.view.info("User already exists. Please log in")
            else:
                self.view.info("You are added. Please log in")
        else:
            self.view.error("Password mismatch. Please try again")

    def login(self, log_in: str, password: str):
        user = self.vault.get_user(log_in)
        if (
            user is None
            or user.password != sha256(password.encode("utf-8")).hexdigest()
        ):
            self.view.error("Unknown user or password mismatch. Try again")
        else:
            self.current_user = user
            self.entries = self.vault.get_items(self.current_user)
            self.index = 0

            self.view.toggle_buttons(True)

    def show_item(self, item: VaultItem) -> None:
        self.view.show(item.name, item.login, item.password)

    def next(self):
        self.index += 1
        if self.index > len(self.entries):
            self.index = 0

        self.show_item(self.entries[self.index])

    def previous(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.entries) - 1

        self.show_item(self.entries[self.index])

    @property
    def view(self) -> MainGui:
        return self._view

    @view.setter
    def view(self, value: MainGui):
        self._view = value

    def remove_user(self, password: str):
        if self.current_user.password == sha256(password.encode("utf-8")).hexdigest():
            if self.vault.remove_user(self.current_user):
                self.view.info("User removed from the system")
            else:
                self.view.error("User not found")
        else:
            self.view.error("Password Mismatch")

    def add_item(self, name: str, login: str, password: str):
        item = self.vault.get_item(self.current_user, name)
        if item is None:
            item = VaultItem(name, login, password)
            if self.vault.add_item(self.current_user, item):
                self.view.info("Item successfully added to your vault")
                self.entries.append(item)
            else:
                self.view.error("Error")
        else:
            self.view.error("Name already exists. Please retry.")

    def edit_item(self, name: str, login: str, password: str):
        item = self.entries[self.index]
        new_item = VaultItem(name, login, password, iid=item.iid)
        self.vault.edit_item(item, new_item)

    def remove_item(self):
        item = self.entries[self.index]
        if self.vault.delete_item(item):
            self.view.info("Item successfully removed")

    def reset(self):
        self.current_user = None
        self.entries.clear()
        self.index = 0

    def search(self, search: str):
        if search == "":
            self.entries = self.vault.get_items(self.current_user)
        else:
            self.entries = self.vault.find_items(self.current_user, search)

        self.index = 0
        item = self.entries[self.index]
        self.view.show(item.name, item.login, item.password)
