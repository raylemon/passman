import sqlite3
from dataclasses import dataclass, field


@dataclass
class User:
    """
    Data class User, used to store user in database
    """
    login: str
    password: str
    uid: int = field(default=-1)

    def to_array(self) -> list[str]:
        """
        Helper method for database storage
        :return: attributes in array
        """
        return [self.login, self.password]


@dataclass
class VaultItem:
    """
    Data class VaultItem, used to store item in database
    """
    name: str
    login: str
    password: str
    iid: int = field(default=-1)

    def to_array(self) -> list[str]:
        """
        Helper method for database storage
        :return: attributes in array
        """
        return [self.name, self.login, self.password]


class Vault:
    def __init__(self, db_path: str):
        """
        Create Vault
        :param db_path: path of database file
        """
        self.connection = sqlite3.connect(db_path)
        if not self.table_exists():
            self.create_tables()

    def __del__(self):
        """
        Close connection
        :return: Nothing
        """
        self.connection.close()

    def table_exists(self) -> bool:
        """
        Check if tables exists in database
        :return: True if table exists, else false
        """
        sql_test = "SELECT * FROM sqlite_master WHERE name = ? AND TYPE = ?"
        try:
            result = self.connection.execute(sql_test, ["T_Users", "table"])
            return result.rowcount == 1
        except sqlite3.DatabaseError:
            return False

    def create_tables(self) -> None:
        """
        Creates tables
        :return: Nothing
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
        Add a user in database
        :param user: user to store in database
        :return: True if user is successfully stored
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
        Remove a user in database
        :param user: user to remove
        :return: true if user is successfully removed
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
        Check if user exists in database
        :param user: user to check
        :return: True if user exists
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
        Validate user and password
        :param user: user to validate
        :return: True if user is validated
        """
        sql_query = "SELECT COUNT(uid) FROM T_Users WHERE login = ? AND password = ?"
        try:
            result = self.connection.execute(sql_query, user.to_array())
            return result.fetchone()[0] > 0
        except sqlite3.IntegrityError:
            return False

    def get_user(self, login: str) -> User | None:
        """
        Get a user by its login
        :param login: login (must be unique!)
        :return: User if found, else Nothing
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
        Get user’s whole list of item
        :param user: owner of items
        :return: list of items
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
        Get user’s item by its name
        :param user: owner of items
        :param name: name of item to get (must be unique)
        :return: Item if it found, else Nothing
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
        Update any item
        :param old_item: item to update
        :param new_item: new information for item
        :return: true if update is successfully
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
        Add item to the vault
        :param user: Owner of items
        :param item: item to store
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
        Delete item from the vault
        :param item: Item to delete
        :return: True if item was successfully deleted
        """
        sql_remove = "DELETE FROM T_Items WHERE iid = ?"
        try:
            result = self.connection.execute(sql_remove, [item.iid])
            self.connection.commit()
            return result.rowcount > 0
        except sqlite3.IntegrityError:
            return False

    def find_items(self, user: User, search_string: str) -> list[VaultItem]:
        """
        Find items by search
        :param user: owner of items
        :param search_string: search string
        :return: list of items
        """
        sql_list_items = "SELECT * FROM T_Items WHERE name LIKE ? AND fk_uid = ?"
        try:
            result = self.connection.execute(
                sql_list_items, [search_string + "%", user.uid]
            )
            result.row_factory = lambda cursor, row: VaultItem(
                iid=row[0], name=row[1], login=row[2], password=row[3]
            )
            return result.fetchall()
        except sqlite3.IntegrityError:
            return []
