class User:
    def __init__(self, login: str, password: str) -> None:
        self.login = login
        self.password = password

    def __repr__(self):
        return f"{self.login} {self.password}"

    def __hash__(self):
        return hash(self.login + self.password)

    def __eq__(self, other):
        return self.login == other.login


class VaultItem:
    def __init__(self, name: str, login: str, password: str) -> None:
        self.name = name
        self.login = login
        self.password = password


class Vault:
    user_vault: dict[User, set[VaultItem]] = {}

    def add_user(self, user: User) -> bool:
        if self.user_exists(user):
            return False
        else:
            self.user_vault[user] = set()
            return True

    def remove_user(self, user: User) -> bool:
        if user in self.user_vault.keys():
            del self.user_vault[user]
            return True
        else:
            return False

    def user_exists(self, user: User) -> bool:
        for u in self.user_vault.keys():
            if user.login == u.login:
                return True
        else:
            return False

    def validate_user(self, user: User) -> bool:
        if self.user_exists(user):
            for u in self.user_vault.keys():
                if u.login == user.login:
                    return user.password == u.password
        else:
            return False

    def get_items(self, user: User) -> list[VaultItem]:
        return list(self.user_vault[user])

    def get_item(self, user: User, name: str) -> VaultItem | None:
        for item in self.user_vault[user]:
            if item.name == name:
                return item
        else:
            return None

    def edit_item(self, user: User, old_item: VaultItem, new_item: VaultItem) -> bool:
        return self.delete_item(user, old_item) and self.add_item(user, new_item)

    def add_item(self, user: User, item: VaultItem) -> bool:
        if item in self.user_vault[user]:
            return False
        else:
            self.user_vault[user].add(item)
            return True

    def delete_item(self, user: User, item: VaultItem) -> bool:
        try:
            self.user_vault[user].remove(item)
            return True
        except KeyError:
            return False

    def find_items(self, user: User, search_string: str) -> list[VaultItem]:
        lst = []
        for item in self.user_vault[user]:
            if item.name.startswith(search_string):
                lst.append(item)
        return lst
