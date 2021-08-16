from lib.base import MongoClientAction


class DatabaseName(MongoClientAction):
    """
    Create database on a mongo server
    """

    def run(self, db_name, profile_name=None):
        super().run(profile_name)

        res = self.database_create(db_name)

        return (res.success, res.result)
