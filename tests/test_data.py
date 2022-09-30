from model.data import User, Vault, VaultItem


class TestVault:
    def setup_method(self, method):
        self.vault = Vault()
        self.toto = User("toto", "toto")
        self.tata = User("tata", "tata")
        self.vault.user_vault[self.toto] = set()
        self.vault.user_vault[self.tata] = set()
        self.item = VaultItem("unique", "toto", "pass")
        self.vault.user_vault[self.toto].add(self.item)

    def test_add_user_success(self):
        user = User("test", "test")
        assert self.vault.add_user(user) is True

    def test_add_user_failure(self):
        user = User("test", "")
        assert self.vault.add_user(user) is False

    def test_remove_user_success(self):
        user = User("toto", "toto")
        assert self.vault.remove_user(user) is True

    def test_remove_user_failure(self):
        user = User("", "")
        assert self.vault.remove_user(user) is False

    def test_remove_user_wrong_pass(self):
        user = User("toto", "123")
        assert self.vault.remove_user(user) is False

    def test_user_exists(self):
        user = User("toto", "toto")
        assert self.vault.user_exists(user) is True

    def test_user_not_exists(self):
        user = User("nobody", "")
        assert self.vault.user_exists(user) is False

    def test_validate_user(self):
        user = User("toto", "toto")
        assert self.vault.validate_user(user) is True

    def test_wrong_password(self):
        user = User("toto", "")
        assert self.vault.validate_user(user) is False

    def test_wrong_user(self):
        user = User("nobody", "")
        assert self.vault.validate_user(user) is False

    def test_list_items(self):
        assert self.vault.get_items(self.toto) == [self.item]

    def test_list_empty(self):
        assert self.vault.get_items(self.tata) == []

    def test_get_item(self):
        assert self.vault.get_item(self.toto, "unique") == self.item

    def test_no_items(self):
        assert self.vault.get_item(self.toto, "nothing") is None

    def test_get_item_wrong_user(self):
        assert self.vault.get_item(self.tata, "unique") is None

    def test_add_item(self):
        item = VaultItem("test", "test", "test")
        assert self.vault.add_item(self.toto, item) is True

    def test_add_item_no_unique(self):
        assert self.vault.add_item(self.toto, self.item) is False

    def test_delete_item(self):
        assert self.vault.delete_item(self.toto, self.item) is True

    def test_delete_wrong_item(self):
        wrong_item = VaultItem("", "", "")
        assert self.vault.delete_item(self.toto, wrong_item) is False

    def test_delete_wrong_user(self):
        assert self.vault.delete_item(self.tata, self.item) is False

    def test_edit_item_name(self):
        new_item = self.item
        new_item.name = "new_unique"
        assert self.vault.edit_item(self.toto, self.item, new_item) is True

    def test_edit_item_login(self):
        new_item = self.item
        new_item.login = "new_login"
        assert self.vault.edit_item(self.toto, self.item, new_item) is True

    def test_edit_item_password(self):
        new_item = self.item
        new_item.password = "new_pass"
        assert self.vault.edit_item(self.toto, self.item, new_item) is True

    def test_edit_wrong_item(self):
        new_item = VaultItem("test", "test", "test")
        bad_item = VaultItem("", "", "")
        assert self.vault.edit_item(self.toto, bad_item, new_item) is False
