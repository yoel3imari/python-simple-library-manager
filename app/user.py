import bcrypt
from app.database import Database


class User:
    def __init__(
        self,
        id: int = None,
        username: str = None,
        password: str = None,
        database: Database = None,
    ):
        self.id = id
        self.username = username
        self.password = password
        self.db = database

        if self.db:
            self.table_name = "users"
            self.db.create_table(
                self.table_name,
                {"username": "TEXT NOT NULL UNIQUE", "password": "TEXT NOT NULL"},
            )
            self._seed()

    def _seed(self):
        admin = self.get_user_by_username("admin")
        if admin is None:
            self.create_user("admin", "password")

    @classmethod
    def from_record(cls, record):
        """
        Converts a database record (tuple) into a User instance.
        :param record: Tuple from database (id, username, password).
        :return: User instance.
        """
        if not record:
            return None
        return cls(id=record[0], username=record[1], password=record[2])

    def create_user(self, username, password):
        if not username or not password:
            raise ValueError("Username and password cannot be empty.")
        pwhash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        data = {"username": username, "password": pwhash}
        return self.db.insert(self.table_name, data)

    def get_user_by_id(self, user_id):
        record = self.db.fetch_one(self.table_name, "id = ?", (user_id,))
        return User.from_record(record)

    def get_user_by_username(self, username):
        record = self.db.fetch_one(self.table_name, "username = ?", (username,))
        return User.from_record(record)

    def search_users(self, search_terms):
        records = self.db.search(self.table_name, search_terms)
        return [User.from_record(record) for record in records]

    def get_all_users(self):
        records = self.db.fetch_all(self.table_name)
        return [User.from_record(record) for record in records]

    def update_user(self, user_id, username=None, password=None):
        if not self.id:
            raise ValueError("User ID is required for updates.")
        data = {}
        if username:
            data["username"] = username
        if password:
            hash_pass = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            data["password"] = hash_pass
        self.db.update(self.table_name, data, "id = ?", (user_id,))

    def delete_user(self, user_id):
        if not self.id:
            raise ValueError("User ID is required for deletion.")
        self.db.delete(self.table_name, "id = ?", (user_id,))

    def __str__(self):
        return f'User [id="{self.id}", username="{self.username}"]'
