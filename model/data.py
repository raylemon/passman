import sqlite3


class User:
    def __init__(self, login: str, password: str, uid: int = -1) -> None:
        self.login = login
        self.password = password
        self.uid = uid

    def __repr__(self):
        return f"{self.login} {self.password}"

    def __hash__(self):
        return hash(self.login + self.password)

    def __eq__(self, other):
        return self.login == other.login

    def to_array(self) -> list[str]:
        return [self.login, self.password]


class VaultItem:
    def __init__(self, name: str, login: str, password: str, iid: int = -1) -> None:
        self.name = name
        self.login = login
        self.password = password
        self.iid = iid

    def to_array(self) -> list[str]:
        return [self.name, self.login, self.password]

    def __repr__(self):
        return f"name = {self.name}, login = {self.login}, pass= {self.password}"

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.login == other.login
            and self.password == other.password
        )


class Vault:
    def __init__(self, db_path: str):
        """

        :param db_path:
        """
        self.connection = sqlite3.connect(db_path)
        if not self.table_exists():
            self.create_tables()

    def __del__(self):
        """

        :return:
        """
        self.connection.close()

    def table_exists(self) -> bool:
        """

        :return:
        """
        sql_test = "SELECT * FROM sqlite_master WHERE name = ? AND TYPE = ?"
        try:
            result = self.connection.execute(sql_test, ["T_Users", "table"])
            return result.rowcount == 1
        except sqlite3.DatabaseError:
            return False

    def create_tables(self) -> None:
        """

        :return:
        """

        sql_create_users = """ CREATE TABLE IF NOT EXISTS T_Users (
                                uid INTEGER PRIMARY KEY AUTOINCREMENT ,
                                login TEXT UNIQUE NOT NULL ,
                                password TEXT NOT NULL
        )"""

        sql_create_items = """ CREATE TABLE IF NOT EXISTS T_Items (
                                iid INTEGER PRIMARY KEY AUTOINCREMENT ,
                                name TEXT UNIQUE NOT NULL ,
                                login TEXT NOT NULL ,
                                password TEXT,
                                fk_uid INTEGER REFERENCES T_Users(uid) ON DELETE CASCADE 
        )"""

        try:
            self.connection.execute(sql_create_users)
            self.connection.execute(sql_create_items)
            self.connection.commit()
        except sqlite3.DatabaseError as dbe:
            print(dbe)

    def add_user(self, user: User) -> bool:
        """

        :param user:
        :return:
        """
        sql_add_user = "INSERT INTO T_Users (login, password) VALUES (?,?)"
        try:
            self.connection.execute(sql_add_user, user.to_array())
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def remove_user(self, user: User) -> bool:
        """

        :param user:
        :return:
        """
        sql_remove_user = "DELETE FROM T_Users WHERE uid = ?"
        try:
            result = self.connection.execute(sql_remove_user, [user.uid])
            self.connection.commit()
            return result.rowcount > 0
        except sqlite3.IntegrityError:
            return False

    def user_exists(self, user: User) -> bool:
        """

        :param user:
        :return:
        """
        sql_query = "SELECT uid FROM T_Users WHERE login = ?"
        try:
            result = self.connection.execute(sql_query, [user.login])
            return result.fetchone()[0] > 0
        except sqlite3.IntegrityError:
            return False
        except TypeError:
            return False

    def validate_user(self, user: User) -> bool:
        """

        :param user:
        :return:
        """
        sql_query = "SELECT COUNT(uid) FROM T_Users WHERE login = ? AND password = ?"
        try:
            result = self.connection.execute(sql_query, user.to_array())
            return result.fetchone()[0] > 0
        except sqlite3.IntegrityError:
            return False

    def get_user(self, login: str) -> User | None:
        """

        :param login:
        :return:
        """
        sql_query = "SELECT * FROM T_Users WHERE login = ?"
        try:
            result = self.connection.execute(sql_query, [login])
            result.row_factory = lambda cursor, row: User(
                uid=row[0], login=row[1], password=row[2]
            )
            return result.fetchone()
        except sqlite3.IntegrityError:
            return None

    def get_items(self, user: User) -> list[VaultItem]:
        """

        :param user:
        :return:
        """
        sql_list_items = "SELECT * FROM T_Items WHERE fk_uid = ?"
        try:
            result = self.connection.execute(sql_list_items, [user.uid])
            result.row_factory = lambda cursor, row: VaultItem(
                name=row[1], login=row[2], password=row[3], iid=row[0]
            )
            return result.fetchall()
        except sqlite3.IntegrityError:
            return []

    def get_item(self, user: User, name: str) -> VaultItem | None:
        """

        :param user:
        :param name:
        :return:
        """
        sql_query = "SELECT * FROM T_Items WHERE name = ? AND fk_uid = ?"
        try:
            result = self.connection.execute(sql_query, [name, user.uid])
            result.row_factory = lambda cursor, row: VaultItem(
                iid=row[0], name=row[1], login=row[2], password=row[3]
            )
            return result.fetchone()
        except sqlite3.IntegrityError:
            return None

    def edit_item(self, old_item: VaultItem, new_item: VaultItem) -> bool:
        """

        :param old_item:
        :param new_item:
        :return:
        """
        sql_update = (
            "UPDATE T_Items SET name = ?, login = ?, password = ? WHERE iid = ?"
        )
        try:
            result = self.connection.execute(
                sql_update, [*new_item.to_array(), old_item.iid]
            )
            self.connection.commit()
            return result.rowcount > 0
        except sqlite3.IntegrityError:
            return False

    def add_item(self, user: User, item: VaultItem) -> bool:
        """

        :param user:
        :param item:
        :return:
        """
        sql_add_item = (
            "INSERT INTO T_Items (name, login, password, fk_uid) VALUES (?,?,?,?)"
        )
        try:
            result = self.connection.execute(sql_add_item, [*item.to_array(), user.uid])
            self.connection.commit()
            return result.rowcount > 0
        except sqlite3.IntegrityError:
            return False

    def delete_item(self, item: VaultItem) -> bool:
        """

        :param item:
        :return:
        """
        sql_remove = "DELETE FROM T_Items WHERE iid = ?"
        try:
            result = self.connection.execute(sql_remove, [item.iid])
            self.connection.commit()
            return result.rowcount > 0
        except sqlite3.IntegrityError:
            return False

    def find_items(self, user: User, search_string: str) -> list[VaultItem]:
        sql_list_items = "SELECT * FROM T_Items WHERE name LIKE ? AND fk_uid = ?"
        try:
            result = self.connection.execute(sql_list_items, [search_string+"%", user.uid])
            result.row_factory = lambda cursor, row: VaultItem(
                iid=row[0], name=row[1], login=row[2], password=row[3]
            )
            return result.fetchall()

        except sqlite3.IntegrityError:
            return []
