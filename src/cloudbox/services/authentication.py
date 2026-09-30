from werkzeug.security import check_password_hash, generate_password_hash

from cloudbox.database import Database


class AuthService:
    def __init__(self, database: Database):
        self.database = database

    def create_user(
        self,
        username: str,
        password: str,
    ) -> int:
        password_hash = generate_password_hash(password)

        with self.database.session() as db:
            cursor = db.execute(
                """
                INSERT INTO users (
                    username,
                    password_hash
                )
                VALUES (?, ?)
                """,
                (username, password_hash),
            )

            return cursor.lastrowid

    def get_user_by_username(
        self,
        username: str,
    ) -> dict | None:
        with self.database.session() as db:
            return db.fetchone(
                """
                SELECT *
                FROM users
                WHERE username = ?
                """,
                (username,),
            )

    def verify_password(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        return check_password_hash(
            password_hash,
            password,
        )

    def authenticate(
        self,
        username: str,
        password: str,
    ) -> dict | None:
        user = self.get_user_by_username(username)

        if user is None:
            return None

        if not self.verify_password(
            password,
            user["password_hash"],
        ):
            return None

        return user