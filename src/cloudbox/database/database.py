from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Callable, Iterable


RowFactory = Callable[[sqlite3.Cursor, tuple[Any, ...]], Any]


def dict_factory(
    cursor: sqlite3.Cursor,
    row: tuple[Any, ...],
) -> dict[str, Any]:
    return {
        column[0]: row[index]
        for index, column in enumerate(cursor.description)
    }


class Database:
    def __init__(
        self,
        path: str | Path,
        *,
        timeout: float = 5.0,
        uri: bool = False,
        isolation_level: str | None = "",
        check_same_thread: bool = True,
        row_factory: RowFactory | None = dict_factory,
        foreign_keys: bool = True,
        wal: bool = True,
    ):
        self.path = Path(path)

        self.timeout = timeout
        self.uri = uri
        self.isolation_level = isolation_level
        self.check_same_thread = check_same_thread
        self.row_factory = row_factory

        self.foreign_keys = foreign_keys
        self.wal = wal

    def initialize(self) -> None:
        """
        Initializes the database by creating the necessary tables.
        """
        with self.session() as session:
            session.executescript(
                """
                CREATE TABLE IF NOT EXISTS migrations (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

    def connect(self) -> sqlite3.Connection:
        if not self.uri:
            self.path.parent.mkdir(parents=True, exist_ok=True)

        connection = sqlite3.connect(
            self.path,
            timeout=self.timeout,
            uri=self.uri,
            isolation_level=self.isolation_level,
            check_same_thread=self.check_same_thread,
        )

        connection.row_factory = self.row_factory

        if self.foreign_keys:
            connection.execute("PRAGMA foreign_keys = ON")

        if self.wal:
            connection.execute("PRAGMA journal_mode = WAL")

        return connection

    def session(self) -> Session:
        return Session(self)


class Session:
    def __init__(self, database: Database):
        self.database = database
        self.connection = database.connect()
        self.closed = False

    def execute(
        self,
        sql: str,
        parameters: Iterable[Any] = (),
    ) -> sqlite3.Cursor:
        self._ensure_open()

        return self.connection.execute(
            sql,
            parameters,
        )

    def executemany(
        self,
        sql: str,
        parameters: Iterable[Iterable[Any]],
    ) -> sqlite3.Cursor:
        self._ensure_open()

        return self.connection.executemany(
            sql,
            parameters,
        )

    def executescript(
        self,
        sql: str,
    ) -> sqlite3.Cursor:
        self._ensure_open()

        return self.connection.executescript(sql)

    def fetchone(
        self,
        sql: str,
        parameters: Iterable[Any] = (),
    ) -> Any:
        return self.execute(sql, parameters).fetchone()

    def fetchall(
        self,
        sql: str,
        parameters: Iterable[Any] = (),
    ) -> list[Any]:
        return self.execute(sql, parameters).fetchall()

    def count(
        self,
        sql: str,
        parameters: Iterable[Any] = (),
    ) -> int:
        return len(self.fetchall(sql, parameters))

    def commit(self) -> None:
        self._ensure_open()
        self.connection.commit()

    def rollback(self) -> None:
        self._ensure_open()
        self.connection.rollback()

    def close(self) -> None:
        if self.closed:
            return

        self.connection.close()
        self.closed = True

    def _ensure_open(self) -> None:
        if self.closed:
            raise RuntimeError("Database session is closed")

    def __enter__(self) -> Session:
        self._ensure_open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: Any,
    ) -> None:
        try:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        finally:
            self.close()