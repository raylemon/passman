from model.data import User, Vault, VaultItem


class TestVault:
    def setup_method(self):
        self.vault = Vault(":memory:")
        self.toto = User("toto", "toto", uid=1)
        self.tata = User("tata", "tata", uid=2)
        self.item = VaultItem("unique", "toto", "pass", iid=1)

        users = [self.toto.to_array(), self.tata.to_array()]

        sql_users = "INSERT INTO T_Users (login, password) VALUES (?,?)"
        sql_item = (
            "INSERT INTO T_Items (name, login, password, fk_uid) VALUES (?,?,?,?)"
        )

        self.vault.connection.executemany(sql_users, users)
        self.vault.connection.execute(sql_item, [*self.item.to_array(), 1])
        self.vault.connection.commit()

    def test_add_user_success(self):
        user = User("test", "test")
        assert self.vault.add_user(user) is True

    def test_add_user_failure(self):
        wrong_user = User("toto", "")
        assert self.vault.add_user(wrong_user) is False

    def test_remove_user_success(self):
        assert self.vault.remove_user(self.toto) is True

    def test_remove_user_failure(self):
        user = User("", "")
        assert self.vault.remove_user(user) is False

    def test_remove_user_wrong_pass(self):
        user = User("toto", "123")
        assert self.vault.remove_user(user) is False

    def test_get_user(self):
        assert self.vault.get_user("toto") == self.toto

    def test_get_no_user(self):
        assert self.vault.get_user("") is None

    def test_user_exists(self):
        assert self.vault.user_exists(self.toto) is True

    def test_user_not_exists(self):
        user = User("nobody", "")
        assert self.vault.user_exists(user) is False

    def test_validate_user(self):
        assert self.vault.validate_user(self.toto) is True

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
        assert self.vault.delete_item(self.item) is True

    def test_delete_wrong_item(self):
        wrong_item = VaultItem("", "", "")
        assert self.vault.delete_item(wrong_item) is False

    def test_delete_wrong_user(self):
        self.item.iid = 2
        assert self.vault.delete_item(self.item) is False

    def test_edit_item_name(self):
        new_item = self.item
        new_item.name = "new_unique"
        assert self.vault.edit_item(self.item, new_item) is True

    def test_edit_item_login(self):
        new_item = self.item
        new_item.login = "new_login"
        assert self.vault.edit_item(self.item, new_item) is True

    def test_edit_item_password(self):
        new_item = self.item
        new_item.password = "new_pass"
        assert self.vault.edit_item(self.item, new_item) is True

    def test_edit_wrong_item(self):
        new_item = VaultItem("test", "test", "test")
        bad_item = VaultItem("", "", "")
        assert self.vault.edit_item(bad_item, new_item) is False

    def test_find_item(self):
        assert self.vault.find_items(self.toto, "uni") == [self.item]

    def test_find_no_items(self):
        assert self.vault.find_items(self.tata, "uni") == []
