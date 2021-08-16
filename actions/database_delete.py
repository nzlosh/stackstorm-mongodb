from lib.base import MongoClientAction


class DatabaseDelete(MongoClientAction):
    """
    Delete the database on a mongo server
    """

    def run(self, db_name, profile_name=None):
        super().run(profile_name)

        res = self.database_delete(db_name)

        return (res.success, res.result)
