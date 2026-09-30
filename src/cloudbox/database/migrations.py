import logging

from .database import Database, Session

logger = logging.getLogger(__name__)

migrations = {
   "001_add_users_table": [
      """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """
   ],
}

def _is_migration_applied(database: Database, migration_name: str) -> bool:
    with database.session() as session:
        result = session.count(
            "SELECT name FROM migrations WHERE name = ?", (migration_name,)
        )
        return result > 0

def _record_migration(database: Database, migration_name: str):
    with database.session() as session:
        session.execute(
            "INSERT INTO migrations (name, applied_at) VALUES (?, CURRENT_TIMESTAMP)",
            (migration_name,),
        )

def run_migrations(database: Database):
    logger.info("Starting database migrations...")
    with database.session() as session:
        for migration_name, sql_statements in migrations.items():
            
            if _is_migration_applied(database, migration_name):
                logger.info(f"Migration '{migration_name}' already applied. Skipping.")
                continue

            logger.info(f"Running migration: {migration_name}")
            for sql in sql_statements:
                session.execute(sql)
            _record_migration(database, migration_name)