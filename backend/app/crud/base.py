from databases import Database


class CrudBase:
    def __init__(self, db: Database) -> None:
        self.db = db
