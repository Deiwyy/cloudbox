from cloudbox.database import Database

class Migrations:
    def __init__(self, database: Database):
        self.database = database

    def migration_ran(self, migration_name: str) -> bool:
        # Check if the migration has already been run
        with self.database.session() as session:
            result = session.fetchone(
                "SELECT COUNT(*) FROM migrations WHERE name = ?",
                (migration_name,),
            )
            return result[0] > 0

    def run_migrations(self):
        # Implement your migration logic here
        pass