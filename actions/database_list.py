from lib.base import MongoClientAction


class DatabaseList(MongoClientAction):
    """
    List available databases on a mongo server
    """

    def run(self, profile_name=None):
        super().run(profile_name)

        res = self.database_list()

        return (res.success, res.result)
